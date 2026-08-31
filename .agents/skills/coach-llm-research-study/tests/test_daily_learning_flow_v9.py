from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO / ".agents/skills/teach-course-material/scripts"))

from daily_learning_flow import (  # noqa: E402
    FlowError,
    authorization_is_active,
    begin_cycle,
    capture_completed_session,
    complete_cycle,
    eligible_til_cycles,
    empty_flow,
    load_flow,
    pause_flow,
    record_knowledge_result,
    record_practice_decision,
    save_flow,
    start_flow,
    transition_phase,
    validate_flow,
)
from handoff_fixture import CONTRACT, build_handoff  # noqa: E402
from append_lesson_evidence import append_evidence  # noqa: E402
from validate_lesson_handoff import validate_handoff  # noqa: E402


SEOUL = ZoneInfo("Asia/Seoul")
NOW = datetime(2026, 8, 28, 9, 0, tzinfo=SEOUL)


def _started_cycle(root: Path) -> dict[str, object]:
    state = start_flow(empty_flow(now=NOW), mode="full-day", now=NOW)
    state = begin_cycle(
        state,
        cycle_id="cycle-tensor-shape-lesson",
        primary_target="CC-DL-01",
        handoff_path="tmp/active-lesson-handoff.md",
        now=NOW,
    )
    return state


def test_same_day_cursor_is_atomic_resumable_and_authorization_expires_at_midnight(
    tmp_path: Path,
) -> None:
    state = start_flow(empty_flow(now=NOW), mode="full-day", now=NOW)
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    path = save_flow(state, tmp_path, now=NOW)
    assert path == tmp_path / "tmp/active-learning-flow.json"
    resumed = load_flow(tmp_path)
    assert resumed["phase"] == "PREPARE_LESSON"
    assert authorization_is_active(resumed, now=NOW)
    assert not authorization_is_active(resumed, now=NOW + timedelta(days=1))
    assert list(path.parent.glob(".active-learning-flow.json.*")) == []


def test_pause_preserves_exact_resume_phase_and_new_day_start_reactivates_it() -> None:
    state = _started_cycle(Path("."))
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    paused = pause_flow(state, now=NOW)
    assert (paused["phase"], paused["resume_phase"]) == ("PAUSED", "TEACH")
    assert paused["cycles"][0]["status"] == "paused"
    next_day = NOW + timedelta(days=1)
    resumed = start_flow(paused, mode="full-day", now=next_day)
    assert resumed["phase"] == "TEACH"
    assert resumed["cycles"][0]["status"] == "active"
    assert authorization_is_active(resumed, now=next_day)


def test_invalid_phase_jump_is_rejected() -> None:
    state = start_flow(empty_flow(now=NOW), mode="full-day", now=NOW)
    with pytest.raises(FlowError, match="invalid daily-flow transition"):
        transition_phase(state, "AWAIT_PRACTICE", now=NOW)


def test_confirmed_evidence_is_captured_in_cursor_not_manual_scratchpad(
    tmp_path: Path,
) -> None:
    state = _started_cycle(tmp_path)
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    save_flow(state, tmp_path, now=NOW)
    handoff, _ = build_handoff(
        tmp_path,
        status="active",
        reviews=[("pass", "fresh-reviewer")],
        delivery=[
            {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis meaning was taught."},
            {"objective": "O002", "state": "pending", "mode": "none", "note": "Awaiting teaching."},
            {"objective": "O003", "state": "pending", "mode": "none", "note": "Awaiting teaching."},
        ],
        evidence=[
            {
                "concept_ids": "C01",
                "objective_ids": "O001",
                "content": "두 축의 의미를 구분하고 결과 shape를 설명했다.",
                "capture_state": "pending",
            }
        ],
    )
    scratch = tmp_path / "til/today.md"
    scratch.parent.mkdir(parents=True)
    scratch.write_text("사용자가 직접 적은 메모\n", encoding="utf-8")
    before = scratch.read_bytes()
    code, message = append_evidence(handoff, "E001", repo_root=tmp_path, now=NOW)
    assert code == 0, message
    assert scratch.read_bytes() == before
    cursor = load_flow(tmp_path)
    assert cursor["cycles"][0]["learner_evidence"][0]["content"] == "두 축의 의미를 구분하고 결과 shape를 설명했다."
    assert "- capture_state: captured" in handoff.read_text(encoding="utf-8")
    code, message = append_evidence(handoff, "E001", repo_root=tmp_path, now=NOW)
    assert (code, message) == (0, "ALREADY_CAPTURED E001")


def test_completed_handoff_requires_all_non_deferred_concepts_confirmed(
    tmp_path: Path,
) -> None:
    handoff, _ = build_handoff(
        tmp_path,
        status="completed",
        reviews=[("pass", "fresh-reviewer")],
    )
    text = handoff.read_text(encoding="utf-8").replace(
        "| C02 | confirmed | E001 | Confirmed by the integrated learner transfer. |",
        "| C02 | uncertain | E001 | The mechanism still needs a different explanation. |",
    )
    handoff.write_text(text, encoding="utf-8")
    report = validate_handoff(handoff, repo_root=tmp_path)
    assert "SESSION_CONCEPT_INCOMPLETE" in {item.code for item in report.errors}


def test_standard_module_plan_is_independent_of_review_slice_and_enforces_depth(
    tmp_path: Path,
) -> None:
    handoff, _ = build_handoff(tmp_path)
    report = validate_handoff(handoff, repo_root=tmp_path)
    assert report.ok, report.errors

    short = CONTRACT.replace("| M04 | 세 축을 결합한 전이", "| M04 | 정렬 실패와 attention 축의 한계")
    handoff, _ = build_handoff(tmp_path, contract=short)
    assert "SESSION_DEPTH" in {item.code for item in validate_handoff(handoff, repo_root=tmp_path).errors}

    too_brief = CONTRACT.replace("| T005 | 20 |", "| T005 | 5 |")
    handoff, _ = build_handoff(tmp_path, contract=too_brief)
    assert "SESSION_DEPTH" in {item.code for item in validate_handoff(handoff, repo_root=tmp_path).errors}


def test_completed_session_advances_to_practice_and_only_terminal_cycle_is_til_eligible(
    tmp_path: Path,
) -> None:
    state = _started_cycle(tmp_path)
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    handoff, _ = build_handoff(
        tmp_path,
        status="completed",
        reviews=[("pass", "fresh-reviewer")],
    )
    state = capture_completed_session(state, handoff, repo_root=tmp_path, now=NOW)
    assert state["phase"] == "DECIDE_PRACTICE"
    state = record_practice_decision(
        state,
        action="NO_EXTRA_PRACTICE",
        mode="NONE",
        path=None,
        now=NOW,
    )
    state = record_knowledge_result(state, no_change=True, now=NOW)
    state = complete_cycle(
        state,
        next_target_preview={"target_state": "START_TARGET", "primary_target": "CC-DL-02"},
        now=NOW,
    )
    assert [item["cycle_id"] for item in eligible_til_cycles(state)] == [
        "cycle-tensor-shape-lesson"
    ]
    assert validate_flow(state, repo_root=tmp_path) == []


def test_single_lesson_capture_pauses_before_practice_and_does_not_expand_authority(
    tmp_path: Path,
) -> None:
    state = start_flow(empty_flow(now=NOW), mode="lesson-only", now=NOW)
    state = begin_cycle(
        state,
        cycle_id="cycle-single-lesson",
        primary_target="CC-DL-01",
        now=NOW,
    )
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    handoff, _ = build_handoff(
        tmp_path,
        lesson_id="single-lesson",
        status="completed",
        reviews=[("pass", "fresh-reviewer")],
    )
    state = capture_completed_session(state, handoff, repo_root=tmp_path, now=NOW)
    assert state["phase"] == "PAUSED"
    assert state["resume_phase"] == "DECIDE_PRACTICE"
    assert state["authorization"] == {"mode": "none", "authorized_on": None}
    with pytest.raises(FlowError, match="full-day authorization"):
        record_practice_decision(
            state,
            action="NO_EXTRA_PRACTICE",
            mode="NONE",
            path=None,
            now=NOW,
        )


def test_expired_full_day_authorization_cannot_mutate_the_next_phase() -> None:
    state = start_flow(empty_flow(now=NOW), mode="full-day", now=NOW)
    state = begin_cycle(
        state,
        cycle_id="cycle-expired-authorization",
        primary_target="CC-DL-01",
        now=NOW,
    )
    with pytest.raises(FlowError, match="current Asia/Seoul date"):
        transition_phase(state, "PREPARE_LESSON", now=NOW + timedelta(days=1))


def test_unfinished_cycle_is_never_a_til_candidate() -> None:
    state = _started_cycle(Path("."))
    assert eligible_til_cycles(state) == []
    paused = pause_flow(state, now=NOW)
    assert eligible_til_cycles(paused) == []
