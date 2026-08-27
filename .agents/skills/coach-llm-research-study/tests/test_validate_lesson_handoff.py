from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from handoff_fixture import CONTRACT, build_handoff, draft_envelope, sha256  # noqa: E402
import validate_lesson_handoff as handoff_validator  # noqa: E402
from validate_lesson_handoff import (  # noqa: E402
    ValidationReport,
    ValidationWarning,
    _comma_ids,
    _location_exists,
    validate_handoff,
)


class LessonHandoffValidatorTests(unittest.TestCase):
    def make_root(self) -> tempfile.TemporaryDirectory[str]:
        return tempfile.TemporaryDirectory()

    def assert_code(self, report, code: str) -> None:
        self.assertIn(code, {error.code for error in report.errors}, report.errors)

    def build_til_ready_handoff(self, root: Path) -> Path:
        content = "배치 축과 특성 축을 구분해 결과 shape를 설명했다."
        draft = root / "til/today.md"
        draft.parent.mkdir(parents=True, exist_ok=True)
        draft.write_text(
            "# 오늘의 학습\n\n"
            + draft_envelope("tensor-shape-lesson", "E001", content)
            + "\n\n## 남은 질문\n\nBroadcasting에서 오른쪽 축부터 비교하는 이유는 무엇인가?\n",
            encoding="utf-8",
        )
        handoff, _ = build_handoff(
            root,
            status="paused",
            reviews=[("pass", "fresh-reviewer")],
            evidence=[{"concept": "C01", "content": content, "append_state": "drafted"}],
            coverage=[
                {
                    "concept": "C01",
                    "state": "confirmed",
                    "evidence_ids": "E001",
                    "representation": "learning",
                    "note": "Learner explanation is present in the draft.",
                },
                {
                    "concept": "C02",
                    "state": "uncertain",
                    "evidence_ids": "none",
                    "representation": "remaining-question",
                    "note": "draft-anchor: Broadcasting에서 오른쪽 축부터 비교하는 이유는 무엇인가?",
                },
                {
                    "concept": "C03",
                    "state": "deferred",
                    "evidence_ids": "none",
                    "representation": "not-required",
                    "note": "Not taught today.",
                },
            ],
            pre_save_verdict="저장 가능",
            reviewed_at="2026-08-20T02:00:00Z",
            reviewed_draft_sha256=sha256(draft.read_bytes()),
            delivery=[
                {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis meaning was taught."},
                {"objective": "O002", "state": "delivered", "mode": "full", "note": "Broadcasting was taught."},
                {"objective": "O003", "state": "pending", "mode": "none", "note": "Not taught today."},
            ],
        )
        return handoff

    def test_preparing_handoff_is_structurally_valid_but_not_ready(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)
            ready = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertFalse(ready.ok)
            self.assert_code(ready, "REVIEW_NOT_PASS")

    def test_active_pass_with_current_hashes_is_ready(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "fresh-reviewer")])
            report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertTrue(report.ok, report.errors)

    def test_til_ready_accepts_complete_learning_and_uncertainty_inventory(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assertTrue(report.ok, report.errors)

    def test_confirmed_concept_requires_evidence_for_every_delivered_objective(self) -> None:
        contract = CONTRACT.replace(
            "| C02 | full | Compare aligned dimensions from the right. | none |",
            "| C01 | full | Compare aligned dimensions from the right. | none |",
        ).replace(
            "| O003 | optional-added | supplement | CURRICULUM.md#CC-DL-01 | Connect tensor axes to batch, token, and hidden axes. | C03 | full | Map one small tensor to an attention input. | none |",
            "| O003 | optional-added | supplement | CURRICULUM.md#CC-DL-01 | Connect tensor axes to batch, token, and hidden axes. | C03 | full | Map one small tensor to an attention input. | none |\n"
            "| O004 | source-core | none | materials/lesson.md#shape-propagation | Distinguish aligned and expanded axes. | C02 | full | Label each aligned axis before broadcasting. | none |",
        ).replace(
            "| source-only | O001, O002 |",
            "| source-only | O001, O002, O004 |",
        ).replace(
            "| I001 | D001, D002, D003 | O001, O002 |",
            "| I001 | D001, D002, D003 | O001, O002, O004 |",
        ).replace(
            "- objective_ids: O001\n- delivery_outline:",
            "- objective_ids: O001, O002\n- delivery_outline:",
        ).replace(
            "- objective_ids: O002\n- delivery_outline:",
            "- objective_ids: O004\n- delivery_outline:",
        )
        delivery = [
            {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis meaning was taught."},
            {"objective": "O002", "state": "delivered", "mode": "full", "note": "Broadcasting was taught."},
            {"objective": "O003", "state": "pending", "mode": "none", "note": "Not taught today."},
            {"objective": "O004", "state": "pending", "mode": "none", "note": "Not taught today."},
        ]
        coverage = [
            {"concept": "C01", "state": "confirmed", "evidence_ids": "E001", "representation": "learning", "note": "One answer was captured."},
            {"concept": "C02", "state": "deferred", "evidence_ids": "none", "representation": "not-required", "note": "No objective was taught."},
            {"concept": "C03", "state": "deferred", "evidence_ids": "none", "representation": "not-required", "note": "Not taught today."},
        ]
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                contract=contract,
                status="paused",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"concept": "C01", "objective_ids": "O001"}],
                coverage=coverage,
                delivery=delivery,
            )
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "TIL_COVERAGE")
            self.assertTrue(any("missing O002" in error.message for error in report.errors))

    def test_til_ready_accepts_objective_complete_concept_evidence(self) -> None:
        contract = CONTRACT.replace(
            "| C02 | full | Compare aligned dimensions from the right. | none |",
            "| C01 | full | Compare aligned dimensions from the right. | none |",
        ).replace(
            "| O003 | optional-added | supplement | CURRICULUM.md#CC-DL-01 | Connect tensor axes to batch, token, and hidden axes. | C03 | full | Map one small tensor to an attention input. | none |",
            "| O003 | optional-added | supplement | CURRICULUM.md#CC-DL-01 | Connect tensor axes to batch, token, and hidden axes. | C03 | full | Map one small tensor to an attention input. | none |\n"
            "| O004 | source-core | none | materials/lesson.md#shape-propagation | Distinguish aligned and expanded axes. | C02 | full | Label each aligned axis before broadcasting. | none |",
        ).replace(
            "| source-only | O001, O002 |",
            "| source-only | O001, O002, O004 |",
        ).replace(
            "| I001 | D001, D002, D003 | O001, O002 |",
            "| I001 | D001, D002, D003 | O001, O002, O004 |",
        ).replace(
            "- objective_ids: O001\n- delivery_outline:",
            "- objective_ids: O001, O002\n- delivery_outline:",
        ).replace(
            "- objective_ids: O002\n- delivery_outline:",
            "- objective_ids: O004\n- delivery_outline:",
        )
        first = "배치 축과 특성 축을 구분했다."
        second = "브로드캐스팅 결과 shape를 오른쪽 축부터 설명했다."
        with self.make_root() as directory:
            root = Path(directory)
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            draft.write_text(
                "# 오늘의 학습\n\n"
                + draft_envelope("tensor-shape-lesson", "E001", first)
                + "\n"
                + draft_envelope("tensor-shape-lesson", "E002", second),
                encoding="utf-8",
            )
            handoff, _ = build_handoff(
                root,
                contract=contract,
                status="paused",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[
                    {"concept": "C01", "objective_ids": "O001", "content": first, "append_state": "drafted"},
                    {"concept": "C01", "objective_ids": "O002", "content": second, "append_state": "drafted"},
                ],
                coverage=[
                    {"concept": "C01", "state": "confirmed", "evidence_ids": "E001, E002", "representation": "learning", "note": "Both delivered objectives are demonstrated."},
                    {"concept": "C02", "state": "deferred", "evidence_ids": "none", "representation": "not-required", "note": "No objective was taught."},
                    {"concept": "C03", "state": "deferred", "evidence_ids": "none", "representation": "not-required", "note": "Not taught today."},
                ],
                pre_save_verdict="저장 가능",
                reviewed_at="2026-08-20T02:00:00Z",
                reviewed_draft_sha256=sha256(draft.read_bytes()),
                delivery=[
                    {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis meaning was taught."},
                    {"objective": "O002", "state": "delivered", "mode": "full", "note": "Broadcasting was taught."},
                    {"objective": "O003", "state": "pending", "mode": "none", "note": "Not taught today."},
                    {"objective": "O004", "state": "pending", "mode": "none", "note": "Not taught today."},
                ],
            )
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assertTrue(report.ok, report.errors)

    def test_til_ready_rejects_missing_confirmed_or_uncertain_concept(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| C01 | confirmed | E001 | learning |",
                "| C01 | confirmed | E001 | missing |",
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

            handoff = self.build_til_ready_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| C02 | uncertain | none | remaining-question |",
                "| C02 | uncertain | none | missing |",
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

    def test_til_ready_rejects_claimed_uncertainty_without_draft_question(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            draft = root / "til/today.md"
            draft.write_text(
                draft.read_text(encoding="utf-8").split("\n\n## 남은 질문", 1)[0] + "\n",
                encoding="utf-8",
            )
            handoff_text = handoff.read_text(encoding="utf-8")
            old_hash = re.search(r"- reviewed_draft_sha256: ([0-9a-f]{64})", handoff_text)
            self.assertIsNotNone(old_hash)
            handoff.write_text(
                handoff_text.replace(old_hash.group(1), sha256(draft.read_bytes()), 1),
                encoding="utf-8",
            )
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

    def test_til_ready_rejects_uncertain_anchor_missing_from_question(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "draft-anchor: Broadcasting에서 오른쪽 축부터 비교하는 이유는 무엇인가?",
                "draft-anchor: 초안에 없는 질문",
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

    def test_til_ready_ignores_deferred_source_content(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.document.learning_coverage["C03"].til_representation, "not-required")

    def test_til_ready_rejects_stale_draft_and_missing_contract_review(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            with (root / "til/today.md").open("a", encoding="utf-8") as stream:
                stream.write("\nchanged after review\n")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_REVIEW_STALE")

            handoff, _ = build_handoff(
                root,
                status="paused",
                pre_save_verdict="저장 가능",
                reviewed_at="2026-08-20T02:00:00Z",
                reviewed_draft_sha256=sha256((root / "til/today.md").read_bytes()),
            )
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "REVIEW_NOT_PASS")

    def test_til_ready_rejects_confirmed_evidence_not_yet_drafted(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "- append_state: drafted",
                "- append_state: pending",
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

    def test_ready_rejects_checkpoint_outside_contract(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="paused", reviews=[("pass", "fresh-reviewer")])
            text = handoff.read_text(encoding="utf-8").replace("- last_completed_step: none", "- last_completed_step: T999")
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertFalse(report.ok)
            self.assert_code(report, "SCHEMA")

    def test_contract_author_cannot_review_own_contract(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "contract-author")])
            report = validate_handoff(handoff, repo_root=root)
            self.assertFalse(report.ok)
            self.assert_code(report, "REVIEW_NOT_PASS")

    def test_second_attempt_requires_changes_and_a_new_reviewer(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("changes_required", "reviewer-one"), ("pass", "reviewer-two")],
            )
            self.assertTrue(validate_handoff(handoff, repo_root=root, ready=True).ok)
            text = handoff.read_text(encoding="utf-8").replace("reviewer-two", "reviewer-one")
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "REVIEW_NOT_PASS")

    def test_unavailable_or_second_nonpass_must_block_teaching(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="blocked", reviews=[("unavailable", "reviewer-one")])
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)
            self.assert_code(validate_handoff(handoff, repo_root=root, ready=True), "REVIEW_NOT_PASS")

            handoff, _ = build_handoff(
                root,
                status="blocked",
                reviews=[("changes_required", "reviewer-one"), ("changes_required", "reviewer-two")],
            )
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)
            self.assert_code(validate_handoff(handoff, repo_root=root, ready=True), "REVIEW_NOT_PASS")

    def test_source_mutation_and_contract_mutation_are_detected(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "fresh-reviewer")])
            (root / "materials/lesson.md").write_text("changed", encoding="utf-8")
            source_report = validate_handoff(handoff, repo_root=root)
            self.assert_code(source_report, "SOURCE_HASH")
            self.assert_code(source_report, "REVIEW_STALE")

            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "fresh-reviewer")], primary_bytes=b"changed")
            changed_contract = handoff.read_text(encoding="utf-8").replace(
                "Trace a tensor operation", "Trace one tensor operation"
            )
            handoff.write_text(changed_contract, encoding="utf-8")
            contract_report = validate_handoff(handoff, repo_root=root)
            self.assert_code(contract_report, "CONTRACT_HASH")
            self.assert_code(contract_report, "REVIEW_STALE")

    def test_index_and_curriculum_changes_stale_an_existing_handoff(self) -> None:
        private_path = "materials/private/example-course/06-01_lesson.md"
        private_contract = CONTRACT.replace("materials/lesson.md", private_path)
        index_path = "materials/private/example-course/INDEX.md"
        for changed_input in (index_path, "CURRICULUM.md"):
            with self.subTest(changed_input=changed_input), self.make_root() as directory:
                root = Path(directory)
                index = root / index_path
                index.parent.mkdir(parents=True)
                index.write_text("# Index\n", encoding="utf-8")
                handoff, _ = build_handoff(
                    root,
                    contract=private_contract,
                    primary_path=private_path,
                    course_index_path=index_path,
                    status="active",
                    reviews=[("pass", "fresh-reviewer")],
                )
                changed_path = root / changed_input
                changed_path.write_text(
                    changed_path.read_text(encoding="utf-8") + "\nchanged\n",
                    encoding="utf-8",
                )
                freshness = type(
                    "Freshness", (), {"errors": [], "warnings": []}
                )()
                with patch(
                    "validate_lesson_handoff.validate_lesson_slice_freshness",
                    return_value=freshness,
                ):
                    report = validate_handoff(handoff, repo_root=root, ready=True)
                self.assert_code(report, "SOURCE_HASH")
                self.assert_code(report, "REVIEW_STALE")

    def test_review_attempt_count_cannot_exceed_two(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="blocked",
                reviews=[
                    ("changes_required", "reviewer-one"),
                    ("changes_required", "reviewer-two"),
                    ("pass", "reviewer-three"),
                ],
            )
            report = validate_handoff(handoff, repo_root=root)
            self.assertFalse(report.ok)
            self.assertEqual(report.exit_code, 2)
            self.assert_code(report, "SCHEMA")

    def test_parent_traversal_and_external_symlink_are_rejected(self) -> None:
        with self.make_root() as directory, self.make_root() as outside_directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace("materials/lesson.md", "../lesson.md")
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "PATH")

            root = Path(directory) / "second"
            external = Path(outside_directory) / "external.md"
            external.write_text("outside", encoding="utf-8")
            (root / "materials").mkdir(parents=True)
            os.symlink(external, root / "materials/link.md")
            handoff, _ = build_handoff(root, primary_path="materials/link.md")
            self.assert_code(validate_handoff(handoff, repo_root=root), "PATH")

    def test_curriculum_role_requires_canonical_path_and_target_membership(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| I002 | curriculum | CURRICULUM.md |", "| I002 | curriculum | materials/lesson.md |"
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "PATH")

            handoff, _ = build_handoff(root)
            (root / "CURRICULUM.md").write_text("# Curriculum without the target\n", encoding="utf-8")
            # Rebuild so the manifest hash is current; only curriculum alignment should fail.
            handoff, _ = build_handoff(root)
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "REVIEW_NOT_PASS")

    def test_roadmap_curriculum_treatment_requires_a_required_added_supplement(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            curriculum = root / "CURRICULUM.md"
            curriculum.write_text(
                "| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| CC-DL-01 | Tensor contracts | D2 | — | explain | primary:SRC-TEST-00-01 | 부분 | 수업 내 보충 | Fixture row. |\n",
                encoding="utf-8",
            )
            invalid_contract = CONTRACT.replace(
                "| CC-DL-01 | 충분 | 그대로 사용 | source-only | O001, O002 | The named source directly supports the selected tensor-shape target. |",
                "| CC-DL-01 | 부분 | 수업 내 보충 | supplement-now | O001, O002 | The target needs an in-lesson supplement. |",
            )
            handoff, _ = build_handoff(root, contract=invalid_contract)
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

            valid_contract = invalid_contract.replace(
                "| O003 | optional-added | supplement |",
                "| O003 | required-added | supplement |",
            ).replace(
                "| supplement-now | O001, O002 |",
                "| supplement-now | O001, O002, O003 |",
            )
            handoff, _ = build_handoff(root, contract=valid_contract)
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)

    def test_private_primary_requires_course_index_and_ready_checks_freshness(self) -> None:
        private_path = "materials/private/kant-deep-learning-basics/06-01_lesson.md"
        private_contract = CONTRACT.replace("materials/lesson.md", private_path)
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                contract=private_contract,
                primary_path=private_path,
            )
            self.assert_code(validate_handoff(handoff, repo_root=root), "CURRICULUM_FRESHNESS")

            index_path = "materials/private/kant-deep-learning-basics/INDEX.md"
            index = root / index_path
            index.write_text("# Index\n", encoding="utf-8")
            handoff, _ = build_handoff(
                root,
                contract=private_contract,
                primary_path=private_path,
                course_index_path=index_path,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
            )
            stale = type("Finding", (), {"code": "SOURCE_HASH_STALE", "path": private_path, "line": 1, "message": "stale source"})()
            freshness = type("Freshness", (), {"errors": [stale], "warnings": []})()
            with patch("validate_lesson_handoff.validate_lesson_slice_freshness", return_value=freshness):
                report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assert_code(report, "CURRICULUM_FRESHNESS")

    def test_unrelated_course_drift_is_a_non_blocking_ready_warning(self) -> None:
        private_path = "materials/private/kant-deep-learning-basics/06-01_lesson.md"
        private_contract = CONTRACT.replace("materials/lesson.md", private_path)
        with self.make_root() as directory:
            root = Path(directory)
            index_path = "materials/private/kant-deep-learning-basics/INDEX.md"
            index = root / index_path
            index.parent.mkdir(parents=True)
            index.write_text("# Index\n", encoding="utf-8")
            handoff, _ = build_handoff(
                root,
                contract=private_contract,
                primary_path=private_path,
                course_index_path=index_path,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
            )
            stale = type(
                "Finding",
                (),
                {
                    "code": "SOURCE_HASH_STALE",
                    "path": "materials/private/kant-deep-learning-basics/08-08_unrelated.md",
                    "line": 1,
                    "message": "unrelated stale source",
                },
            )()
            freshness = type("Freshness", (), {"errors": [], "warnings": [stale]})()
            with patch("validate_lesson_handoff.validate_lesson_slice_freshness", return_value=freshness):
                report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.exit_code, 0)
            self.assertEqual(1, len(report.warnings))
            self.assertIn("unrelated stale source", report.as_json()["warnings"][0]["message"])

    def test_ready_requires_target_relation_to_manifested_source_core_primary(self) -> None:
        primary_path = "materials/private/example-course/00-01_lesson.md"
        index_path = "materials/private/example-course/INDEX.md"
        private_contract = CONTRACT.replace("materials/lesson.md", primary_path)
        cases = {
            "primary": ("primary:SRC-TEST-00-01", True),
            "supporting": ("supporting:SRC-TEST-00-01", True),
            "unrelated": ("primary:SRC-TEST-00-02", False),
            "context-only": ("context:SRC-TEST-00-01", False),
            "registry-missing": ("primary:SRC-TEST-00-03", False),
        }
        for name, (relation, should_pass) in cases.items():
            with self.subTest(case=name), self.make_root() as directory:
                root = Path(directory)
                index = root / index_path
                index.parent.mkdir(parents=True)
                index.write_text(
                    "# Index\n\n- source_namespace: TEST\n\n## 강의 자료\n\n"
                    "| 파일 | 설명 |\n| --- | --- |\n"
                    "| `00-01_lesson.md` | selected |\n"
                    "| `00-02_other.md` | unrelated |\n",
                    encoding="utf-8",
                )
                build_handoff(
                    root,
                    contract=private_contract,
                    primary_path=primary_path,
                    course_index_path=index_path,
                )
                primary = root / primary_path
                other = primary.parent / "00-02_other.md"
                other.write_text("# Other\n", encoding="utf-8")
                (root / "CURRICULUM.md").write_text(
                    "| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |\n"
                    "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                    f"| CC-DL-01 | Tensor contracts | D2 | — | explain | {relation} | 충분 | 그대로 사용 | Fixture row. |\n\n"
                    "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
                    "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                    f"| SRC-TEST-00-01 | `{primary_path}` | HTML 토글 펼침 Markdown | `{sha256(primary.read_bytes())}` | complete | complete | 2026-08-20 | selected |\n"
                    f"| SRC-TEST-00-02 | `materials/private/example-course/00-02_other.md` | HTML 토글 펼침 Markdown | `{sha256(other.read_bytes())}` | complete | complete | 2026-08-20 | unrelated |\n",
                    encoding="utf-8",
                )
                handoff, _ = build_handoff(
                    root,
                    contract=private_contract,
                    primary_path=primary_path,
                    course_index_path=index_path,
                    status="active",
                    reviews=[("pass", "fresh-reviewer")],
                )
                report = validate_handoff(handoff, repo_root=root, ready=True)
                if should_pass:
                    self.assertTrue(report.ok, report.errors)
                else:
                    self.assert_code(report, "CURRICULUM_SOURCE_RELATION")

    def test_warning_only_cli_prints_warning_and_exits_zero(self) -> None:
        report = ValidationReport(
            path=Path("tmp/active-lesson-handoff.md"),
            ready_requested=True,
            til_ready_requested=False,
            errors=[],
            document=None,
            warnings=[ValidationWarning(12, "CURRICULUM_FRESHNESS", "unrelated source drift")],
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch.object(handoff_validator, "validate_handoff", return_value=report),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            exit_code = handoff_validator.main(["--ready", "tmp/active-lesson-handoff.md"])
        self.assertEqual(0, exit_code)
        self.assertIn("OK tmp/active-lesson-handoff.md [ready]", stdout.getvalue())
        self.assertIn("WARNING tmp/active-lesson-handoff.md:12", stderr.getvalue())

    def test_concept_source_path_must_be_manifested(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "materials/lesson.md#shape-propagation", "materials/unreviewed.md#shape-propagation"
            )
            # Keep the declared contract hash current so this isolates manifest alignment.
            start = text.index("<!-- lesson-contract:start -->") + len("<!-- lesson-contract:start -->\n")
            end = text.index("\n<!-- lesson-contract:end -->")
            text = re_sub_field(text, "contract_sha256", sha256(text[start:end]))
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "REVIEW_NOT_PASS")

    def test_review_verdict_and_blocking_findings_must_agree(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "fresh-reviewer")])
            text = handoff.read_text(encoding="utf-8").replace(
                "- none\n<!-- semantic-review-attempt:1:end -->",
                "- Softmax mechanics are missing.\n<!-- semantic-review-attempt:1:end -->",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "REVIEW_NOT_PASS")

            handoff, _ = build_handoff(root, status="review_pending", reviews=[("changes_required", "another-reviewer")])
            text = handoff.read_text(encoding="utf-8").replace(
                "- Revise the named contract point.\n<!-- semantic-review-attempt:1:end -->",
                "- none\n<!-- semantic-review-attempt:1:end -->",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "REVIEW_NOT_PASS")

            handoff, _ = build_handoff(root, status="review_pending", reviews=[("changes_required", "mixed-reviewer")])
            text = handoff.read_text(encoding="utf-8").replace(
                "- Revise the named contract point.\n<!-- semantic-review-attempt:1:end -->",
                "- none\n- Revise the named contract point.\n<!-- semantic-review-attempt:1:end -->",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "REVIEW_NOT_PASS")

    def test_mutable_draft_cannot_be_a_manifest_input(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, hashes = build_handoff(root)
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            draft.write_text("learner scratch\n", encoding="utf-8")
            text = handoff.read_text(encoding="utf-8")
            draft_hash = sha256(draft.read_bytes())
            text = text.replace(
                "<!-- lesson-contract:start -->",
                f"| I003 | til | til/today.md | {draft_hash} |\n\n<!-- lesson-contract:start -->",
                1,
            )
            manifest_hash = sha256(
                "".join(
                    sorted(
                        [
                            f"primary\tmaterials/lesson.md\t{sha256((root / 'materials/lesson.md').read_bytes())}\n",
                            f"curriculum\tCURRICULUM.md\t{sha256((root / 'CURRICULUM.md').read_bytes())}\n",
                            f"til\ttil/today.md\t{draft_hash}\n",
                        ]
                    )
                )
            )
            text = re_sub_field(text, "input_manifest_sha256", manifest_hash)
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "PATH")

    def test_evidence_state_and_content_hash_are_checked(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"verdict": "partial", "append_state": "pending"}],
            )
            self.assert_code(validate_handoff(handoff, repo_root=root), "EVIDENCE_STATE")
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"verdict": "confirmed", "append_state": "pending"}],
            )
            text = handoff.read_text(encoding="utf-8").replace("배치 축과 특성 축", "배치 축과 시간 축")
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "EVIDENCE_STATE")

    def test_schema_v3_is_rejected_with_rebuild_error(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            handoff.write_text(
                handoff.read_text(encoding="utf-8").replace("- schema_version: 4", "- schema_version: 3"),
                encoding="utf-8",
            )
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "SCHEMA")
            self.assertTrue(any("rebuild older handoffs" in error.message for error in report.errors))

    def test_source_coverage_requires_every_primary_in_manifest_order(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| I001 | D001, D002, D003 | O001, O002 | G001 | none | none |",
                "| I999 | D001, D002, D003 | O001, O002 | G001 | none | none |",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

    def test_full_source_can_separate_learning_goals_and_guidance(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            report = validate_handoff(handoff, repo_root=root)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.document.declared_goals["D003"].disposition, "guidance")
            self.assertEqual(report.document.guidance["G001"].kind, "reference")

    def test_guidance_cannot_enter_teaching_delivery_or_evidence(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "- check_question: Which axis contains the three features?",
                "- check_question: Which axis contains the three features in G001?",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| O001 | pending | none | Awaiting instruction. |",
                "| O001 | pending | none | Awaiting G001 guidance. |",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

            handoff, _ = build_handoff(root, evidence=[{"content": "G001의 안내를 학습했다."}])
            self.assert_code(validate_handoff(handoff, repo_root=root), "EVIDENCE_STATE")

            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace("| C01 | deferred | none | not-required | Not taught yet. |", "| C01 | deferred | none | not-required | G001 was not taught. |")
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "TIL_COVERAGE")

    def test_source_gap_cannot_masquerade_as_source_core(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| D001 | I001 | materials/lesson.md#Identify the batch and feature axes. | learning | O001 | materials/lesson.md#axes | none |",
                "| D001 | I001 | materials/lesson.md#Identify the batch and feature axes. | source-gap | O001 | none | The goal has no body support. |",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

    def test_reviewed_defer_gap_preserves_source_gap_without_invented_objective(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            (root / "CURRICULUM.md").write_text(
                "| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| CC-DL-01 | Tensor contracts | D2 | — | explain | primary:SRC-TEST-00-01 | 부분 | 별도 자료 확보 | Fixture row. |\n",
                encoding="utf-8",
            )
            contract = CONTRACT.replace(
                "| CC-DL-01 | 충분 | 그대로 사용 | source-only | O001, O002 | The named source directly supports the selected tensor-shape target. |",
                "| CC-DL-01 | 부분 | 별도 자료 확보 | defer-gap | O001, O002 | Teach supported tensor content and acquire the missing goal separately. |",
            ).replace(
                "| D001 | I001 | materials/lesson.md#Identify the batch and feature axes. | learning | O001 | materials/lesson.md#axes | none |",
                "| D001 | I001 | materials/lesson.md#Identify the batch and feature axes. | source-gap | none | none | The source declares this goal without enough body support. |",
            ).replace(
                "| F002 | supplement | CURRICULUM.md#CC-DL-01 | O003 | The attention-axis connection is optional roadmap enrichment. |",
                "| F002 | supplement | CURRICULUM.md#CC-DL-01 | O003 | The attention-axis connection is optional roadmap enrichment. |\n"
                "| F003 | underspecification | materials/lesson.md#Identify the batch and feature axes. | D001 | Preserve the unsupported goal as a source gap. |",
            )
            handoff, _ = build_handoff(root, contract=contract)
            report = validate_handoff(handoff, repo_root=root)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.document.declared_goals["D001"].linked_ids, [])

    def test_goal_wording_cannot_be_its_own_body_support(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| D001 | I001 | materials/lesson.md#Identify the batch and feature axes. | learning | O001 | materials/lesson.md#axes | none |",
                "| D001 | I001 | materials/lesson.md#Identify the batch and feature axes. | learning | O001 | materials/lesson.md#Identify the batch and feature axes. | none |",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

    def test_objective_ids_and_teaching_note_assignment_are_complete(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| O002 | source-core | none |",
                "| O004 | source-core | none |",
                1,
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "SCHEMA")

            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "- objective_ids: O002",
                "- objective_ids: O001",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

    def test_teaching_step_assessment_policy_is_structural(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "- check_basis: if learner identifies both axes -> continue to shape propagation; else -> reteach rows and columns with labels",
                "- check_basis: Ask because every step needs a question.",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "ASSESSMENT_ALIGNMENT")

            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "if learner identifies both axes -> continue to shape propagation; else -> reteach rows and columns with labels",
                "if learner identifies both axes -> repeat the same explanation; else -> repeat the same explanation",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "ASSESSMENT_ALIGNMENT")

            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "- check_question: none",
                "- check_question: Explain the course outline.",
                1,
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "ASSESSMENT_ALIGNMENT")

            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "- check_question: Which axis contains the three features?",
                "- check_question: flatten에서 이론·복습·실습은 각각 무엇을 확인하게 해 주나요?",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "ASSESSMENT_ALIGNMENT")

    def test_none_step_cannot_await_an_answer(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                delivery=[
                    {"objective": "O001", "state": "delivered", "mode": "full", "note": "Taught."},
                    {"objective": "O002", "state": "delivered", "mode": "full", "note": "Taught."},
                    {"objective": "O003", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                ],
            )
            text = handoff.read_text(encoding="utf-8").replace("- next_action: teach", "- next_action: await-answer")
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "ASSESSMENT_ALIGNMENT")

    def test_adaptive_step_cannot_await_before_delivery(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace("- next_action: teach", "- next_action: await-answer")
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "ASSESSMENT_ALIGNMENT")

    def test_teaching_step_order_may_differ_from_objective_audit_order(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8")
            start_one = text.index("#### T001")
            start_two = text.index("#### T002")
            start_three = text.index("#### T003")
            block_one = text[start_one:start_two]
            block_two = text[start_two:start_three]
            swapped = block_two.replace("#### T002", "#### T001", 1) + block_one.replace("#### T001", "#### T002", 1)
            text = text[:start_one] + swapped + text[start_three:]
            text = text.replace("- target_objectives: O001", "- target_objectives: O002")
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.document.teaching_steps["T001"].objective_ids, ["O002"])

    def test_objective_source_must_be_exact_and_manifested(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "materials/lesson.md#shape-propagation | Predict the output shape",
                "materials/unreviewed.md#shape-propagation | Predict the output shape",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "REVIEW_NOT_PASS")

            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "materials/lesson.md#shape-propagation | Predict the output shape",
                "materials/lesson.md#missing-section | Predict the output shape",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "SOURCE_LOCATION")

    def test_full_source_required_objective_cannot_be_deferred(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| O002 | source-core | none | materials/lesson.md#shape-propagation | Predict the output shape of a broadcast operation. | C02 | full | Compare aligned dimensions from the right. | none |",
                "| O002 | source-core | none | materials/lesson.md#shape-propagation | Predict the output shape of a broadcast operation. | C02 | deferred | none | none |",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

    def test_focused_mode_still_rejects_deferred_required_added_objective(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8")
            text = text.replace("- mode: full-source", "- mode: focused")
            text = text.replace(
                "| O003 | optional-added | supplement | CURRICULUM.md#CC-DL-01 | Connect tensor axes to batch, token, and hidden axes. | C03 | full | Map one small tensor to an attention input. | none |",
                "| O003 | required-added | prerequisite | CURRICULUM.md#CC-DL-01 | Connect tensor axes to batch, token, and hidden axes. | C03 | deferred | none | none |",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root)
            self.assertTrue(
                any("required-added objective cannot be deferred" in error.message for error in report.errors),
                report.errors,
            )

    def test_objective_id_lists_have_no_three_digit_ceiling(self) -> None:
        self.assertEqual(["O999", "O1000"], _comma_ids("O999, O1000", r"O\d{3,}"))

    def test_pdf_source_locations_require_an_in_bounds_page(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            pdf = root / "materials/lesson.pdf"
            pdf.parent.mkdir(parents=True)
            pdf.write_bytes(b"%PDF-1.4\n")
            with patch("validate_lesson_handoff._pdf_page_count", return_value=2):
                self.assertTrue(_location_exists("materials/lesson.pdf#page-2", root))
                self.assertTrue(_location_exists("materials/lesson.pdf#page-2: formula", root))
                self.assertFalse(_location_exists("materials/lesson.pdf#page-3", root))
                self.assertFalse(_location_exists("materials/lesson.pdf#bogus", root))

    def test_markdown_goal_locations_accept_nested_quote_and_list_prefixes(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            source = root / "materials/quoted-goals.md"
            source.parent.mkdir(parents=True)
            source.write_text("> - first goal\n> 1. second goal\n", encoding="utf-8")
            self.assertTrue(_location_exists("materials/quoted-goals.md#first goal", root))
            self.assertTrue(_location_exists("materials/quoted-goals.md#second goal", root))

    def test_bridge_requires_exact_confirmed_learner_evidence(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| C01 | full | Trace both axes before naming the operation. | none |",
                "| C01 | bridge | Trace both axes before naming the operation. | none |",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

            handoff, _ = build_handoff(
                root,
                evidence=[{"concept": "C01", "verdict": "confirmed", "append_state": "pending"}],
                delivery=[
                    {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis trace was taught."},
                    {"objective": "O002", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                    {"objective": "O003", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                ],
            )
            text = handoff.read_text(encoding="utf-8").replace(
                "| C01 | full | Trace both axes before naming the operation. | none |",
                "| C01 | bridge | Trace both axes before naming the operation. | learner-evidence:E001 |",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)

    def test_completed_rejects_pending_objective_delivery(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "fresh-reviewer")])
            text = handoff.read_text(encoding="utf-8").replace("- status: active", "- status: completed")
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

    def test_delivered_objective_cannot_remain_daily_deferred(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                delivery=[
                    {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis trace was taught."},
                    {"objective": "O002", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                    {"objective": "O003", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                ],
            )
            text = handoff.read_text(encoding="utf-8").replace(
                "| C01 | uncertain | none | missing | Taught but not demonstrated. |",
                "| C01 | deferred | none | not-required | Not taught yet. |",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

    def test_recovery_may_retain_later_delivered_objectives(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                delivery=[
                    {"objective": "O001", "state": "pending", "mode": "none", "note": "Earliest Step remains."},
                    {"objective": "O002", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                    {"objective": "O003", "state": "delivered", "mode": "full", "note": "Retained from earlier out-of-order teaching."},
                ],
            )
            report = validate_handoff(handoff, repo_root=root)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.document.current_position["current_step"], "T001")

    def test_objective_delivery_requires_one_ordered_row_per_objective(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| O003 | pending | none | Awaiting instruction. |\n",
                "",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

    def test_materialized_untouched_preparing_template_has_no_phantom_blocks(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            (root / "materials").mkdir(parents=True)
            source = root / "materials/lesson.md"
            curriculum = root / "CURRICULUM.md"
            source.write_text("# source\n\n## exact-location\n", encoding="utf-8")
            curriculum.write_text(
                "# curriculum\n\n"
                "| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| CC-DL-01 | Tensor contracts | D2 | — | explain | primary:SRC-TEST-00-01 | 충분 | 그대로 사용 | Fixture row. |\n\n"
                "## exact-location\n",
                encoding="utf-8",
            )
            source_hash = sha256(source.read_bytes())
            curriculum_hash = sha256(curriculum.read_bytes())
            template = (SKILL / "assets/active-lesson-handoff-template.md").read_text(encoding="utf-8")
            raw_path = root / "tmp/raw-template.md"
            raw_path.parent.mkdir(parents=True)
            raw_path.write_text(template, encoding="utf-8")
            self.assertFalse(validate_handoff(raw_path, repo_root=root).ok)

            text = template.replace("replace-with-stable-lesson-id", "template-lesson")
            text = text.replace("YYYY-MM-DDTHH:MM:SSZ", "2026-08-20T00:00:00Z")
            text = text.replace("YYYY-MM-DD", "2026-08-20")
            text = text.replace("materials/private/course/NN-NN_lesson.md", "materials/lesson.md")
            text = text.replace(
                "| I002 | course-index | materials/private/course/INDEX.md | replace-with-file-sha256 |\n",
                "",
            )
            text = text.replace("| I003 | curriculum |", "| I002 | curriculum |")
            text = text.replace(
                "| I001 | primary | materials/lesson.md | replace-with-file-sha256 |",
                f"| I001 | primary | materials/lesson.md | {source_hash} |",
            )
            text = text.replace(
                "| I002 | curriculum | CURRICULUM.md | replace-with-file-sha256 |",
                f"| I002 | curriculum | CURRICULUM.md | {curriculum_hash} |",
            )
            manifest_hash = sha256(
                "".join(
                    sorted(
                        [
                            f"primary\tmaterials/lesson.md\t{source_hash}\n",
                            f"curriculum\tCURRICULUM.md\t{curriculum_hash}\n",
                        ]
                    )
                )
            )
            start = text.index("<!-- lesson-contract:start -->") + len("<!-- lesson-contract:start -->\n")
            end = text.index("\n<!-- lesson-contract:end -->")
            contract_hash = hashlib.sha256(text[start:end].encode("utf-8")).hexdigest()
            text = text.replace("replace-with-64-lowercase-hex", manifest_hash, 1)
            text = text.replace("replace-with-64-lowercase-hex", contract_hash, 1)
            ready_path = root / "tmp/active-lesson-handoff.md"
            ready_path.write_text(text, encoding="utf-8")
            report = validate_handoff(ready_path, repo_root=root)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.document.review_attempt_count, 0)
            self.assertEqual(report.document.evidence, {})

    def test_json_cli_and_error_format(self) -> None:
        (REPO / "tmp").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=REPO / "tmp") as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            relative_directory = root.relative_to(REPO)
            text = handoff.read_text(encoding="utf-8")
            text = text.replace("materials/lesson.md", f"{relative_directory.as_posix()}/materials/lesson.md")
            source_hash = sha256((root / "materials/lesson.md").read_bytes())
            curriculum_hash = sha256((REPO / "CURRICULUM.md").read_bytes())
            import re

            text = re.sub(
                r"\| I002 \| curriculum \| CURRICULUM\.md \| [0-9a-f]{64} \|",
                f"| I002 | curriculum | CURRICULUM.md | {curriculum_hash} |",
                text,
                count=1,
            )
            manifest_hash = sha256(
                "".join(
                    sorted(
                        [
                            f"primary\t{relative_directory.as_posix()}/materials/lesson.md\t{source_hash}\n",
                            f"curriculum\tCURRICULUM.md\t{curriculum_hash}\n",
                        ]
                    )
                )
            )
            # Both source-location text and manifest paths changed. Recompute only the
            # declared hashes; the preparing template needs no semantic review.
            contract_start = text.index("<!-- lesson-contract:start -->") + len("<!-- lesson-contract:start -->\n")
            contract_end = text.index("\n<!-- lesson-contract:end -->")
            contract_hash = sha256(text[contract_start:contract_end])
            text = re_sub_field(text, "input_manifest_sha256", manifest_hash)
            text = re_sub_field(text, "contract_sha256", contract_hash)
            handoff.write_text(text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts/validate_lesson_handoff.py"), "--json", handoff.relative_to(REPO).as_posix()],
                cwd=REPO,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["warnings"], [])

    def test_cli_usage_error_uses_validator_error_contract(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SKILL / "scripts/validate_lesson_handoff.py")],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertRegex(
            result.stderr,
            r"^ERROR <cli>:1 \[SCHEMA\] the following arguments are required: handoff\n$",
        )

        conflict = subprocess.run(
            [
                sys.executable,
                str(SKILL / "scripts/validate_lesson_handoff.py"),
                "--ready",
                "--til-ready",
                "tmp/active-lesson-handoff.md",
            ],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(conflict.returncode, 2)
        self.assertEqual(conflict.stdout, "")
        self.assertRegex(conflict.stderr, r"^ERROR <cli>:1 \[SCHEMA\] argument --til-ready: not allowed with argument --ready\n$")


def re_sub_field(text: str, key: str, value: str) -> str:
    import re

    return re.sub(rf"^- {re.escape(key)}: .*$", f"- {key}: {value}", text, count=1, flags=re.MULTILINE)


def refresh_contract_hash(text: str) -> str:
    start = text.index("<!-- lesson-contract:start -->") + len("<!-- lesson-contract:start -->\n")
    end = text.index("\n<!-- lesson-contract:end -->")
    return re_sub_field(text, "contract_sha256", sha256(text[start:end]))


if __name__ == "__main__":
    unittest.main()
