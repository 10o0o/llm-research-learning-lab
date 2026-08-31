#!/usr/bin/env python3
"""Atomically capture one confirmed learner-evidence item in the daily cursor."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path


COACH_SCRIPTS = Path(__file__).resolve().parents[2] / "coach-llm-research-study" / "scripts"
if str(COACH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(COACH_SCRIPTS))

from validate_lesson_handoff import (  # noqa: E402
    ValidationError,
    validate_handoff,
)
from daily_learning_flow import (  # noqa: E402
    DEFAULT_CURSOR_PATH,
    FlowError,
    load_flow,
    record_lesson_evidence,
    save_flow,
)


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
        try:
            directory_fd = os.open(path.parent, os.O_RDONLY)
        except OSError:
            directory_fd = None
        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def _render_error(path: Path, error: ValidationError) -> str:
    return error.rendered(path)


def append_evidence(
    handoff_path: Path | str,
    evidence_id: str,
    *,
    repo_root: Path | str | None = None,
    cursor: str = DEFAULT_CURSOR_PATH,
    now: datetime | None = None,
) -> tuple[int, str]:
    report = validate_handoff(handoff_path, repo_root=repo_root, check_draft=False)
    if not report.ok or report.document is None:
        return report.exit_code, "\n".join(_render_error(report.path, error) for error in report.errors)
    doc = report.document
    item = doc.evidence.get(evidence_id)
    if item is None:
        error = ValidationError(1, "EVIDENCE_STATE", f"unknown learner evidence ID: {evidence_id}")
        return 1, _render_error(report.path, error)
    if item.values.get("provenance") != "learner" or item.values.get("verdict") != "confirmed":
        error = ValidationError(item.line, "EVIDENCE_STATE", f"{evidence_id} is not confirmed learner-authored evidence")
        return 1, _render_error(report.path, error)
    if item.values.get("capture_state") not in {"pending", "captured"}:
        error = ValidationError(item.line, "EVIDENCE_STATE", f"{evidence_id} is not eligible for daily-flow capture")
        return 1, _render_error(report.path, error)
    if doc.metadata.get("status") not in {"active", "paused", "completed"}:
        error = ValidationError(item.line, "REVIEW_NOT_PASS", "evidence append requires an active, paused, or completed reviewed lesson")
        return 1, _render_error(report.path, error)

    try:
        state = load_flow(doc.repo_root, path=cursor)
        relative_handoff = report.path.resolve().relative_to(doc.repo_root).as_posix()
        state = record_lesson_evidence(
            state,
            cycle_id=doc.metadata["cycle_id"],
            lesson_id=doc.metadata["lesson_id"],
            handoff_path=relative_handoff,
            evidence={
                "evidence_id": evidence_id,
                "concept_ids": [value.strip() for value in item.values["concept_ids"].split(",")],
                "objective_ids": [value.strip() for value in item.values["objective_ids"].split(",")],
                "kind": item.values["kind"],
                "provenance": item.values["provenance"],
                "verdict": item.values["verdict"],
                "content": item.content,
                "content_sha256": item.values["content_sha256"],
                "captured_at": item.values["captured_at"],
            },
            now=now,
        )
        save_flow(state, doc.repo_root, path=cursor, now=now)
    except (FlowError, ValueError) as exc:
        error = ValidationError(item.line, "FLOW_STATE", str(exc))
        return 1, _render_error(report.path, error)

    state_changed = item.values.get("capture_state") != "captured"
    if state_changed:
        span_start, span_end = item.capture_value_span
        if span_start <= 0 or span_end < span_start:
            error = ValidationError(item.line, "SCHEMA", f"cannot locate {evidence_id} capture_state")
            return 2, _render_error(report.path, error)
        updated_handoff = doc.text[:span_start] + "captured" + doc.text[span_end:]
        _atomic_write(report.path, updated_handoff)

    final_report = validate_handoff(report.path, repo_root=doc.repo_root, check_draft=False)
    if not final_report.ok:
        return final_report.exit_code, "\n".join(_render_error(final_report.path, error) for error in final_report.errors)
    if state_changed:
        return 0, f"CAPTURED {evidence_id} -> {cursor}"
    return 0, f"ALREADY_CAPTURED {evidence_id}"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path, help="repository-relative active handoff Markdown path")
    parser.add_argument("--evidence", required=True, help="learner evidence ID such as E001")
    parser.add_argument("--cursor", default=DEFAULT_CURSOR_PATH, help="ignored daily-flow cursor path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        code, message = append_evidence(args.handoff, args.evidence, cursor=args.cursor)
    except Exception as exc:  # pragma: no cover - last-resort CLI boundary
        print(f"ERROR {args.handoff.as_posix()}:1 [SCHEMA] internal error: {exc}", file=sys.stderr)
        return 2
    print(message, file=sys.stdout if code == 0 else sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
