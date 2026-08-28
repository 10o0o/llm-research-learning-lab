from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(REPO / ".agents/skills/coach-llm-research-study/scripts"))
sys.path.insert(0, str(REPO / ".agents/skills/coach-llm-research-study/tests"))

from handoff_fixture import build_handoff  # noqa: E402
from route_practice import route_practice  # noqa: E402
from test_validate_practice_artifact import PracticeArtifactValidatorTests  # noqa: E402
from validate_lesson_handoff import validate_handoff  # noqa: E402
from validate_practice_artifact import (  # noqa: E402
    external_completion_commit_target,
    validate,
)
from validate_practice_notebook import _canonical_hash  # noqa: E402


def _codes(items) -> set[str]:
    return {item.code for item in items}


def _v4_notebook(root: Path) -> tuple[Path, Path]:
    notebook = PracticeArtifactValidatorTests().build_notebook(root)
    lesson = root / "materials/lesson.md"
    lesson.write_text(
        "# Lesson\n\n"
        "## learning-goals\n\n"
        "- Identify the batch and feature axes.\n"
        "- Predict the output shape of a broadcast operation.\n"
        "- Review the course map only when it affects the current path.\n\n"
        "## axes\n\nTensor axes.\n\n"
        "## shape-propagation\n\nBroadcast shapes.\n\n"
        "## orientation\n\nUse the course map when navigation is needed.\n\n"
        "## Tensor 카드\n\nTensor 이름을 인자로 받는다.\n",
        encoding="utf-8",
    )
    initial = json.loads(notebook.read_text(encoding="utf-8"))
    initial["metadata"]["llm_research_lab"]["practice"]["sources"][0][
        "sha256"
    ] = hashlib.sha256(lesson.read_bytes()).hexdigest()
    notebook.write_text(json.dumps(initial, ensure_ascii=False), encoding="utf-8")
    handoff, _ = build_handoff(
        root,
        status="completed",
        reviews=[("pass", "fresh-reviewer")],
    )
    report = validate_handoff(handoff, repo_root=root)
    assert report.ok and report.document is not None, report.errors
    doc = report.document
    evidence = [
        {
            "evidence_id": item.evidence_id,
            "concept_ids": [value.strip() for value in item.values["concept_ids"].split(",")],
            "objective_ids": [value.strip() for value in item.values["objective_ids"].split(",")],
            "kind": item.values["kind"],
            "content": item.content,
            "content_sha256": item.values["content_sha256"],
            "captured_at": item.values["captured_at"],
        }
        for item in doc.evidence.values()
        if item.values.get("verdict") == "confirmed"
    ]
    concepts = [
        concept_id
        for concept_id, coverage in doc.learning_coverage.items()
        if coverage.today_state == "confirmed"
    ]
    projection = [
        {
            "concept_id": concept_id,
            "objective_ids": [
                objective.objective_id
                for objective in doc.objectives.values()
                if objective.concept_id == concept_id and objective.treatment != "deferred"
            ],
            "evidence_ids": list(doc.learning_coverage[concept_id].evidence_ids),
        }
        for concept_id in concepts
    ]
    payload = json.loads(notebook.read_text(encoding="utf-8"))
    practice = payload["metadata"]["llm_research_lab"]["practice"]
    practice["schema_version"] = 4
    practice.pop("til")
    practice["learning_input"] = {
        "kind": "lesson-session",
        "cycle_id": doc.metadata["cycle_id"],
        "lesson_id": doc.metadata["lesson_id"],
        "handoff_path": "tmp/active-lesson-handoff.md",
        "handoff_sha256": hashlib.sha256(handoff.read_bytes()).hexdigest(),
        "primary_target": doc.target_decision.primary_target,
        "bridge_target": None,
        "concept_ids": concepts,
        "evidence_ids": [item["evidence_id"] for item in evidence],
        "concept_sha256": _canonical_hash(projection),
        "learner_evidence_sha256": _canonical_hash(evidence),
    }
    practice["outcomes"][0].pop("til_location")
    practice["outcomes"][0]["concept_ids"] = concepts
    practice["outcomes"][0]["evidence_ids"] = [item["evidence_id"] for item in evidence]
    notebook.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return notebook, handoff


def test_session_based_v4_passes_and_legacy_v3_stays_supported(tmp_path: Path) -> None:
    v3 = PracticeArtifactValidatorTests().build_notebook(tmp_path / "legacy")
    assert validate(v3, repo_root=tmp_path / "legacy", check_collection=False) == []

    notebook, _ = _v4_notebook(tmp_path / "v4")
    assert validate(notebook, repo_root=tmp_path / "v4", check_collection=False) == []


def test_session_hash_drift_is_repair_required_and_cleanup_is_offline_warning(
    tmp_path: Path,
) -> None:
    notebook, handoff = _v4_notebook(tmp_path)
    handoff.write_text(handoff.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert "SESSION_REPAIR_REQUIRED" in _codes(
        validate(notebook, repo_root=tmp_path, check_collection=False)
    )

    notebook, handoff = _v4_notebook(tmp_path / "offline")
    handoff.unlink()
    warnings = []
    assert validate(
        notebook,
        repo_root=tmp_path / "offline",
        check_collection=False,
        learner_state=True,
        warnings=warnings,
    ) == []
    assert _codes(warnings) == {"SESSION_SOURCE_OFFLINE"}
    assert "SESSION_REPAIR_REQUIRED" in _codes(
        validate(
            notebook,
            repo_root=tmp_path / "offline",
            check_collection=False,
            completion_ready=True,
        )
    )


def test_session_outcomes_require_exact_concept_and_evidence_relations(
    tmp_path: Path,
) -> None:
    notebook, _ = _v4_notebook(tmp_path)
    payload = json.loads(notebook.read_text(encoding="utf-8"))
    outcome = payload["metadata"]["llm_research_lab"]["practice"]["outcomes"][0]
    outcome["concept_ids"] = ["C99"]
    notebook.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    assert "SESSION_REPAIR_REQUIRED" in _codes(
        validate(notebook, repo_root=tmp_path, check_collection=False)
    )


def test_router_distinguishes_session_and_til_repair_and_keeps_competition(
) -> None:
    session = route_practice(
        "evaluation-data",
        learning_input_kind="lesson-session",
        learning_input_ready=False,
    )
    assert session.practice_action == "SESSION_REPAIR_REQUIRED"
    legacy = route_practice("evaluation-data", til_ready=False)
    assert legacy.practice_action == "TIL_REPAIR_REQUIRED"
    competition = route_practice(
        "valuable-competition",
        learning_input_kind="lesson-session",
        external_item_verified_current=True,
        external_item_valuable=True,
    )
    assert (
        competition.practice_action,
        competition.practice_mode,
        competition.approval_required,
    ) == ("PROPOSE_EXTERNAL_PRACTICE", "EXTERNAL_COMPETITION", True)


def test_external_challenge_commit_target_requires_interpretation_and_exact_path(
    tmp_path: Path,
) -> None:
    challenge = tmp_path / "challenges/deep-ml/solutions/example.py"
    challenge.parent.mkdir(parents=True)
    challenge.write_text("result = 3\n", encoding="utf-8")
    assert external_completion_commit_target(
        challenge,
        repo_root=tmp_path,
        interpretation_evidence=["입력 크기가 늘 때 비교 횟수가 어떻게 변하는지 확인했다."],
    ) == "challenges/deep-ml/solutions/example.py"
    try:
        external_completion_commit_target(
            challenge,
            repo_root=tmp_path,
            interpretation_evidence=[],
        )
    except ValueError as error:
        assert "interpretation" in str(error)
    else:  # pragma: no cover
        raise AssertionError("platform-only completion must not pass")
