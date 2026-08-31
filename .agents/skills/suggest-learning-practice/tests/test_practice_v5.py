from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest


SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from migrate_practice_v4_to_v5 import migrate_file, migrate_payload  # noqa: E402
from record_practice_creation_review import record_review  # noqa: E402
from route_practice import route_practice  # noqa: E402
from test_validate_practice_artifact import (  # noqa: E402
    PracticeArtifactValidatorTests,
    code_cell,
    markdown_cell,
)
from validate_practice_artifact import validate  # noqa: E402
from validate_practice_notebook import (  # noqa: E402
    _canonical_hash,
    _milestone_definition_hash,
    collect_observables,
    captured_session_projection_hash,
    practice_contract_hash,
)


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _practice(payload: dict[str, object]) -> dict[str, object]:
    return payload["metadata"]["llm_research_lab"]["practice"]


def _codes(items) -> set[str]:
    return {item.code for item in items}


def _replace_once(text: str, before: str, after: str) -> str:
    return text.replace(before, after, 1)


def _write_curriculum(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "CURRICULUM.md").write_text(
        """# Curriculum

| Target ID | 설명 |
| --- | --- |
| CC-DL-01 | Tensor 계약 |

| Milestone ID | Practice layer | Module IDs | 구현 깊이 | 선수 Milestone ID | Endpoint closure | 요구 산출물 |
| --- | --- | --- | --- | --- | --- | --- |
| MA-TEST-01 | MODULE_ASSIGNMENT | MOD-TEST-01 | I3_WORKFLOW | — | — | data to model to loss to train and evaluation |
| PC-TEST-01 | PHASE_CAPSTONE | MOD-TEST-01 | I5_RESEARCH | MA-TEST-01 | — | baseline ablation error analysis reproducibility limitations |
""",
        encoding="utf-8",
    )


def _set_pass_review(payload: dict[str, object], reviewer: str = "reviewer-v5") -> None:
    practice = _practice(payload)
    practice["creation_reviews"] = []
    practice["creation_reviews"] = [
        {
            "iteration": 1,
            "reviewer_id": reviewer,
            "reviewed_at": "2026-08-31T12:00:00+09:00",
            "learner_surface_verdict": "pass",
            "metadata_verdict": "pass",
            "verdict": "pass",
            "contract_sha256": practice_contract_hash(payload),
            "recheck_of": None,
        }
    ]


def _brief_text(payload: dict[str, object]) -> str:
    return "".join(payload["cells"][2]["source"])


def _set_brief_text(payload: dict[str, object], text: str) -> None:
    payload["cells"][2]["source"] = text.splitlines(keepends=True)


def _append_brief_claims(payload: dict[str, object], claims: list[str]) -> None:
    brief = _brief_text(payload)
    marker = "\n<details><summary>힌트 1</summary>\n"
    insertion = "".join(f"\n- {claim}\n" for claim in claims)
    if marker in brief:
        brief = brief.replace(marker, insertion + marker, 1)
    else:
        brief += insertion
    _set_brief_text(payload, brief)


def _next_requirement_id(practice: dict[str, object]) -> str:
    return f"C-E01-{len(practice['requirements']) + 1:02d}"


def _next_target_id(practice: dict[str, object]) -> str:
    return f"T-E01-{len(practice['learner_targets']) + 1:02d}"


def _add_requirement(
    practice: dict[str, object],
    *,
    claim: str,
    owner: str,
    target_ids: list[str],
    kind: str = "derive",
    rationale: str = "",
) -> str:
    requirement_id = _next_requirement_id(practice)
    requirement = {
        "id": requirement_id,
        "exercise_id": "E01",
        "kind": kind,
        "claim": claim,
        "owner": owner,
        "source_locations": [],
        "rationale": rationale,
        "visible_cell_id": "e01-brief",
        "target_ids": target_ids,
    }
    if kind == "practice-given" and owner == "learner":
        requirement["learner_outcome_ids"] = ["O03"]
    practice["requirements"].append(requirement)
    return requirement_id


def _append_reflection_prompt(
    payload: dict[str, object],
    *,
    marker: str,
    placeholder: str,
) -> None:
    payload["cells"][6]["source"].extend(
        [
            f"\n{marker}\n",
            f"\n{placeholder}\n",
        ]
    )


def _add_reflection_target(
    payload: dict[str, object],
    *,
    marker: str,
    claim: str,
    outcome_ids: list[str],
    result_cell_ids: list[str],
    kind: str,
) -> str:
    practice = _practice(payload)
    target_id = _next_target_id(practice)
    placeholder = "**작성:** 아직 작성하지 않음"
    _append_brief_claims(payload, [claim])
    requirement_id = _add_requirement(
        practice,
        claim=claim,
        owner="learner",
        target_ids=[target_id],
    )
    practice["learner_targets"].append(
        {
            "id": target_id,
            "exercise_id": "E01",
            "kind": kind,
            "cell_id": "e01-reflection",
            "marker": marker,
            "placeholder": placeholder,
            "outcome_ids": outcome_ids,
            "requirement_ids": [requirement_id],
            "result_cell_ids": result_cell_ids,
        }
    )
    practice["exercises"][0]["learner_target_ids"].append(target_id)
    _append_reflection_prompt(payload, marker=marker, placeholder=placeholder)
    return target_id


def _v4_finalized_til(root: Path) -> Path:
    notebook = PracticeArtifactValidatorTests().build_notebook(root)
    payload = _load(notebook)
    practice = _practice(payload)
    practice["schema_version"] = 4
    til = practice.pop("til")
    practice["learning_input"] = {"kind": "finalized-til", **til}
    _save(notebook, payload)
    return notebook


def _v5_prelab(root: Path, *, lifecycle: str = "fresh") -> Path:
    _write_curriculum(root)
    notebook = _v4_finalized_til(root)
    payload = _load(notebook)
    practice = _practice(payload)
    old_input = practice.pop("learning_input")
    practice.update(
        {
            "schema_version": 5,
            "practice_layer": "PRE_LAB",
            "implementation_depth": "I1_MECHANISM",
            "lifecycle": lifecycle,
            "milestone_id": None,
            "milestone_definition_sha256": None,
            "learning_inputs": [
                {"id": "L001", "role": "primary", **old_input}
            ],
            "prior_practice_evidence": [],
            "creation_reviews": [],
            "result_cell_ids": [],
        }
    )
    if lifecycle == "fresh":
        _set_pass_review(payload)
    _save(notebook, payload)
    return notebook


def _add_required_interpretation(payload: dict[str, object]) -> None:
    claim = "관찰한 결과와 모델 평가의 한계를 한 문장으로 해석해야 합니다."
    marker = "관찰한 결과와 한계를 해석하세요."
    _add_reflection_target(
        payload,
        marker=marker,
        claim=claim,
        outcome_ids=["O03"],
        result_cell_ids=["e01-fixture"],
        kind="interpretation",
    )


WORKFLOW_CONTRACT = {
    "data_contract": "Partition the fixed four-row linear dataset into three training rows and one evaluation row.",
    "component_contract": "Implement a reusable LinearRegressor that computes x * weight + bias.",
    "loss_contract": "Compute mean squared error from prediction and target arrays.",
    "training_contract": "Apply one explicit gradient-descent weight update and report loss before and after it.",
    "evaluation_contract": "Evaluate the held-out split with count and mean squared error under the same contract.",
}


def _exercise_bundle(
    *,
    exercise_id: str,
    title: str,
    claims: list[str],
    implementation: str,
    fixture: str,
    check: str,
    marker: str,
    placeholder: str,
    symbol: str,
    primary_outcome_id: str,
    supporting_outcome_ids: list[str],
    code_outcome_ids: list[str],
    reflection_kind: str | None = None,
    reflection_marker: str | None = None,
    reflection_claims: list[str] | None = None,
    reflection_outcome_ids: list[str] | None = None,
    reflection_result_cell_ids: list[str] | None = None,
) -> tuple[
    list[dict[str, object]],
    dict[str, object],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    number = int(exercise_id[1:])
    claim_lines = "".join(f"- {claim}\n" for claim in claims)
    brief = f"""## 실습 {number}. {title}

이 단계는 앞 단계의 실제 값을 받아 다음 단계가 사용할 공개 계약을 만듭니다.

### 요구사항

{claim_lines}
<details><summary>힌트 1</summary>

함수의 입력과 반환값을 작은 배열 하나로 먼저 추적하세요.

</details>

<details><summary>힌트 2</summary>

제공된 조립 코드는 유지하고 TODO 한 문장만 완성하세요.

</details>
"""
    code_requirement_id = f"C-{exercise_id}-01"
    code_target_id = f"T-{exercise_id}-01"
    observed, error = collect_observables(check)
    assert error is None
    observables = [
        {
            "ordinal": observable.ordinal,
            "kind": observable.kind,
            "fingerprint": observable.fingerprint,
            "category": "normal",
            "requirement_ids": [code_requirement_id],
        }
        for observable in observed
    ]
    requirements: list[dict[str, object]] = [
        {
            "id": code_requirement_id,
            "exercise_id": exercise_id,
            "kind": "derive",
            "claim": claims[0],
            "owner": "learner",
            "source_locations": [],
            "rationale": "",
            "visible_cell_id": f"e{number:02d}-brief",
            "target_ids": [code_target_id],
        }
    ]
    targets: list[dict[str, object]] = [
        {
            "id": code_target_id,
            "exercise_id": exercise_id,
            "kind": "code",
            "cell_id": f"e{number:02d}-implementation",
            "marker": marker,
            "placeholder": placeholder,
            "symbol": symbol,
            "outcome_ids": code_outcome_ids,
            "requirement_ids": [code_requirement_id],
        }
    ]
    reflection = (
        "### 확인 결과 정리\n\n"
        "선택 메모입니다. 이 메모는 실습 완료 조건이 아닙니다.\n"
    )
    learner_target_ids = [code_target_id]
    if reflection_kind is not None:
        assert reflection_marker is not None
        assert reflection_claims
        assert reflection_outcome_ids
        assert reflection_result_cell_ids
        reflection_target_id = f"T-{exercise_id}-02"
        learner_target_ids.append(reflection_target_id)
        reflection = (
            "### 관찰 결과 해석\n\n"
            + "\n".join(reflection_claims)
            + f"\n\n{reflection_marker}\n\n**작성:** 아직 작성하지 않음\n"
        )
        reflection_requirement_ids: list[str] = []
        for index, claim in enumerate(reflection_claims, start=2):
            requirement_id = f"C-{exercise_id}-{index:02d}"
            reflection_requirement_ids.append(requirement_id)
            requirements.append(
                {
                    "id": requirement_id,
                    "exercise_id": exercise_id,
                    "kind": "derive",
                    "claim": claim,
                    "owner": "learner",
                    "source_locations": [],
                    "rationale": "",
                    "visible_cell_id": f"e{number:02d}-brief",
                    "target_ids": [reflection_target_id],
                }
            )
        targets.append(
            {
                "id": reflection_target_id,
                "exercise_id": exercise_id,
                "kind": reflection_kind,
                "cell_id": f"e{number:02d}-reflection",
                "marker": reflection_marker,
                "placeholder": "**작성:** 아직 작성하지 않음",
                "outcome_ids": reflection_outcome_ids,
                "requirement_ids": reflection_requirement_ids,
                "result_cell_ids": reflection_result_cell_ids,
            }
        )
    cells = [
        markdown_cell(f"e{number:02d}-brief", "brief", brief, exercise_id),
        code_cell(
            f"e{number:02d}-implementation",
            "implementation",
            implementation,
            exercise_id,
        ),
        code_cell(f"e{number:02d}-fixture", "fixture", fixture, exercise_id),
        code_cell(
            f"e{number:02d}-check",
            "check",
            check,
            exercise_id,
            observables=observables,
        ),
        markdown_cell(
            f"e{number:02d}-reflection",
            "reflection",
            reflection,
            exercise_id,
        ),
    ]
    exercise = {
        "id": exercise_id,
        "primary_outcome_id": primary_outcome_id,
        "supporting_outcome_ids": supporting_outcome_ids,
        "scaffold_stage": "guided",
        "learner_target_ids": learner_target_ids,
    }
    return cells, exercise, requirements, targets


def _install_workflow_surface(payload: dict[str, object]) -> None:
    practice = _practice(payload)
    bundles = [
        _exercise_bundle(
            exercise_id="E01",
            title="고정 데이터를 학습과 평가로 나누기",
            claims=[WORKFLOW_CONTRACT["data_contract"]],
            implementation='''def make_splits() -> dict[str, np.ndarray]:
    all_x = np.array([[0.0], [1.0], [2.0], [3.0]])
    all_y = np.array([[1.0], [3.0], [5.0], [7.0]])
    split_at = 3

    # TODO: 앞의 세 행과 마지막 한 행을 나누세요
    split_values = NotImplemented

    x_train, y_train, x_eval, y_eval = split_values
    return {
        "x_train": x_train,
        "y_train": y_train,
        "x_eval": x_eval,
        "y_eval": y_eval,
    }
''',
            fixture='''splits = make_splits()
print("train/eval:", splits["x_train"].shape, splits["x_eval"].shape)
''',
            check='''def check_e01() -> None:
    splits = make_splits()
    np.testing.assert_equal(splits["x_train"].shape, (3, 1))
    np.testing.assert_allclose(splits["y_eval"], np.array([[7.0]]))


check_e01()
''',
            marker="# TODO: 앞의 세 행과 마지막 한 행을 나누세요",
            placeholder="split_values = NotImplemented",
            symbol="make_splits",
            primary_outcome_id="O01",
            supporting_outcome_ids=["O02"],
            code_outcome_ids=["O01"],
        ),
        _exercise_bundle(
            exercise_id="E02",
            title="재사용 가능한 선형 모델 구현하기",
            claims=[WORKFLOW_CONTRACT["component_contract"]],
            implementation='''class LinearRegressor:
    def __init__(self, weight: float, bias: float) -> None:
        self.weight = float(weight)
        self.bias = float(bias)

    def __call__(self, x: np.ndarray) -> np.ndarray:
        # TODO: 선형 예측식을 완성하세요
        prediction = NotImplemented

        return np.asarray(prediction, dtype=float)
''',
            fixture='''demo_model = LinearRegressor(weight=2.0, bias=1.0)
print("prediction:", demo_model(np.array([[0.0], [1.0]])).ravel())
''',
            check='''def check_e02() -> None:
    model = LinearRegressor(weight=2.0, bias=1.0)
    np.testing.assert_allclose(
        model(np.array([[0.0], [1.0]])),
        np.array([[1.0], [3.0]]),
    )


check_e02()
''',
            marker="# TODO: 선형 예측식을 완성하세요",
            placeholder="prediction = NotImplemented",
            symbol="LinearRegressor.__call__",
            primary_outcome_id="O01",
            supporting_outcome_ids=["O02"],
            code_outcome_ids=["O01"],
        ),
        _exercise_bundle(
            exercise_id="E03",
            title="평균제곱오차 계산하기",
            claims=[WORKFLOW_CONTRACT["loss_contract"]],
            implementation='''def mse_loss(prediction: np.ndarray, target: np.ndarray) -> float:
    # TODO: 원소별 오차의 제곱을 평균내세요
    loss = NotImplemented

    return float(loss)
''',
            fixture='''demo_loss = mse_loss(np.array([[1.0], [3.0]]), np.array([[0.0], [4.0]]))
print("mse:", demo_loss)
''',
            check='''def check_e03() -> None:
    observed = mse_loss(
        np.array([[1.0], [3.0]]),
        np.array([[0.0], [4.0]]),
    )
    np.testing.assert_allclose(observed, 1.0)


check_e03()
''',
            marker="# TODO: 원소별 오차의 제곱을 평균내세요",
            placeholder="loss = NotImplemented",
            symbol="mse_loss",
            primary_outcome_id="O01",
            supporting_outcome_ids=["O02"],
            code_outcome_ids=["O01"],
        ),
        _exercise_bundle(
            exercise_id="E04",
            title="한 번의 학습 업데이트 실행하기",
            claims=[WORKFLOW_CONTRACT["training_contract"]],
            implementation='''def train_step(
    model: LinearRegressor,
    x: np.ndarray,
    target: np.ndarray,
    learning_rate: float,
) -> dict[str, float]:
    prediction = model(x)
    before = mse_loss(prediction, target)
    gradient = float(np.mean(2.0 * (prediction - target) * x))

    # TODO: 계산한 gradient로 weight를 한 번 갱신하세요
    model.weight = NotImplemented

    after = mse_loss(model(x), target)
    return {"before": before, "after": after, "weight": model.weight}
''',
            fixture='''training_splits = make_splits()
training_model = LinearRegressor(weight=0.0, bias=0.0)
training_result = train_step(
    training_model,
    training_splits["x_train"],
    training_splits["y_train"],
    learning_rate=0.1,
)
print("train loss:", training_result["before"], "->", training_result["after"])
''',
            check='''def check_e04() -> None:
    splits = make_splits()
    model = LinearRegressor(weight=0.0, bias=0.0)
    result = train_step(model, splits["x_train"], splits["y_train"], 0.1)
    np.testing.assert_allclose(result["weight"], 13.0 / 15.0)
    np.testing.assert_equal(result["after"] < result["before"], True)


check_e04()
''',
            marker="# TODO: 계산한 gradient로 weight를 한 번 갱신하세요",
            placeholder="model.weight = NotImplemented",
            symbol="train_step",
            primary_outcome_id="O01",
            supporting_outcome_ids=["O02"],
            code_outcome_ids=["O01"],
        ),
        _exercise_bundle(
            exercise_id="E05",
            title="보지 않은 한 행을 평가하고 해석하기",
            claims=[
                WORKFLOW_CONTRACT["evaluation_contract"],
                "Interpret the distinct training and held-out evaluation results without treating one tiny split as generalization proof.",
            ],
            implementation='''def evaluate(
    model: LinearRegressor,
    x: np.ndarray,
    target: np.ndarray,
) -> dict[str, float | int]:
    prediction = model(x)
    loss = mse_loss(prediction, target)

    # TODO: 평가 행 수와 loss를 결과로 조립하세요
    result = NotImplemented

    return result
''',
            fixture='''evaluation_splits = make_splits()
evaluation_model = LinearRegressor(weight=0.0, bias=1.0)
evaluation_result = evaluate(
    evaluation_model,
    evaluation_splits["x_eval"],
    evaluation_splits["y_eval"],
)
print("held-out:", evaluation_result)
''',
            check='''def check_e05() -> None:
    splits = make_splits()
    model = LinearRegressor(weight=0.0, bias=1.0)
    result = evaluate(model, splits["x_eval"], splits["y_eval"])
    np.testing.assert_equal(result["count"], 1)
    np.testing.assert_allclose(result["loss"], 36.0)


check_e05()
''',
            marker="# TODO: 평가 행 수와 loss를 결과로 조립하세요",
            placeholder="result = NotImplemented",
            symbol="evaluate",
            primary_outcome_id="O01",
            supporting_outcome_ids=["O02", "O03"],
            code_outcome_ids=["O01"],
            reflection_kind="interpretation",
            reflection_marker="학습 결과와 평가 결과가 각각 무엇을 말하는지 해석하세요.",
            reflection_claims=[
                "Interpret the distinct training and held-out evaluation results without treating one tiny split as generalization proof."
            ],
            reflection_outcome_ids=["O03"],
            reflection_result_cell_ids=["e04-fixture", "e05-fixture"],
        ),
    ]
    payload["cells"] = payload["cells"][:2]
    practice["exercises"] = []
    practice["requirements"] = []
    practice["learner_targets"] = []
    for cells, exercise, requirements, targets in bundles:
        payload["cells"].extend(cells)
        practice["exercises"].append(exercise)
        practice["requirements"].extend(requirements)
        practice["learner_targets"].extend(targets)
    practice["outcomes"] = [
        {
            "id": "O01",
            "til_location": "오늘의 학습 > 작은 회귀 workflow",
            "action": "implement",
            "exercise_ids": ["E01", "E02", "E03", "E04", "E05"],
            "required_evidence": "distinct data model loss train evaluation implementation",
            "curriculum_target_ids": ["CC-DL-01"],
        },
        {
            "id": "O02",
            "til_location": "오늘의 학습 > 작은 회귀 workflow",
            "action": "test",
            "exercise_ids": ["E01", "E02", "E03", "E04", "E05"],
            "required_evidence": "deterministic stage checks",
            "curriculum_target_ids": ["CC-DL-01"],
        },
        {
            "id": "O03",
            "til_location": "오늘의 학습 > 작은 회귀 workflow",
            "action": "interpret",
            "exercise_ids": ["E05"],
            "required_evidence": "training and evaluation result interpretation",
            "curriculum_target_ids": ["CC-DL-01"],
        },
    ]


RESEARCH_CONTRACT = {
    "hypothesis": "A single fixed-budget gradient step should lower held-out loss relative to the zero-update baseline.",
    "baseline": "Record held-out count and loss for the zero-update model as the baseline result.",
    "control_or_ablation": "Run exactly one update with the same split, initialization, and evaluation function as the controlled comparison.",
    "error_analysis": "Classify which condition has the larger held-out absolute error from the observed comparison.",
    "reproducibility": "Keep the arrays, initialization, learning rate, update count, and execution order fixed.",
    "limitations": "Explain that one noiseless linear holdout cannot establish behavior on noisy or nonlinear data.",
}


def _append_capstone_surface(payload: dict[str, object]) -> None:
    practice = _practice(payload)
    bundles = [
        _exercise_bundle(
            exercise_id="E06",
            title="업데이트 없는 baseline 기록하기",
            claims=[
                "Return the zero-update held-out metrics with the label baseline.",
                RESEARCH_CONTRACT["hypothesis"],
                RESEARCH_CONTRACT["baseline"],
            ],
            implementation='''def baseline_result(splits: dict[str, np.ndarray]) -> dict[str, object]:
    model = LinearRegressor(weight=0.0, bias=0.0)

    # TODO: 업데이트 없는 평가 결과를 계산하세요
    baseline = NotImplemented

    return {"label": "baseline", "metrics": baseline}
''',
            fixture='''capstone_splits = make_splits()
observed_baseline = baseline_result(capstone_splits)
print("baseline:", observed_baseline)
''',
            check='''def check_e06() -> None:
    result = baseline_result(make_splits())
    np.testing.assert_equal(result["label"], "baseline")
    np.testing.assert_allclose(result["metrics"]["loss"], 49.0)


check_e06()
''',
            marker="# TODO: 업데이트 없는 평가 결과를 계산하세요",
            placeholder="baseline = NotImplemented",
            symbol="baseline_result",
            primary_outcome_id="O05",
            supporting_outcome_ids=["O01"],
            code_outcome_ids=["O01"],
            reflection_kind="design",
            reflection_marker="baseline이 가설을 검증하는 기준이 되는 이유를 작성하세요.",
            reflection_claims=[
                RESEARCH_CONTRACT["hypothesis"],
                RESEARCH_CONTRACT["baseline"],
            ],
            reflection_outcome_ids=["O05"],
            reflection_result_cell_ids=["e06-fixture"],
        ),
        _exercise_bundle(
            exercise_id="E07",
            title="동일 조건의 one-step 비교 실행하기",
            claims=[
                "Return the one-step held-out metrics with the label one-step.",
                RESEARCH_CONTRACT["control_or_ablation"],
                RESEARCH_CONTRACT["reproducibility"],
            ],
            implementation='''def one_step_result(splits: dict[str, np.ndarray]) -> dict[str, object]:
    model = LinearRegressor(weight=0.0, bias=0.0)
    train_step(model, splits["x_train"], splits["y_train"], 0.1)

    # TODO: 같은 평가 함수로 one-step 결과를 계산하세요
    comparison = NotImplemented

    return {"label": "one-step", "metrics": comparison}
''',
            fixture='''observed_one_step = one_step_result(make_splits())
print("one-step:", observed_one_step)
''',
            check='''def check_e07() -> None:
    baseline = baseline_result(make_splits())
    comparison = one_step_result(make_splits())
    np.testing.assert_equal(comparison["label"], "one-step")
    np.testing.assert_equal(
        comparison["metrics"]["loss"] < baseline["metrics"]["loss"],
        True,
    )


check_e07()
''',
            marker="# TODO: 같은 평가 함수로 one-step 결과를 계산하세요",
            placeholder="comparison = NotImplemented",
            symbol="one_step_result",
            primary_outcome_id="O05",
            supporting_outcome_ids=["O01"],
            code_outcome_ids=["O01"],
            reflection_kind="design",
            reflection_marker="비교에서 고정한 조건이 무엇인지 작성하세요.",
            reflection_claims=[
                RESEARCH_CONTRACT["control_or_ablation"],
                RESEARCH_CONTRACT["reproducibility"],
            ],
            reflection_outcome_ids=["O05"],
            reflection_result_cell_ids=["e07-fixture"],
        ),
        _exercise_bundle(
            exercise_id="E08",
            title="조건별 오류를 비교하고 한계 해석하기",
            claims=[
                "Return both held-out absolute errors and label the larger-error condition.",
                RESEARCH_CONTRACT["error_analysis"],
                RESEARCH_CONTRACT["limitations"],
            ],
            implementation='''def error_report(splits: dict[str, np.ndarray]) -> dict[str, object]:
    baseline = baseline_result(splits)["metrics"]
    one_step = one_step_result(splits)["metrics"]
    baseline_error = float(np.sqrt(baseline["loss"]))
    one_step_error = float(np.sqrt(one_step["loss"]))

    # TODO: 더 큰 절대 오차를 가진 조건을 고르세요
    larger_error_condition = NotImplemented

    return {
        "baseline_error": baseline_error,
        "one_step_error": one_step_error,
        "larger_error_condition": larger_error_condition,
    }
''',
            fixture='''observed_errors = error_report(make_splits())
print("error analysis:", observed_errors)
''',
            check='''def check_e08() -> None:
    report = error_report(make_splits())
    np.testing.assert_equal(report["larger_error_condition"], "baseline")
    np.testing.assert_equal(
        report["baseline_error"] > report["one_step_error"],
        True,
    )


check_e08()
''',
            marker="# TODO: 더 큰 절대 오차를 가진 조건을 고르세요",
            placeholder="larger_error_condition = NotImplemented",
            symbol="error_report",
            primary_outcome_id="O04",
            supporting_outcome_ids=["O03"],
            code_outcome_ids=["O04"],
            reflection_kind="interpretation",
            reflection_marker="오류 비교가 보여 주는 것과 보여 주지 못하는 것을 해석하세요.",
            reflection_claims=[
                RESEARCH_CONTRACT["error_analysis"],
                RESEARCH_CONTRACT["limitations"],
            ],
            reflection_outcome_ids=["O03"],
            reflection_result_cell_ids=["e08-fixture"],
        ),
    ]
    for cells, exercise, requirements, targets in bundles:
        payload["cells"].extend(cells)
        practice["exercises"].append(exercise)
        practice["requirements"].extend(requirements)
        practice["learner_targets"].extend(targets)
    practice["outcomes"][0]["exercise_ids"].extend(["E06", "E07"])
    practice["outcomes"][2]["exercise_ids"].append("E08")
    practice["outcomes"].extend(
        [
            {
                "id": "O04",
                "til_location": "오늘의 학습 > 통제 비교",
                "action": "debug",
                "exercise_ids": ["E08"],
                "required_evidence": "condition-level error classification",
                "curriculum_target_ids": ["CC-DL-01"],
            },
            {
                "id": "O05",
                "til_location": "오늘의 학습 > 통제 비교",
                "action": "design",
                "exercise_ids": ["E06", "E07"],
                "required_evidence": "baseline and controlled comparison design",
                "curriculum_target_ids": ["CC-DL-01"],
            },
        ]
    )


def _complete_module_artifact(notebook: Path) -> None:
    payload = _load(notebook)
    solutions = {
        "split_values = NotImplemented": (
            "split_values = (\n"
            "        all_x[:split_at],\n"
            "        all_y[:split_at],\n"
            "        all_x[split_at:],\n"
            "        all_y[split_at:],\n"
            "    )"
        ),
        "prediction = NotImplemented": "prediction = x * self.weight + self.bias",
        "loss = NotImplemented": "loss = np.mean((prediction - target) ** 2)",
        "model.weight = NotImplemented": (
            "model.weight = model.weight - learning_rate * gradient"
        ),
        "result = NotImplemented": (
            'result = {"loss": loss, "count": int(x.shape[0])}'
        ),
    }
    for cell in payload["cells"]:
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        for placeholder, solution in solutions.items():
            if placeholder in source:
                source = source.replace(placeholder, solution, 1)
        cell["source"] = source.splitlines(keepends=True)
    for cell in payload["cells"]:
        if cell.get("id") != "e05-reflection":
            continue
        reflection = "".join(cell["source"]).replace(
            "**작성:** 아직 작성하지 않음",
            "학습 loss 감소는 고정 학습 split의 한 단계 변화이고, held-out loss는 별도 한 행의 관찰일 뿐 일반화 증명은 아닙니다.",
            1,
        )
        cell["source"] = reflection.splitlines(keepends=True)
    execution_count = 0
    result_cells = set(_practice(payload)["result_cell_ids"])
    for cell in payload["cells"]:
        if cell.get("cell_type") != "code":
            continue
        execution_count += 1
        cell["execution_count"] = execution_count
        if cell.get("id") in result_cells:
            cell["outputs"] = [
                {
                    "output_type": "stream",
                    "name": "stdout",
                    "text": [f"observed {cell['id']}\n"],
                }
            ]
        else:
            cell["outputs"] = []
    _save(notebook, payload)


def _git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def _init_git_repo(root: Path) -> None:
    _git(["init"], root)
    _git(["config", "user.name", "Test User"], root)
    _git(["config", "user.email", "test@example.com"], root)


def _commit_paths(root: Path, paths: list[str], message: str) -> str:
    _git(["add", *paths], root)
    _git(["commit", "-m", message], root)
    return _git(["rev-parse", "HEAD"], root)


def _v5_module(root: Path) -> Path:
    notebook = _v5_prelab(root)
    payload = _load(notebook)
    practice = _practice(payload)
    practice["practice_layer"] = "MODULE_ASSIGNMENT"
    practice["implementation_depth"] = "I3_WORKFLOW"
    practice["milestone_id"] = "MA-TEST-01"
    practice["milestone_definition_sha256"] = _milestone_definition_hash(
        root, "MA-TEST-01"
    )
    _install_workflow_surface(payload)
    practice["result_cell_ids"] = ["e04-fixture", "e05-fixture"]
    practice["workflow_contract"] = {
        **WORKFLOW_CONTRACT,
        "stage_cell_ids": {
            "data": ["e01-implementation", "e01-fixture", "e01-check"],
            "model": ["e02-implementation", "e02-fixture"],
            "loss": ["e03-implementation", "e03-fixture"],
            "train": ["e04-implementation", "e04-fixture"],
            "evaluation": [
                "e05-implementation",
                "e05-fixture",
                "e05-check",
            ],
        },
    }
    _set_pass_review(payload)
    _save(notebook, payload)
    return notebook


def _captured_session(*, schema_version: int = 10) -> dict[str, object]:
    evidence = [
        {
            "evidence_id": "E001",
            "concept_ids": ["C01"],
            "objective_ids": ["O001"],
            "kind": "transfer",
            "content": "hidden state를 다음 시점으로 전달한다.",
            "content_sha256": "1" * 64,
            "captured_at": "2026-08-31T12:00:00+09:00",
        }
    ]
    captured: dict[str, object] = {
        "schema_version": schema_version,
        "cycle_id": "2026-08-31-sequence-10",
        "lesson_id": "sequence-lesson-10",
        "primary_target": "CC-DL-01",
        "bridge_target": None,
        "handoff_sha256": "2" * 64,
        "concepts": [
            {
                "concept_id": "C01",
                "evidence_ids": ["E001"],
                "objective_ids": ["O001"],
                "observable_outcomes": ["trace recurrence"],
                "source_location": "materials/lesson.md#Tensor-card",
                "title": "recurrence",
            }
        ],
        "learner_evidence": evidence,
        "learner_evidence_sha256": _canonical_hash(evidence),
        "source_provenance": [],
        "projection_sha256": None,
    }
    captured["projection_sha256"] = captured_session_projection_hash(captured)
    return captured


def _live_like_archived_v4(
    root: Path,
) -> tuple[Path, Path, Path, list[Path], list[dict[str, object]]]:
    """Create a v4 attempt whose immutable lesson bytes now live in its archive."""

    notebook = _v4_finalized_til(root)
    payload = _load(notebook)
    practice = _practice(payload)
    captured = _captured_session(schema_version=9)
    cycle_id = str(captured["cycle_id"])
    lesson_id = str(captured["lesson_id"])
    archive = root / "tmp/lesson-attempts" / cycle_id
    source_cache = archive / "source-cache"
    source_cache.mkdir(parents=True, exist_ok=True)

    handoff_bytes = (root / "materials/lesson.md").read_bytes()
    archived_handoff = archive / "active-lesson-handoff.md"
    archived_handoff.write_bytes(handoff_bytes)
    handoff_sha = hashlib.sha256(handoff_bytes).hexdigest()
    captured["handoff_sha256"] = handoff_sha

    provenance: list[dict[str, object]] = []
    archived_caches: list[Path] = []
    for index in range(1, 4):
        cache_bytes = f"<html><body>captured source {index}</body></html>\n".encode()
        digest = hashlib.sha256(cache_bytes).hexdigest()
        captured_path = f"tmp/active-lesson-sources/{lesson_id}/{digest}.html"
        captured_receipt = (
            f"tmp/active-lesson-sources/{lesson_id}/{digest}.receipt.json"
        )
        cache_path = source_cache / f"{digest}.html"
        receipt_path = source_cache / f"{digest}.receipt.json"
        cache_path.write_bytes(cache_bytes)
        receipt = {
            "byte_count": len(cache_bytes),
            "final_url": f"https://example.com/final/{index}",
            "kind": "primary",
            "lesson_id": lesson_id,
            "media_type": "text/html",
            "official_hosts": ["example.com"],
            "original_url": f"https://example.com/source/{index}",
            "path": captured_path,
            "receipt_path": captured_receipt,
            "retrieved_at": f"2026-08-31T12:0{index}:00+09:00",
            "sha256": digest,
            "status": "CACHED",
        }
        receipt_path.write_text(
            json.dumps(receipt, ensure_ascii=False), encoding="utf-8"
        )
        provenance.append(
            {
                "artifact": f"External source {index}",
                "course": "Captured course",
                "final_url": receipt["final_url"],
                "included_units": [f"unit {index} [{captured_path}#text: source]"],
                "offering_or_edition": "2026",
                "official_url": receipt["original_url"],
                "path": captured_path,
                "primary_id": f"I{index:03d}",
                "provider": "Example Provider",
                "receipt_path": captured_receipt,
                "role": "external-primary",
                "scope": f"bounded source {index}",
                "scope_id": None,
                "scope_kind": "ephemeral-slice",
                "sha256": digest,
            }
        )
        archived_caches.append(cache_path)
    captured["source_provenance"] = provenance
    captured["concepts"][0]["source_location"] = (
        f"{provenance[0]['path']}#text: source"
    )
    captured["projection_sha256"] = captured_session_projection_hash(captured)

    practice["learning_input"] = {
        "kind": "lesson-session",
        "cycle_id": cycle_id,
        "lesson_id": lesson_id,
        "handoff_path": "tmp/active-lesson-handoff.md",
        "handoff_sha256": handoff_sha,
        "primary_target": captured["primary_target"],
        "bridge_target": captured["bridge_target"],
        "concept_ids": ["C01"],
        "evidence_ids": ["E001"],
        "concept_sha256": "3" * 64,
        "learner_evidence_sha256": captured["learner_evidence_sha256"],
    }
    practice["sources"] = [
        {
            "id": "S001",
            "kind": "lesson",
            "path": "tmp/active-lesson-handoff.md",
            "sha256": handoff_sha,
        }
    ]
    outcome = practice["outcomes"][0]
    outcome.pop("til_location")
    outcome["concept_ids"] = ["C01"]
    outcome["evidence_ids"] = ["E001"]
    before_cells = copy.deepcopy(payload["cells"])
    _save(notebook, payload)

    active_handoff = root / "tmp/active-lesson-handoff.md"
    active_handoff.parent.mkdir(parents=True, exist_ok=True)
    active_handoff.write_text("# replacement lesson\n", encoding="utf-8")
    cursor_path = root / "tmp/active-learning-flow.json"
    cursor_path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "active_cycle_id": cycle_id,
                "cycles": [
                    {"cycle_id": cycle_id, "captured_session": captured}
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return notebook, cursor_path, archived_handoff, archived_caches, before_cells


def _v5_captured_prelab(
    root: Path,
    *,
    captured_schema_version: int = 10,
) -> tuple[Path, Path]:
    notebook = _v5_prelab(root)
    payload = _load(notebook)
    practice = _practice(payload)
    captured = _captured_session(schema_version=captured_schema_version)
    cursor_path = root / "tmp/active-learning-flow.json"
    cursor_path.parent.mkdir(parents=True, exist_ok=True)
    cursor = {
        "schema_version": 2,
        "active_cycle_id": captured["cycle_id"],
        "cycles": [
            {
                "cycle_id": captured["cycle_id"],
                "lesson_id": "mutable-top-level-value-is-not-provenance",
                "primary_target": "TR-SYS-99",
                "captured_session": captured,
            }
        ],
    }
    cursor_path.write_text(json.dumps(cursor, ensure_ascii=False), encoding="utf-8")
    practice["learning_inputs"] = [
        {
            "id": "L001",
            "role": "primary",
            "kind": "captured-cycle",
            "cycle_id": captured["cycle_id"],
            "lesson_id": captured["lesson_id"],
            "primary_target": captured["primary_target"],
            "bridge_target": captured["bridge_target"],
            "concept_ids": ["C01"],
            "evidence_ids": ["E001"],
            "captured_session_sha256": captured["projection_sha256"],
        }
    ]
    outcome = practice["outcomes"][0]
    outcome.pop("til_location")
    outcome["concept_ids"] = ["L001:C01"]
    outcome["evidence_ids"] = ["L001:E001"]
    _set_pass_review(payload)
    _save(notebook, payload)
    return notebook, cursor_path


def _v5_capstone(root: Path) -> Path:
    notebook = _v5_module(root)
    _init_git_repo(root)
    module_payload = _load(notebook)
    prior_paths = []
    prior_commit_shas: list[str] = []
    for name in ("prior-a.ipynb", "prior-b.ipynb"):
        prior = root / "practice/math" / name
        prior.write_text(json.dumps(module_payload, ensure_ascii=False), encoding="utf-8")
        _complete_module_artifact(prior)
        prior_paths.append(prior)
        prior_commit_shas.append(
            _commit_paths(
                root,
                [prior.relative_to(root).as_posix()],
                f"practice: complete {prior.stem}",
            )
        )

    payload = copy.deepcopy(module_payload)
    practice = _practice(payload)
    practice["practice_layer"] = "PHASE_CAPSTONE"
    practice["implementation_depth"] = "I5_RESEARCH"
    practice["milestone_id"] = "PC-TEST-01"
    practice["milestone_definition_sha256"] = _milestone_definition_hash(
        root, "PC-TEST-01"
    )
    practice["research_contract"] = dict(RESEARCH_CONTRACT)
    _append_capstone_surface(payload)
    practice["result_cell_ids"].extend(
        ["e06-fixture", "e07-fixture", "e08-fixture"]
    )
    practice["prior_practice_evidence"] = [
        {
            "id": f"P{index:03d}",
            "path": path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "commit_sha": prior_commit_shas[index - 1],
            "practice_layer": "MODULE_ASSIGNMENT",
            "implementation_depth": "I3_WORKFLOW",
            "milestone_id": "MA-TEST-01",
        }
        for index, path in enumerate(prior_paths, start=1)
    ]
    _set_pass_review(payload, "capstone-reviewer")
    _save(notebook, payload)
    return notebook


def test_v5_prelab_and_legacy_v3_v4_matrix(tmp_path: Path) -> None:
    prelab = _v5_prelab(tmp_path / "v5")
    assert validate(prelab, repo_root=tmp_path / "v5", check_collection=False) == []

    v3 = PracticeArtifactValidatorTests().build_notebook(tmp_path / "v3")
    assert validate(v3, repo_root=tmp_path / "v3", check_collection=False) == []
    v4 = _v4_finalized_til(tmp_path / "v4")
    assert validate(v4, repo_root=tmp_path / "v4", check_collection=False) == []

    payload = _load(v4)
    _practice(payload)["practice_layer"] = "MODULE_ASSIGNMENT"
    _save(v4, payload)
    assert "LEGACY_MILESTONE_CREDIT" in _codes(
        validate(v4, repo_root=tmp_path / "v4", check_collection=False)
    )


def test_captured_cycle_uses_only_cursor_v2_immutable_projection(tmp_path: Path) -> None:
    notebook, cursor_path = _v5_captured_prelab(tmp_path)
    assert validate(notebook, repo_root=tmp_path, check_collection=False) == []

    cursor = _load(cursor_path)
    cursor["cycles"][0]["lesson_id"] = "changed-mutable-field"
    cursor["cycles"][0]["primary_target"] = "CC-OTHER-99"
    _save(cursor_path, cursor)
    assert validate(notebook, repo_root=tmp_path, check_collection=False) == []

    cursor["cycles"][0]["captured_session"]["lesson_id"] = "drifted-capture"
    _save(cursor_path, cursor)
    assert "SESSION_REPAIR_REQUIRED" in _codes(
        validate(notebook, repo_root=tmp_path, check_collection=False)
    )


def test_module_assignment_requires_workflow_results_and_fresh_review(
    tmp_path: Path,
) -> None:
    notebook = _v5_module(tmp_path)
    assert validate(notebook, repo_root=tmp_path, check_collection=False) == []
    completion_codes = _codes(
        validate(
            notebook,
            repo_root=tmp_path,
            check_collection=False,
            completion_ready=True,
        )
    )
    assert {"COMPLETION_INCOMPLETE", "COMPLETION_RESULT_MISSING"}.issubset(
        completion_codes
    )

    payload = _load(notebook)
    _practice(payload)["result_cell_ids"] = []
    _save(notebook, payload)
    codes = _codes(validate(notebook, repo_root=tmp_path, check_collection=False))
    assert {"RESULT_EVIDENCE", "PRACTICE_REVIEW_STALE"}.issubset(codes)


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda practice: practice.update(implementation_depth="I4_EXPERIMENT"), "PRACTICE_PROGRESSION"),
        (lambda practice: practice.update(prior_practice_evidence=[]), "PRIOR_PRACTICE"),
        (lambda practice: practice["research_contract"].update(baseline=""), "RESEARCH_CONTRACT"),
    ],
)
def test_phase_capstone_matrix(tmp_path: Path, mutation, expected: str) -> None:
    notebook = _v5_capstone(tmp_path)
    assert validate(notebook, repo_root=tmp_path, check_collection=False) == []
    payload = _load(notebook)
    mutation(_practice(payload))
    _save(notebook, payload)
    assert expected in _codes(validate(notebook, repo_root=tmp_path, check_collection=False))


def test_milestone_definition_hash_drift_fails(tmp_path: Path) -> None:
    notebook = _v5_module(tmp_path)
    curriculum = tmp_path / "CURRICULUM.md"
    curriculum.write_text(
        curriculum.read_text(encoding="utf-8").replace(
            "data to model to loss to train and evaluation",
            "changed milestone definition",
        ),
        encoding="utf-8",
    )
    assert "MILESTONE_CREDIT" in _codes(
        validate(notebook, repo_root=tmp_path, check_collection=False)
    )


def test_router_priority_and_milestone_deferral(tmp_path: Path) -> None:
    _write_curriculum(tmp_path)
    capstone = route_practice(
        "evaluation-data",
        phase_capstone_ready=True,
        phase_capstone_id="PC-TEST-01",
        module_assignment_ready=True,
        module_assignment_id="MA-TEST-01",
        prelab_required=True,
        repo_root=tmp_path,
    )
    assert (capstone.practice_layer, capstone.implementation_depth) == (
        "PHASE_CAPSTONE",
        "I5_RESEARCH",
    )
    module = route_practice(
        "evaluation-data",
        module_assignment_ready=True,
        module_assignment_id="MA-TEST-01",
        prelab_required=True,
        repo_root=tmp_path,
    )
    assert module.practice_layer == "MODULE_ASSIGNMENT"
    prelab = route_practice("evaluation-data", prelab_required=True)
    assert (prelab.practice_layer, prelab.milestone_id) == ("PRE_LAB", None)
    deferred = route_practice(
        "evaluation-data",
        prelab_required=False,
        defer_to_milestone_id="MA-TEST-01",
        repo_root=tmp_path,
    )
    deferred_capstone = route_practice(
        "evaluation-data",
        defer_to_milestone_id="PC-TEST-01",
        repo_root=tmp_path,
    )
    assert deferred_capstone.milestone_id == "PC-TEST-01"
    assert (deferred.practice_action, deferred.practice_mode) == (
        "DEFER_TO_MILESTONE",
        "NONE",
    )


def test_router_requires_explicit_blocker_or_exact_milestone() -> None:
    with pytest.raises(ValueError, match="explicit blocker"):
        route_practice("evaluation-data")


@pytest.mark.parametrize(
    "milestone_id",
    ["MA-missing-01", "MA-X", "CC-DL-01", "MA-NOT-IN-CURRICULUM-01"],
)
def test_router_rejects_malformed_or_missing_deferred_milestone(
    tmp_path: Path,
    milestone_id: str,
) -> None:
    _write_curriculum(tmp_path)
    with pytest.raises(ValueError, match="defer_to_milestone_id"):
        route_practice(
            "evaluation-data",
            defer_to_milestone_id=milestone_id,
            repo_root=tmp_path,
        )


@pytest.mark.parametrize(
    ("kwargs", "argument_name"),
    [
        (
            {
                "module_assignment_id": "MA-NOT-IN-CURRICULUM-01",
                "module_assignment_ready": True,
            },
            "module_assignment_id",
        ),
        (
            {
                "module_assignment_id": "PC-TEST-01",
                "module_assignment_ready": True,
            },
            "module_assignment_id",
        ),
        (
            {
                "phase_capstone_id": "PC-NOT-IN-CURRICULUM-01",
                "phase_capstone_ready": True,
            },
            "phase_capstone_id",
        ),
        (
            {
                "phase_capstone_id": "MA-TEST-01",
                "phase_capstone_ready": True,
            },
            "phase_capstone_id",
        ),
    ],
)
def test_router_rejects_wrong_layer_or_missing_ready_milestone(
    tmp_path: Path,
    kwargs: dict[str, object],
    argument_name: str,
) -> None:
    _write_curriculum(tmp_path)
    with pytest.raises(ValueError, match=argument_name):
        route_practice("evaluation-data", repo_root=tmp_path, **kwargs)


def test_router_rejects_id_outside_the_curriculum_milestone_table(
    tmp_path: Path,
) -> None:
    (tmp_path / "CURRICULUM.md").write_text(
        "# Curriculum\n\n| MA-FAKE-01 | unrelated value |\n| --- | --- |\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="exactly one current Curriculum milestone"):
        route_practice(
            "evaluation-data",
            defer_to_milestone_id="MA-FAKE-01",
            repo_root=tmp_path,
        )


def test_router_does_not_upgrade_depth_only_equivalence_to_no_extra(
    tmp_path: Path,
) -> None:
    _write_curriculum(tmp_path)
    decision = route_practice(
        "evaluation-data",
        required_implementation_depth="I3_WORKFLOW",
        equivalent_implementation_depth="I5_RESEARCH",
        module_assignment_ready=True,
        module_assignment_id="MA-TEST-01",
        repo_root=tmp_path,
    )
    assert decision.practice_action == "CREATE_LOCAL_PRACTICE"
    assert decision.practice_layer == "MODULE_ASSIGNMENT"


def test_v4_to_v5_migration_is_atomic_idempotent_and_cell_exact(
    tmp_path: Path,
) -> None:
    notebook = _v4_finalized_til(tmp_path)
    payload = _load(notebook)
    payload["cells"][3]["execution_count"] = 7
    payload["cells"][3]["outputs"] = [
        {"output_type": "stream", "name": "stdout", "text": ["사용자 출력\n"]}
    ]
    _save(notebook, payload)
    before_cells = copy.deepcopy(payload["cells"])

    migrated = migrate_payload(payload)
    assert migrated["cells"] == before_cells
    practice = _practice(migrated)
    assert (
        practice["schema_version"],
        practice["practice_layer"],
        practice["implementation_depth"],
        practice["lifecycle"],
        practice["milestone_id"],
    ) == (5, "PRE_LAB", "I1_MECHANISM", "preserved_attempt", None)

    changed, cells_hash = migrate_file(notebook, repo_root=tmp_path)
    assert changed
    assert _load(notebook)["cells"] == before_cells
    first_bytes = notebook.read_bytes()
    changed_again, second_hash = migrate_file(notebook, repo_root=tmp_path)
    assert not changed_again
    assert notebook.read_bytes() == first_bytes
    assert second_hash == cells_hash


def test_archived_v4_migration_passes_learner_state_without_live_handoff(
    tmp_path: Path,
) -> None:
    notebook, cursor, _, _, before_cells = _live_like_archived_v4(tmp_path)

    changed, cells_hash = migrate_file(
        notebook, repo_root=tmp_path, cursor_path=cursor
    )
    assert changed
    migrated = _load(notebook)
    assert migrated["cells"] == before_cells
    sources = _practice(migrated)["sources"]
    assert sources[0]["path"].startswith(
        "tmp/lesson-attempts/2026-08-31-sequence-10/"
    )
    assert len(sources) == 4
    assert all(
        source["cache_path"].startswith(
            "tmp/lesson-attempts/2026-08-31-sequence-10/source-cache/"
        )
        and source["captured_path"].startswith("tmp/active-lesson-sources/")
        for source in sources[1:]
    )
    assert validate(
        notebook,
        repo_root=tmp_path,
        check_collection=False,
        learner_state=True,
    ) == []

    first_bytes = notebook.read_bytes()
    changed_again, second_hash = migrate_file(
        notebook, repo_root=tmp_path, cursor_path=cursor
    )
    assert not changed_again
    assert notebook.read_bytes() == first_bytes
    assert second_hash == cells_hash


def test_preserved_archive_byte_or_hash_mismatch_fails_validation(
    tmp_path: Path,
) -> None:
    notebook, cursor, archived_handoff, archived_caches, _ = (
        _live_like_archived_v4(tmp_path)
    )
    migrate_file(notebook, repo_root=tmp_path, cursor_path=cursor)
    original_cache = archived_caches[0].read_bytes()
    archived_caches[0].write_bytes(original_cache + b"tampered")
    assert {
        "EXTERNAL_SOURCE_RECEIPT",
    }.issubset(
        _codes(
            validate(
                notebook,
                repo_root=tmp_path,
                check_collection=False,
                learner_state=True,
            )
        )
    )

    archived_caches[0].write_bytes(original_cache)
    archived_receipt = archived_caches[0].with_suffix(".receipt.json")
    original_receipt = archived_receipt.read_bytes()
    receipt_payload = json.loads(original_receipt)
    receipt_payload["byte_count"] += 1
    archived_receipt.write_text(json.dumps(receipt_payload), encoding="utf-8")
    assert "EXTERNAL_SOURCE_RECEIPT" in _codes(
        validate(
            notebook,
            repo_root=tmp_path,
            check_collection=False,
            learner_state=True,
        )
    )

    archived_receipt.write_bytes(original_receipt)
    archived_handoff.write_text("# tampered archived handoff\n", encoding="utf-8")
    assert "SOURCE_AUDIT" in _codes(
        validate(
            notebook,
            repo_root=tmp_path,
            check_collection=False,
            learner_state=True,
        )
    )


def test_already_v5_preserved_attempt_repairs_only_missing_archive_bindings(
    tmp_path: Path,
) -> None:
    notebook, cursor, _, _, before_cells = _live_like_archived_v4(tmp_path)
    migrate_file(notebook, repo_root=tmp_path, cursor_path=cursor)
    regressed = _load(notebook)
    practice = _practice(regressed)
    handoff_sha = practice["sources"][0]["sha256"]
    practice["sources"] = [
        {
            "id": "S001",
            "kind": "lesson",
            "path": "tmp/active-lesson-handoff.md",
            "sha256": handoff_sha,
        }
    ]
    _save(notebook, regressed)

    changed, _ = migrate_file(notebook, repo_root=tmp_path, cursor_path=cursor)
    assert changed
    assert _load(notebook)["cells"] == before_cells
    assert validate(
        notebook,
        repo_root=tmp_path,
        check_collection=False,
        learner_state=True,
    ) == []
    repaired_bytes = notebook.read_bytes()
    changed_again, _ = migrate_file(
        notebook, repo_root=tmp_path, cursor_path=cursor
    )
    assert not changed_again
    assert notebook.read_bytes() == repaired_bytes


def test_fresh_v5_is_never_rewritten_by_the_preserved_attempt_migrator(
    tmp_path: Path,
) -> None:
    notebook = _v5_prelab(tmp_path)
    before = notebook.read_bytes()
    before_cells = copy.deepcopy(_load(notebook)["cells"])

    changed, _ = migrate_file(notebook, repo_root=tmp_path)

    assert not changed
    assert notebook.read_bytes() == before
    assert _load(notebook)["cells"] == before_cells


def test_preserved_archive_migration_rejects_handoff_symlink_escape(
    tmp_path: Path,
) -> None:
    notebook, cursor, archived_handoff, _, _ = _live_like_archived_v4(tmp_path)
    before = notebook.read_bytes()
    archived_handoff.unlink()
    archived_handoff.symlink_to(tmp_path / "materials/lesson.md")

    with pytest.raises(ValueError, match="symbolic links"):
        migrate_file(notebook, repo_root=tmp_path, cursor_path=cursor)

    assert notebook.read_bytes() == before


def test_preserved_attempt_rejects_duplicate_captured_inputs_and_cross_cycle_archive(
    tmp_path: Path,
) -> None:
    notebook, cursor_path, _, _, _ = _live_like_archived_v4(tmp_path)
    migrate_file(notebook, repo_root=tmp_path, cursor_path=cursor_path)

    duplicate = _load(notebook)
    duplicate_input = copy.deepcopy(_practice(duplicate)["learning_inputs"][0])
    duplicate_input["id"] = "L002"
    duplicate_input["role"] = "supporting"
    _practice(duplicate)["learning_inputs"].append(duplicate_input)
    _save(notebook, duplicate)
    assert "SESSION_REPAIR_REQUIRED" in _codes(
        validate(
            notebook,
            repo_root=tmp_path,
            check_collection=False,
            learner_state=True,
        )
    )

    cross_cycle = copy.deepcopy(duplicate)
    practice = _practice(cross_cycle)
    practice["learning_inputs"] = [practice["learning_inputs"][0]]
    cursor = _load(cursor_path)
    captured = copy.deepcopy(cursor["cycles"][0]["captured_session"])
    captured["cycle_id"] = "2026-08-31-sequence-11"
    captured["projection_sha256"] = captured_session_projection_hash(captured)
    cursor["cycles"] = [
        {
            "cycle_id": captured["cycle_id"],
            "captured_session": captured,
        }
    ]
    cursor["active_cycle_id"] = captured["cycle_id"]
    cursor_path.write_text(json.dumps(cursor), encoding="utf-8")
    input_record = practice["learning_inputs"][0]
    input_record["cycle_id"] = captured["cycle_id"]
    input_record["captured_session_sha256"] = captured["projection_sha256"]
    _save(notebook, cross_cycle)
    codes = _codes(
        validate(
            notebook,
            repo_root=tmp_path,
            check_collection=False,
            learner_state=True,
        )
    )
    assert {"EXTERNAL_SOURCE_IDENTITY", "SOURCE_AUDIT"}.issubset(codes)


def test_v4_session_migration_mismatch_preserves_original_bytes(tmp_path: Path) -> None:
    notebook = _v4_finalized_til(tmp_path)
    payload = _load(notebook)
    practice = _practice(payload)
    captured = _captured_session()
    practice["learning_input"] = {
        "kind": "lesson-session",
        "cycle_id": captured["cycle_id"],
        "lesson_id": "mismatch",
        "handoff_path": "tmp/ignored-attempt/handoff.md",
        "handoff_sha256": captured["handoff_sha256"],
        "primary_target": captured["primary_target"],
        "bridge_target": captured["bridge_target"],
        "concept_ids": ["C01"],
        "evidence_ids": ["E001"],
        "concept_sha256": "3" * 64,
        "learner_evidence_sha256": captured["learner_evidence_sha256"],
    }
    outcome = practice["outcomes"][0]
    outcome.pop("til_location")
    outcome["concept_ids"] = ["C01"]
    outcome["evidence_ids"] = ["E001"]
    _save(notebook, payload)
    before_bytes = notebook.read_bytes()
    cursor = {
        "schema_version": 2,
        "cycles": [{"cycle_id": captured["cycle_id"], "captured_session": captured}],
    }
    cursor_path = tmp_path / "tmp/active-learning-flow.json"
    cursor_path.parent.mkdir(parents=True, exist_ok=True)
    cursor_path.write_text(json.dumps(cursor, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="lesson_id"):
        migrate_file(notebook, repo_root=tmp_path, cursor_path=cursor_path)
    assert notebook.read_bytes() == before_bytes


def test_v4_session_migration_requires_matching_captured_projection(
    tmp_path: Path,
) -> None:
    notebook = _v4_finalized_til(tmp_path)
    payload = _load(notebook)
    practice = _practice(payload)
    captured = _captured_session()
    practice["learning_input"] = {
        "kind": "lesson-session",
        "cycle_id": captured["cycle_id"],
        "lesson_id": captured["lesson_id"],
        "handoff_path": "tmp/ignored-attempt/handoff.md",
        "handoff_sha256": captured["handoff_sha256"],
        "primary_target": captured["primary_target"],
        "bridge_target": captured["bridge_target"],
        "concept_ids": ["C01"],
        "evidence_ids": ["E001"],
        "concept_sha256": "3" * 64,
        "learner_evidence_sha256": captured["learner_evidence_sha256"],
    }
    outcome = practice["outcomes"][0]
    outcome.pop("til_location")
    outcome["concept_ids"] = ["C01"]
    outcome["evidence_ids"] = ["E001"]
    cursor = {
        "schema_version": 2,
        "cycles": [
            {"cycle_id": captured["cycle_id"], "captured_session": captured}
        ],
    }
    migrated = migrate_payload(payload, cursor=cursor)
    migrated_input = _practice(migrated)["learning_inputs"][0]
    assert migrated_input["captured_session_sha256"] == captured["projection_sha256"]
    assert _practice(migrated)["outcomes"][0]["concept_ids"] == ["L001:C01"]

    drifted = copy.deepcopy(payload)
    _practice(drifted)["learning_input"]["lesson_id"] = "wrong"
    with pytest.raises(ValueError, match="lesson_id"):
        migrate_payload(drifted, cursor=cursor)


def test_creation_review_recording_is_metadata_only_and_supports_one_repair(
    tmp_path: Path,
) -> None:
    notebook = _v4_finalized_til(tmp_path)
    migrated = migrate_payload(_load(notebook))
    before_cells = copy.deepcopy(migrated["cells"])
    first = record_review(
        migrated,
        reviewer_id="surface-reviewer",
        reviewed_at="2026-08-31T12:00:00+09:00",
        learner_surface_verdict="repair_required",
        metadata_verdict="pass",
    )
    assert first["cells"] == before_cells
    first_hash = _practice(first)["creation_reviews"][0]["contract_sha256"]

    first["cells"][0]["source"].append("\n학습 목적을 더 분명히 설명합니다.\n")
    repaired_cells = copy.deepcopy(first["cells"])
    second = record_review(
        first,
        reviewer_id="fresh-metadata-reviewer",
        reviewed_at="2026-08-31T12:30:00+09:00",
        learner_surface_verdict="pass",
        metadata_verdict="pass",
    )
    assert second["cells"] == repaired_cells
    reviews = _practice(second)["creation_reviews"]
    assert reviews[0]["contract_sha256"] == first_hash
    assert reviews[1]["contract_sha256"] != first_hash
    _save(notebook, second)
    assert validate(
        notebook,
        repo_root=tmp_path,
        check_collection=False,
        learner_state=True,
    ) == []


def test_module_assignment_rejects_one_cell_fake_workflow_and_missing_surface_mapping(
    tmp_path: Path,
) -> None:
    notebook = _v5_module(tmp_path)
    payload = _load(notebook)
    practice = _practice(payload)
    practice["workflow_contract"]["stage_cell_ids"] = {
        stage: ["e01-fixture"]
        for stage in practice["workflow_contract"]["stage_cell_ids"]
    }
    _save(notebook, payload)
    assert "WORKFLOW_CONTRACT" in _codes(
        validate(notebook, repo_root=tmp_path, check_collection=False)
    )

    notebook = _v5_module(tmp_path / "surface")
    payload = _load(notebook)
    evaluation_brief = next(
        cell for cell in payload["cells"] if cell.get("id") == "e05-brief"
    )
    evaluation_brief["source"] = "".join(evaluation_brief["source"]).replace(
        WORKFLOW_CONTRACT["evaluation_contract"],
        "",
        1,
    ).splitlines(keepends=True)
    _save(notebook, payload)
    codes = _codes(validate(notebook, repo_root=tmp_path / "surface", check_collection=False))
    assert {"WORKFLOW_CONTRACT", "PRACTICE_REVIEW_STALE"}.issubset(
        codes
    )


def test_module_assignment_requires_interpretation_of_train_and_eval_results(
    tmp_path: Path,
) -> None:
    notebook = _v5_module(tmp_path)
    payload = _load(notebook)
    practice = _practice(payload)
    practice["result_cell_ids"].append("e01-fixture")
    interpretation_target = next(
        target
        for target in practice["learner_targets"]
        if target.get("kind") == "interpretation"
    )
    interpretation_target["result_cell_ids"] = ["e01-fixture"]
    _set_pass_review(payload)
    _save(notebook, payload)
    assert "RESULT_EVIDENCE" in _codes(
        validate(notebook, repo_root=tmp_path, check_collection=False)
    )


def test_module_assignment_rejects_distinct_but_noop_stage_shells(
    tmp_path: Path,
) -> None:
    notebook = _v5_module(tmp_path)
    payload = _load(notebook)
    replacements = {
        "e01-implementation": '''def make_splits() -> dict[str, np.ndarray]:
    # TODO: 앞의 세 행과 마지막 한 행을 나누세요
    split_values = NotImplemented
    return split_values
''',
        "e02-implementation": '''class LinearRegressor:
    def __init__(self, weight: float, bias: float) -> None:
        pass

    def __call__(self, x: np.ndarray) -> np.ndarray:
        # TODO: 선형 예측식을 완성하세요
        prediction = NotImplemented
        return prediction
''',
        "e03-implementation": '''def mse_loss(prediction: np.ndarray, target: np.ndarray) -> float:
    # TODO: 원소별 오차의 제곱을 평균내세요
    loss = NotImplemented
    return loss
''',
        "e04-implementation": '''def train_step(
    model: LinearRegressor,
    x: np.ndarray,
    target: np.ndarray,
    learning_rate: float,
) -> dict[str, float]:
    # TODO: 계산한 gradient로 weight를 한 번 갱신하세요
    model.weight = NotImplemented
    return {}
''',
        "e05-implementation": '''def evaluate(
    model: LinearRegressor,
    x: np.ndarray,
    target: np.ndarray,
) -> dict[str, float | int]:
    # TODO: 평가 행 수와 loss를 결과로 조립하세요
    result = NotImplemented
    return result
''',
    }
    for cell in payload["cells"]:
        cell_id = cell.get("id")
        if cell_id in replacements:
            cell["source"] = replacements[cell_id].splitlines(keepends=True)
    _set_pass_review(payload, "adversarial-reviewer")
    _save(notebook, payload)
    assert "WORKFLOW_CONTRACT" in _codes(
        validate(notebook, repo_root=tmp_path, check_collection=False)
    )


def test_capstone_requires_surface_mapped_research_contract(tmp_path: Path) -> None:
    notebook = _v5_capstone(tmp_path)
    payload = _load(notebook)
    practice = _practice(payload)
    practice["research_contract"]["baseline"] = "Metadata-only baseline sentence."
    _save(notebook, payload)
    codes = _codes(validate(notebook, repo_root=tmp_path, check_collection=False))
    assert {"RESEARCH_CONTRACT", "PRACTICE_REVIEW_STALE"}.issubset(codes)


def test_capstone_requires_distinct_baseline_control_and_error_results(
    tmp_path: Path,
) -> None:
    notebook = _v5_capstone(tmp_path)
    payload = _load(notebook)
    practice = _practice(payload)
    for target in practice["learner_targets"]:
        if target.get("kind") in {"design", "interpretation"}:
            target["result_cell_ids"] = ["e08-fixture"]
    _save(notebook, payload)
    codes = _codes(validate(notebook, repo_root=tmp_path, check_collection=False))
    assert {"RESEARCH_CONTRACT", "PRACTICE_REVIEW_STALE"}.issubset(codes)


def test_review_hash_tracks_api_and_scaffold_suffix_but_not_learner_edits(
    tmp_path: Path,
) -> None:
    notebook = _v5_module(tmp_path)
    baseline = _load(notebook)
    baseline_hash = _practice(baseline)["creation_reviews"][0]["contract_sha256"]

    learner_edit = _load(notebook)
    data_cell = next(
        cell for cell in learner_edit["cells"] if cell.get("id") == "e01-implementation"
    )
    data_cell["source"] = _replace_once(
        "".join(data_cell["source"]),
        "split_values = NotImplemented",
        "split_values = (all_x[:3], all_y[:3], all_x[3:], all_y[3:])",
    ).splitlines(keepends=True)
    reflection_cell = next(
        cell for cell in learner_edit["cells"] if cell.get("id") == "e05-reflection"
    )
    reflection_cell["source"] = _replace_once(
        "".join(reflection_cell["source"]),
        "**작성:** 아직 작성하지 않음",
        "학습자가 관찰한 결과를 요약합니다.",
    ).splitlines(keepends=True)
    assert practice_contract_hash(learner_edit) == baseline_hash

    api_edit = _load(notebook)
    api_cell = next(
        cell for cell in api_edit["cells"] if cell.get("id") == "e01-implementation"
    )
    api_cell["source"] = _replace_once(
        "".join(api_cell["source"]),
        "def make_splits() -> dict[str, np.ndarray]:",
        "def make_splits(split_at: int = 3) -> dict[str, np.ndarray]:",
    ).splitlines(keepends=True)
    assert practice_contract_hash(api_edit) != baseline_hash

    suffix_edit = _load(notebook)
    suffix_cell = next(
        cell for cell in suffix_edit["cells"] if cell.get("id") == "e01-implementation"
    )
    suffix_cell["source"] = _replace_once(
        "".join(suffix_cell["source"]),
        '"x_train": x_train,',
        '"training_x": x_train,',
    ).splitlines(keepends=True)
    assert practice_contract_hash(suffix_edit) != baseline_hash


def test_v9_captured_cycle_cannot_claim_fresh_v5_credit(tmp_path: Path) -> None:
    notebook, cursor_path = _v5_captured_prelab(
        tmp_path,
        captured_schema_version=9,
    )
    cursor = _load(cursor_path)
    captured = cursor["cycles"][0]["captured_session"]
    assert captured["schema_version"] == 9
    assert captured["projection_sha256"] == captured_session_projection_hash(
        captured
    )
    assert "PRACTICE_PROGRESSION" in _codes(
        validate(notebook, repo_root=tmp_path, check_collection=False)
    )


@pytest.mark.parametrize(
    ("mutator", "expected"),
    [
        (
            lambda payload: _practice(payload)["prior_practice_evidence"].__setitem__(
                0,
                {
                    **_practice(payload)["prior_practice_evidence"][0],
                    "commit_sha": "f" * 40,
                },
            ),
            "PRIOR_PRACTICE",
        ),
        (
            lambda payload: _practice(payload)["prior_practice_evidence"].__setitem__(
                0,
                {
                    **_practice(payload)["prior_practice_evidence"][0],
                    "path": "practice/math/missing.ipynb",
                },
            ),
            "PRIOR_PRACTICE",
        ),
        (
            lambda payload: _practice(payload)["prior_practice_evidence"].__setitem__(
                0,
                {
                    **_practice(payload)["prior_practice_evidence"][0],
                    "sha256": "0" * 64,
                },
            ),
            "PRIOR_PRACTICE_DRIFT",
        ),
    ],
)
def test_capstone_prior_commit_provenance_failures(
    tmp_path: Path,
    mutator,
    expected: str,
) -> None:
    notebook = _v5_capstone(tmp_path)
    payload = _load(notebook)
    mutator(payload)
    _save(notebook, payload)
    assert expected in _codes(validate(notebook, repo_root=tmp_path, check_collection=False))


def test_capstone_rejects_prior_completion_commit_with_an_extra_path(
    tmp_path: Path,
) -> None:
    notebook = _v5_capstone(tmp_path)
    payload = _load(notebook)
    practice = _practice(payload)
    prior_record = practice["prior_practice_evidence"][0]
    prior_path = tmp_path / prior_record["path"]
    prior_payload = _load(prior_path)
    model_cell = next(
        cell
        for cell in prior_payload["cells"]
        if cell.get("id") == "e02-implementation"
    )
    model_cell["source"] = _replace_once(
        "".join(model_cell["source"]),
        "prediction = x * self.weight + self.bias",
        "prediction = self.bias + x * self.weight",
    ).splitlines(keepends=True)
    _save(prior_path, prior_payload)
    extra = tmp_path / "unrelated.txt"
    extra.write_text("not part of the practice completion\n", encoding="utf-8")
    bundle_commit = _commit_paths(
        tmp_path,
        [prior_record["path"], extra.relative_to(tmp_path).as_posix()],
        "practice: bundled completion should fail",
    )
    prior_record["sha256"] = hashlib.sha256(prior_path.read_bytes()).hexdigest()
    prior_record["commit_sha"] = bundle_commit
    _save(notebook, payload)
    assert "PRIOR_PRACTICE" in _codes(
        validate(notebook, repo_root=tmp_path, check_collection=False)
    )
