#!/usr/bin/env python3
"""Record an already-completed independent v5 practice review atomically.

This helper does not perform or approve a review. It only records the supplied
learner-surface and metadata verdicts while preserving every Notebook cell.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import stat
import tempfile
from datetime import datetime
from pathlib import Path

from validate_practice_notebook import practice_contract_hash


VERDICTS = {"pass", "repair_required"}


def _practice(payload: dict[str, object]) -> dict[str, object]:
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError("Notebook metadata is missing")
    lab = metadata.get("llm_research_lab")
    if not isinstance(lab, dict) or not isinstance(lab.get("practice"), dict):
        raise ValueError("metadata.llm_research_lab.practice is missing")
    return lab["practice"]


def _rfc3339(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(
            value[:-1] + "+00:00" if value.endswith("Z") else value
        )
    except ValueError:
        return False
    return parsed.tzinfo is not None


def record_review(
    payload: dict[str, object],
    *,
    reviewer_id: str,
    reviewed_at: str,
    learner_surface_verdict: str,
    metadata_verdict: str,
) -> dict[str, object]:
    """Return a payload with one factual review record and unchanged cells."""

    updated = copy.deepcopy(payload)
    cells_before = copy.deepcopy(updated.get("cells"))
    practice = _practice(updated)
    if practice.get("schema_version") != 5:
        raise ValueError("creation reviews can be recorded only on schema v5")
    if not reviewer_id.strip():
        raise ValueError("reviewer_id must be non-empty")
    if not _rfc3339(reviewed_at):
        raise ValueError("reviewed_at must be RFC 3339 with a timezone")
    if learner_surface_verdict not in VERDICTS or metadata_verdict not in VERDICTS:
        raise ValueError("both review verdicts must be pass or repair_required")
    reviews = practice.get("creation_reviews")
    if not isinstance(reviews, list):
        raise ValueError("creation_reviews must be a list")
    if len(reviews) >= 2:
        raise ValueError("at most two creation reviews may be recorded")
    if reviews:
        first = reviews[0]
        if not isinstance(first, dict) or first.get("verdict") != "repair_required":
            raise ValueError("a second review is allowed only after one repair_required review")
        if first.get("reviewer_id") == reviewer_id:
            raise ValueError("the second review must use a fresh reviewer")
    verdict = (
        "pass"
        if learner_surface_verdict == metadata_verdict == "pass"
        else "repair_required"
    )
    iteration = len(reviews) + 1
    review = {
        "iteration": iteration,
        "reviewer_id": reviewer_id,
        "reviewed_at": reviewed_at,
        "learner_surface_verdict": learner_surface_verdict,
        "metadata_verdict": metadata_verdict,
        "verdict": verdict,
        "contract_sha256": practice_contract_hash(updated),
        "recheck_of": None if iteration == 1 else 1,
    }
    reviews.append(review)
    if updated.get("cells") != cells_before:
        raise AssertionError("recording a review changed Notebook cells")
    return updated


def _atomic_write(path: Path, payload: dict[str, object]) -> None:
    mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=1)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--reviewed-at", required=True)
    parser.add_argument(
        "--learner-surface-verdict", choices=sorted(VERDICTS), required=True
    )
    parser.add_argument("--metadata-verdict", choices=sorted(VERDICTS), required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo = args.repo_root.resolve()
    notebook = args.notebook if args.notebook.is_absolute() else repo / args.notebook
    try:
        notebook = notebook.resolve(strict=True)
        relative = notebook.relative_to(repo)
        if not relative.parts or relative.parts[0] != "practice" or notebook.suffix != ".ipynb":
            raise ValueError("review target must be one practice/*.ipynb file")
        payload = json.loads(notebook.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Notebook root must be an object")
        cells_before = copy.deepcopy(payload.get("cells"))
        updated = record_review(
            payload,
            reviewer_id=args.reviewer_id,
            reviewed_at=args.reviewed_at,
            learner_surface_verdict=args.learner_surface_verdict,
            metadata_verdict=args.metadata_verdict,
        )
        _atomic_write(notebook, updated)
        rewritten = json.loads(notebook.read_text(encoding="utf-8"))
        if rewritten.get("cells") != cells_before:
            raise AssertionError("atomic review recording changed Notebook cells")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}, ensure_ascii=False))
        return 1
    review = _practice(updated)["creation_reviews"][-1]
    print(
        json.dumps(
            {
                "status": "RECORDED",
                "path": relative.as_posix(),
                "iteration": review["iteration"],
                "verdict": review["verdict"],
                "contract_sha256": review["contract_sha256"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
