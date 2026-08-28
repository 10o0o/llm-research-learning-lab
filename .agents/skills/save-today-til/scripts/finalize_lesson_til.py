#!/usr/bin/env python3
"""Merge, validate, and path-limit commit one composed lesson TIL."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
COACH_SCRIPTS = REPO_ROOT / ".agents/skills/coach-llm-research-study/scripts"
for directory in (SCRIPT_DIR, COACH_SCRIPTS):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from compose_lesson_til import _atomic_write  # noqa: E402
from prepare_til_input import PreflightError, prepare_til_input  # noqa: E402
from validate_lesson_handoff import validate_handoff  # noqa: E402
from validate_til import CANONICAL_HEADINGS, validate_file  # noqa: E402


H2_RE = re.compile(r"^## (.+)$", re.MULTILINE)


class FinalizationError(Exception):
    pass


def _run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise FinalizationError(f"git {' '.join(args)} failed: {detail}")
    return result


def _split_til(text: str, expected_date: str) -> dict[str, str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith(f"# {expected_date}\n"):
        raise FinalizationError(f"TIL must start with '# {expected_date}'")
    matches = list(H2_RE.finditer(normalized))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        if name not in CANONICAL_HEADINGS or name in sections:
            raise FinalizationError(f"invalid or duplicate TIL section: {name}")
        body_start = match.end()
        if normalized[body_start : body_start + 1] == "\n":
            body_start += 1
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized)
        sections[name] = normalized[body_start:body_end].strip()
    if "오늘의 학습" not in sections:
        raise FinalizationError("TIL is missing 오늘의 학습")
    return sections


def _merge_related(existing: str, incoming: str) -> str:
    lines: list[str] = []
    seen: set[str] = set()
    for block in (existing, incoming):
        for raw_line in block.splitlines():
            line = raw_line.strip()
            if line and line not in seen:
                seen.add(line)
                lines.append(line)
    return "\n".join(lines)


def merge_daily_til(existing: str | None, incoming: str, study_date: str) -> str:
    """Merge one already composed session into the canonical daily sections."""
    incoming_sections = _split_til(incoming, study_date)
    existing_sections = _split_til(existing, study_date) if existing else {}
    merged: dict[str, str] = {}
    for section in CANONICAL_HEADINGS:
        old = existing_sections.get(section, "").strip()
        new = incoming_sections.get(section, "").strip()
        if section == "관련 기록":
            body = _merge_related(old, new)
        elif not old:
            body = new
        elif not new or new == old or new in old:
            body = old
        else:
            body = f"{old}\n\n{new}"
        if body:
            merged[section] = body
    chunks = [f"# {study_date}"]
    for section in CANONICAL_HEADINGS:
        if section in merged:
            chunks.extend([f"## {section}", merged[section]])
    return "\n\n".join(chunks).rstrip() + "\n"


def _rebase_same_day_til_manifest(
    text: str,
    doc: object,
    *,
    finalized_til_path: str,
    finalized_til_hash: str,
) -> str:
    """Refresh only a prior same-day TIL input after it becomes this lesson's output.

    A `til` manifest entry is normally immutable lesson context.  The one
    exception is a prior finalized TIL at the same dated destination: finalizing
    the next session intentionally merges into that exact file.  Its changed
    bytes must therefore update the terminal operational handoff record, while
    source inputs and the reviewed contract remain untouched.
    """

    manifest = getattr(doc, "manifest", ())
    matching = [
        entry
        for entry in manifest
        if entry.role == "til" and entry.path == finalized_til_path
    ]
    if not matching:
        return text
    if len(matching) != 1:
        raise FinalizationError("same-day TIL manifest input must occur exactly once")
    entry = matching[0]
    if entry.sha256 == finalized_til_hash:
        return text

    row_pattern = re.compile(
        rf"(?m)^\| {re.escape(entry.item_id)} \| til \| {re.escape(entry.path)} \| {entry.sha256} \|$"
    )
    row_replacement = f"| {entry.item_id} | til | {entry.path} | {finalized_til_hash} |"
    updated, row_count = row_pattern.subn(row_replacement, text, count=1)
    if row_count != 1:
        raise FinalizationError("cannot refresh the same-day TIL manifest row")

    canonical_rows = [
        f"{candidate.role}\t{candidate.path}\t"
        f"{finalized_til_hash if candidate.item_id == entry.item_id else candidate.sha256}\n"
        for candidate in manifest
    ]
    manifest_hash = hashlib.sha256("".join(sorted(canonical_rows)).encode("utf-8")).hexdigest()

    def replace_field(payload: str, field: str, value: str) -> str:
        pattern = re.compile(rf"(?m)^- {re.escape(field)}: [0-9a-f]{{64}}$")
        replaced, count = pattern.subn(f"- {field}: {value}", payload, count=1)
        if count != 1:
            raise FinalizationError(f"cannot refresh {field} after same-day TIL merge")
        return replaced

    updated = replace_field(updated, "input_manifest_sha256", manifest_hash)
    return replace_field(updated, "reviewed_input_manifest_sha256", manifest_hash)


def _mark_committed(
    handoff: Path,
    root: Path,
    commit_sha: str,
    *,
    doc: object,
    finalized_til_path: str,
) -> None:
    before = handoff.read_text(encoding="utf-8")
    final_til = root / finalized_til_path
    if not final_til.is_file():
        raise FinalizationError("finalized dated TIL is missing before handoff completion")
    rebased = _rebase_same_day_til_manifest(
        before,
        doc,
        finalized_til_path=finalized_til_path,
        finalized_til_hash=hashlib.sha256(final_til.read_bytes()).hexdigest(),
    )
    section_start = rebased.find("## TIL Composition\n")
    if section_start < 0:
        raise FinalizationError("handoff has no TIL Composition section")
    prefix = rebased[:section_start]
    section = rebased[section_start:]
    section, state_count = re.subn(
        r"(?m)^- state: composed$", "- state: committed", section, count=1
    )
    section, commit_count = re.subn(
        r"(?m)^- commit_sha: pending$", f"- commit_sha: {commit_sha}", section, count=1
    )
    if (state_count, commit_count) != (1, 1):
        raise FinalizationError("handoff is not in composed/pending-commit state")
    _atomic_write(handoff, prefix + section)
    report = validate_handoff(handoff, repo_root=root, check_draft=True)
    if not report.ok:
        _atomic_write(handoff, before)
        detail = "\n".join(error.rendered(report.path) for error in report.errors)
        raise FinalizationError("committed handoff state did not validate\n" + detail)


def _recover_same_day_til_commit(
    handoff: Path,
    root: Path,
) -> None:
    """Repair the handoff after an older finalizer committed before marking it.

    This narrow recovery applies only when the current dated TIL is unchanged
    from a path-limited `til: YYYY-MM-DD 학습 기록` commit.  It never accepts a
    merely edited or externally committed baseline as a reviewed input.
    """

    provisional = validate_handoff(handoff, repo_root=root, check_draft=True)
    doc = provisional.document
    if doc is None or doc.til_composition.get("state") != "composed":
        return
    dated_path = doc.til_composition.get("dated_til_path", "")
    study_date = doc.metadata.get("study_date", "")
    if not dated_path or dated_path == "pending" or not study_date:
        return
    matching = [entry for entry in doc.manifest if entry.role == "til" and entry.path == dated_path]
    if len(matching) != 1:
        return
    dated_til = root / dated_path
    if not dated_til.is_file():
        return
    actual_hash = hashlib.sha256(dated_til.read_bytes()).hexdigest()
    if actual_hash == matching[0].sha256:
        return
    subject = _run_git(root, "log", "-1", "--format=%s", "--", dated_path, check=False)
    commit = _run_git(root, "log", "-1", "--format=%H", "--", dated_path, check=False)
    clean = _run_git(root, "diff", "--quiet", "HEAD", "--", dated_path, check=False)
    commit_sha = commit.stdout.strip()
    if (
        subject.returncode != 0
        or subject.stdout.strip() != f"til: {study_date} 학습 기록"
        or clean.returncode != 0
        or not commit_sha
        or _commit_paths(root, commit_sha) != [dated_path]
    ):
        return
    before = handoff.read_text(encoding="utf-8")
    updated = _rebase_same_day_til_manifest(
        before,
        doc,
        finalized_til_path=dated_path,
        finalized_til_hash=actual_hash,
    )
    if updated != before:
        _atomic_write(handoff, updated)


def _commit_paths(root: Path, commit_sha: str) -> list[str]:
    result = _run_git(
        root,
        "diff-tree",
        "--no-commit-id",
        "--name-only",
        "-r",
        commit_sha,
    )
    return [line for line in result.stdout.splitlines() if line]


def finalize_lesson_til(
    handoff_path: Path | str,
    *,
    repo_root: Path | str = REPO_ROOT,
    allow_explicit_request: bool = False,
) -> dict[str, str | bool]:
    """Finalize one composed handoff without touching any non-TIL tracked path."""
    root = Path(repo_root).resolve()
    handoff = Path(handoff_path)
    if not handoff.is_absolute():
        handoff = root / handoff
    _recover_same_day_til_commit(handoff, root)
    report = validate_handoff(
        handoff,
        repo_root=root,
        til_ready=True,
        check_draft=True,
    )
    if not report.ok or report.document is None:
        detail = "\n".join(error.rendered(report.path) for error in report.errors)
        raise FinalizationError("handoff is not TIL-ready\n" + detail)
    doc = report.document
    policy = doc.metadata["til_finalize_policy"]
    if policy == "explicit-request" and not allow_explicit_request:
        raise FinalizationError("explicit-request policy requires an explicit save approval")
    if doc.til_composition.get("state") != "composed":
        raise FinalizationError("TIL Composition must be composed before finalization")

    try:
        incoming = prepare_til_input(repo_root=root, handoff=handoff)
    except PreflightError as error:
        raise FinalizationError(str(error)) from error
    study_date = doc.metadata["study_date"]
    relative = Path(doc.til_composition["dated_til_path"])
    destination = (root / relative).resolve(strict=False)
    try:
        destination.relative_to(root)
    except ValueError as error:
        raise FinalizationError("dated TIL path escapes the repository") from error
    existing = destination.read_text(encoding="utf-8") if destination.exists() else None
    if destination.exists():
        existing_errors = validate_file(destination)
        if existing_errors:
            raise FinalizationError("existing dated TIL is invalid\n" + "\n".join(existing_errors))
    merged = merge_daily_til(existing, incoming, study_date)
    destination_before = destination.read_bytes() if destination.exists() else None
    _atomic_write(destination, merged)
    errors = validate_file(destination)
    if errors:
        if destination_before is None:
            destination.unlink()
        else:
            _atomic_write(destination, destination_before.decode("utf-8"))
        raise FinalizationError("merged dated TIL is invalid\n" + "\n".join(errors))

    relative_text = relative.as_posix()
    diff_check = _run_git(root, "diff", "--check", "--", relative_text, check=False)
    if diff_check.returncode != 0:
        raise FinalizationError("dated TIL failed git diff --check\n" + diff_check.stderr.strip())
    _run_git(root, "add", "--", relative_text)
    cached_check = _run_git(root, "diff", "--cached", "--check", "--", relative_text, check=False)
    if cached_check.returncode != 0:
        raise FinalizationError("staged dated TIL failed git diff --cached --check\n" + cached_check.stderr.strip())
    staged = _run_git(root, "diff", "--cached", "--name-only", "--", relative_text).stdout.splitlines()
    reused_commit = False
    if staged == [relative_text]:
        commit = _run_git(
            root,
            "commit",
            "--only",
            "-m",
            f"til: {study_date} 학습 기록",
            "--",
            relative_text,
        )
        if commit.returncode != 0:  # pragma: no cover - _run_git raises first
            raise FinalizationError(commit.stderr.strip())
        commit_sha = _run_git(root, "rev-parse", "HEAD").stdout.strip()
    elif not staged and not _run_git(root, "diff", "--quiet", "HEAD", "--", relative_text, check=False).returncode:
        commit_sha = _run_git(root, "log", "-1", "--format=%H", "--", relative_text).stdout.strip()
        reused_commit = True
    else:
        raise FinalizationError("the dated TIL is not the sole staged target for this save")
    if not commit_sha or _commit_paths(root, commit_sha) != [relative_text]:
        raise FinalizationError("the resulting commit is not path-limited to the dated TIL")
    _mark_committed(
        handoff,
        root,
        commit_sha,
        doc=doc,
        finalized_til_path=relative_text,
    )
    return {
        "dated_til_path": relative_text,
        "commit_sha": commit_sha,
        "merged_existing": existing is not None,
        "reused_commit": reused_commit,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", nargs="?", type=Path, default=Path("tmp/active-lesson-handoff.md"))
    parser.add_argument("--allow-explicit-request", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = finalize_lesson_til(
            args.handoff,
            allow_explicit_request=args.allow_explicit_request,
        )
    except (OSError, UnicodeError, FinalizationError) as error:
        print(f"ERROR {args.handoff}:1 [TIL_FINALIZE] {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
