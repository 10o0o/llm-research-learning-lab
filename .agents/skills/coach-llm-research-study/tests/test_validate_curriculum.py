from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT = REPO_ROOT / ".agents/skills/coach-llm-research-study/scripts/validate_curriculum.py"
CURRICULUM = REPO_ROOT / "CURRICULUM.md"

SPEC = importlib.util.spec_from_file_location("curriculum_validator_under_test", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class CurriculumValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.valid_text = CURRICULUM.read_text(encoding="utf-8")

    def validate_text(self, text: str, *, repo_root: Path | None = None):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            path = temporary_root / "CURRICULUM.md"
            path.write_text(text, encoding="utf-8")
            return validator.validate_curriculum(
                path,
                repo_root=repo_root or REPO_ROOT,
            )

    @staticmethod
    def codes(findings) -> set[str]:
        return {finding.code for finding in findings}

    def test_repository_curriculum_passes_structural_validation(self) -> None:
        self.assertEqual([], validator.validate_curriculum(CURRICULUM))

    def test_repository_curriculum_passes_strict_source_validation(self) -> None:
        self.assertEqual(
            [],
            validator.validate_curriculum(CURRICULUM, strict_sources=True),
        )

    def test_repository_deep_learning_course_passes_scoped_validation(self) -> None:
        self.assertEqual(
            [],
            validator.validate_curriculum(
                CURRICULUM,
                strict_sources=True,
                course_index=REPO_ROOT / "materials/private/kant-deep-learning-basics/INDEX.md",
            ),
        )

    def test_course_freshness_detects_source_and_index_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/kant-deep-learning-basics"
            course.mkdir(parents=True)
            source = course / "06-01_lesson.md"
            source.write_text("# Lesson\n", encoding="utf-8")
            digest = validator.sha256_file(source)
            index = course / "INDEX.md"
            index.write_text(
                "# Index\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `06-01_lesson.md` | fixture |\n",
                encoding="utf-8",
            )
            curriculum = root / "CURRICULUM.md"
            curriculum.write_text(
                "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                f"| SRC-KDL-06-01 | `materials/private/kant-deep-learning-basics/06-01_lesson.md` | HTML 토글 펼침 Markdown | `{digest}` | complete | complete | 2026-08-25 | fixture |\n",
                encoding="utf-8",
            )
            configured = {
                "KDL": ("kant-deep-learning-basics", ("06-01",)),
            }
            with mock.patch.dict(validator.COURSES, configured, clear=True):
                self.assertEqual(
                    [],
                    validator.validate_course_index_freshness(
                        curriculum,
                        index,
                        repo_root=root,
                    ),
                )
                source.write_text("# Changed lesson\n", encoding="utf-8")
                findings = validator.validate_course_index_freshness(
                    curriculum,
                    index,
                    repo_root=root,
                )
            self.assertIn("SOURCE_HASH_STALE", self.codes(findings))

    def test_structural_mode_does_not_require_private_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            clone_root = Path(temporary_directory)
            clone_curriculum = clone_root / "CURRICULUM.md"
            clone_curriculum.write_text(self.valid_text, encoding="utf-8")
            self.assertEqual(
                [],
                validator.validate_curriculum(
                    clone_curriculum,
                    strict_sources=False,
                    repo_root=clone_root,
                ),
            )

    def test_duplicate_competency_id_is_rejected(self) -> None:
        changed = self.valid_text.replace(
            "| CC-MATH-02 | rank·최소제곱",
            "| CC-MATH-01 | rank·최소제곱",
            1,
        )
        findings = self.validate_text(changed)
        self.assertIn("COMPETENCY_DUPLICATE", self.codes(findings))
        self.assertIn("COMPETENCY_MISSING", self.codes(findings))

    def test_unknown_evidence_token_is_rejected(self) -> None:
        changed = self.valid_text.replace(
            "| explain, calculate, shape, implement |",
            "| explain, hallucinate, shape, implement |",
            1,
        )
        self.assertIn("EVIDENCE_ENUM", self.codes(self.validate_text(changed)))

    def test_missing_prerequisite_is_rejected(self) -> None:
        changed = self.valid_text.replace(
            "| CC-MATH-03 | 미분·chain rule·gradient·autodiff를 손계산, 계산 그래프, 코드의 gradient 흐름으로 연결한다. | D2 | CC-MATH-01 |",
            "| CC-MATH-03 | 미분·chain rule·gradient·autodiff를 손계산, 계산 그래프, 코드의 gradient 흐름으로 연결한다. | D2 | CC-MATH-99 |",
            1,
        )
        self.assertIn("PREREQUISITE_MISSING", self.codes(self.validate_text(changed)))

    def test_prerequisite_cycle_is_rejected(self) -> None:
        changed = self.valid_text.replace(
            "| CC-MATH-01 | 벡터·행렬·선형변환을 기하와 좌표, 행렬곱 shape, 작은 NumPy 구현으로 연결한다. | D2 | — |",
            "| CC-MATH-01 | 벡터·행렬·선형변환을 기하와 좌표, 행렬곱 shape, 작은 NumPy 구현으로 연결한다. | D2 | CC-MATH-02 |",
            1,
        )
        self.assertIn("PREREQUISITE_CYCLE", self.codes(self.validate_text(changed)))

    def test_context_only_source_cannot_be_sufficient(self) -> None:
        changed = self.valid_text.replace(
            "context:SRC-KAM-02-01 | 없음 | 별도 자료 확보 | bootstrap sampling",
            "context:SRC-KAM-02-01 | 충분 | 그대로 사용 | bootstrap sampling",
            1,
        )
        self.assertIn(
            "SUFFICIENT_WITHOUT_DIRECT_SOURCE",
            self.codes(self.validate_text(changed)),
        )

    def test_partial_coverage_requires_gap_treatment(self) -> None:
        changed = self.valid_text.replace(
            "| 부분 | 수업 내 보충 | rank-deficient 최소제곱",
            "| 부분 | 그대로 사용 | rank-deficient 최소제곱",
            1,
        )
        self.assertIn("GAP_ACTION_REQUIRED", self.codes(self.validate_text(changed)))

    def test_progress_field_is_rejected(self) -> None:
        changed = self.valid_text + "\n| 항목 | 점수 |\n|---|---|\n| 예시 | 1 |\n"
        self.assertIn("PROGRESS_FIELD", self.codes(self.validate_text(changed)))

    def test_registry_requires_all_expected_sources(self) -> None:
        changed = self.valid_text.replace(
            next(
                line + "\n"
                for line in self.valid_text.splitlines()
                if line.startswith("| SRC-KDL-05-04 |")
            ),
            "",
            1,
        )
        codes = self.codes(self.validate_text(changed))
        self.assertIn("SOURCE_COUNT", codes)
        self.assertIn("SOURCE_MISSING", codes)

    def test_source_count_uses_current_expected_catalog_length(self) -> None:
        changed = self.valid_text.replace(
            next(
                line + "\n"
                for line in self.valid_text.splitlines()
                if line.startswith("| SRC-KDL-05-04 |")
            ),
            "",
            1,
        )
        findings = self.validate_text(changed)
        source_count = next(
            finding for finding in findings if finding.code == "SOURCE_COUNT"
        )
        self.assertIn(
            f"expected {len(validator.EXPECTED_SOURCE_IDS)}",
            source_count.message,
        )

    def test_invalid_hash_shape_is_rejected(self) -> None:
        changed = self.valid_text.replace(
            "`dc64b1fc6531ba45489c570ca240386f69f23beb78074c2dfdfe17a18ab45787`",
            "`NOT-A-SHA256`",
            1,
        )
        self.assertIn("SOURCE_HASH", self.codes(self.validate_text(changed)))

    def test_strict_mode_detects_stale_source_hash(self) -> None:
        with mock.patch.object(validator, "sha256_file", return_value="0" * 64):
            findings = validator.validate_curriculum(
                CURRICULUM,
                strict_sources=True,
            )
        self.assertIn("SOURCE_HASH_STALE", self.codes(findings))


if __name__ == "__main__":
    unittest.main()
