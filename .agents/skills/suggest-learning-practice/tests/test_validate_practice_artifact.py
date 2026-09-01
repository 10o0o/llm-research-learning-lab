from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from validate_practice_artifact import validate as validate_artifact  # noqa: E402
from validate_practice_notebook import collect_observables  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def practice_cell_meta(
    role: str,
    exercise_id: str | None = None,
    *,
    observables: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    practice: dict[str, object] = {"role": role}
    if exercise_id is not None:
        practice["exercise_id"] = exercise_id
    if observables is not None:
        practice["observables"] = observables
    return {"llm_research_lab": {"practice": practice}}


def markdown_cell(
    cell_id: str,
    role: str,
    text: str,
    exercise_id: str | None = None,
) -> dict[str, object]:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": practice_cell_meta(role, exercise_id),
        "source": text.splitlines(keepends=True),
    }


def code_cell(
    cell_id: str,
    role: str,
    text: str,
    exercise_id: str | None = None,
    *,
    observables: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": practice_cell_meta(role, exercise_id, observables=observables),
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


class PracticeArtifactValidatorTests(unittest.TestCase):
    def build_notebook(self, root: Path) -> Path:
        notebook = root / "practice/math/vector-practice.ipynb"
        notebook.parent.mkdir(parents=True, exist_ok=True)
        til = root / "til/2026/08/2026-08-20.md"
        til.parent.mkdir(parents=True, exist_ok=True)
        til.write_text("# TIL\n", encoding="utf-8")
        lesson = root / "materials/lesson.md"
        lesson.parent.mkdir(exist_ok=True)
        lesson.write_text(
            "# Lesson\n\n## Tensor 카드\n\nTensor 이름을 인자로 받는다.\n",
            encoding="utf-8",
        )

        intro = """# Tensor 카드 만들기

배열의 이름은 제공된 뼈대가 보존하고, 배열의 shape를 직접 읽어 카드에 채웁니다.

필요할 때만 [기준 TIL](../../til/2026/08/2026-08-20.md)을 복습하세요.
"""
        brief = """## 실습 1. 배열의 shape 기록하기

이름 전달과 오류 처리는 준비되어 있습니다. 배열에서 shape를 읽는 핵심만 완성하세요.

### 요구사항

- 반환된 `name`은 함수에 입력한 이름과 같아야 합니다.
- `shape`은 NumPy 배열의 shape를 일반 tuple로 기록해야 합니다.
- 배열 대신 다른 값을 받으면 `TypeError`로 실패해야 합니다.

### 작은 예

`np.zeros((2, 3))`의 두 축을 어떤 tuple로 보존할지 먼저 예상하세요.

<details><summary>힌트 1</summary>

배열 객체가 이미 가진 shape 속성을 확인하세요.

</details>

<details><summary>힌트 2</summary>

반환 dict는 제공되어 있으므로 `shape` 변수 하나만 채우면 됩니다.

</details>
"""
        implementation_code = '''def tensor_card(name: str, tensor: np.ndarray) -> dict[str, object]:
    """Return a name and shape card for one NumPy array."""
    if not isinstance(tensor, np.ndarray):
        raise TypeError("tensor must be a NumPy array")

    # TODO: 배열의 shape를 tuple로 읽으세요
    raise NotImplementedError("shape를 채우세요")

    return {"name": name, "shape": shape}


def display_card(card: dict[str, object]) -> str:
    """Provided presentation helper; it is not learner-owned."""
    return f"{card['name']}: {card['shape']}"
'''
        fixture_code = """# 예제 입력으로 동작을 살펴보세요
sample = np.zeros((2, 3))
print(display_card(tensor_card("sample", sample)))
"""
        check_code = '''# 구현을 마친 뒤 이 셀을 실행하세요
def check_e01() -> None:
    # 기본 동작
    card = tensor_card("sample", np.zeros((2, 3)))
    np.testing.assert_equal(card["name"], "sample")
    np.testing.assert_equal(card["shape"], (2, 3))

    # 경계값
    scalar = tensor_card("scalar", np.array(1.0))
    np.testing.assert_equal(scalar["shape"], ())

    # 잘못된 입력
    try:
        tensor_card("bad", [1, 2])
    except TypeError:
        pass
    else:
        raise AssertionError("배열이 아니면 TypeError여야 합니다")


check_e01()
'''
        observed, error = collect_observables(check_code)
        self.assertIsNone(error)
        mappings = [
            ("normal", "C-E01-01"),
            ("normal", "C-E01-02"),
            ("edge", "C-E01-02"),
            ("failure", "C-E01-03"),
        ]
        observables = [
            {
                "ordinal": item.ordinal,
                "kind": item.kind,
                "fingerprint": item.fingerprint,
                "category": category,
                "requirement_ids": [requirement_id],
            }
            for item, (category, requirement_id) in zip(observed, mappings, strict=True)
        ]
        reflection = """### 확인 결과 정리

선택 복습입니다. 원한다면 관찰한 shape와 scalar의 빈 shape가 무엇을 뜻하는지 메모해도 좋습니다. 이 메모는 실습 완료 조건이 아닙니다.
"""
        requirements = [
            {
                "id": "C-E01-01",
                "exercise_id": "E01",
                "kind": "source-given",
                "claim": "반환된 `name`은 함수에 입력한 이름과 같아야 합니다.",
                "owner": "provided",
                "source_locations": [
                    {
                        "source_id": "S001",
                        "locator": "Tensor 카드",
                        "anchor": "Tensor 이름을 인자로 받는다",
                    }
                ],
                "rationale": "",
                "visible_cell_id": "e01-brief",
                "target_ids": [],
            },
            {
                "id": "C-E01-02",
                "exercise_id": "E01",
                "kind": "derive",
                "claim": "`shape`은 NumPy 배열의 shape를 일반 tuple로 기록해야 합니다.",
                "owner": "learner",
                "source_locations": [],
                "rationale": "",
                "visible_cell_id": "e01-brief",
                "target_ids": ["T-E01-01"],
            },
            {
                "id": "C-E01-03",
                "exercise_id": "E01",
                "kind": "practice-given",
                "claim": "배열 대신 다른 값을 받으면 `TypeError`로 실패해야 합니다.",
                "owner": "provided",
                "source_locations": [],
                "rationale": "제공된 함수 경계에서 잘못된 입력을 조기에 설명하기 위한 오류 처리",
                "visible_cell_id": "e01-brief",
                "target_ids": [],
            },
        ]
        payload = {
            "cells": [
                markdown_cell("intro", "intro", intro),
                code_cell("setup", "setup", "# 공통 준비\nimport numpy as np\n"),
                markdown_cell("e01-brief", "brief", brief, "E01"),
                code_cell("e01-implementation", "implementation", implementation_code, "E01"),
                code_cell("e01-fixture", "fixture", fixture_code, "E01"),
                code_cell("e01-check", "check", check_code, "E01", observables=observables),
                markdown_cell("e01-reflection", "reflection", reflection, "E01"),
            ],
            "metadata": {
                "llm_research_lab": {
                    "practice": {
                        "schema_version": 3,
                        "artifact_kind": "standalone-practice",
                        "scaffold_mode": "guided-fading",
                        "practice_mode": "NOTEBOOK",
                        "curriculum_targets": ["CC-DL-01"],
                        "til": {"path": "til/2026/08/2026-08-20.md", "sha256": sha256(til)},
                        "sources": [
                            {"id": "S001", "kind": "lesson", "path": "materials/lesson.md", "sha256": sha256(lesson)}
                        ],
                        "outcomes": [
                            {
                                "id": "O01",
                                "til_location": "오늘의 학습 > Tensor shape",
                                "action": "implement",
                                "exercise_ids": ["E01"],
                                "required_evidence": "shape 구현과 공개 검사",
                                "curriculum_target_ids": ["CC-DL-01"],
                            }
                        ],
                        "exercises": [
                            {
                                "id": "E01",
                                "primary_outcome_id": "O01",
                                "supporting_outcome_ids": [],
                                "scaffold_stage": "guided",
                                "learner_target_ids": ["T-E01-01"],
                            }
                        ],
                        "requirements": requirements,
                        "learner_targets": [
                            {
                                "id": "T-E01-01",
                                "exercise_id": "E01",
                                "kind": "code",
                                "cell_id": "e01-implementation",
                                "marker": "# TODO: 배열의 shape를 tuple로 읽으세요",
                                "placeholder": 'raise NotImplementedError("shape를 채우세요")',
                                "symbol": "tensor_card",
                                "outcome_ids": ["O01"],
                                "requirement_ids": ["C-E01-02"],
                            }
                        ],
                    }
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        notebook.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return notebook

    @staticmethod
    def codes(problems) -> set[str]:
        return {problem.code for problem in problems}

    @staticmethod
    def load(path: Path) -> dict[str, object]:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def save(path: Path, payload: dict[str, object]) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def problems(self, notebook: Path, root: Path, *, learner_state: bool = False):
        return validate_artifact(
            notebook,
            repo_root=root,
            check_collection=False,
            learner_state=learner_state,
        )

    def test_guided_scaffold_and_complete_helper_pass_creation_ready(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(self.problems(self.build_notebook(root), root), [])

    def test_full_claim_relation_not_just_tokens_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            source = "".join(payload["cells"][2]["source"]).replace(
                "반환된 `name`은 함수에 입력한 이름과 같아야 합니다.",
                "반환된 `name`과 함수에 입력한 이름은 서로 달라도 됩니다.",
            )
            payload["cells"][2]["source"] = source.splitlines(keepends=True)
            self.save(notebook, payload)
            self.assertIn("SPEC_DISCLOSURE", self.codes(self.problems(notebook, root)))

    def test_checked_learner_class_api_name_must_be_disclosed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            practice = payload["metadata"]["llm_research_lab"]["practice"]
            brief = """## 실습 1. 작은 모듈의 속성 등록하기

### 요구사항

- 생성자에서 입력을 처리할 모듈 속성을 등록해야 합니다.

<details><summary>힌트 1</summary>

생성자에서 `self.` 뒤에 속성을 저장하세요.

</details>

<details><summary>힌트 2</summary>

검사에서 접근하는 속성 이름도 확인하세요.

</details>
"""
            implementation = '''class TinyModel:
    def __init__(self):
        # TODO: 입력을 처리할 모듈 속성을 등록하세요
        self.feature = NotImplemented
'''
            check = '''def check_e01() -> None:
    model = TinyModel()
    np.testing.assert_equal(model.feature, 1)


check_e01()
'''
            observed, error = collect_observables(check)
            self.assertIsNone(error)
            payload["cells"][2]["source"] = brief.splitlines(keepends=True)
            payload["cells"][3]["source"] = implementation.splitlines(keepends=True)
            payload["cells"][5]["source"] = check.splitlines(keepends=True)
            payload["cells"][5]["metadata"]["llm_research_lab"]["practice"]["observables"] = [
                {
                    "ordinal": observed[0].ordinal,
                    "kind": observed[0].kind,
                    "fingerprint": observed[0].fingerprint,
                    "category": "normal",
                    "requirement_ids": ["C-E01-01"],
                }
            ]
            practice["requirements"] = [
                {
                    "id": "C-E01-01",
                    "exercise_id": "E01",
                    "kind": "source-given",
                    "claim": "생성자에서 입력을 처리할 모듈 속성을 등록해야 합니다.",
                    "owner": "learner",
                    "source_locations": [
                        {
                            "source_id": "S001",
                            "locator": "Tensor 카드",
                            "anchor": "Tensor 이름을 인자로 받는다",
                        }
                    ],
                    "rationale": "",
                    "visible_cell_id": "e01-brief",
                    "target_ids": ["T-E01-01"],
                }
            ]
            target = practice["learner_targets"][0]
            target.update(
                {
                    "marker": "# TODO: 입력을 처리할 모듈 속성을 등록하세요",
                    "placeholder": "self.feature = NotImplemented",
                    "symbol": "TinyModel",
                    "requirement_ids": ["C-E01-01"],
                }
            )
            self.save(notebook, payload)
            self.assertIn("SPEC_DISCLOSURE", self.codes(self.problems(notebook, root)))

            claim = "생성자에서 `self.feature`라는 입력 처리 모듈 속성을 등록해야 합니다."
            practice["requirements"][0]["claim"] = claim
            payload["cells"][2]["source"] = (
                "## 실습 1. 작은 모듈의 속성 등록하기\n\n### 요구사항\n\n- "
                + claim
                + "\n\n<details><summary>힌트 1</summary>\n\n생성자에서 `self.` 뒤에 속성을 저장하세요.\n\n</details>\n"
                + "\n<details><summary>힌트 2</summary>\n\n검사에서 접근하는 속성 이름도 확인하세요.\n\n</details>\n"
            ).splitlines(keepends=True)
            self.save(notebook, payload)
            self.assertEqual(self.problems(notebook, root), [])

    def test_multifacet_rules_cannot_be_reduced_to_keyword_presence(self) -> None:
        cases = [
            (
                "probability는 마지막 class 축 `dim=-1`에 Softmax를 적용해 만들며 모든 원소가 양수이고 각 sample의 합이 1이어야 합니다.",
                "probability는 마지막 class 축 `dim=-1`에 Softmax를 적용해 만들며 원소가 음수여도 되고 각 sample의 합이 1이어야 합니다.",
            ),
            (
                "prediction은 `probability >= threshold`인 원소를 1로 정하고 `torch.long`으로 반환해야 합니다.",
                "prediction은 `probability > threshold`인 원소를 1로 정하고 `torch.long`으로 반환해야 합니다.",
            ),
            (
                "dtype과 device는 Tensor 속성을 각각 문자열로 기록해야 합니다.",
                "dtype과 device는 Tensor 속성을 각각 원래 객체로 기록해야 합니다.",
            ),
            (
                "accuracy는 맞은 sample 수를 batch 크기로 나눈 Python `float`이어야 합니다.",
                "accuracy는 맞은 sample 수의 합인 Python `float`이어야 합니다.",
            ),
            (
                "history가 비어 있으면 `ValueError`로 거부해야 합니다.",
                "history가 비어 있으면 `None`을 반환해야 합니다.",
            ),
        ]
        original = "`shape`은 NumPy 배열의 shape를 일반 tuple로 기록해야 합니다."
        for claim, contradiction in cases:
            with self.subTest(claim=claim), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                notebook = self.build_notebook(root)
                payload = self.load(notebook)
                requirement = payload["metadata"]["llm_research_lab"]["practice"]["requirements"][1]
                requirement["claim"] = claim
                brief = "".join(payload["cells"][2]["source"]).replace(original, contradiction)
                payload["cells"][2]["source"] = brief.splitlines(keepends=True)
                self.save(notebook, payload)
                self.assertIn("SPEC_DISCLOSURE", self.codes(self.problems(notebook, root)))

    def test_nonexistent_source_anchor_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            requirement = payload["metadata"]["llm_research_lab"]["practice"]["requirements"][0]
            requirement["source_locations"][0]["anchor"] = "원문에 없는 문장"
            self.save(notebook, payload)
            self.assertIn("SOURCE_ANCHOR", self.codes(self.problems(notebook, root)))

    def test_creation_ready_rejects_resolved_target_but_learner_state_accepts_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            source = "".join(payload["cells"][3]["source"]).replace(
                'raise NotImplementedError("shape를 채우세요")',
                "shape = tuple(tensor.shape)",
            ).replace("    # TODO: 배열의 shape를 tuple로 읽으세요\n", "")
            payload["cells"][3]["source"] = source.splitlines(keepends=True)
            payload["cells"][3]["execution_count"] = 4
            payload["cells"][3]["outputs"] = [{"output_type": "stream", "name": "stdout", "text": ["worked\n"]}]
            self.save(notebook, payload)
            self.assertIn("PREFILLED_CORE", self.codes(self.problems(notebook, root)))
            self.assertIn("EXECUTED", self.codes(self.problems(notebook, root)))
            self.assertEqual(self.problems(notebook, root, learner_state=True), [])

    def test_schema_v1_has_explicit_migration_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            payload["metadata"]["llm_research_lab"]["practice"]["schema_version"] = 1
            self.save(notebook, payload)
            self.assertEqual(self.codes(self.problems(notebook, root)), {"SCHEMA_MIGRATION"})

    def test_practice_given_learner_target_needs_direct_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            requirement = payload["metadata"]["llm_research_lab"]["practice"]["requirements"][2]
            requirement["owner"] = "learner"
            requirement["target_ids"] = ["T-E01-01"]
            self.save(notebook, payload)
            self.assertIn("TARGET_OWNERSHIP", self.codes(self.problems(notebook, root)))

    def test_requirement_and_target_links_must_be_reciprocal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            target = payload["metadata"]["llm_research_lab"]["practice"]["learner_targets"][0]
            target["requirement_ids"] = ["C-E01-01"]
            self.save(notebook, payload)
            self.assertIn("TARGET_OWNERSHIP", self.codes(self.problems(notebook, root)))

    def test_more_than_three_targets_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            profile = payload["metadata"]["llm_research_lab"]["practice"]["exercises"][0]
            profile["learner_target_ids"] = [f"T-E01-{index:02d}" for index in range(1, 5)]
            self.save(notebook, payload)
            self.assertIn("TARGET_SCOPE", self.codes(self.problems(notebook, root)))

    def test_callable_free_design_target_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            payload["cells"][3]["source"] = [
                "scenario = {'shape': (2, 3)}\n",
                "# TODO: 관찰한 shape의 의미를 한 문장으로 적으세요\n",
                'response = "작성 전"\n',
            ]
            target = payload["metadata"]["llm_research_lab"]["practice"]["learner_targets"][0]
            target["kind"] = "interpretation"
            target["marker"] = "# TODO: 관찰한 shape의 의미를 한 문장으로 적으세요"
            target["placeholder"] = 'response = "작성 전"'
            target.pop("symbol")
            self.save(notebook, payload)
            self.assertEqual(self.problems(notebook, root), [])

    def test_reflection_only_requirement_needs_no_fake_assertion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            practice = payload["metadata"]["llm_research_lab"]["practice"]
            claim = "관찰한 shape가 sample 축과 feature 축을 어떻게 구분하는지 한 문장으로 설명해야 합니다."
            marker = "관찰한 shape에서 두 축의 역할을 설명하세요."
            placeholder = "**작성:** 아직 작성하지 않음"
            payload["cells"][2]["source"].append(f"\n- {claim}\n")
            payload["cells"][6]["source"].extend([f"\n{marker}\n", f"\n{placeholder}\n"])
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
            self.save(notebook, payload)
            self.assertEqual(self.problems(notebook, root), [])

            practice["learner_targets"][-1]["kind"] = "code"
            self.save(notebook, payload)
            self.assertIn("CHECK_TRACE", self.codes(self.problems(notebook, root)))

    def test_untracked_mandatory_reflection_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            reflection = "".join(payload["cells"][6]["source"]).replace(
                "선택 복습입니다. 원한다면 관찰한 shape와 scalar의 빈 shape가 무엇을 뜻하는지 메모해도 좋습니다. 이 메모는 실습 완료 조건이 아닙니다.",
                "관찰한 shape와 scalar의 빈 shape가 무엇을 뜻하는지 반드시 적으세요.",
            )
            payload["cells"][6]["source"] = reflection.splitlines(keepends=True)
            self.save(notebook, payload)
            self.assertIn("TARGET_TRACE", self.codes(self.problems(notebook, root)))

    def test_internal_authoring_tokens_fail_learner_surface(self) -> None:
        leaks = [
            "C-E01-01",
            "T-E01-01",
            "Contract ID",
            "Learner Target",
            "source-given",
            "practice-given",
            "guided-fading",
            "## Practice Coverage Map",
            "# contract: C-E01-01",
            "# provided-fixture: E01",
            "# test-check: E01",
            "# setup-check: imports",
            "# TODO: E01",
            "### 실제 사용 맥락",
            "### 작은 유사 사례와 계약",
        ]
        for leak in leaks:
            with self.subTest(leak=leak), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                notebook = self.build_notebook(root)
                payload = self.load(notebook)
                payload["cells"][2]["source"].append(f"\n{leak}\n")
                self.save(notebook, payload)
                self.assertIn("LEARNER_SURFACE_LEAK", self.codes(self.problems(notebook, root)))

    def test_added_deleted_or_reordered_observable_fails_trace(self) -> None:
        def add_assertion(source: str) -> str:
            return source.replace(
                "    # 경계값\n",
                "    np.testing.assert_equal(1, 1)\n\n    # 경계값\n",
            )

        def delete_assertion(source: str) -> str:
            return source.replace('    np.testing.assert_equal(card["name"], "sample")\n', "")

        def reorder_assertions(source: str) -> str:
            first = '    np.testing.assert_equal(card["name"], "sample")\n'
            second = '    np.testing.assert_equal(card["shape"], (2, 3))\n'
            return source.replace(first + second, second + first)

        for mutate in (add_assertion, delete_assertion, reorder_assertions):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                notebook = self.build_notebook(root)
                payload = self.load(notebook)
                payload["cells"][5]["source"] = mutate("".join(payload["cells"][5]["source"])).splitlines(keepends=True)
                self.save(notebook, payload)
                self.assertIn("CHECK_TRACE", self.codes(self.problems(notebook, root)))

    def test_observable_must_map_to_one_atomic_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            observables = payload["cells"][5]["metadata"]["llm_research_lab"]["practice"]["observables"]
            observables[0]["requirement_ids"] = ["C-E01-01", "C-E01-02"]
            self.save(notebook, payload)
            self.assertIn("CHECK_TRACE", self.codes(self.problems(notebook, root)))

    def test_cell_role_order_hint_and_surface_errors_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            payload["cells"][2]["source"] = [
                line for line in payload["cells"][2]["source"] if "힌트 2" not in line
            ]
            payload["cells"][4], payload["cells"][5] = payload["cells"][5], payload["cells"][4]
            self.save(notebook, payload)
            codes = self.codes(self.problems(notebook, root))
            self.assertIn("HINT_ADJACENCY", codes)
            self.assertIn("EXERCISE_ORDER", codes)

    def test_source_hash_and_missing_metadata_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            payload["metadata"]["llm_research_lab"]["practice"]["sources"][0]["sha256"] = "0" * 64
            self.save(notebook, payload)
            self.assertIn("SOURCE_AUDIT", self.codes(self.problems(notebook, root)))

            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            payload["metadata"].pop("llm_research_lab")
            self.save(notebook, payload)
            self.assertIn("AUDIT_METADATA", self.codes(self.problems(notebook, root)))

    def test_broken_link_plain_assert_and_setup_machinery_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = self.load(notebook)
            payload["cells"][0]["source"].append("\n[broken](../../missing.md)\n")
            payload["cells"][1]["source"].append("import subprocess\n")
            payload["cells"][5]["source"].insert(2, "    assert True\n")
            self.save(notebook, payload)
            codes = self.codes(self.problems(notebook, root))
            self.assertIn("BROKEN_LINK", codes)
            self.assertIn("NOTEBOOK_SETUP", codes)
            self.assertIn("TEST_CONTRACT", codes)

    def test_new_bundle_is_rejected_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = root / "practice/dl/bundle"
            bundle.mkdir(parents=True)
            codes = self.codes(validate_artifact(bundle, repo_root=root, check_collection=False))
            self.assertEqual(codes, {"NOTEBOOK_ONLY"})

    def test_instructor_practice_metadata_still_requires_index_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            course = root / "materials/private/course"
            provided = course / "course-provided-practice/practice.md"
            provided.parent.mkdir(parents=True)
            lesson = course / "lesson.md"
            lesson.write_text("# Lesson\n\nTensor 이름을 인자로 받는다.\n", encoding="utf-8")
            provided.write_text("# Practice\n", encoding="utf-8")
            index = course / "INDEX.md"
            index.write_text(
                """# Course

## 강의 자료

| 파일 | 원본 |
| --- | --- |
| `lesson.md` | [원본](https://example.com) |

## 강의 제공 실습

| Practice path | Related lesson path | Variant | Format | Original |
| --- | --- | --- | --- | --- |
| `course-provided-practice/practice.md` | `missing.md` | single | Markdown | [원본](https://example.com) |
""",
                encoding="utf-8",
            )
            payload = self.load(notebook)
            practice = payload["metadata"]["llm_research_lab"]["practice"]
            practice["sources"] = [
                {"id": "S001", "kind": "course-index", "path": "materials/private/course/INDEX.md", "sha256": sha256(index)},
                {"id": "S002", "kind": "lesson", "path": "materials/private/course/lesson.md", "sha256": sha256(lesson)},
                {
                    "id": "S003",
                    "kind": "instructor-practice",
                    "path": "materials/private/course/course-provided-practice/practice.md",
                    "sha256": sha256(provided),
                    "related_lesson": "materials/private/course/lesson.md",
                    "variant": "single",
                },
            ]
            practice["requirements"][0]["source_locations"] = [
                {
                    "source_id": "S002",
                    "locator": "Lesson",
                    "anchor": "Tensor 이름을 인자로 받는다",
                }
            ]
            self.save(notebook, payload)
            self.assertIn("PRACTICE_MAPPING", self.codes(self.problems(notebook, root)))


if __name__ == "__main__":
    unittest.main()
