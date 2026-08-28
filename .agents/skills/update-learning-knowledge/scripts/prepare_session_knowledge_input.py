#!/usr/bin/env python3
"""Prepare exact TIL-independent evidence for the day-flow knowledge phase."""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
COACH_SCRIPTS = SCRIPT_DIR.parents[1] / "coach-llm-research-study" / "scripts"
if str(COACH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(COACH_SCRIPTS))

from daily_learning_flow import (  # noqa: E402
    DEFAULT_CURSOR_PATH,
    FlowError,
    load_flow,
    sha256_file,
    validate_flow,
)


class KnowledgeInputError(RuntimeError):
    """Raised when practice/session evidence is not ready for knowledge synthesis."""


def prepare_session_knowledge_input(
    *,
    repo_root: Path | str,
    cursor: str = DEFAULT_CURSOR_PATH,
    cycle_id: str | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    state = load_flow(root, path=cursor)
    errors = validate_flow(state, repo_root=root, verify_commits=True)
    if errors:
        raise KnowledgeInputError("cursor verification failed: " + "; ".join(errors))
    selected_id = cycle_id or state.get("active_cycle_id")
    cycle = next(
        (item for item in state.get("cycles", []) if item.get("cycle_id") == selected_id),
        None,
    )
    if cycle is None:
        raise KnowledgeInputError("no exact cycle is selected for knowledge synthesis")
    if cycle.get("status") == "completed":
        raise KnowledgeInputError("completed cycles already passed the knowledge phase")
    if state.get("phase") != "UPDATE_KNOWLEDGE":
        raise KnowledgeInputError("PRACTICE_INCOMPLETE: cycle has not reached UPDATE_KNOWLEDGE")
    practice = cycle.get("practice", {})
    if practice.get("state") not in {"completed", "no-extra-practice"}:
        raise KnowledgeInputError("PRACTICE_INCOMPLETE: practice is not terminal")
    if not cycle.get("concepts") or not cycle.get("learner_evidence"):
        raise KnowledgeInputError("session evidence was not captured")
    if practice.get("state") == "completed":
        raw_path = practice.get("path")
        path = root / str(raw_path)
        if not path.is_file() or sha256_file(path) != practice.get("sha256"):
            raise KnowledgeInputError("completed practice artifact is missing or has hash drift")
        if not practice.get("interpretation_evidence"):
            raise KnowledgeInputError("completed practice lacks learner interpretation")
    return {
        "cycle_id": cycle["cycle_id"],
        "lesson_id": cycle.get("lesson_id"),
        "primary_target": cycle["primary_target"],
        "bridge_target": cycle.get("bridge_target"),
        "concepts": deepcopy(cycle["concepts"]),
        "learner_evidence": deepcopy(cycle["learner_evidence"]),
        "practice": deepcopy(practice),
        "source_provenance": deepcopy(cycle.get("source_provenance", [])),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cursor", default=DEFAULT_CURSOR_PATH)
    parser.add_argument("--cycle-id")
    args = parser.parse_args(argv)
    try:
        root = next(
            candidate
            for candidate in Path(__file__).resolve().parents
            if (candidate / "AGENTS.md").is_file()
        )
        result = prepare_session_knowledge_input(
            repo_root=root,
            cursor=args.cursor,
            cycle_id=args.cycle_id,
        )
    except (OSError, StopIteration, FlowError, KnowledgeInputError) as error:
        print(f"ERROR {args.cursor}:1 [KNOWLEDGE_INPUT] {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
