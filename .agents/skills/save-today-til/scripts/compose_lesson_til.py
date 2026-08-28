#!/usr/bin/env python3
"""Compose one evidence-linked handoff TIL draft and seal its v8 state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
COACH_SCRIPTS = REPO_ROOT / ".agents/skills/coach-llm-research-study/scripts"
for directory in (SCRIPT_DIR, COACH_SCRIPTS):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from validate_lesson_handoff import (  # noqa: E402
    CURRICULUM_ID_RE,
    TIL_ITEM_REPRESENTATIONS,
    TIL_ITEM_SECTIONS,
    _draft_marker_blocks,
    _normalize_newlines,
    _safe_repo_path,
    validate_handoff,
)


RESET_COMMENT = "<!-- 형식 없이 자유롭게 작성하세요. 저장할 때 $save-today-til을 사용합니다. -->"


class CompositionError(Exception):
    pass


def _sha256(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old_mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, old_mode)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _restore(path: Path, existed: bool, payload: bytes) -> None:
    """Restore one pre-transaction file state after a composition failure."""
    if existed:
        _atomic_write(path, payload.decode("utf-8"))
    elif path.exists():
        path.unlink()


def _remove_raw_envelopes(text: str, lesson_id: str) -> str:
    escaped = re.escape(lesson_id)
    pattern = re.compile(
        rf"^<!-- lesson-evidence:{escaped}:E\d{{3}}:[0-9a-f]{{64}} -->[ \t]*\n"
        rf".*?^<!-- /lesson-evidence:{escaped}:E\d{{3}} -->[ \t]*(?:\n|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub("", text).replace(RESET_COMMENT, "").strip()


def _relative_link(from_path: PurePosixPath, target: PurePosixPath) -> str:
    source_parent = from_path.parent.parts
    target_parts = target.parts
    common = 0
    for left, right in zip(source_parent, target_parts):
        if left != right:
            break
        common += 1
    return "/".join([".."] * (len(source_parent) - common) + list(target_parts[common:]))


def _dated_til_path(doc: Any) -> PurePosixPath:
    study_date = doc.metadata["study_date"]
    return PurePosixPath(f"til/{study_date[:4]}/{study_date[5:7]}/{study_date}.md")


def _related_records(doc: Any) -> list[str]:
    dated_til_path = _dated_til_path(doc)
    lines: list[str] = []
    for entry in doc.manifest:
        if entry.role != "primary":
            continue
        target = PurePosixPath(entry.path)
        label = target.name
        lines.append(f"- [{label}]({_relative_link(dated_til_path, target)})")
    for identity in doc.external_identities.values():
        lines.extend(
            [
                f"- [공식 자료]({identity.official_url})",
                f"- provider/course: {identity.provider} / {identity.course}",
                f"- offering/edition: {identity.offering_or_edition}",
                f"- artifact: {identity.artifact}",
                f"- scope: {identity.scope}",
            ]
        )
    decision = doc.target_decision
    if decision is None or not CURRICULUM_ID_RE.fullmatch(decision.primary_target):
        raise CompositionError("handoff has no valid primary target")
    lines.append(f"- 관련 역량: `{decision.primary_target}`")
    if decision.bridge_target != "none":
        treatment = doc.curriculum_treatments.get(decision.bridge_target)
        bridge_delivered = treatment is not None and any(
            doc.objective_delivery.get(objective_id) is not None
            and doc.objective_delivery[objective_id].state == "delivered"
            for objective_id in treatment.objective_ids
        )
        if bridge_delivered:
            lines.append(f"- 보충 선수 역량: `{decision.bridge_target}`")
    return list(dict.fromkeys(lines))


def _validated_items(doc: Any, raw_items: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
    if not raw_items:
        raise CompositionError("at least one TIL item is required")
    items: list[dict[str, Any]] = []
    cited_confirmed: set[str] = set()
    for index, raw in enumerate(raw_items, start=1):
        item_id = f"D{index:03d}"
        section = str(raw.get("section", "")).strip()
        representation = str(raw.get("representation", "")).strip()
        text = _normalize_newlines(str(raw.get("text", ""))).strip()
        evidence_ids = [str(item).strip() for item in raw.get("evidence_ids", [])]
        if section not in TIL_ITEM_SECTIONS:
            raise CompositionError(f"{item_id} section is not allowed: {section}")
        if representation not in TIL_ITEM_REPRESENTATIONS:
            raise CompositionError(f"{item_id} representation is not allowed: {representation}")
        if representation == "remaining-question" and section != "남은 질문":
            raise CompositionError(f"{item_id} remaining-question belongs under 남은 질문")
        if representation == "changed-understanding" and section != "배운 점":
            raise CompositionError(f"{item_id} changed-understanding belongs under 배운 점")
        if representation == "learning" and section == "남은 질문":
            raise CompositionError(f"{item_id} learning text may not appear under 남은 질문")
        if not text:
            raise CompositionError(f"{item_id} text must not be empty")
        if len(evidence_ids) != len(set(evidence_ids)):
            raise CompositionError(f"{item_id} contains duplicate Evidence IDs")
        unknown = [item for item in evidence_ids if item not in doc.evidence]
        if unknown:
            raise CompositionError(f"{item_id} references unknown evidence: {', '.join(unknown)}")
        if mode == "handoff-generated" and not evidence_ids:
            raise CompositionError(f"{item_id} requires learner evidence in handoff-generated mode")
        verdicts = {doc.evidence[item].values.get("verdict") for item in evidence_ids}
        if representation == "learning" and any(verdict != "confirmed" for verdict in verdicts):
            raise CompositionError(f"{item_id} learning text may cite confirmed evidence only")
        if representation == "changed-understanding" and not ({"confirmed"} <= verdicts and bool(verdicts - {"confirmed"})):
            raise CompositionError(f"{item_id} changed-understanding requires corrected and confirmed evidence")
        if representation == "remaining-question" and evidence_ids and verdicts == {"confirmed"}:
            raise CompositionError(f"{item_id} remaining-question requires unresolved evidence")
        cited_confirmed.update(
            evidence_id
            for evidence_id in evidence_ids
            if doc.evidence[evidence_id].values.get("verdict") == "confirmed"
        )
        items.append(
            {
                "item_id": item_id,
                "section": section,
                "evidence_ids": evidence_ids,
                "representation": representation,
                "text": text,
                "content_sha256": _sha256(text),
            }
        )
    required_confirmed = {
        evidence.evidence_id
        for evidence in doc.evidence.values()
        if evidence.values.get("verdict") == "confirmed"
    }
    missing = sorted(required_confirmed - cited_confirmed)
    if missing:
        raise CompositionError("confirmed learner evidence is absent from the composition: " + ", ".join(missing))
    return items


def _render_draft(doc: Any, items: list[dict[str, Any]]) -> str:
    by_section = {section: [] for section in ("오늘의 학습", "배운 점", "남은 질문")}
    lesson_id = doc.metadata["lesson_id"]
    for item in items:
        raw_evidence = ",".join(item["evidence_ids"]) or "none"
        envelope = (
            f"<!-- lesson-til-item:{lesson_id}:{item['item_id']}:{item['representation']}:{raw_evidence}:{item['content_sha256']} -->\n"
            f"{item['text']}\n"
            f"<!-- /lesson-til-item:{lesson_id}:{item['item_id']} -->"
        )
        by_section[item["section"]].append(envelope)
    chunks = [f"# {doc.metadata['study_date']}", "## 오늘의 학습", "\n\n".join(by_section["오늘의 학습"])]
    for section in ("배운 점", "남은 질문"):
        if by_section[section]:
            chunks.extend([f"## {section}", "\n\n".join(by_section[section])])
    chunks.extend(["## 관련 기록", "\n".join(_related_records(doc))])
    return "\n\n".join(chunks).rstrip() + "\n"


def _render_composition_section(
    *,
    mode: str,
    review: str,
    composed_at: str,
    draft_hash: str,
    dated_til_path: str,
    items: list[dict[str, Any]],
) -> str:
    rows = "\n".join(
        f"| {item['item_id']} | {item['section']} | {', '.join(item['evidence_ids']) or 'none'} | {item['representation']} | {item['content_sha256']} |"
        for item in items
    )
    return (
        "## TIL Composition\n\n"
        f"- mode: {mode}\n"
        "- state: composed\n"
        f"- review: {review}\n"
        f"- composed_at: {composed_at}\n"
        f"- draft_sha256: {draft_hash}\n"
        f"- dated_til_path: {dated_til_path}\n"
        "- commit_sha: pending\n\n"
        "| Item ID | Section | Evidence IDs | Representation | Content SHA-256 |\n"
        "| --- | --- | --- | --- | --- |\n"
        f"{rows}\n"
    )


def compose_lesson_til(
    handoff_path: Path | str,
    raw_items: list[dict[str, Any]],
    *,
    repo_root: Path | str = REPO_ROOT,
    mode: str | None = None,
    review: str | None = None,
    manual_text_sha256: str | None = None,
    composed_at: str | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    handoff = Path(handoff_path)
    if not handoff.is_absolute():
        handoff = root / handoff
    report = validate_handoff(handoff, repo_root=root, check_draft=False)
    if not report.ok or report.document is None:
        rendered = "\n".join(error.rendered(report.path) for error in report.errors)
        raise CompositionError("handoff is not structurally valid\n" + rendered)
    doc = report.document
    if doc.metadata.get("status") not in {"paused", "completed"}:
        raise CompositionError("TIL composition requires paused or completed lesson status")
    draft_path, path_error = _safe_repo_path(doc.metadata.get("draft_path", ""), root)
    if path_error or draft_path is None:
        raise CompositionError(f"invalid draft path: {path_error}")
    try:
        existing = _normalize_newlines(draft_path.read_text(encoding="utf-8")) if draft_path.exists() else RESET_COMMENT + "\n"
    except (OSError, UnicodeError) as error:
        raise CompositionError(f"cannot read draft: {error}") from error

    existing_state = doc.til_composition.get("state", "pending")
    if existing_state != "pending":
        raise CompositionError("only a pending composition may be written; resume saving an existing composition")
    draft_report = validate_handoff(handoff, repo_root=root, check_draft=True)
    if not draft_report.ok:
        rendered = "\n".join(error.rendered(draft_report.path) for error in draft_report.errors)
        raise CompositionError("raw handoff draft is not valid\n" + rendered)
    raw_blocks, raw_balanced = _draft_marker_blocks(existing, doc.metadata["lesson_id"])
    pending_confirmed = [
        evidence.evidence_id
        for evidence in doc.evidence.values()
        if evidence.values.get("verdict") == "confirmed"
        and evidence.values.get("append_state") != "drafted"
    ]
    if pending_confirmed:
        raise CompositionError(
            "confirmed learner evidence must be drafted before composition: "
            + ", ".join(pending_confirmed)
        )
    drafted_ids = {
        evidence.evidence_id
        for evidence in doc.evidence.values()
        if evidence.values.get("append_state") == "drafted"
    }
    manual_text = _remove_raw_envelopes(existing, doc.metadata["lesson_id"])
    inferred_mode = "mixed" if manual_text else "handoff-generated"
    selected_mode = mode or inferred_mode
    if selected_mode not in {"handoff-generated", "mixed"}:
        raise CompositionError("mode must be handoff-generated or mixed")
    if selected_mode == "handoff-generated" and manual_text:
        raise CompositionError("manual or self-study text requires mixed composition review")
    if selected_mode == "mixed":
        if not manual_text_sha256 or manual_text_sha256 != _sha256(manual_text):
            raise CompositionError("mixed composition requires the exact manual_text_sha256")
        selected_review = review or "pending"
        if selected_review not in {"pending", "pass", "repair_required"}:
            raise CompositionError("mixed composition review must be pending, pass, or repair_required")
    else:
        selected_review = "not-required"
        if review not in {None, "not-required"}:
            raise CompositionError("handoff-generated composition does not accept a semantic review verdict")
        if not raw_balanced or {block[0] for block in raw_blocks} != drafted_ids:
            raise CompositionError("raw learner-evidence envelopes are missing or invalid")

    items = _validated_items(doc, raw_items, selected_mode)
    draft_text = _render_draft(doc, items)
    draft_hash = _sha256(draft_text.encode("utf-8"))
    timestamp = composed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    try:
        parsed_timestamp = datetime.fromisoformat(
            timestamp[:-1] + "+00:00" if timestamp.endswith("Z") else timestamp
        )
    except ValueError as error:
        raise CompositionError("composed_at must be an RFC 3339 timestamp") from error
    if parsed_timestamp.tzinfo is None:
        raise CompositionError("composed_at must include a timezone")
    dated_til_path = _dated_til_path(doc).as_posix()
    composition_section = _render_composition_section(
        mode=selected_mode,
        review=selected_review,
        composed_at=timestamp,
        draft_hash=draft_hash,
        dated_til_path=dated_til_path,
        items=items,
    )
    updated_handoff, count = re.subn(
        r"^## TIL Composition\n.*\Z",
        composition_section,
        doc.text,
        count=1,
        flags=re.MULTILINE | re.DOTALL,
    )
    if count != 1:
        raise CompositionError("handoff TIL Composition section is missing")

    draft_existed = draft_path.exists()
    handoff_existed = handoff.exists()
    draft_before = draft_path.read_bytes() if draft_existed else b""
    handoff_before = handoff.read_bytes() if handoff_existed else b""
    try:
        _atomic_write(draft_path, draft_text)
        _atomic_write(handoff, updated_handoff)
        sealed = validate_handoff(handoff, repo_root=root, check_draft=True)
        if not sealed.ok:
            rendered = "\n".join(error.rendered(sealed.path) for error in sealed.errors)
            raise CompositionError("composed handoff did not validate\n" + rendered)
    except Exception:
        _restore(draft_path, draft_existed, draft_before)
        _restore(handoff, handoff_existed, handoff_before)
        raise
    return {
        "mode": selected_mode,
        "review": selected_review,
        "draft_path": doc.metadata["draft_path"],
        "draft_sha256": draft_hash,
        "dated_til_path": dated_til_path,
        "items": [item["item_id"] for item in items],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path)
    parser.add_argument("--spec", required=True, help="JSON file path or '-' for stdin")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        raw = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text(encoding="utf-8")
        spec = json.loads(raw)
        result = compose_lesson_til(
            args.handoff,
            spec["items"],
            mode=spec.get("mode"),
            review=spec.get("review"),
            manual_text_sha256=spec.get("manual_text_sha256"),
            composed_at=spec.get("composed_at"),
        )
    except (OSError, KeyError, json.JSONDecodeError, ValueError, CompositionError) as error:
        print(f"ERROR {args.handoff}:1 [TIL_COMPOSITION] {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
