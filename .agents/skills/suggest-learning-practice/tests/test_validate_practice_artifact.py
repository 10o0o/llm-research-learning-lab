from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys


SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from validate_practice_artifact import validate as validate_artifact  # noqa: E402


def validate(*args, **kwargs):
    """Keep historical bundle-contract tests explicit about compatibility mode."""
    kwargs.setdefault("allow_legacy_bundle", True)
    return validate_artifact(*args, **kwargs)


def markdown_cell(text: str) -> dict[str, object]:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code_cell(text: str) -> dict[str, object]:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.splitlines(keepends=True)}


class PracticeArtifactValidatorTests(unittest.TestCase):
    def build_bundle(self, root: Path, *, prefilled: bool = False, global_hint: bool = False) -> Path:
        bundle = root / "practice/dl/tensor-contract"
        (bundle / "src/tensor_contract").mkdir(parents=True)
        (bundle / "tests").mkdir()
        til = root / "til/2026/08/2026-08-20.md"
        til.parent.mkdir(parents=True)
        til.write_text("# TIL\n", encoding="utf-8")
        source = root / "materials/lesson.md"
        source.parent.mkdir()
        source.write_text("# Source\n", encoding="utf-8")
        markdown = """# Tensor contract practice

- 기준 TIL: [2026-08-20](../../../til/2026/08/2026-08-20.md)
- 관련 강의자료: [lesson](../../../materials/lesson.md)

## Practice Coverage Map

| Outcome ID | TIL location | Practice action | Artifact/Exercise | Required evidence |
| --- | --- | --- | --- | --- |
| O01 | 오늘의 학습 > Tensor shape | implement | E01 | passing contracts and interpretation |
"""
        if global_hint:
            markdown += "\n## 점진적 힌트\n\n- 멀리 떨어진 힌트\n"
        exercise = """## E01. Tensor contract

### 실제 사용 맥락

Validate a batch boundary.

### 실행 전 회상·예측

Predict the output shape before running tests.

### 작은 유사 사례와 계약

For `(2, 3)`, return the two dimensions as metadata.

### 구현

Implement the public function in `src/`.

<details>
<summary>힌트 1: 관찰할 상태</summary>

Inspect `shape` before converting it.
</details>

<details>
<summary>힌트 2: 작은 trace</summary>

Trace `(2, 3)` one axis at a time.
</details>

### 테스트와 실패 진단

Run pytest and identify the first contract failure.

### 결과 해석

Explain which boundary the test protects.
"""
        notebook = {
            "cells": [
                markdown_cell(markdown),
                code_cell(
                    "# setup-check: repository-root import\n"
                    "import importlib\n"
                    "from pathlib import Path\n"
                    "import sys\n"
                    "bundle_src = Path('practice/dl/tensor-contract/src').resolve()\n"
                    "sys.path.insert(0, str(bundle_src))\n"
                    "import tensor_contract as practice_api\n"
                    "import tensor_contract.core as core_module\n"
                    "def refresh_core():\n"
                    "    importlib.reload(core_module)\n"
                    "    importlib.reload(practice_api)\n"
                    "def run_exercise_tests(exercise_id):\n"
                    "    return exercise_id\n"
                    "refresh_core()\n"
                ),
                markdown_cell(exercise),
                code_cell(
                    "# TODO: E01\n"
                    "# provided-fixture: E01\n"
                    "refresh_core()\n"
                    "fixture = None\n"
                    "observed = practice_api.describe(fixture)\n"
                ),
                code_cell(
                    "# test-check: E01\n"
                    "run_exercise_tests(\"E01\")\n"
                ),
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        (bundle / "workbook.ipynb").write_text(json.dumps(notebook), encoding="utf-8")
        implementation = "return tuple(value.shape)" if prefilled else "raise NotImplementedError('learner implementation')"
        (bundle / "src/tensor_contract/__init__.py").write_text(
            "from .core import describe\n\n__all__ = ['describe']\n",
            encoding="utf-8",
        )
        (bundle / "src/tensor_contract/core.py").write_text(
            f"def describe(value: object) -> tuple[int, ...]:\n    \"\"\"Return a shape contract.\"\"\"\n    {implementation}\n",
            encoding="utf-8",
        )
        (bundle / "tests/test_core.py").write_text(
            """from tensor_contract import describe


class TestE01:
    def test_normal_shape_contract(self):
        assert describe(None) is not None


    def test_edge_scalar_contract(self):
        assert describe(None) is not None


    def test_failure_invalid_input_contract(self):
        assert describe(None) is not None
""",
            encoding="utf-8",
        )
        return bundle

    def build_notebook(self, root: Path, *, prefilled: bool = False) -> Path:
        notebook_path = root / "practice/math/vector-contract.ipynb"
        notebook_path.parent.mkdir(parents=True)
        til = root / "til/2026/08/2026-08-20.md"
        til.parent.mkdir(parents=True)
        til.write_text("# TIL\n", encoding="utf-8")
        source = root / "materials/lesson.md"
        source.parent.mkdir()
        source.write_text("# Source\n", encoding="utf-8")
        overview = """# Vector contract practice

- 기준 TIL: [2026-08-20](../../til/2026/08/2026-08-20.md)
- 관련 강의자료: [lesson](../../materials/lesson.md)

## Practice Coverage Map

| Outcome ID | TIL location | Practice action | Artifact/Exercise | Required evidence |
| --- | --- | --- | --- | --- |
| O01 | 오늘의 학습 > vector contract | implement | E01 | passing contracts and interpretation |
"""
        exercise = """## E01. Vector contract

### 실제 사용 맥락

Validate one small vector boundary.

### 실행 전 회상·예측

Predict the result before running the fixture.

### 작은 유사 사례와 계약

| Contract ID | Kind | Learner-visible requirement |
| --- | --- | --- |
| C-E01-01 | practice-given | Return the provided value without changing its public type. |
| C-E01-02 | derive | Preserve the visible normal and edge fixtures. |
| C-E01-03 | practice-given | Reject the declared invalid input boundary. |

#### 학습자가 구현·판단할 것

Implement the transformation and explain the observed boundary.

### 구현

Implement the learner function below.

<details>
<summary>힌트 1: 관찰할 상태</summary>

Inspect the input first.
</details>

<details>
<summary>힌트 2: 작은 trace</summary>

Trace one value through the function.
</details>
"""
        implementation = "return value" if prefilled else "raise NotImplementedError('learner implementation')"
        payload = {
            "cells": [
                markdown_cell(overview),
                code_cell("# setup-check: notebook-only imports\nfrom pathlib import Path\n"),
                markdown_cell(exercise),
                code_cell(
                    "# TODO: E01\n"
                    "def describe(value: object) -> object:\n"
                    "    \"\"\"Return the observed value.\"\"\"\n"
                    f"    {implementation}\n"
                ),
                code_cell(
                    "# provided-fixture: E01\n"
                    "fixture = None\n"
                    "observed = describe(fixture)\n"
                ),
                markdown_cell(
                    "### 테스트와 실패 진단\n\n"
                    "Run the local normal, edge, and failure checks.\n"
                ),
                code_cell(
                    "# test-check: E01\n"
                    "def check_e01():\n"
                    "    # normal\n"
                    "    # contract: C-E01-01\n"
                    "    np.testing.assert_equal(True, True)\n"
                    "    # edge\n"
                    "    # contract: C-E01-02\n"
                    "    np.testing.assert_equal(True, True)\n"
                    "    # failure\n"
                    "    # contract: C-E01-03\n"
                    "    np.testing.assert_equal(True, True)\n"
                    "check_e01()\n"
                ),
                markdown_cell(
                    "### 결과 해석\n\n"
                    "Explain the result and the protected boundary.\n"
                ),
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        notebook_path.write_text(json.dumps(payload), encoding="utf-8")
        return notebook_path

    def codes(self, problems) -> set[str]:
        return {problem.code for problem in problems}

    def test_valid_bundle_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(validate(self.build_bundle(root), repo_root=root, check_collection=False), [])

    def test_new_bundle_is_rejected_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            codes = self.codes(
                validate_artifact(self.build_bundle(root), repo_root=root, check_collection=False)
            )
            self.assertEqual(codes, {"NOTEBOOK_ONLY"})

    def test_valid_notebook_only_artifact_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(
                validate(self.build_notebook(root), repo_root=root, check_collection=False),
                [],
            )

    def test_notebook_only_prefilled_core_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root, prefilled=True)
            self.assertIn(
                "PREFILLED_CORE",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_missing_fixture_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"].pop(4)
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "EXERCISE_FIXTURE",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_missing_setup_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"].pop(1)
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "IMPORT_SETUP",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_bundle_setup_helper_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][1]["source"].append("import subprocess\n")
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "NOTEBOOK_SETUP",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_missing_test_check_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"].pop(6)
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "EXERCISE_TEST",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_missing_check_call_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][6]["source"] = [
                line for line in payload["cells"][6]["source"] if line != "check_e01()\n"
            ]
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "EXERCISE_TEST",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_missing_contract_category_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][6]["source"] = [
                line for line in payload["cells"][6]["source"] if line != "    # edge\n"
            ]
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "TEST_CONTRACT",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_plain_assert_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][6]["source"] = [
                line.replace("np.testing.assert_equal(True, True)", "assert True")
                for line in payload["cells"][6]["source"]
            ]
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "TEST_CONTRACT",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_wrong_cell_order_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][4], payload["cells"][6] = payload["cells"][6], payload["cells"][4]
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "EXERCISE_ORDER",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_missing_contract_table_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][2]["source"] = [
                line
                for line in payload["cells"][2]["source"]
                if not line.startswith("| Contract ID")
            ]
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "CONTRACT_SPEC",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_invalid_or_cross_exercise_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][2]["source"] = [
                line.replace(
                    "| C-E01-02 | derive |",
                    "| C-E02-02 | hidden |",
                )
                for line in payload["cells"][2]["source"]
            ]
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "CONTRACT_SPEC",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_notebook_only_undeclared_and_unused_contracts_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][6]["source"] = [
                line.replace("C-E01-02", "C-E01-09")
                for line in payload["cells"][6]["source"]
            ]
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "CONTRACT_TRACE",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_hidden_fixed_requirements_without_contract_markers_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = self.build_notebook(root)
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][6]["source"] = code_cell(
                "# test-check: E01\n"
                "def check_e01():\n"
                "    # normal\n"
                "    np.testing.assert_equal(recommend_start(5_000), 'deep_learning_candidate')\n"
                "    np.testing.assert_equal(card()['dtype'], 'torch.float32')\n"
                "    np.testing.assert_equal(card()['device'], 'cpu')\n"
                "    np.testing.assert_equal(predict(0.5), 1)\n"
                "    # edge\n"
                "    np.testing.assert_allclose(grad_norm(), 2.0)\n"
                "    # failure\n"
                "    try:\n"
                "        select_checkpoint_epoch([])\n"
                "    except ValueError:\n"
                "        pass\n"
                "    else:\n"
                "        raise AssertionError('empty history must fail')\n"
                "check_e01()\n"
            )["source"]
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "CONTRACT_TRACE",
                self.codes(validate(notebook, repo_root=root, check_collection=False)),
            )

    def test_bundle_dynamic_global_rebinding_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            notebook = bundle / "workbook.ipynb"
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            payload["cells"][1]["source"].append("globals().update({})\n")
            notebook.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIn(
                "DYNAMIC_GLOBALS",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_prefilled_core_and_global_hints_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root, prefilled=True, global_hint=True)
            codes = self.codes(validate(bundle, repo_root=root, check_collection=False))
            self.assertIn("PREFILLED_CORE", codes)
            self.assertIn("GLOBAL_HINT", codes)

    def test_executed_cell_and_unmapped_outcome_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][-1]["execution_count"] = 1
            notebook["cells"][-1]["outputs"] = [{"output_type": "stream", "name": "stdout", "text": ["fake\n"]}]
            notebook["cells"][0]["source"] = [line.replace("| E01 |", "| E02 |") for line in notebook["cells"][0]["source"]]
            path.write_text(json.dumps(notebook), encoding="utf-8")
            codes = self.codes(validate(bundle, repo_root=root, check_collection=False))
            self.assertIn("EXECUTED", codes)
            self.assertIn("COVERAGE", codes)

    def test_missing_adjacent_hint_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][2]["source"] = [
                line.replace("<summary>힌트 1: 관찰할 상태</summary>", "<summary>참고</summary>")
                for line in notebook["cells"][2]["source"]
            ]
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "HINT_ADJACENCY",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_missing_exercise_fixture_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][3]["source"] = [
                line
                for line in notebook["cells"][3]["source"]
                if line != "# provided-fixture: E01\n"
            ]
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "EXERCISE_FIXTURE",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_missing_exercise_refresh_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][3]["source"] = [
                line for line in notebook["cells"][3]["source"] if line != "refresh_core()\n"
            ]
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "BUNDLE_REFRESH",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_missing_exercise_test_check_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"].pop(4)
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "EXERCISE_TEST",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_empty_explanation_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][2]["source"] = [
                line for line in notebook["cells"][2]["source"] if line != "Validate a batch boundary.\n"
            ]
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "EXERCISE",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_missing_or_broken_setup_import_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"].pop(1)
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "IMPORT_SETUP",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

            notebook["cells"].insert(
                1,
                code_cell(
                    "# setup-check: broken import\n"
                    "from package_that_does_not_exist import missing\n"
                ),
            )
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "IMPORT_SETUP",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_broken_course_practice_mapping_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            course = root / "materials/private/course"
            practice = course / "course-provided-practice"
            practice.mkdir(parents=True)
            (course / "lesson.md").write_text("# Lesson\n", encoding="utf-8")
            (practice / "practice.md").write_text("# Practice\n", encoding="utf-8")
            (course / "INDEX.md").write_text(
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
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][0]["source"].extend(
                [
                    "\n",
                    "- mapped lesson: [lesson](../../../materials/private/course/lesson.md)\n",
                    "- mapped practice: [practice](../../../materials/private/course/course-provided-practice/practice.md)\n",
                ]
            )
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "PRACTICE_MAPPING",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )


if __name__ == "__main__":
    unittest.main()
