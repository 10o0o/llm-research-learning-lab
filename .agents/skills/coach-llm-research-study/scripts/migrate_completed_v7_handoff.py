#!/usr/bin/env python3
"""One-time, evidence-preserving migration of the completed Stat110 v7 handoff."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_lesson_handoff import _draft_marker_blocks, validate_handoff  # noqa: E402


DEFAULT_LESSON_ID = "stat110-events-naive-probability-04"
FIRST_PART_BOUNDARY = "CC-PROB-01 전체 완료가 아니라 첫 explain·calculate 증거다."


class MigrationError(Exception):
    pass


def _sha256(value: bytes | str) -> str:
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def _atomic_write(path: Path, text: str) -> None:
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _single(pattern: str, text: str, label: str, flags: int = 0) -> re.Match[str]:
    matches = list(re.finditer(pattern, text, flags))
    if len(matches) != 1:
        raise MigrationError(f"expected exactly one {label}, found {len(matches)}")
    return matches[0]


def _manifest_rows(text: str, root: Path) -> tuple[list[tuple[str, str, str, str]], str]:
    match = _single(
        r"^## Input Manifest\n\n(?P<body>.*?)\n\n<!-- lesson-contract:start -->$",
        text,
        "Input Manifest",
        re.MULTILINE | re.DOTALL,
    )
    rows: list[tuple[str, str, str, str]] = []
    for line in match.group("body").splitlines()[2:]:
        cells = [cell.strip() for cell in line.strip()[1:-1].split("|")] if line.startswith("|") and line.endswith("|") else []
        if len(cells) != 4:
            raise MigrationError("v7 Input Manifest contains a malformed row")
        rows.append(tuple(cells))
    if [row[0] for row in rows] != [f"I{index:03d}" for index in range(1, len(rows) + 1)]:
        raise MigrationError("v7 Input Manifest IDs are not contiguous")
    for _, _, raw_path, digest in rows:
        candidate = (root / raw_path).resolve(strict=False)
        try:
            candidate.relative_to(root)
        except ValueError as error:
            raise MigrationError(f"manifest path escapes the repository: {raw_path}") from error
        if not candidate.is_file() or _sha256(candidate.read_bytes()) != digest:
            raise MigrationError(f"manifest source is missing or stale: {raw_path}")
    digest = _sha256("".join(sorted(f"{role}\t{path}\t{sha}\n" for _, role, path, sha in rows)))
    return rows, digest


def _evidence_blocks(text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for match in re.finditer(
        r"^<!-- learner-evidence:(E\d{3}):start -->\n(?P<body>.*?)^<!-- learner-evidence:\1:end -->$",
        text,
        re.MULTILINE | re.DOTALL,
    ):
        content = _single(
            r"^<!-- learner-content:start -->\n(?P<content>.*?)\n<!-- learner-content:end -->$",
            match.group("body"),
            f"{match.group(1)} learner content",
            re.MULTILINE | re.DOTALL,
        ).group("content")
        blocks.append((match.group(1), content))
    if [item[0] for item in blocks] != [f"E{index:03d}" for index in range(1, len(blocks) + 1)]:
        raise MigrationError("v7 learner evidence IDs are not contiguous")
    return blocks


def _migrate_contract(contract: str, evidence_region: str) -> str:
    if "### Session Plan" in contract or "- step_role:" in contract:
        raise MigrationError("handoff contract is not an unmigrated v7 contract")
    step_matches = list(re.finditer(r"^#### (T\d{3})\n\n(?P<body>.*?)(?=^#### T\d{3}\n|^### Deferred$)", contract, re.MULTILINE | re.DOTALL))
    if not step_matches or [match.group(1) for match in step_matches] != [f"T{index:03d}" for index in range(1, len(step_matches) + 1)]:
        raise MigrationError("v7 Teaching Step IDs are absent or non-contiguous")
    examples: list[str] = []
    rewritten_steps: list[tuple[int, int, str]] = []
    for index, match in enumerate(step_matches, start=1):
        step_id = match.group(1)
        body = match.group("body")
        concept = _single(r"(?m)^- concept_id: (C\d{2})$", body, f"{step_id} concept").group(1)
        objectives = _single(r"(?m)^- objective_ids: (O\d{3}(?:, O\d{3})*)$", body, f"{step_id} objectives").group(1)
        example_id = f"X{index:03d}"
        examples.append(f"| {example_id} | Preserve the completed {step_id} fixture. | Existing v7 tiny example for {step_id}. | {objectives} |")
        role = "concept-model" if index == 1 else "contrast-limit" if index == 2 else "worked-example"
        migrated_body = re.sub(
            r"(?m)^- concept_id: C\d{2}$",
            f"- step_role: {role}\n- concept_ids: {concept}",
            body,
            count=1,
        )
        migrated_body = re.sub(
            r"(?m)^(- objective_ids: .+)$",
            rf"\1\n- example_id: {example_id}",
            migrated_body,
            count=1,
        )
        rewritten_steps.append((match.start(), match.end(), f"#### {step_id}\n\n{migrated_body.rstrip()}\n\n"))

    last_step = step_matches[-1].group(1)
    last_concept = _single(r"(?m)^- concept_id: (C\d{2})$", step_matches[-1].group("body"), "exit concept").group(1)
    last_objectives = _single(r"(?m)^- objective_ids: (.+)$", step_matches[-1].group("body"), "exit objectives").group(1)
    exit_kind: str | None = None
    for block in re.finditer(r"^### E\d{3}\n\n(?P<body>.*?)(?=^### E\d{3}\n|\Z)", evidence_region, re.MULTILINE | re.DOTALL):
        body = block.group("body")
        concept_match = re.search(r"(?m)^- concept: (.+)$", body)
        objective_match = re.search(r"(?m)^- objective_ids: (.+)$", body)
        kind_match = re.search(r"(?m)^- kind: (.+)$", body)
        verdict_match = re.search(r"(?m)^- verdict: (.+)$", body)
        if (
            concept_match
            and objective_match
            and kind_match
            and verdict_match
            and concept_match.group(1) == last_concept
            and objective_match.group(1) == last_objectives
            and verdict_match.group(1) == "confirmed"
        ):
            exit_kind = kind_match.group(1)
    if exit_kind is None:
        raise MigrationError("no confirmed v7 evidence matches the completed exit Step")

    rebuilt = contract
    for start, end, replacement in reversed(rewritten_steps):
        rebuilt = rebuilt[:start] + replacement + rebuilt[end:]
    insertion = (
        "### Session Plan\n\n"
        "- session_goal: Preserve the already completed v7 micro-lesson without expanding its source or learning scope.\n"
        f"- exit_step: {last_step}\n"
        f"- exit_evidence_kind: {exit_kind}\n\n"
        "### Example Map\n\n"
        "| Example ID | Purpose | Fixture | Objective IDs |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(examples)
        + "\n\n"
    )
    return rebuilt.replace("### Prepared Teaching Steps\n\n", insertion + "### Prepared Teaching Steps\n\n", 1).rstrip()


def migrate_completed_v7_handoff(
    handoff_path: Path | str,
    *,
    repo_root: Path | str = REPO_ROOT,
    expected_lesson_id: str = DEFAULT_LESSON_ID,
    updated_at: str | None = None,
    require_stat110_boundary: bool = True,
) -> None:
    root = Path(repo_root).resolve()
    handoff = Path(handoff_path)
    if not handoff.is_absolute():
        handoff = root / handoff
    before_bytes = handoff.read_bytes()
    text = before_bytes.decode("utf-8")
    if f"- lesson_id: {expected_lesson_id}" not in text:
        raise MigrationError("handoff lesson ID does not match the approved recovery target")
    required_lines = ("- schema_version: 7", "- status: completed", "- next_action: complete", "- verdict: pass")
    if any(text.count(line) != 1 for line in required_lines):
        raise MigrationError("handoff is not one completed, independently reviewed v7 lesson")
    if require_stat110_boundary and FIRST_PART_BOUNDARY not in text:
        raise MigrationError("Stat110 recovery lacks the explicit first-part/non-mastery boundary")
    objective_delivery = _single(
        r"^## Objective Delivery\n\n(?P<body>.*?)(?=^## Daily Learning Coverage$)",
        text,
        "Objective Delivery",
        re.MULTILINE | re.DOTALL,
    ).group("body")
    if re.search(r"(?m)^\| O\d{3} \| (?!delivered \|)", objective_delivery):
        raise MigrationError("completed v7 handoff contains a non-delivered objective")

    _, manifest_hash = _manifest_rows(text, root)
    declared_manifest = _single(r"(?m)^- input_manifest_sha256: ([0-9a-f]{64})$", text, "manifest hash").group(1)
    reviewed_manifest = _single(r"(?m)^- reviewed_input_manifest_sha256: ([0-9a-f]{64})$", text, "reviewed manifest hash").group(1)
    if manifest_hash != declared_manifest or manifest_hash != reviewed_manifest:
        raise MigrationError("v7 manifest or review hash is stale")
    contract_match = _single(
        r"^<!-- lesson-contract:start -->\n(?P<body>.*?)\n<!-- lesson-contract:end -->$",
        text,
        "lesson contract",
        re.MULTILINE | re.DOTALL,
    )
    old_contract = contract_match.group("body")
    old_hash = _sha256(old_contract)
    if _single(r"(?m)^- contract_sha256: ([0-9a-f]{64})$", text, "contract hash").group(1) != old_hash:
        raise MigrationError("v7 declared contract hash is stale")
    if _single(r"(?m)^- reviewed_contract_sha256: ([0-9a-f]{64})$", text, "reviewed contract hash").group(1) != old_hash:
        raise MigrationError("v7 semantic review is stale")

    evidence_section = _single(r"^## Learner Evidence\n(?P<body>.*)\Z", text, "Learner Evidence", re.MULTILINE | re.DOTALL).group("body")
    learner_content_before = _evidence_blocks(text)
    draft_path = root / _single(r"(?m)^- draft_path: (.+)$", text, "draft path").group(1)
    draft_text = draft_path.read_text(encoding="utf-8")
    draft_blocks, balanced = _draft_marker_blocks(draft_text, expected_lesson_id)
    drafted: dict[str, str] = {}
    for block in re.finditer(
        r"^<!-- learner-evidence:(E\d{3}):start -->\n(?P<body>.*?)^<!-- learner-evidence:\1:end -->$",
        evidence_section,
        re.MULTILINE | re.DOTALL,
    ):
        body = block.group("body")
        verdict = re.search(r"(?m)^- verdict: (.+)$", body)
        append_state = re.search(r"(?m)^- append_state: (.+)$", body)
        if verdict and append_state and verdict.group(1) == "confirmed" and append_state.group(1) == "drafted":
            content = _single(
                r"^<!-- learner-content:start -->\n(?P<content>.*?)\n<!-- learner-content:end -->$",
                body,
                f"{block.group(1)} learner content",
                re.MULTILINE | re.DOTALL,
            ).group("content")
            drafted[block.group(1)] = content
    draft_by_id = {evidence_id: (digest, body) for evidence_id, digest, body, _ in draft_blocks}
    if (
        not balanced
        or set(draft_by_id) != set(drafted)
        or any(
            body != drafted[evidence_id] or digest != _sha256(body)
            for evidence_id, (digest, body) in draft_by_id.items()
        )
    ):
        raise MigrationError("v7 draft envelopes do not exactly match drafted confirmed evidence")

    new_contract = _migrate_contract(old_contract, evidence_section)
    new_contract_hash = _sha256(new_contract)
    migrated = text[: contract_match.start("body")] + new_contract + text[contract_match.end("body") :]
    migrated = migrated.replace(
        "- status: completed\n",
        "- status: completed\n- session_profile: short\n- til_finalize_policy: auto-commit\n",
        1,
    ).replace("- schema_version: 7", "- schema_version: 8", 1)
    timestamp = updated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    migrated = re.sub(r"(?m)^- updated_at: .+$", f"- updated_at: {timestamp}", migrated, count=1)
    migrated = re.sub(r"(?m)^- contract_sha256: [0-9a-f]{64}$", f"- contract_sha256: {new_contract_hash}", migrated, count=1)
    migrated = re.sub(r"(?m)^- reviewed_contract_sha256: [0-9a-f]{64}$", f"- reviewed_contract_sha256: {new_contract_hash}", migrated, count=1)
    migrated = migrated.replace("- concept: ", "- concept_ids: ")
    migrated = re.sub(
        r"(?ms)^## Daily Learning Coverage\n\n.*?(?=^\| Concept ID \|)",
        "## Daily Learning Coverage\n\n",
        migrated,
        count=1,
    )
    step_ids = re.findall(r"^#### (T\d{3})$", new_contract, re.MULTILINE)
    delivery_rows = "\n".join(
        f"| {step_id} | completed | Preserved completed v7 delivery. |" for step_id in step_ids
    )
    migrated = migrated.replace(
        "## Daily Learning Coverage\n",
        "## Teaching Step Delivery\n\n"
        "| Step ID | State | Basis/Note |\n"
        "| --- | --- | --- |\n"
        f"{delivery_rows}\n\n"
        "## Daily Learning Coverage\n",
        1,
    )
    migrated = re.sub(
        r"(?m)^- resume_note: .+$",
        "- resume_note: The recovered short session arc is complete; compose and finalize its evidence-backed TIL.",
        migrated,
        count=1,
    )
    migrated = migrated.rstrip() + (
        "\n\n## TIL Composition\n\n"
        "- mode: pending\n"
        "- state: pending\n"
        "- review: pending\n"
        "- composed_at: pending\n"
        "- draft_sha256: pending\n"
        "- dated_til_path: pending\n"
        "- commit_sha: pending\n\n"
        "| Item ID | Section | Evidence IDs | Representation | Content SHA-256 |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| none | none | none | none | none |\n"
    )
    if _evidence_blocks(migrated) != learner_content_before:
        raise MigrationError("learner evidence bytes changed during migration")

    _atomic_write(handoff, migrated)
    report = validate_handoff(handoff, repo_root=root, check_draft=True)
    if not report.ok:
        _atomic_write(handoff, text)
        detail = "\n".join(error.rendered(report.path) for error in report.errors)
        raise MigrationError("migrated v8 handoff did not validate\n" + detail)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", nargs="?", type=Path, default=Path("tmp/active-lesson-handoff.md"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        migrate_completed_v7_handoff(args.handoff)
    except (OSError, UnicodeError, MigrationError) as error:
        print(f"ERROR {args.handoff}:1 [V7_RECOVERY] {error}", file=sys.stderr)
        return 1
    print(f"OK {args.handoff.as_posix()} [migrated-v7-to-v8-short]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
