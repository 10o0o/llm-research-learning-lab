from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pypdf import PdfWriter


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT = REPO_ROOT / ".agents/skills/coach-llm-research-study/scripts/validate_curriculum.py"
CURRICULUM = REPO_ROOT / "CURRICULUM.md"
PRIVATE_ROOT = REPO_ROOT / "materials/private"
KDL_INDEX = PRIVATE_ROOT / "kant-deep-learning-basics/INDEX.md"
STAT110_INDEX = PRIVATE_ROOT / "harvard-stat110-probability/INDEX.md"
PRIVATE_INDEXES = (
    PRIVATE_ROOT / "kant-basic-math/INDEX.md",
    PRIVATE_ROOT / "kant-advanced-machine-learning/INDEX.md",
    KDL_INDEX,
    STAT110_INDEX,
)

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
        missing = [path for path in PRIVATE_INDEXES if not path.is_file()]
        if missing:
            self.skipTest("private course indexes are not available in this checkout")
        self.assertEqual(
            [],
            validator.validate_curriculum(CURRICULUM, strict_sources=True),
        )

    def test_repository_deep_learning_course_passes_scoped_validation(self) -> None:
        if not KDL_INDEX.is_file():
            self.skipTest("private KDL course index is not available in this checkout")
        self.assertEqual(
            [],
            validator.validate_curriculum(
                CURRICULUM,
                strict_sources=True,
                course_index=KDL_INDEX,
            ),
        )

    def test_repository_stat110_course_passes_scoped_validation(self) -> None:
        if not STAT110_INDEX.is_file():
            self.skipTest("private Stat110 course index is not available in this checkout")
        self.assertEqual(
            [],
            validator.validate_curriculum(
                CURRICULUM,
                strict_sources=True,
                course_index=STAT110_INDEX,
            ),
        )

    def test_course_freshness_detects_source_and_index_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example-deep-learning"
            course.mkdir(parents=True)
            source = course / "06-01_lesson.md"
            source.write_text("# Lesson\n", encoding="utf-8")
            digest = validator.sha256_file(source)
            index = course / "INDEX.md"
            index.write_text(
                "# Index\n\n- source_namespace: EXAMPLE-DL\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `06-01_lesson.md` | fixture |\n",
                encoding="utf-8",
            )
            curriculum = root / "CURRICULUM.md"
            curriculum.write_text(
                "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                f"| SRC-EXAMPLE-DL-06-01 | `materials/private/example-deep-learning/06-01_lesson.md` | HTML 토글 펼침 Markdown | `{digest}` | complete | complete | 2026-08-25 | fixture |\n",
                encoding="utf-8",
            )
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

    def test_course_scope_registry_validates_identity_source_and_pdf_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example-probability"
            course.mkdir(parents=True)
            source = course / "00-01_probability.pdf"
            writer = PdfWriter()
            for _ in range(3):
                writer.add_blank_page(width=612, height=792)
            with source.open("wb") as handle:
                writer.write(handle)
            digest = validator.sha256_file(source)
            index = course / "INDEX.md"
            valid_scope_row = (
                "| SCOPE-EXAMPLE-PROB-00-01-01 | SRC-EXAMPLE-PROB-00-01 | First concept | "
                "Definition unit [materials/private/example-probability/00-01_probability.pdf#page-2: selected definition] | "
                "Previous unit [materials/private/example-probability/00-01_probability.pdf#page-1]; "
                "Following unit [materials/private/example-probability/00-01_probability.pdf#page-3] | focused fixture |"
            )
            index.write_text(
                "# Index\n\n- source_namespace: EXAMPLE-PROB\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-01_probability.pdf` | fixture |\n\n"
                "## 학습 범위\n\n"
                "| Scope ID | Source ID | Title | Included units | Boundary units | Note |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                + valid_scope_row
                + "\n",
                encoding="utf-8",
            )
            curriculum = root / "CURRICULUM.md"
            curriculum.write_text(
                "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                f"| SRC-EXAMPLE-PROB-00-01 | `materials/private/example-probability/00-01_probability.pdf` | PDF | `{digest}` | complete | complete | 2026-08-28 | fixture |\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [],
                validator.validate_course_index_freshness(
                    curriculum, index, repo_root=root
                ),
            )

            index.write_text(index.read_text(encoding="utf-8") + valid_scope_row + "\n", encoding="utf-8")
            self.assertIn(
                "INDEX_SCOPE_DUPLICATE",
                self.codes(
                    validator.validate_course_index_freshness(
                        curriculum, index, repo_root=root
                    )
                ),
            )
            index.write_text(
                index.read_text(encoding="utf-8").replace("#page-2: selected definition", "#page-9: selected definition"),
                encoding="utf-8",
            )
            self.assertIn(
                "INDEX_SCOPE_LOCATION",
                self.codes(
                    validator.validate_course_index_freshness(
                        curriculum, index, repo_root=root
                    )
                ),
            )
            index.write_text(
                index.read_text(encoding="utf-8")
                .replace(valid_scope_row + "\n" + valid_scope_row, valid_scope_row)
                .replace("#page-9: selected definition", "#page-2: selected definition")
                .replace("SRC-EXAMPLE-PROB-00-01", "SRC-EXAMPLE-PROB-99-99"),
                encoding="utf-8",
            )
            self.assertIn(
                "INDEX_SCOPE_SOURCE",
                self.codes(
                    validator.validate_course_index_freshness(
                        curriculum, index, repo_root=root
                    )
                ),
            )

    def test_unrelated_scope_drift_is_a_lesson_warning_but_strict_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/two-source-course"
            course.mkdir(parents=True)
            paths = []
            digests = []
            for lesson in ("00-01", "00-02"):
                source = course / f"{lesson}_lesson.pdf"
                writer = PdfWriter()
                writer.add_blank_page(width=612, height=792)
                with source.open("wb") as handle:
                    writer.write(handle)
                paths.append(source.relative_to(root).as_posix())
                digests.append(validator.sha256_file(source))

            index = course / "INDEX.md"
            index.write_text(
                "# Index\n\n- source_namespace: TWO\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-01_lesson.pdf` | selected |\n"
                "| `00-02_lesson.pdf` | unrelated |\n\n"
                "## 학습 범위\n\n"
                "| Scope ID | Source ID | Title | Included units | Boundary units | Note |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                f"| SCOPE-TWO-00-01-01 | SRC-TWO-00-01 | Selected | Selected unit [{paths[0]}#page-1] | none | valid selected scope |\n"
                f"| SCOPE-TWO-00-02-01 | SRC-TWO-00-02 | Unrelated | Unrelated unit [{paths[1]}#page-9] | none | stale unrelated scope |\n",
                encoding="utf-8",
            )
            curriculum = root / "CURRICULUM.md"
            curriculum.write_text(
                "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                f"| SRC-TWO-00-01 | `{paths[0]}` | PDF | `{digests[0]}` | complete | complete | 2026-08-28 | selected |\n"
                f"| SRC-TWO-00-02 | `{paths[1]}` | PDF | `{digests[1]}` | complete | complete | 2026-08-28 | unrelated |\n",
                encoding="utf-8",
            )

            strict = validator.validate_course_index_freshness(
                curriculum,
                index,
                repo_root=root,
            )
            self.assertIn("INDEX_SCOPE_LOCATION", self.codes(strict))
            lesson = validator.validate_lesson_slice_freshness(
                curriculum,
                index,
                {paths[0]},
                repo_root=root,
            )
            self.assertEqual([], lesson.errors)
            self.assertIn("INDEX_SCOPE_LOCATION", self.codes(lesson.warnings))

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
            "context:SRC-KAM-02-01,SRC-KAM-05-01 | 없음 | 별도 자료 확보 | resampling",
            "context:SRC-KAM-02-01,SRC-KAM-05-01 | 충분 | 그대로 사용 | resampling",
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

    def test_registry_accepts_a_data_driven_source_catalog(self) -> None:
        source = validator.Source(
            identifier="SRC-HARV-STAT110-2E-00-01",
            line=1,
            relative_path=(
                "materials/private/harvard-stat110-probability/"
                "00-01_introduction_to_probability_2e.pdf"
            ),
            material_format="PDF",
            digest="0" * 64,
            integrity="complete",
            audit_status="complete",
            audit_date="2026-08-27",
            note="fixture",
        )
        findings: list = []
        validator._validate_sources([source], "CURRICULUM.md", findings)
        self.assertEqual([], findings)

    def test_source_id_requires_an_uppercase_namespace_and_numeric_suffix(self) -> None:
        changed = self.valid_text.replace("| SRC-KDL-05-04 |", "| SRC-kdl-05-04 |", 1)
        self.assertIn("SOURCE_ID", self.codes(self.validate_text(changed)))

    def test_source_filename_must_match_source_id_suffix(self) -> None:
        changed = self.valid_text.replace(
            "materials/private/kant-deep-learning-basics/05-04_파라미터_업데이트_코드_흐름.md",
            "materials/private/kant-deep-learning-basics/05-03_파라미터_업데이트_코드_흐름.md",
            1,
        )
        self.assertIn("SOURCE_PATH_ID_MISMATCH", self.codes(self.validate_text(changed)))

    def test_strict_mode_discovers_an_unregistered_course_index(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/new-course"
            course.mkdir(parents=True)
            (course / "00-01_lesson.md").write_text("# Lesson\n", encoding="utf-8")
            (course / "INDEX.md").write_text(
                "# Index\n\n- source_namespace: NEW-COURSE\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-01_lesson.md` | fixture |\n",
                encoding="utf-8",
            )
            findings = []
            validator._strict_source_checks([], root, findings)
            self.assertIn("INDEX_NOT_REGISTERED", self.codes(findings))

    def test_strict_mode_detects_both_registry_index_parity_directions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example-course"
            course.mkdir(parents=True)
            registered = course / "00-01_registered.md"
            indexed = course / "00-02_indexed.md"
            registered.write_text("# Registered\n", encoding="utf-8")
            indexed.write_text("# Indexed\n", encoding="utf-8")
            (course / "INDEX.md").write_text(
                "# Index\n\n- source_namespace: EXAMPLE\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-02_indexed.md` | fixture |\n",
                encoding="utf-8",
            )
            sources = [
                validator.Source(
                    identifier="SRC-EXAMPLE-00-01",
                    line=1,
                    relative_path="materials/private/example-course/00-01_registered.md",
                    material_format="HTML 토글 펼침 Markdown",
                    digest=validator.sha256_file(registered),
                    integrity="complete",
                    audit_status="complete",
                    audit_date="2026-08-27",
                    note="fixture",
                )
            ]
            findings = []
            validator._strict_source_checks(sources, root, findings)
            self.assertIn("INDEX_NOT_REGISTERED", self.codes(findings))
            self.assertIn("REGISTRY_NOT_INDEXED", self.codes(findings))

    def test_lesson_slice_blocks_selected_drift_and_warns_on_unrelated_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example-course"
            course.mkdir(parents=True)
            selected = course / "00-01_selected.md"
            unrelated = course / "00-02_unrelated.md"
            selected.write_text("# Selected\n", encoding="utf-8")
            unrelated.write_text("# Unrelated\n", encoding="utf-8")
            selected_digest = validator.sha256_file(selected)
            index = course / "INDEX.md"
            index.write_text(
                "# Index\n\n- source_namespace: EXAMPLE\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-01_selected.md` | selected |\n"
                "| `00-02_unrelated.md` | unrelated |\n",
                encoding="utf-8",
            )
            curriculum = root / "CURRICULUM.md"
            curriculum.write_text(
                "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                f"| SRC-EXAMPLE-00-01 | `materials/private/example-course/00-01_selected.md` | HTML 토글 펼침 Markdown | `{selected_digest}` | complete | complete | 2026-08-27 | selected |\n"
                f"| SRC-EXAMPLE-00-02 | `materials/private/example-course/00-02_unrelated.md` | HTML 토글 펼침 Markdown | `{'0' * 64}` | complete | complete | 2026-08-27 | unrelated |\n",
                encoding="utf-8",
            )

            slice_report = validator.validate_lesson_slice_freshness(
                curriculum,
                index,
                {"materials/private/example-course/00-01_selected.md"},
                repo_root=root,
            )
            self.assertEqual([], slice_report.errors)
            self.assertIn("SOURCE_HASH_STALE", self.codes(slice_report.warnings))
            self.assertIn(
                "SOURCE_HASH_STALE",
                self.codes(validator.validate_course_index_freshness(curriculum, index, repo_root=root)),
            )

            selected.write_text("# Selected changed\n", encoding="utf-8")
            selected_report = validator.validate_lesson_slice_freshness(
                curriculum,
                index,
                {"materials/private/example-course/00-01_selected.md"},
                repo_root=root,
            )
            self.assertIn("SOURCE_HASH_STALE", self.codes(selected_report.errors))

    def test_lesson_slice_requires_selected_source_registry_and_index_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example-course"
            course.mkdir(parents=True)
            selected = course / "00-01_selected.md"
            selected.write_text("# Selected\n", encoding="utf-8")
            index = course / "INDEX.md"
            index.write_text(
                "# Index\n\n- source_namespace: EXAMPLE\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-01_selected.md` | selected |\n",
                encoding="utf-8",
            )
            curriculum = root / "CURRICULUM.md"
            curriculum.write_text(
                "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n",
                encoding="utf-8",
            )
            report = validator.validate_lesson_slice_freshness(
                curriculum,
                index,
                {"materials/private/example-course/00-01_selected.md"},
                repo_root=root,
            )
            self.assertIn("LESSON_SLICE_REGISTRY", self.codes(report.errors))

    def test_lesson_slice_blocks_selected_index_duplicate_and_warns_unrelated_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example-course"
            course.mkdir(parents=True)
            selected = course / "00-01_selected.md"
            unrelated = course / "00-02_unrelated.md"
            selected.write_text("# Selected\n", encoding="utf-8")
            unrelated.write_text("# Unrelated\n", encoding="utf-8")
            index = course / "INDEX.md"
            index.write_text(
                "# Index\n\n- source_namespace: EXAMPLE\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-01_selected.md` | selected |\n"
                "| `00-01_selected.md` | selected duplicate |\n"
                "| `00-02_unrelated.md` | unrelated |\n"
                "| `00-02_unrelated.md` | unrelated duplicate |\n",
                encoding="utf-8",
            )
            curriculum = root / "CURRICULUM.md"
            curriculum.write_text(
                "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                f"| SRC-EXAMPLE-00-01 | `materials/private/example-course/00-01_selected.md` | HTML 토글 펼침 Markdown | `{validator.sha256_file(selected)}` | complete | complete | 2026-08-27 | selected |\n"
                f"| SRC-EXAMPLE-00-02 | `materials/private/example-course/00-02_unrelated.md` | HTML 토글 펼침 Markdown | `{validator.sha256_file(unrelated)}` | complete | complete | 2026-08-27 | unrelated |\n",
                encoding="utf-8",
            )

            report = validator.validate_lesson_slice_freshness(
                curriculum,
                index,
                {"materials/private/example-course/00-01_selected.md"},
                repo_root=root,
            )
            selected_path = "materials/private/example-course/00-01_selected.md"
            unrelated_path = "materials/private/example-course/00-02_unrelated.md"
            self.assertTrue(any(
                finding.code == "INDEX_DUPLICATE"
                and selected_path in finding.affected_source_paths
                and finding.line == 10
                for finding in report.errors
            ))
            self.assertTrue(any(
                finding.code == "INDEX_DUPLICATE"
                and unrelated_path in finding.affected_source_paths
                and finding.line == 12
                for finding in report.warnings
            ))
            course_findings = validator.validate_course_index_freshness(
                curriculum, index, repo_root=root,
            )
            self.assertEqual(
                2,
                sum(finding.code == "INDEX_DUPLICATE" for finding in course_findings),
            )

    def test_lesson_slice_blocks_selected_duplicate_source_id_in_either_row_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example-course"
            course.mkdir(parents=True)
            selected = course / "00-01_selected.md"
            other = course / "00-01_other.md"
            selected.write_text("# Selected\n", encoding="utf-8")
            other.write_text("# Other\n", encoding="utf-8")
            index = course / "INDEX.md"
            index.write_text(
                "# Index\n\n- source_namespace: EXAMPLE\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-01_selected.md` | selected |\n"
                "| `00-01_other.md` | other |\n",
                encoding="utf-8",
            )
            rows = {
                "selected": (
                    f"| SRC-EXAMPLE-00-01 | `materials/private/example-course/00-01_selected.md` | HTML 토글 펼침 Markdown | `{validator.sha256_file(selected)}` | complete | complete | 2026-08-27 | selected |\n"
                ),
                "other": (
                    f"| SRC-EXAMPLE-00-01 | `materials/private/example-course/00-01_other.md` | HTML 토글 펼침 Markdown | `{validator.sha256_file(other)}` | complete | complete | 2026-08-27 | other |\n"
                ),
            }
            for order in (("selected", "other"), ("other", "selected")):
                with self.subTest(order=order):
                    curriculum = root / "CURRICULUM.md"
                    curriculum.write_text(
                        "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                        "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                        + "".join(rows[name] for name in order),
                        encoding="utf-8",
                    )
                    report = validator.validate_lesson_slice_freshness(
                        curriculum,
                        index,
                        {"materials/private/example-course/00-01_selected.md"},
                        repo_root=root,
                    )
                    self.assertIn("SOURCE_DUPLICATE", self.codes(report.errors))

    def test_lesson_slice_classifies_duplicate_registry_paths_by_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example-course"
            course.mkdir(parents=True)
            selected = course / "00-01_selected.md"
            unrelated = course / "00-02_unrelated.md"
            selected.write_text("# Selected\n", encoding="utf-8")
            unrelated.write_text("# Unrelated\n", encoding="utf-8")
            index = course / "INDEX.md"
            index.write_text(
                "# Index\n\n- source_namespace: EXAMPLE\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-01_selected.md` | selected |\n"
                "| `00-02_unrelated.md` | unrelated |\n",
                encoding="utf-8",
            )
            selected_path = "materials/private/example-course/00-01_selected.md"
            unrelated_path = "materials/private/example-course/00-02_unrelated.md"
            digest = validator.sha256_file(selected)
            unrelated_digest = validator.sha256_file(unrelated)

            def report_for(duplicate_path: str, duplicate_digest: str):
                curriculum = root / "CURRICULUM.md"
                curriculum.write_text(
                    "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                    "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                    f"| SRC-EXAMPLE-00-01 | `{selected_path}` | HTML 토글 펼침 Markdown | `{digest}` | complete | complete | 2026-08-27 | selected |\n"
                    f"| SRC-EXAMPLE-00-02 | `{unrelated_path}` | HTML 토글 펼침 Markdown | `{unrelated_digest}` | complete | complete | 2026-08-27 | unrelated |\n"
                    f"| SRC-EXAMPLE-99-99 | `{duplicate_path}` | HTML 토글 펼침 Markdown | `{duplicate_digest}` | complete | complete | 2026-08-27 | duplicate |\n",
                    encoding="utf-8",
                )
                return validator.validate_lesson_slice_freshness(
                    curriculum,
                    index,
                    {selected_path},
                    repo_root=root,
                )

            selected_report = report_for(selected_path, digest)
            self.assertIn("SOURCE_PATH_DUPLICATE", self.codes(selected_report.errors))
            unrelated_report = report_for(unrelated_path, unrelated_digest)
            self.assertNotIn(
                "SOURCE_PATH_DUPLICATE", self.codes(unrelated_report.errors),
            )
            self.assertIn(
                "SOURCE_PATH_DUPLICATE", self.codes(unrelated_report.warnings),
            )

    def test_course_namespace_is_required_formatted_bound_and_unique(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)

            def add_course(directory: str, namespace_line: str, source_id: str, lesson: str):
                course = root / "materials/private" / directory
                course.mkdir(parents=True)
                source_path = course / lesson
                source_path.write_text("# Lesson\n", encoding="utf-8")
                (course / "INDEX.md").write_text(
                    f"# Index\n\n{namespace_line}\n\n## 강의 자료\n\n"
                    "| 파일 | 설명 |\n| --- | --- |\n"
                    f"| `{lesson}` | fixture |\n",
                    encoding="utf-8",
                )
                return validator.Source(
                    identifier=source_id,
                    line=1,
                    relative_path=f"materials/private/{directory}/{lesson}",
                    material_format="HTML 토글 펼침 Markdown",
                    digest=validator.sha256_file(source_path),
                    integrity="complete",
                    audit_status="complete",
                    audit_date="2026-08-27",
                    note="fixture",
                )

            missing = add_course("missing", "- description: none", "SRC-MISSING-00-01", "00-01_lesson.md")
            invalid = add_course("invalid", "- source_namespace: invalid", "SRC-INVALID-00-01", "00-01_lesson.md")
            duplicate = add_course(
                "duplicate",
                "- source_namespace: DUPLICATE\n- source_namespace: DUPLICATE",
                "SRC-DUPLICATE-00-01",
                "00-01_lesson.md",
            )
            mismatch = add_course("mismatch", "- source_namespace: EXPECTED", "SRC-OTHER-00-01", "00-01_lesson.md")
            first = add_course("first", "- source_namespace: SHARED", "SRC-SHARED-00-01", "00-01_lesson.md")
            second = add_course("second", "- source_namespace: SHARED", "SRC-SHARED-00-02", "00-02_lesson.md")
            findings: list = []
            validator._strict_source_checks(
                [missing, invalid, duplicate, mismatch, first, second], root, findings,
            )
            codes = self.codes(findings)
            self.assertEqual(
                2,
                sum(
                    finding.code == "INDEX_NAMESPACE_COUNT"
                    for finding in findings
                ),
            )
            self.assertIn("INDEX_NAMESPACE_FORMAT", codes)
            self.assertIn("SOURCE_NAMESPACE_MISMATCH", codes)
            self.assertIn("INDEX_NAMESPACE_COLLISION", codes)

            scoped_cases = {
                "duplicate": "INDEX_NAMESPACE_COUNT",
                "mismatch": "SOURCE_NAMESPACE_MISMATCH",
                "first": "INDEX_NAMESPACE_COLLISION",
            }
            all_sources = [missing, invalid, duplicate, mismatch, first, second]
            for directory, expected_code in scoped_cases.items():
                with self.subTest(scoped_directory=directory):
                    scoped_findings: list = []
                    validator._strict_source_checks(
                        all_sources,
                        root,
                        scoped_findings,
                        course_index=(
                            root / "materials/private" / directory / "INDEX.md"
                        ),
                    )
                    self.assertIn(expected_code, self.codes(scoped_findings))

    def test_registry_summary_detects_registry_and_private_count_drift(self) -> None:
        changed = self.valid_text.replace(
            "| 4 | 71 | 241 | 204 | 37 | 0 | 648 | 3 |",
            "| 4 | 72 | 241 | 204 | 37 | 0 | 648 | 3 |",
            1,
        )
        self.assertIn("REGISTRY_SUMMARY_MISMATCH", self.codes(self.validate_text(changed)))

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example"
            course.mkdir(parents=True)
            markdown = course / "00-01_lesson.md"
            asset = course / "asset.png"
            pdf = course / "00-02_lesson.pdf"
            markdown.write_text("# Lesson\n\n![asset](asset.png)\n", encoding="utf-8")
            asset.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            pdf.write_bytes(b"%PDF-1.4\n1 0 obj<</Type /Page>>endobj\n%%EOF\n")
            sources = [
                validator.Source(
                    "SRC-EXAMPLE-00-01", 1,
                    "materials/private/example/00-01_lesson.md",
                    "HTML 토글 펼침 Markdown", validator.sha256_file(markdown),
                    "complete", "complete", "2026-08-27", "fixture",
                ),
                validator.Source(
                    "SRC-EXAMPLE-00-02", 2,
                    "materials/private/example/00-02_lesson.pdf",
                    "PDF", validator.sha256_file(pdf),
                    "limited", "complete", "2026-08-27", "fixture",
                ),
            ]
            with mock.patch.object(validator, "_pdf_page_count", return_value=1):
                actual, unreadable = validator._private_registry_summary(sources, root)
            self.assertEqual([], unreadable)
            self.assertEqual(
                validator.RegistrySummary(1, 2, 1, 1, 0, 0, 1, 1),
                actual,
            )
            findings: list = []
            with mock.patch.object(validator, "_pdf_page_count", return_value=1):
                validator._validate_private_registry_summary(
                    validator.RegistrySummary(1, 2, 1, 1, 0, 0, 2, 1),
                    sources,
                    root,
                    "CURRICULUM.md",
                    findings,
                )
            self.assertIn("REGISTRY_SUMMARY_MISMATCH", self.codes(findings))
            asset.unlink()
            findings = []
            with mock.patch.object(validator, "_pdf_page_count", return_value=1):
                validator._validate_private_registry_summary(
                    validator.RegistrySummary(1, 2, 1, 1, 0, 0, 1, 1),
                    sources,
                    root,
                    "CURRICULUM.md",
                    findings,
                )
            self.assertIn("REGISTRY_SUMMARY_UNREADABLE", self.codes(findings))

            asset.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            findings = []
            with mock.patch.object(validator, "_pdf_page_count", return_value=None):
                validator._validate_private_registry_summary(
                    validator.RegistrySummary(1, 2, 1, 1, 0, 0, 1, 1),
                    sources,
                    root,
                    "CURRICULUM.md",
                    findings,
                )
            self.assertIn("REGISTRY_SUMMARY_UNREADABLE", self.codes(findings))

    def test_invalid_hash_shape_is_rejected(self) -> None:
        changed = self.valid_text.replace(
            "`dc64b1fc6531ba45489c570ca240386f69f23beb78074c2dfdfe17a18ab45787`",
            "`NOT-A-SHA256`",
            1,
        )
        self.assertIn("SOURCE_HASH", self.codes(self.validate_text(changed)))

    def test_strict_mode_detects_stale_source_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "materials/private/example-course"
            course.mkdir(parents=True)
            source = course / "00-01_lesson.md"
            source.write_text("# Lesson\n", encoding="utf-8")
            index = course / "INDEX.md"
            index.write_text(
                "# Index\n\n- source_namespace: EXAMPLE\n\n## 강의 자료\n\n"
                "| 파일 | 설명 |\n| --- | --- |\n"
                "| `00-01_lesson.md` | fixture |\n",
                encoding="utf-8",
            )
            curriculum = root / "CURRICULUM.md"
            curriculum.write_text(
                "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                f"| SRC-EXAMPLE-00-01 | `materials/private/example-course/00-01_lesson.md` | HTML 토글 펼침 Markdown | `{'f' * 64}` | complete | complete | 2026-08-27 | fixture |\n",
                encoding="utf-8",
            )
            with mock.patch.object(validator, "sha256_file", return_value="0" * 64):
                findings = validator.validate_course_index_freshness(
                    curriculum,
                    index,
                    repo_root=root,
                )
            self.assertIn("SOURCE_HASH_STALE", self.codes(findings))


if __name__ == "__main__":
    unittest.main()
