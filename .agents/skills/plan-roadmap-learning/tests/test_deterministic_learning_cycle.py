from __future__ import annotations

import json
import shutil
import subprocess
import sys
from email.message import Message
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
COACH = REPO / ".agents/skills/coach-llm-research-study"
PRACTICE = REPO / ".agents/skills/suggest-learning-practice"
for path in (
    SKILL / "scripts",
    COACH / "scripts",
    COACH / "tests",
    PRACTICE / "scripts",
    PRACTICE / "tests",
):
    sys.path.insert(0, str(path))

from cache_external_source import cache_external_source  # noqa: E402
from handoff_fixture import CONTRACT, build_handoff  # noqa: E402
from inspect_target_graph import inspect_target_graph  # noqa: E402
from daily_learning_flow import (  # noqa: E402
    begin_cycle,
    capture_completed_session,
    empty_flow,
    start_flow,
    transition_phase,
)
from route_practice import route_practice  # noqa: E402
import test_validate_practice_artifact as practice_fixture  # noqa: E402
from test_practice_v5 import (  # noqa: E402
    WORKFLOW_CONTRACT,
    _install_workflow_surface,
    _set_pass_review,
)
from validate_curriculum import curriculum_snapshot_from_text  # noqa: E402
from validate_lesson_handoff import validate_handoff  # noqa: E402
from validate_practice_artifact import validate as validate_practice  # noqa: E402
from validate_practice_notebook import _milestone_definition_hash  # noqa: E402


OFFICIAL_URL = "https://docs.example.edu/evaluation/lesson"
FINAL_URL = "https://docs.example.edu/evaluation/lesson.html"
RETRIEVED_AT = "2026-08-27T01:02:03Z"
EXTERNAL_BYTES = b"""<!doctype html><html><body>
<p>Define the evaluation question and one dataset slice.</p>
<p>Choose one metric and classify one failure.</p>
<p>Review the evaluation report only when it affects the current decision.</p>
<h2>question-and-slice</h2><p>State the comparison question before selecting data.</p>
<h2>metric-and-errors</h2><p>Connect the metric to concrete error categories.</p>
<h2>reporting</h2><p>Use the report when a model decision is needed.</p>
</body></html>"""


class _FakeResponse:
    def __init__(self, body: bytes) -> None:
        self._body = body
        self._offset = 0
        self.headers = Message()
        self.headers["Content-Type"] = "text/html; charset=utf-8"
        self.headers["Content-Length"] = str(len(body))

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = len(self._body) - self._offset
        chunk = self._body[self._offset : self._offset + size]
        self._offset += len(chunk)
        return chunk

    def geturl(self) -> str:
        return FINAL_URL

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None


class _FakeOpener:
    def __init__(self, body: bytes) -> None:
        self._response = _FakeResponse(body)

    def open(self, request, timeout: int):
        assert request.full_url == OFFICIAL_URL
        assert request.get_header("Cookie") is None
        assert timeout == 30
        return self._response


def _public_resolver(host: str, port: int, *, type: int):
    del host, port, type
    return [(2, 1, 6, "", ("93.184.216.34", 443))]


def _external_contract(cache_path: str, receipt_path: str) -> str:
    contract = CONTRACT
    replacements = {
        "Trace a tensor operation and explain its shape contract.": "Design one comparable evaluation and explain its data and metric contract.",
        "target_evidence_requirements: explain": "target_evidence_requirements: explain, implement, interpret, design, transfer",
        "target_evidence_basis: CURRICULUM.md requires an explain-back for CC-DL-01.": "target_evidence_basis: CURRICULUM.md requires explain, implement, interpret, design, and transfer evidence for CC-EVAL-01.",
        "target_evidence_gap: explain": "target_evidence_gap: explain, implement, interpret, design, transfer",
        "lesson_evidence_scope: explain": "lesson_evidence_scope: explain, interpret, design, transfer",
        "lesson_scope_basis: This reviewed session directly assesses the missing explain-back.": "lesson_scope_basis: This reviewed session assesses evaluation reasoning and transfer; implementation remains learner-owned practice.",
        "residual_target_evidence: none": "residual_target_evidence: implement",
        "residual_practice_basis: No target-level evidence is left outside this lesson; later practice may deepen implementation without backfilling session evidence.": "residual_practice_basis: A learner-owned evaluation workflow must implement the dataset, metric, and error-analysis path after the lesson.",
        "Identify the batch and feature axes.": "Define the evaluation question and one dataset slice.",
        "Predict the output shape of a broadcast operation.": "Choose one metric and classify one failure.",
        "Review the course map only when it affects the current path.": "Review the evaluation report only when it affects the current decision.",
        "#axes": "#question-and-slice",
        "#shape-propagation": "#metric-and-errors",
        "#orientation": "#reporting",
        "Axis meaning is required before shape propagation.": "The evaluation question and slice are required before interpreting a metric.",
        "The learner has not yet demonstrated this shape trace.": "The learner has not yet demonstrated this evaluation design.",
        "Identify the batch and feature axes in a small tensor.": "Define the evaluation question and one dataset slice.",
        "Connect tensor axes to batch, token, and hidden axes.": "Connect slice-level errors to a model-comparison decision.",
        "Axis meaning": "Question and slice",
        "Shape propagation": "Metric and error analysis",
        "Attention connection": "Model-comparison connection",
        "Establish axis meaning before tracing a shape-changing operation.": "Establish the question and slice before choosing a summary metric.",
        "Trace a 2 by 3 matrix by row and column.": "Compare two named model outputs on one deterministic slice.",
        "Which axis contains the three features?": "Which examples belong to the declared slice?",
        "Align dimensions from the right and explain each resulting axis.": "Compute one metric and classify the errors it hides.",
        "Broadcast a 2 by 1 tensor with a 1 by 3 tensor.": "Compare aggregate accuracy with one slice-level failure count.",
        "What is the result shape and why?": "Which error category changes the model decision and why?",
        "Reuse the same axis language for a small attention-shaped tensor.": "Reuse the same error categories for one model-comparison decision.",
        "Map batch, token, and hidden axes for one small tensor.": "Map one slice-level failure to the model-comparison claim.",
    }
    for old, new in replacements.items():
        contract = contract.replace(old, new)
    contract = contract.replace("CC-DL-01", "CC-EVAL-01").replace(
        "TR-SYS-03", "TR-EVAL-02"
    )
    contract = contract.replace(
        "- selection_mode: user-named-target", "- selection_mode: planner"
    )
    contract = contract.replace("materials/lesson.md#", f"{cache_path}#text: ")
    contract = contract.replace(
        "| CC-EVAL-01 | 충분 | 그대로 사용 | source-only | O001, O002 | The named source directly supports the selected tensor-shape target. |",
        "| CC-EVAL-01 | 부분 | 수업 내 보충 | resolved-external | O001, O002 | The reviewed official source resolves this cycle without changing durable coverage. |",
    )
    contract = contract.replace(
        "| none | none | none | none | none | none | none | none | none | none | none |",
        f"| I001 | Example University | Evaluation Systems | 2026 offering | Evaluation lesson | {OFFICIAL_URL} | {FINAL_URL} | {RETRIEVED_AT} | text/html | evaluation-data exercise | {receipt_path} |",
        1,
    )
    return contract.replace(
        "| none | none | none | none | none |",
        "| CC-EVAL-01 | I001 | primary | O001, O002 | Full source-body audit against the actual cycle target. |",
        1,
    )


def _explicit_route_states(curriculum_path: Path) -> dict[str, str]:
    snapshot = curriculum_snapshot_from_text(curriculum_path.read_text(encoding="utf-8"))
    states = {target_id: "satisfied" for target_id in snapshot.targets}
    states.update(
        {
            "CC-EVAL-01": "blocking",
            "CC-EVAL-02": "blocking",
            "CC-EVAL-03": "blocking",
            "TR-EVAL-02": "blocking",
        }
    )
    return states


def test_mocked_cycle_preserves_the_selected_frontier_across_every_artifact(
    tmp_path: Path,
) -> None:
    curriculum = tmp_path / "CURRICULUM.md"
    roadmap = tmp_path / "ROADMAP.md"
    shutil.copy2(REPO / "CURRICULUM.md", curriculum)
    roadmap.write_text(
        "# Test roadmap\n\n"
        "## 정적 목표 endpoint\n\n"
        "| 우선순위 | 단계 | 방향 | Endpoint |\n"
        "| ---: | ---: | --- | --- |\n"
        "| 2 | `2B` | Post-training·Evaluation | `TR-EVAL-02` |\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Cycle Fixture"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "cycle@example.com"], cwd=tmp_path, check=True)
    (tmp_path / ".gitignore").write_text("tmp/\ntil/today.md\npractice/\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "cycle baseline"], cwd=tmp_path, check=True)

    states = _explicit_route_states(curriculum)
    initial_graph = inspect_target_graph(
        roadmap,
        curriculum,
        target_states=states,
    )
    route = initial_graph["routes"]["TR-EVAL-02"]
    blocking_frontier = [
        candidate
        for candidate in route["frontier_candidates"]
        if candidate["state"] == "blocking"
    ]
    assert [candidate["target_id"] for candidate in blocking_frontier] == [
        "CC-EVAL-01"
    ]
    primary_target = blocking_frontier[0]["target_id"]

    receipt = cache_external_source(
        lesson_id="deterministic-evaluation-cycle",
        url=OFFICIAL_URL,
        official_hosts=["example.edu"],
        repo_root=tmp_path,
        opener=_FakeOpener(EXTERNAL_BYTES),
        resolver=_public_resolver,
        retrieved_at=RETRIEVED_AT,
    )
    assert receipt["status"] == "CACHED"
    assert (tmp_path / receipt["path"]).read_bytes() == EXTERNAL_BYTES

    learner_explanations = (
        "비교할 평가 질문과 그 질문에 맞는 dataset slice를 구분해 설명했다.",
        "선택한 metric이 숨길 수 있는 slice-level failure를 분류했다.",
        "질문과 slice, metric의 한계를 함께 사용해 어떤 모델을 선택할지 전이해 설명했다.",
    )
    state = start_flow(empty_flow(), mode="full-day")
    state = begin_cycle(
        state,
        cycle_id="cycle-deterministic-evaluation-cycle",
        primary_target=primary_target,
    )
    state = transition_phase(state, "PREPARE_LESSON")
    state = transition_phase(state, "TEACH")
    contract = _external_contract(receipt["path"], receipt["receipt_path"])
    repair_handoff, _ = build_handoff(
        tmp_path,
        contract=contract,
        status="repair_pending",
        reviews=[("repair_required", "deterministic-slice-reviewer")],
        lesson_id="deterministic-evaluation-cycle",
        primary_role="external-primary",
        primary_path=receipt["path"],
        primary_bytes=EXTERNAL_BYTES,
    )
    repair_report = validate_handoff(
        repair_handoff,
        repo_root=tmp_path,
        check_draft=False,
    )
    assert repair_report.ok, repair_report.errors
    assert repair_report.as_json()["workflow_action"] == "REPAIR_CONTRACT"

    reviewed_handoff, _ = build_handoff(
        tmp_path,
        contract=contract,
        status="active",
        reviews=[
            ("repair_required", "deterministic-slice-reviewer"),
            ("pass", "deterministic-slice-reviewer"),
        ],
        lesson_id="deterministic-evaluation-cycle",
        primary_role="external-primary",
        primary_path=receipt["path"],
        primary_bytes=EXTERNAL_BYTES,
    )
    reviewed_report = validate_handoff(
        reviewed_handoff,
        repo_root=tmp_path,
        ready=True,
        check_draft=False,
    )
    assert reviewed_report.ok, reviewed_report.errors
    assert reviewed_report.as_json()["workflow_action"] == "TEACH_OR_RESUME"

    handoff, _ = build_handoff(
        tmp_path,
        contract=contract,
        status="completed",
        reviews=[
            ("repair_required", "deterministic-slice-reviewer"),
            ("pass", "deterministic-slice-reviewer"),
        ],
        evidence=[
            {
                "concept_ids": "C01",
                "objective_ids": "O001",
                "content": learner_explanations[0],
                "capture_state": "captured",
            },
            {
                "concept_ids": "C02",
                "objective_ids": "O002",
                "content": learner_explanations[1],
                "capture_state": "captured",
            },
            {
                "concept_ids": "C01, C02, C03",
                "objective_ids": "O001, O002, O003",
                "kind": "transfer",
                "content": learner_explanations[2],
                "capture_state": "captured",
            },
        ],
        lesson_id="deterministic-evaluation-cycle",
        primary_role="external-primary",
        primary_path=receipt["path"],
        primary_bytes=EXTERNAL_BYTES,
        coverage=[
            {
                "concept": "C01",
                "state": "confirmed",
                "evidence_ids": "E001",
                "representation": "learning",
                "note": "Learner explanation is drafted.",
            },
            {
                "concept": "C02",
                "state": "confirmed",
                "evidence_ids": "E002",
                "representation": "learning",
                "note": "Learner prediction is drafted.",
            },
            {
                "concept": "C03",
                "state": "confirmed",
                "evidence_ids": "E003",
                "representation": "learning",
                "note": "The integrated transfer demonstrates the model-comparison connection.",
            },
        ],
        delivery=[
            {
                "objective": "O001",
                "state": "delivered",
                "mode": "full",
                "note": "The first evaluated objective was delivered.",
            },
            {
                "objective": "O002",
                "state": "delivered",
                "mode": "full",
                "note": "The second evaluated objective was delivered.",
            },
            {
                "objective": "O003",
                "state": "delivered",
                "mode": "full",
                "note": "The final transfer connection was delivered.",
            },
        ],
    )
    completed = validate_handoff(handoff, repo_root=tmp_path)
    assert completed.ok, completed.errors
    assert completed.document is not None
    assert completed.document.target_decision.primary_target == primary_target
    assert completed.document.target_decision.endpoint == "TR-EVAL-02"
    capture_ready = validate_handoff(
        handoff,
        repo_root=tmp_path,
        capture_ready=True,
    )
    assert capture_ready.ok, capture_ready.errors
    state = capture_completed_session(state, handoff, repo_root=tmp_path)
    assert state["phase"] == "DECIDE_PRACTICE"
    cycle = state["cycles"][0]
    assert len(cycle["learner_evidence_sha256"]) == 64
    assert len(state["learner_evidence_sha256"]) == 64

    practice_decision = route_practice(
        "evaluation-data",
        learning_input_kind="lesson-session",
        learning_input_ready=True,
        module_assignment_id="MA-EVALUATION-01",
        module_assignment_ready=True,
        module_assignment_depth="I4_EXPERIMENT",
        repo_root=tmp_path,
    )
    assert (
        practice_decision.practice_action,
        practice_decision.practice_mode,
    ) == ("CREATE_LOCAL_PRACTICE", "DATASET_PROJECT")

    notebook = practice_fixture.PracticeArtifactValidatorTests().build_notebook(tmp_path)
    payload = json.loads(notebook.read_text(encoding="utf-8"))
    metadata = payload["metadata"]["llm_research_lab"]["practice"]
    _install_workflow_surface(payload)
    captured_session = cycle["captured_session"]
    cursor_path = tmp_path / "tmp/active-learning-flow.json"
    cursor_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    confirmed_concepts = [
        item["concept_id"] for item in captured_session["concepts"]
    ]
    evidence_ids = [
        item["evidence_id"] for item in captured_session["learner_evidence"]
    ]
    metadata.update(
        {
            "schema_version": 5,
            "practice_mode": practice_decision.practice_mode,
            "practice_layer": practice_decision.practice_layer,
            "implementation_depth": practice_decision.implementation_depth,
            "lifecycle": "fresh",
            "milestone_id": practice_decision.milestone_id,
            "milestone_definition_sha256": _milestone_definition_hash(
                tmp_path,
                practice_decision.milestone_id,
            ),
            "learning_inputs": [
                {
                    "id": "L001",
                    "role": "primary",
                    "kind": "captured-cycle",
                    "cycle_id": captured_session["cycle_id"],
                    "lesson_id": captured_session["lesson_id"],
                    "primary_target": captured_session["primary_target"],
                    "bridge_target": captured_session["bridge_target"],
                    "concept_ids": confirmed_concepts,
                    "evidence_ids": evidence_ids,
                    "captured_session_sha256": captured_session[
                        "projection_sha256"
                    ],
                }
            ],
            "prior_practice_evidence": [],
            "creation_reviews": [],
            "result_cell_ids": ["e04-fixture", "e05-fixture"],
            "workflow_contract": {
                **WORKFLOW_CONTRACT,
                "stage_cell_ids": {
                    "data": [
                        "e01-implementation",
                        "e01-fixture",
                        "e01-check",
                    ],
                    "model": ["e02-implementation", "e02-fixture"],
                    "loss": ["e03-implementation", "e03-fixture"],
                    "train": ["e04-implementation", "e04-fixture"],
                    "evaluation": [
                        "e05-implementation",
                        "e05-fixture",
                        "e05-check",
                    ],
                },
            },
        }
    )
    metadata.pop("til")
    for outcome in metadata["outcomes"]:
        outcome.pop("til_location")
        outcome["concept_ids"] = [f"L001:{item}" for item in confirmed_concepts]
        outcome["evidence_ids"] = [f"L001:{item}" for item in evidence_ids]
    metadata["curriculum_targets"] = [primary_target]
    for outcome in metadata["outcomes"]:
        outcome["curriculum_target_ids"] = [primary_target]
    metadata["sources"] = [
        {
            "id": "S001",
            "kind": "external-reference",
            "provider": "Example University",
            "course": "Evaluation Systems",
            "offering_or_edition": "2026 offering",
            "artifact": "Evaluation lesson",
            "url": OFFICIAL_URL,
            "final_url": FINAL_URL,
            "retrieved_at": RETRIEVED_AT,
            "media_type": "text/html",
            "sha256": receipt["sha256"],
            "scope": "evaluation-data exercise",
            "cache_path": receipt["path"],
            "receipt_path": receipt["receipt_path"],
        }
    ]
    source_claim = (
        "Define the evaluation question and one dataset slice before "
        "interpreting the held-out result."
    )
    source_requirement = next(
        requirement
        for requirement in metadata["requirements"]
        if requirement["id"] == "C-E05-02"
    )
    source_requirement["kind"] = "source-given"
    source_requirement["claim"] = source_claim
    source_requirement["source_locations"] = [
        {
            "source_id": "S001",
            "locator": "text: Define the evaluation question and one dataset slice.",
            "anchor": "Define the evaluation question and one dataset slice.",
        }
    ]
    evaluation_brief = next(
        cell for cell in payload["cells"] if cell.get("id") == "e05-brief"
    )
    evaluation_brief["source"] = "".join(evaluation_brief["source"]).replace(
        "<details><summary>힌트 1</summary>",
        f"- {source_claim}\n\n<details><summary>힌트 1</summary>",
        1,
    ).splitlines(keepends=True)
    _set_pass_review(payload, reviewer="cycle-practice-reviewer")
    notebook.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    assert (
        metadata["practice_layer"],
        metadata["implementation_depth"],
        metadata["milestone_id"],
    ) == ("MODULE_ASSIGNMENT", "I4_EXPERIMENT", "MA-EVALUATION-01")
    assert validate_practice(
        notebook,
        repo_root=tmp_path,
        check_collection=False,
        strict_external_sources=True,
    ) == []

    updated_states = dict(states)
    updated_states[primary_target] = "satisfied"
    next_graph = inspect_target_graph(
        roadmap,
        curriculum,
        target_states=updated_states,
    )
    next_blocking = [
        candidate["target_id"]
        for candidate in next_graph["routes"]["TR-EVAL-02"][
            "frontier_candidates"
        ]
        if candidate["state"] == "blocking"
    ]
    assert next_blocking[0] == "CC-EVAL-02"
    assert next_blocking[0] != primary_target
