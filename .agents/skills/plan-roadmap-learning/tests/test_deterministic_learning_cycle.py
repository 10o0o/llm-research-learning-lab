from __future__ import annotations

import json
import shutil
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
from handoff_fixture import CONTRACT, build_handoff, draft_envelope, sha256  # noqa: E402
from inspect_target_graph import inspect_target_graph  # noqa: E402
from route_practice import route_practice  # noqa: E402
import test_validate_practice_artifact as practice_fixture  # noqa: E402
from validate_curriculum import curriculum_snapshot_from_text  # noqa: E402
from validate_lesson_handoff import validate_handoff  # noqa: E402
from validate_practice_artifact import validate as validate_practice  # noqa: E402


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
    )
    draft = tmp_path / "til/today.md"
    draft.parent.mkdir(parents=True)
    draft.write_text(
        "# 오늘의 학습\n\n"
        + draft_envelope(
            "deterministic-evaluation-cycle", "E001", learner_explanations[0]
        )
        + "\n"
        + draft_envelope(
            "deterministic-evaluation-cycle", "E002", learner_explanations[1]
        )
        + "\n## 관련 기록\n\n"
        + f"- [공식 자료]({OFFICIAL_URL})\n"
        + "- offering/edition: 2026 offering\n"
        + "- scope: evaluation-data exercise\n"
        + f"- 관련 역량: `{primary_target}`\n",
        encoding="utf-8",
    )
    contract = _external_contract(receipt["path"], receipt["receipt_path"])
    handoff, _ = build_handoff(
        tmp_path,
        contract=contract,
        status="paused",
        reviews=[("pass", "fresh-deterministic-reviewer")],
        evidence=[
            {
                "concept": "C01",
                "objective_ids": "O001",
                "content": learner_explanations[0],
                "append_state": "drafted",
            },
            {
                "concept": "C02",
                "objective_ids": "O002",
                "content": learner_explanations[1],
                "append_state": "drafted",
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
                "state": "deferred",
                "evidence_ids": "none",
                "representation": "not-required",
                "note": "Optional connection was not taught.",
            },
        ],
        pre_save_verdict="저장 가능",
        reviewed_at="2026-08-27T02:00:00Z",
        reviewed_draft_sha256=sha256(draft.read_bytes()),
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
                "state": "pending",
                "mode": "none",
                "note": "Optional connection was not taught.",
            },
        ],
    )
    ready = validate_handoff(handoff, repo_root=tmp_path, ready=True)
    assert ready.ok, ready.errors
    assert ready.document is not None
    assert ready.document.target_decision.primary_target == primary_target
    assert ready.document.target_decision.endpoint == "TR-EVAL-02"
    til_ready = validate_handoff(handoff, repo_root=tmp_path, til_ready=True)
    assert til_ready.ok, til_ready.errors

    practice_decision = route_practice("evaluation-data")
    assert (
        practice_decision.practice_action,
        practice_decision.practice_mode,
    ) == ("CREATE_LOCAL_PRACTICE", "DATASET_PROJECT")

    notebook = practice_fixture.PracticeArtifactValidatorTests().build_notebook(tmp_path)
    payload = json.loads(notebook.read_text(encoding="utf-8"))
    metadata = payload["metadata"]["llm_research_lab"]["practice"]
    metadata["practice_mode"] = practice_decision.practice_mode
    metadata["curriculum_targets"] = [primary_target]
    metadata["outcomes"][0]["curriculum_target_ids"] = [primary_target]
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
    source_location = metadata["requirements"][0]["source_locations"][0]
    source_location["locator"] = (
        "text: Define the evaluation question and one dataset slice."
    )
    source_location["anchor"] = (
        "Define the evaluation question and one dataset slice."
    )
    notebook.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
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
