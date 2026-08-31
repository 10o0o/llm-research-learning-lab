from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

from test_validate_practice_artifact import PracticeArtifactValidatorTests


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))

from migrate_practice_v2_to_v3 import migrate_payload  # noqa: E402
from route_practice import route_practice  # noqa: E402
from validate_practice_artifact import (  # noqa: E402
    completion_commit_target,
    validate,
)


def _builder(root: Path) -> Path:
    return PracticeArtifactValidatorTests().build_notebook(root)


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _codes(problems) -> set[str]:
    return {problem.code for problem in problems}


def _completed_notebook(root: Path) -> Path:
    notebook = _builder(root)
    payload = _load(notebook)
    implementation = "".join(payload["cells"][3]["source"]).replace(
        '    raise NotImplementedError("shape를 채우세요")\n',
        "    shape = tuple(tensor.shape)\n",
    )
    payload["cells"][3]["source"] = implementation.splitlines(keepends=True)
    for index, count in ((1, 1), (3, 2), (4, 3), (5, 4)):
        payload["cells"][index]["execution_count"] = count
    _save(notebook, payload)
    return notebook


def test_v2_to_v3_migration_preserves_every_cell_field() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        notebook = _builder(root)
        payload = _load(notebook)
        practice = payload["metadata"]["llm_research_lab"]["practice"]
        practice["schema_version"] = 2
        practice.pop("practice_mode")
        practice.pop("curriculum_targets")
        path_by_id = {item["id"]: item["path"] for item in practice["sources"]}
        for source in practice["sources"]:
            source.pop("id")
        for outcome in practice["outcomes"]:
            outcome.pop("curriculum_target_ids")
        for requirement in practice["requirements"]:
            for location in requirement["source_locations"]:
                location["path"] = path_by_id[location.pop("source_id")]
        before_cells = copy.deepcopy(payload["cells"])
        before_projection = [
            {
                "id": cell.get("id"),
                "source": cell.get("source"),
                "outputs": cell.get("outputs"),
                "execution_count": cell.get("execution_count"),
            }
            for cell in before_cells
        ]
        migrated = migrate_payload(
            payload,
            practice_mode="NOTEBOOK",
            outcome_targets={"O01": ["CC-DL-01"]},
        )
        after_projection = [
            {
                "id": cell.get("id"),
                "source": cell.get("source"),
                "outputs": cell.get("outputs"),
                "execution_count": cell.get("execution_count"),
            }
            for cell in migrated["cells"]
        ]
        assert after_projection == before_projection
        migrated_practice = migrated["metadata"]["llm_research_lab"]["practice"]
        assert migrated_practice["sources"][0]["id"] == "S001"
        assert migrated_practice["requirements"][0]["source_locations"][0]["source_id"] == "S001"
        assert migrated_practice["outcomes"][0]["curriculum_target_ids"] == ["CC-DL-01"]


def test_mode_router_follows_outcome_semantics() -> None:
    assert route_practice(
        "math-tensor-mechanism", prelab_required=True
    ).practice_mode == "NOTEBOOK"
    assert route_practice(
        "inference-performance", prelab_required=True
    ).practice_mode == "BENCHMARK"
    assert route_practice(
        "evaluation-data", prelab_required=True
    ).practice_mode == "DATASET_PROJECT"
    local_fallback = route_practice("short-algorithm-api", prelab_required=True)
    assert (local_fallback.practice_action, local_fallback.practice_mode) == (
        "CREATE_LOCAL_PRACTICE",
        "NOTEBOOK",
    )
    challenge = route_practice(
        "short-algorithm-api",
        external_item_verified_current=True,
        external_item_valuable=True,
    )
    assert (
        challenge.practice_action,
        challenge.practice_mode,
        challenge.approval_required,
        challenge.approval_scope,
    ) == (
        "PROPOSE_EXTERNAL_PRACTICE",
        "EXTERNAL_CHALLENGE",
        True,
        "ACCOUNT_ACCESS_PARTICIPATION_SUBMISSION",
    )
    unhelpful = route_practice(
        "short-algorithm-api",
        external_item_verified_current=True,
        external_item_valuable=False,
        prelab_required=True,
    )
    assert (unhelpful.practice_action, unhelpful.practice_mode) == (
        "CREATE_LOCAL_PRACTICE",
        "NOTEBOOK",
    )
    assert route_practice(
        "math-tensor-mechanism", equivalent_evidence=True
    ).practice_mode == "NONE"


def test_mode_router_reuses_only_a_direct_valuable_unblocked_artifact() -> None:
    reusable = route_practice(
        "inference-performance",
        existing_direct_artifact=True,
        prelab_required=True,
    )
    assert reusable.practice_action == "CONTINUE_EXISTING_PRACTICE"
    for excluded in (
        {"existing_required_execution": False},
        {"existing_cost_effective": False},
        {"existing_paused": True},
        {"conceptual_blocker": True},
    ):
        decision = route_practice(
            "inference-performance",
            existing_direct_artifact=True,
            prelab_required=True,
            **excluded,
        )
        assert (decision.practice_action, decision.practice_mode) == (
            "CREATE_LOCAL_PRACTICE",
            "BENCHMARK",
        )


def test_repository_kdl_outcome_target_migration_is_exact_and_legacy_is_untouched() -> None:
    notebook = _load(
        REPO / "practice/deep-learning/deep-learning-basics-01-04-complete.ipynb"
    )
    practice = notebook["metadata"]["llm_research_lab"]["practice"]
    assert practice["schema_version"] == 3
    assert practice["practice_mode"] == "NOTEBOOK"
    expected = {
        "O01": ["CC-ML-01"],
        "O02": ["CC-ML-01", "CC-DL-02", "CC-DL-06"],
        "O03": ["CC-DL-01", "CC-DL-05"],
        "O04": ["CC-DL-01"],
        "O05": ["CC-DL-01"],
        "O06": ["CC-DL-01"],
        "O07": ["CC-DL-05"],
        "O08": ["CC-DL-05"],
        "O09": ["CC-DL-04"],
        "O10": ["CC-DL-02"],
        "O11": ["CC-DL-02", "CC-ML-02"],
        "O12": ["CC-DL-02", "CC-MATH-03"],
        "O13": ["CC-DL-02", "CC-DL-06"],
    }
    assert {
        outcome["id"]: outcome["curriculum_target_ids"]
        for outcome in practice["outcomes"]
    } == expected
    assert all("id" in source for source in practice["sources"])
    assert all(
        "path" not in location and "source_id" in location
        for requirement in practice["requirements"]
        for location in requirement["source_locations"]
    )

    legacy = _load(REPO / "practice/math/linear-algebra-recall.ipynb")
    legacy_practice = (
        legacy.get("metadata", {}).get("llm_research_lab", {}).get("practice")
    )
    assert legacy_practice is None or legacy_practice.get("schema_version") != 3


def test_target_outcome_and_stable_source_relations_are_bidirectional() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        notebook = _builder(root)
        payload = _load(notebook)
        practice = payload["metadata"]["llm_research_lab"]["practice"]
        practice["outcomes"][0]["curriculum_target_ids"] = ["CC-ML-01"]
        _save(notebook, payload)
        assert "TARGET_RELATION" in _codes(validate(notebook, repo_root=root, check_collection=False))

        payload = _load(_builder(root))
        location = payload["metadata"]["llm_research_lab"]["practice"]["requirements"][0]["source_locations"][0]
        location["source_id"] = "S999"
        _save(notebook, payload)
        assert "AUDIT_METADATA" in _codes(validate(notebook, repo_root=root, check_collection=False))


def test_external_receipt_strict_and_offline_warning() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        notebook = _builder(root)
        payload = _load(notebook)
        practice = payload["metadata"]["llm_research_lab"]["practice"]
        body = b"Tensor \xec\x9d\xb4\xeb\xa6\x84\xec\x9d\x84 \xec\x9d\xb8\xec\x9e\x90\xeb\xa1\x9c \xeb\xb0\x9b\xeb\x8a\x94\xeb\x8b\xa4."
        digest = hashlib.sha256(body).hexdigest()
        cache_path = f"tmp/active-lesson-sources/practice-source/{digest}.txt"
        receipt_path = f"tmp/active-lesson-sources/practice-source/{digest}.receipt.json"
        external = {
            "id": "S001",
            "kind": "external-reference",
            "provider": "Example University",
            "course": "Tensor Course",
            "offering_or_edition": "2026",
            "artifact": "Tensor lesson",
            "url": "https://docs.example.edu/tensor",
            "final_url": "https://docs.example.edu/tensor.txt",
            "retrieved_at": "2026-08-27T01:02:03Z",
            "media_type": "text/plain",
            "sha256": digest,
            "scope": "Tensor card",
            "cache_path": cache_path,
            "receipt_path": receipt_path,
        }
        practice["sources"] = [external]
        _save(notebook, payload)
        warnings = []
        assert validate(
            notebook,
            repo_root=root,
            check_collection=False,
            learner_state=True,
            warnings=warnings,
        ) == []
        assert _codes(warnings) == {"EXTERNAL_SOURCE_OFFLINE"}
        assert "EXTERNAL_SOURCE_OFFLINE" in _codes(
            validate(
                notebook,
                repo_root=root,
                check_collection=False,
                learner_state=True,
                strict_external_sources=True,
            )
        )

        cache_file = root / cache_path
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_bytes(body)
        receipt = {
            "status": "CACHED",
            "lesson_id": "practice-source",
            "kind": "primary",
            "original_url": external["url"],
            "final_url": external["final_url"],
            "media_type": external["media_type"],
            "retrieved_at": external["retrieved_at"],
            "sha256": digest,
            "path": cache_path,
            "receipt_path": receipt_path,
            "byte_count": len(body),
        }
        (root / receipt_path).write_text(json.dumps(receipt), encoding="utf-8")
        assert validate(
            notebook,
            repo_root=root,
            check_collection=False,
            learner_state=True,
            strict_external_sources=True,
        ) == []


def test_completion_gate_checks_targets_execution_freshness_and_errors() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        incomplete = _builder(root)
        assert "COMPLETION_INCOMPLETE" in _codes(
            validate(incomplete, repo_root=root, check_collection=False, completion_ready=True)
        )

        notebook = _completed_notebook(root)
        assert validate(
            notebook, repo_root=root, check_collection=False, completion_ready=True
        ) == []
        assert completion_commit_target(notebook, repo_root=root) == "practice/math/vector-practice.ipynb"

        payload = _load(notebook)
        payload["cells"][5]["execution_count"] = 2
        _save(notebook, payload)
        assert "COMPLETION_STALE_CHECK" in _codes(
            validate(notebook, repo_root=root, check_collection=False, completion_ready=True)
        )

        payload["cells"][5]["execution_count"] = 4
        payload["cells"][5]["outputs"] = [
            {"output_type": "error", "ename": "AssertionError", "evalue": "failed", "traceback": []}
        ]
        _save(notebook, payload)
        assert "COMPLETION_ERROR_OUTPUT" in _codes(
            validate(notebook, repo_root=root, check_collection=False, completion_ready=True)
        )


def test_completion_gate_rejects_required_blank_reflection() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        notebook = _completed_notebook(root)
        payload = _load(notebook)
        practice = payload["metadata"]["llm_research_lab"]["practice"]
        claim = "관찰한 shape의 두 축 의미를 한 문장으로 설명해야 합니다."
        marker = "관찰한 shape의 두 축 의미를 설명하세요."
        placeholder = "**작성:** 아직 작성하지 않음"
        payload["cells"][2]["source"].append(f"\n- {claim}\n")
        payload["cells"][6]["source"].extend(
            [f"\n{marker}\n", f"\n{placeholder}\n"]
        )
        practice["requirements"].append(
            {
                "id": "C-E01-04",
                "exercise_id": "E01",
                "kind": "derive",
                "claim": claim,
                "owner": "learner",
                "source_locations": [],
                "rationale": "",
                "visible_cell_id": "e01-brief",
                "target_ids": ["T-E01-02"],
            }
        )
        practice["learner_targets"].append(
            {
                "id": "T-E01-02",
                "exercise_id": "E01",
                "kind": "interpretation",
                "cell_id": "e01-reflection",
                "marker": marker,
                "placeholder": placeholder,
                "outcome_ids": ["O01"],
                "requirement_ids": ["C-E01-04"],
            }
        )
        practice["exercises"][0]["learner_target_ids"].append("T-E01-02")
        _save(notebook, payload)
        assert "COMPLETION_INCOMPLETE" in _codes(
            validate(notebook, repo_root=root, check_collection=False, completion_ready=True)
        )
