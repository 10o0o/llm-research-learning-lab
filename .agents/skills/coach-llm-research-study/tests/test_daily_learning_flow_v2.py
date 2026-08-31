from __future__ import annotations

import json
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest


SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from daily_learning_flow import (  # noqa: E402
    FlowError,
    _canonical_json,
    begin_cycle,
    capture_completed_session,
    captured_session_projection_sha256,
    eligible_til_cycles,
    empty_flow,
    migrate_cursor_v1_to_v2,
    migrate_flow_v1_to_v2,
    record_practice_decision,
    sha256_bytes,
    start_flow,
    supersede_cycle,
    transition_phase,
    validate_flow,
)
from handoff_fixture import build_handoff  # noqa: E402


NOW = datetime(2026, 8, 31, 9, 0, tzinfo=ZoneInfo("Asia/Seoul"))


def _legacy_v1_state(*, handoff_sha256: str = "a" * 64) -> dict[str, object]:
    state = start_flow(empty_flow(now=NOW), mode="full-day", now=NOW)
    state = begin_cycle(
        state,
        cycle_id="legacy-rnn-attempt",
        primary_target="CC-DL-01",
        now=NOW,
    )
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    cycle = state["cycles"][0]
    evidence = [
        {
            "evidence_id": "E001",
            "concept_ids": ["C01"],
            "objective_ids": ["O001"],
            "kind": "code_interpretation",
            "content": "첫 줄\n\n```python\nh = cell(x, h)\n```\n\n마지막 줄",
            "content_sha256": sha256_bytes(
                "첫 줄\n\n```python\nh = cell(x, h)\n```\n\n마지막 줄".encode("utf-8")
            ),
            "captured_at": "2026-08-30T12:00:00+09:00",
        }
    ]
    cycle.update(
        {
            "lesson_id": "legacy-rnn-lesson",
            "handoff_sha256": handoff_sha256,
            "concepts": [
                {
                    "concept_id": "C01",
                    "title": "recurrence",
                    "source_location": "materials/lesson.md#recurrence",
                    "objective_ids": ["O001"],
                    "observable_outcomes": ["Trace recurrent state."],
                    "evidence_ids": ["E001"],
                }
            ],
            "learner_evidence": evidence,
            "learner_evidence_sha256": sha256_bytes(_canonical_json(evidence)),
            "source_provenance": [
                {
                    "primary_id": "I001",
                    "role": "primary",
                    "path": "materials/lesson.md",
                    "sha256": "b" * 64,
                }
            ],
        }
    )
    state["learner_evidence_sha256"] = sha256_bytes(
        _canonical_json(
            [
                {
                    "cycle_id": cycle["cycle_id"],
                    "sha256": cycle["learner_evidence_sha256"],
                }
            ]
        )
    )
    legacy = deepcopy(state)
    legacy["schema_version"] = 1
    legacy_cycle = legacy["cycles"][0]
    legacy_cycle.pop("captured_session")
    legacy_cycle.pop("supersession")
    legacy_cycle["practice"].pop("milestone_id")
    return legacy


def _write_preserved_attempt_notebook(
    root: Path,
    state: dict[str, object],
    *,
    cycle_id: str = "legacy-rnn-attempt",
) -> Path:
    cycle = next(
        item for item in state["cycles"] if item["cycle_id"] == cycle_id
    )
    captured = cycle["captured_session"]
    concept_ids = [item["concept_id"] for item in captured["concepts"]]
    evidence_ids = [item["evidence_id"] for item in captured["learner_evidence"]]
    payload = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 7,
                "id": "learner-e01",
                "metadata": {},
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": ["preserved learner output\n"],
                    }
                ],
                "source": ["h = cell(x, h)\n"],
            }
        ],
        "metadata": {
            "llm_research_lab": {
                "practice": {
                    "schema_version": 5,
                    "practice_layer": "PRE_LAB",
                    "implementation_depth": "I1_MECHANISM",
                    "lifecycle": "preserved_attempt",
                    "milestone_id": None,
                    "milestone_definition_sha256": None,
                    "learning_inputs": [
                        {
                            "id": "L001",
                            "role": "primary",
                            "kind": "captured-cycle",
                            "cycle_id": captured["cycle_id"],
                            "lesson_id": captured["lesson_id"],
                            "primary_target": captured["primary_target"],
                            "bridge_target": captured["bridge_target"],
                            "concept_ids": concept_ids,
                            "evidence_ids": evidence_ids,
                            "captured_session_sha256": captured["projection_sha256"],
                        }
                    ],
                }
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    notebook = root / "practice/deep-learning/rnn-lstm-state-contracts.ipynb"
    notebook.parent.mkdir(parents=True, exist_ok=True)
    notebook.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    return notebook


def _assert_old_fields_unchanged(old: object, new: object) -> None:
    if isinstance(old, dict):
        assert isinstance(new, dict)
        for key, value in old.items():
            if key == "schema_version":
                continue
            assert key in new
            _assert_old_fields_unchanged(value, new[key])
    elif isinstance(old, list):
        assert isinstance(new, list) and len(old) == len(new)
        for before, after in zip(old, new, strict=True):
            _assert_old_fields_unchanged(before, after)
    else:
        assert new == old


def test_v1_to_v2_migration_is_deterministic_idempotent_and_preserves_evidence() -> None:
    legacy = _legacy_v1_state()
    migrated = migrate_flow_v1_to_v2(legacy)
    _assert_old_fields_unchanged(legacy, migrated)
    assert migrated["schema_version"] == 2
    captured = migrated["cycles"][0]["captured_session"]
    assert captured["schema_version"] == 9
    assert captured["learner_evidence"] == legacy["cycles"][0]["learner_evidence"]
    assert captured["projection_sha256"] == captured_session_projection_sha256(captured)
    assert migrate_flow_v1_to_v2(migrated) == migrated


def test_cursor_migration_writes_identical_bytes_on_retry(tmp_path: Path) -> None:
    path = tmp_path / "tmp/active-learning-flow.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(_canonical_json(_legacy_v1_state()))
    migrate_cursor_v1_to_v2(tmp_path)
    first = path.read_bytes()
    migrate_cursor_v1_to_v2(tmp_path)
    assert path.read_bytes() == first


def test_supersede_preserves_all_learning_bytes_and_permits_replacement_cycle(
    tmp_path: Path,
) -> None:
    archive = tmp_path / "tmp/lesson-attempts/legacy-rnn-attempt/handoff.md"
    archive.parent.mkdir(parents=True)
    archive.write_bytes(b"preserved v9 handoff\n")
    archive_hash = sha256_bytes(archive.read_bytes())
    state = migrate_flow_v1_to_v2(
        _legacy_v1_state(handoff_sha256=archive_hash)
    )
    cycle_before = deepcopy(state["cycles"][0])
    practice = _write_preserved_attempt_notebook(tmp_path, state)
    practice_hash = sha256_bytes(practice.read_bytes())
    receipt = {
        "path": "practice/deep-learning/rnn-lstm-state-contracts.ipynb",
        "sha256": practice_hash,
        "practice_layer": "PRE_LAB",
        "implementation_depth": "I1_MECHANISM",
        "attempt_state": "preserved_attempt",
    }
    superseded = supersede_cycle(
        state,
        cycle_id="legacy-rnn-attempt",
        reason="Restart under CC-SEQ-01 and schema v10.",
        replacement_cycle_id="fresh-rnn-sequence-module",
        archive_path="tmp/lesson-attempts/legacy-rnn-attempt/handoff.md",
        archive_sha256=archive_hash,
        practice_receipt=receipt,
        repo_root=tmp_path,
        now=NOW,
    )
    cycle_after = superseded["cycles"][0]
    for key in (
        "concepts",
        "learner_evidence",
        "learner_evidence_sha256",
        "captured_session",
        "learning_commits",
        "practice",
    ):
        assert cycle_after[key] == cycle_before[key]
    assert cycle_after["status"] == "superseded"
    assert superseded["phase"] == "SELECT_TARGET"
    assert superseded["active_cycle_id"] is None
    assert eligible_til_cycles(superseded) == []
    retried = supersede_cycle(
        superseded,
        cycle_id="legacy-rnn-attempt",
        reason="Restart under CC-SEQ-01 and schema v10.",
        replacement_cycle_id="fresh-rnn-sequence-module",
        archive_path="tmp/lesson-attempts/legacy-rnn-attempt/handoff.md",
        archive_sha256=archive_hash,
        practice_receipt=receipt,
        repo_root=tmp_path,
        now=NOW,
    )
    assert retried == superseded
    replacement = begin_cycle(
        superseded,
        cycle_id="fresh-rnn-sequence-module",
        primary_target="CC-SEQ-01",
        now=NOW,
    )
    assert replacement["active_cycle_id"] == "fresh-rnn-sequence-module"


def test_supersede_rejects_a_receipt_whose_bytes_do_not_match(tmp_path: Path) -> None:
    archive = tmp_path / "tmp/lesson-attempts/legacy-rnn-attempt/handoff.md"
    archive.parent.mkdir(parents=True)
    archive.write_bytes(b"actual archive")
    archive_hash = sha256_bytes(archive.read_bytes())
    state = migrate_flow_v1_to_v2(
        _legacy_v1_state(handoff_sha256=archive_hash)
    )
    practice = _write_preserved_attempt_notebook(tmp_path, state)
    receipt = {
        "path": "practice/deep-learning/rnn-lstm-state-contracts.ipynb",
        "sha256": sha256_bytes(practice.read_bytes()),
        "practice_layer": "PRE_LAB",
        "implementation_depth": "I1_MECHANISM",
        "attempt_state": "preserved_attempt",
    }
    with pytest.raises(FlowError, match="archive_sha256 differs"):
        supersede_cycle(
            state,
            cycle_id="legacy-rnn-attempt",
            reason="Restart under schema v10.",
            replacement_cycle_id="fresh-rnn-sequence-module",
            archive_path="tmp/lesson-attempts/legacy-rnn-attempt/handoff.md",
            archive_sha256="0" * 64,
            practice_receipt=receipt,
            repo_root=tmp_path,
            now=NOW,
        )
    mismatched_practice = {**receipt, "sha256": "0" * 64}
    with pytest.raises(FlowError, match="practice_receipt sha256 differs"):
        supersede_cycle(
            state,
            cycle_id="legacy-rnn-attempt",
            reason="Restart under schema v10.",
            replacement_cycle_id="fresh-rnn-sequence-module",
            archive_path="tmp/lesson-attempts/legacy-rnn-attempt/handoff.md",
            archive_sha256=archive_hash,
            practice_receipt=mismatched_practice,
            repo_root=tmp_path,
            now=NOW,
        )


def test_supersede_rejects_arbitrary_paths_claims_and_notebook_metadata(
    tmp_path: Path,
) -> None:
    archive = tmp_path / "tmp/lesson-attempts/legacy-rnn-attempt/handoff.md"
    archive.parent.mkdir(parents=True)
    archive.write_bytes(b"exact old handoff")
    archive_hash = sha256_bytes(archive.read_bytes())
    state = migrate_flow_v1_to_v2(
        _legacy_v1_state(handoff_sha256=archive_hash)
    )
    practice = _write_preserved_attempt_notebook(tmp_path, state)
    receipt = {
        "path": "practice/deep-learning/rnn-lstm-state-contracts.ipynb",
        "sha256": sha256_bytes(practice.read_bytes()),
        "practice_layer": "PRE_LAB",
        "implementation_depth": "I1_MECHANISM",
        "attempt_state": "preserved_attempt",
    }
    arbitrary_archive = tmp_path / "tmp/arbitrary-handoff.md"
    arbitrary_archive.parent.mkdir(parents=True, exist_ok=True)
    arbitrary_archive.write_bytes(archive.read_bytes())
    with pytest.raises(FlowError, match="tmp/lesson-attempts/legacy-rnn-attempt"):
        supersede_cycle(
            state,
            cycle_id="legacy-rnn-attempt",
            reason="Restart under schema v10.",
            replacement_cycle_id="fresh-rnn-sequence-module",
            archive_path="tmp/arbitrary-handoff.md",
            archive_sha256=archive_hash,
            practice_receipt=receipt,
            repo_root=tmp_path,
            now=NOW,
        )

    for field, value, message in (
        ("practice_layer", "MODULE_ASSIGNMENT", "practice_layer must be PRE_LAB"),
        (
            "implementation_depth",
            "I3_WORKFLOW",
            "implementation_depth must be I1_MECHANISM",
        ),
    ):
        claimed = {**receipt, field: value}
        with pytest.raises(FlowError, match=message):
            supersede_cycle(
                state,
                cycle_id="legacy-rnn-attempt",
                reason="Restart under schema v10.",
                replacement_cycle_id="fresh-rnn-sequence-module",
                archive_path="tmp/lesson-attempts/legacy-rnn-attempt/handoff.md",
                archive_sha256=archive_hash,
                practice_receipt=claimed,
                repo_root=tmp_path,
                now=NOW,
            )

    arbitrary_practice = tmp_path / "tmp/arbitrary-practice.ipynb"
    arbitrary_practice.write_bytes(practice.read_bytes())
    outside_receipt = {
        **receipt,
        "path": "tmp/arbitrary-practice.ipynb",
        "sha256": sha256_bytes(arbitrary_practice.read_bytes()),
    }
    with pytest.raises(FlowError, match=r"practice/\*\.ipynb"):
        supersede_cycle(
            state,
            cycle_id="legacy-rnn-attempt",
            reason="Restart under schema v10.",
            replacement_cycle_id="fresh-rnn-sequence-module",
            archive_path="tmp/lesson-attempts/legacy-rnn-attempt/handoff.md",
            archive_sha256=archive_hash,
            practice_receipt=outside_receipt,
            repo_root=tmp_path,
            now=NOW,
        )

    wrong_handoff_state = migrate_flow_v1_to_v2(
        _legacy_v1_state(handoff_sha256="b" * 64)
    )
    wrong_handoff_practice = _write_preserved_attempt_notebook(
        tmp_path,
        wrong_handoff_state,
    )
    wrong_handoff_receipt = {
        **receipt,
        "sha256": sha256_bytes(wrong_handoff_practice.read_bytes()),
    }
    with pytest.raises(FlowError, match="must equal the selected old handoff hash"):
        supersede_cycle(
            wrong_handoff_state,
            cycle_id="legacy-rnn-attempt",
            reason="Restart under schema v10.",
            replacement_cycle_id="fresh-rnn-sequence-module",
            archive_path="tmp/lesson-attempts/legacy-rnn-attempt/handoff.md",
            archive_sha256=archive_hash,
            practice_receipt=wrong_handoff_receipt,
            repo_root=tmp_path,
            now=NOW,
        )

    practice = _write_preserved_attempt_notebook(tmp_path, state)
    receipt["sha256"] = sha256_bytes(practice.read_bytes())
    payload = json.loads(practice.read_text(encoding="utf-8"))
    payload["metadata"]["llm_research_lab"]["practice"]["milestone_id"] = "MA-SEQUENCE-01"
    practice.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    drifted_receipt = {**receipt, "sha256": sha256_bytes(practice.read_bytes())}
    with pytest.raises(FlowError, match="null milestone"):
        supersede_cycle(
            state,
            cycle_id="legacy-rnn-attempt",
            reason="Restart under schema v10.",
            replacement_cycle_id="fresh-rnn-sequence-module",
            archive_path="tmp/lesson-attempts/legacy-rnn-attempt/handoff.md",
            archive_sha256=archive_hash,
            practice_receipt=drifted_receipt,
            repo_root=tmp_path,
            now=NOW,
        )


def test_validate_flow_rechecks_supersession_notebook_provenance(tmp_path: Path) -> None:
    archive = tmp_path / "tmp/lesson-attempts/legacy-rnn-attempt/handoff.md"
    archive.parent.mkdir(parents=True)
    archive.write_bytes(b"exact old handoff")
    archive_hash = sha256_bytes(archive.read_bytes())
    state = migrate_flow_v1_to_v2(
        _legacy_v1_state(handoff_sha256=archive_hash)
    )
    practice = _write_preserved_attempt_notebook(tmp_path, state)
    receipt = {
        "path": "practice/deep-learning/rnn-lstm-state-contracts.ipynb",
        "sha256": sha256_bytes(practice.read_bytes()),
        "practice_layer": "PRE_LAB",
        "implementation_depth": "I1_MECHANISM",
        "attempt_state": "preserved_attempt",
    }
    superseded = supersede_cycle(
        state,
        cycle_id="legacy-rnn-attempt",
        reason="Restart under schema v10.",
        replacement_cycle_id="fresh-rnn-sequence-module",
        archive_path="tmp/lesson-attempts/legacy-rnn-attempt/handoff.md",
        archive_sha256=archive_hash,
        practice_receipt=receipt,
        repo_root=tmp_path,
        now=NOW,
    )
    payload = json.loads(practice.read_text(encoding="utf-8"))
    payload["metadata"]["llm_research_lab"]["practice"]["learning_inputs"][0][
        "cycle_id"
    ] = "different-old-cycle"
    practice.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    superseded["cycles"][0]["supersession"]["practice_receipt"]["sha256"] = (
        sha256_bytes(practice.read_bytes())
    )
    errors = validate_flow(superseded, repo_root=tmp_path)
    assert any("selected old cycle" in error for error in errors)


def test_migrated_v9_capture_cannot_defer_to_a_milestone(tmp_path: Path) -> None:
    state = migrate_flow_v1_to_v2(_legacy_v1_state())
    state = transition_phase(state, "DECIDE_PRACTICE", now=NOW)
    with pytest.raises(FlowError, match="schema-v9 provenance is ineligible"):
        record_practice_decision(
            state,
            action="DEFER_TO_MILESTONE",
            mode="NONE",
            path=None,
            milestone_id="MA-SEQUENCE-01",
            now=NOW,
        )

    invalid = deepcopy(state)
    invalid["cycles"][0]["status"] = "milestone-pending"
    invalid["cycles"][0]["practice"].update(
        {
            "state": "milestone-pending",
            "action": "DEFER_TO_MILESTONE",
            "mode": "NONE",
            "path": None,
            "milestone_id": "MA-SEQUENCE-01",
        }
    )
    invalid["active_cycle_id"] = None
    invalid["phase"] = "SELECT_TARGET"
    assert any(
        "requires captured schema-v10 provenance" in error
        for error in validate_flow(invalid, repo_root=tmp_path)
    )


def test_milestone_deferral_releases_cycle_without_claiming_completion(
    tmp_path: Path,
) -> None:
    state = start_flow(empty_flow(now=NOW), mode="full-day", now=NOW)
    state = begin_cycle(
        state,
        cycle_id="cycle-sequence-session",
        primary_target="CC-DL-01",
        now=NOW,
    )
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    handoff, _ = build_handoff(
        tmp_path,
        lesson_id="sequence-session",
        status="completed",
        reviews=[("pass", "independent-reviewer")],
    )
    state = capture_completed_session(state, handoff, repo_root=tmp_path, now=NOW)
    deferred = record_practice_decision(
        state,
        action="DEFER_TO_MILESTONE",
        mode="NONE",
        path=None,
        milestone_id="MA-SEQUENCE-01",
        now=NOW,
    )
    cycle = deferred["cycles"][0]
    assert cycle["status"] == "milestone-pending"
    assert cycle["practice"]["state"] == "milestone-pending"
    assert cycle["knowledge"]["state"] == "pending"
    assert cycle["completed_on"] is None
    assert deferred["phase"] == "SELECT_TARGET"
    assert deferred["active_cycle_id"] is None
    assert eligible_til_cycles(deferred) == []
    assert validate_flow(deferred, repo_root=tmp_path) == []


def test_local_assignment_decision_preserves_its_exact_milestone(
    tmp_path: Path,
) -> None:
    state = start_flow(empty_flow(now=NOW), mode="full-day", now=NOW)
    state = begin_cycle(
        state,
        cycle_id="cycle-sequence-assignment",
        primary_target="CC-DL-01",
        now=NOW,
    )
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    handoff, _ = build_handoff(
        tmp_path,
        lesson_id="sequence-assignment",
        status="completed",
        reviews=[("pass", "independent-reviewer")],
    )
    captured = capture_completed_session(state, handoff, repo_root=tmp_path, now=NOW)

    assigned = record_practice_decision(
        captured,
        action="CREATE_LOCAL_PRACTICE",
        mode="NOTEBOOK",
        path="practice/deep-learning/sequence-assignment.ipynb",
        milestone_id="MA-SEQUENCE-01",
        now=NOW,
    )
    cycle = assigned["cycles"][0]
    assert cycle["practice"]["state"] == "awaiting"
    assert cycle["practice"]["milestone_id"] == "MA-SEQUENCE-01"
    assert assigned["phase"] == "AWAIT_PRACTICE"
    assert validate_flow(assigned, repo_root=tmp_path) == []

    with pytest.raises(FlowError, match="valid MA-/PC- milestone"):
        record_practice_decision(
            captured,
            action="CREATE_LOCAL_PRACTICE",
            mode="NOTEBOOK",
            path="practice/deep-learning/sequence-assignment.ipynb",
            milestone_id="later",
            now=NOW,
        )
    with pytest.raises(FlowError, match="local created/continued assignment"):
        record_practice_decision(
            captured,
            action="PROPOSE_EXTERNAL_PRACTICE",
            mode="EXTERNAL_COMPETITION",
            path="practice/deep-learning/sequence-competition.ipynb",
            milestone_id="MA-SEQUENCE-01",
            now=NOW,
        )


def test_captured_session_projection_is_immutable_and_new_capture_requires_v10(
    tmp_path: Path,
) -> None:
    state = start_flow(empty_flow(now=NOW), mode="full-day", now=NOW)
    state = begin_cycle(
        state,
        cycle_id="cycle-current-session",
        primary_target="CC-DL-01",
        now=NOW,
    )
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    handoff, _ = build_handoff(
        tmp_path,
        lesson_id="current-session",
        status="completed",
        reviews=[("pass", "independent-reviewer")],
    )
    captured = capture_completed_session(state, handoff, repo_root=tmp_path, now=NOW)
    projection = captured["cycles"][0]["captured_session"]
    assert projection["schema_version"] == 10
    tampered = deepcopy(captured)
    tampered["cycles"][0]["captured_session"]["lesson_id"] = "changed"
    assert any("captured_session" in item for item in validate_flow(tampered, repo_root=tmp_path))

    legacy_text = handoff.read_text(encoding="utf-8").replace(
        "- schema_version: 10", "- schema_version: 9", 1
    )
    handoff.write_text(legacy_text, encoding="utf-8")
    with pytest.raises(FlowError, match="schema_version must be 10"):
        capture_completed_session(state, handoff, repo_root=tmp_path, now=NOW)
