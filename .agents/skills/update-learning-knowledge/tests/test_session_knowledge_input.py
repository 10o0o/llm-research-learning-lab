from __future__ import annotations

import sys
from pathlib import Path

import pytest


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
COACH = REPO / ".agents/skills/coach-llm-research-study"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(COACH / "scripts"))
sys.path.insert(0, str(COACH / "tests"))

from daily_learning_flow import (  # noqa: E402
    begin_cycle,
    capture_completed_session,
    empty_flow,
    record_practice_decision,
    save_flow,
    start_flow,
    transition_phase,
)
from handoff_fixture import build_handoff  # noqa: E402
from prepare_session_knowledge_input import (  # noqa: E402
    KnowledgeInputError,
    prepare_session_knowledge_input,
)


def _captured_state(root: Path) -> dict[str, object]:
    state = start_flow(empty_flow(), mode="full-day")
    state = begin_cycle(
        state,
        cycle_id="cycle-tensor-shape-lesson",
        primary_target="CC-DL-01",
    )
    state = transition_phase(state, "PREPARE_LESSON")
    state = transition_phase(state, "TEACH")
    handoff, _ = build_handoff(
        root,
        status="completed",
        reviews=[("pass", "fresh-reviewer")],
    )
    return capture_completed_session(state, handoff, repo_root=root)


def test_knowledge_is_blocked_until_practice_is_terminal(tmp_path: Path) -> None:
    state = _captured_state(tmp_path)
    save_flow(state, tmp_path)
    with pytest.raises(KnowledgeInputError, match="PRACTICE_INCOMPLETE"):
        prepare_session_knowledge_input(repo_root=tmp_path)


def test_no_extra_practice_still_exposes_session_evidence_without_a_til(
    tmp_path: Path,
) -> None:
    state = _captured_state(tmp_path)
    state = record_practice_decision(
        state,
        action="NO_EXTRA_PRACTICE",
        mode="NONE",
        path=None,
    )
    save_flow(state, tmp_path)
    result = prepare_session_knowledge_input(repo_root=tmp_path)
    assert result["cycle_id"] == "cycle-tensor-shape-lesson"
    assert result["primary_target"] == "CC-DL-01"
    assert result["concepts"]
    assert result["learner_evidence"]
    assert "til" not in result
