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

from pypdf import PdfWriter


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from handoff_fixture import CONTRACT, build_handoff, sha256  # noqa: E402
import validate_lesson_handoff as handoff_validator  # noqa: E402
from validate_lesson_handoff import (  # noqa: E402
    ValidationReport,
    ValidationWarning,
    _comma_ids,
    _location_exists,
    can_mechanically_rebuild_same_lesson,
    validate_handoff,
)
from migrate_paused_v8_handoff import (  # noqa: E402
    MigrationError,
    migrate_paused_v8_handoff,
)


class LessonHandoffValidatorTests(unittest.TestCase):
    def make_root(self) -> tempfile.TemporaryDirectory[str]:
        return tempfile.TemporaryDirectory()

    def assert_code(self, report, code: str) -> None:
        self.assertIn(code, {error.code for error in report.errors}, report.errors)

    def short_three_step_contract(self) -> str:
        contract = re.sub(
            r"\n#### T004\n.*?(?=\n### Deferred)",
            "\n",
            CONTRACT,
            count=1,
            flags=re.DOTALL,
        )
        contract = re.sub(r"(?m)^\| X004 \|.*\n", "", contract, count=1)
        contract = contract.replace("- exit_step: T005", "- exit_step: T003")
        contract = contract.replace(
            "#### T002\n\n- step_role: concept-model\n- concept_ids: C01\n- objective_ids: O001\n- example_id: X001",
            "#### T002\n\n- step_role: contrast-limit\n- concept_ids: C02\n- objective_ids: O002\n- example_id: X002",
        )
        contract = contract.replace(
            "#### T003\n\n- step_role: worked-example\n- concept_ids: C02\n- objective_ids: O002\n- example_id: X002",
            "#### T003\n\n- step_role: synthesis-transfer\n- concept_ids: C03\n- objective_ids: O003\n- example_id: X003",
        )
        return contract

    def build_focused_private_handoff(self, root: Path) -> Path:
        source_path = "materials/private/example-course/00-01_lesson.md"
        source = root / source_path
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(
            b"# Lesson\n\n"
            b"## learning-goals\n\n"
            b"- Identify the batch and feature axes.\n"
            b"- Predict the output shape of a broadcast operation.\n"
            b"- Review the course map only when it affects the current path.\n\n"
            b"## book-goal\n\nA global source goal outside this lesson.\n\n"
            b"## axes\n\nTensor axes.\n\n"
            b"## shape-propagation\n\nBroadcast shapes.\n\n"
            b"## orientation\n\nUse the course map when navigation is needed.\n\n"
            b"## appendix\n\nGlobal reference material outside this lesson.\n"
        )
        index_path = "materials/private/example-course/INDEX.md"
        (root / index_path).write_text(
            "# Example course\n\n- source_namespace: TEST\n\n"
            "## 강의 자료\n\n"
            "| 파일 | 설명 |\n| --- | --- |\n"
            "| `00-01_lesson.md` | fixture |\n\n"
            "## 학습 범위\n\n"
            "| Scope ID | Source ID | Title | Included units | Boundary units | Note |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            f"| SCOPE-TEST-00-01-01 | SRC-TEST-00-01 | Tensor shape unit | Tensor axes [{source_path}#axes]; Broadcast propagation [{source_path}#shape-propagation] | Orientation context [{source_path}#orientation] | Only the selected mechanism is reviewed. |\n",
            encoding="utf-8",
        )
        contract = CONTRACT.replace("materials/lesson.md", source_path)
        contract = contract.replace("- mode: full-source", "- mode: focused")
        contract = contract.replace(
            "| I001 | entire-source | none | entire-source | none | none |",
            f"| I001 | registered-slice | SCOPE-TEST-00-01-01 | Tensor axes [{source_path}#axes]; Broadcast propagation [{source_path}#shape-propagation] | Orientation context [{source_path}#orientation] | The rest of the source is outside this focused unit. |",
        )
        contract = contract.replace(
            "| I001 | D001, D002, D003 | O001, O002 | G001 |",
            "| I001 | none | O001, O002 | none |",
        )
        contract = contract.replace(
            "| D001 | I001 | "
            + source_path
            + "#Identify the batch and feature axes. | learning | O001 | "
            + source_path
            + "#axes | none |",
            "| none | none | none | none | none | none | This focused slice contains no explicit declared goal sentence. |",
        )
        contract = contract.replace(
            "| D002 | I001 | "
            + source_path
            + "#Predict the output shape of a broadcast operation. | learning | O002 | "
            + source_path
            + "#shape-propagation | none |\n",
            "",
        )
        contract = contract.replace(
            "| D003 | I001 | "
            + source_path
            + "#Review the course map only when it affects the current path. | guidance | G001 | "
            + source_path
            + "#orientation | It is navigation guidance, not learner knowledge or skill. |\n",
            "",
        )
        contract = contract.replace(
            "| G001 | reference | "
            + source_path
            + "#orientation | The course map is an on-demand navigation reference. | The learner asks where this tensor topic fits in the course. |",
            "| none | none | none | none | none |",
        )
        handoff, _ = build_handoff(
            root,
            contract=contract,
            status="active",
            reviews=[("pass", "focused-reviewer")],
            primary_path=source_path,
            primary_bytes=source.read_bytes(),
            course_index_path=index_path,
        )
        return handoff

    def build_large_pdf_focused_handoff(self, root: Path) -> Path:
        source_path = "materials/private/large-course/00-01_large.pdf"
        source = root / source_path
        source.parent.mkdir(parents=True, exist_ok=True)
        writer = PdfWriter()
        for _ in range(630):
            writer.add_blank_page(width=612, height=792)
        with source.open("wb") as handle:
            writer.write(handle)
        source_hash = sha256(source.read_bytes())
        index_path = "materials/private/large-course/INDEX.md"
        (root / index_path).write_text(
            "# Large course\n\n- source_namespace: LARGE\n\n"
            "## 강의 자료\n\n"
            "| 파일 | 설명 |\n| --- | --- |\n"
            "| `00-01_large.pdf` | 630-page fixture |\n\n"
            "## 학습 범위\n\n"
            "| Scope ID | Source ID | Title | Included units | Boundary units | Note |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            f"| SCOPE-LARGE-00-01-01 | SRC-LARGE-00-01 | Three-page concept unit | Core concept sequence [{source_path}#page-14--18] | Previous context [{source_path}#page-13]; Following context [{source_path}#page-19] | Bound the lesson without a whole-book exclusion inventory. |\n",
            encoding="utf-8",
        )
        (root / "CURRICULUM.md").write_text(
            "# Curriculum\n\n"
            "| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
            "| CC-DL-01 | Tensor contracts | D2 | — | explain | primary:SRC-LARGE-00-01 | 충분 | 그대로 사용 | Fixture row. |\n"
            "| TR-SYS-03 | Systems endpoint | D3 | CC-DL-01 | design | — | 없음 | 트랙 선택 시 확보 | Fixture endpoint. |\n\n"
            "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            f"| SRC-LARGE-00-01 | `{source_path}` | PDF | `{source_hash}` | complete | complete | 2026-08-28 | Fixture source. |\n",
            encoding="utf-8",
        )
        contract = CONTRACT.replace("materials/lesson.md", source_path)
        contract = contract.replace("- mode: full-source", "- mode: focused")
        contract = contract.replace("#axes", "#page-14")
        contract = contract.replace("#shape-propagation", "#page-17")
        contract = contract.replace("#orientation", "#page-18")
        contract = contract.replace(
            "| I001 | entire-source | none | entire-source | none | none |",
            f"| I001 | registered-slice | SCOPE-LARGE-00-01-01 | Core concept sequence [{source_path}#page-14--18] | Previous context [{source_path}#page-13]; Following context [{source_path}#page-19] | The other 627 pages are outside this focused unit. |",
        )
        contract = contract.replace(
            "| I001 | D001, D002, D003 | O001, O002 | G001 |",
            "| I001 | none | O001, O002 | none |",
        )
        start = contract.index("### Declared Goal Alignment")
        end = contract.index("### Guidance Map")
        contract = (
            contract[:start]
            + "### Declared Goal Alignment\n\n"
            + "| Goal ID | Primary ID | Goal location | Disposition | Linked IDs | Body support | Reason |\n"
            + "| --- | --- | --- | --- | --- | --- | --- |\n"
            + "| none | none | none | none | none | none | This focused slice contains no declared goal sentence. |\n\n"
            + contract[end:]
        )
        guidance_start = contract.index("### Guidance Map")
        guidance_end = contract.index("### Observable Objective Map")
        contract = (
            contract[:guidance_start]
            + "### Guidance Map\n\n"
            + "| Guidance ID | Kind | Source location | Summary | Trigger |\n"
            + "| --- | --- | --- | --- | --- |\n"
            + "| none | none | none | none | none |\n\n"
            + contract[guidance_end:]
        )
        return build_handoff(
            root,
            contract=contract,
            status="active",
            reviews=[("pass", "large-slice-reviewer")],
            primary_path=source_path,
            primary_bytes=source.read_bytes(),
            course_index_path=index_path,
        )[0]

    def test_preparing_handoff_is_structurally_valid_but_not_ready(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)
            ready = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertFalse(ready.ok)
            self.assert_code(ready, "REVIEW_NOT_PASS")

    def test_same_lesson_rebuild_requires_no_delivery_or_evidence(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="repair_pending",
                reviews=[("repair_required", "reviewer-one")],
            )
            report = validate_handoff(handoff, repo_root=root)
            self.assertTrue(report.ok, report.errors)
            self.assertIsNotNone(report.document)
            assert report.document is not None
            self.assertTrue(
                can_mechanically_rebuild_same_lesson(
                    report.document,
                    primary_target="CC-DL-01",
                    primary_paths={"materials/lesson.md"},
                )
            )
            self.assertFalse(
                can_mechanically_rebuild_same_lesson(
                    report.document,
                    primary_target="CC-PROB-01",
                    primary_paths={"materials/lesson.md"},
                )
            )

            handoff, _ = build_handoff(
                root,
                status="paused",
                reviews=[("pass", "reviewer-one")],
                evidence=[{"concept": "C01"}],
                delivery=[
                    {"objective": "O001", "state": "delivered", "mode": "full", "note": "Taught."},
                    {"objective": "O002", "state": "pending", "mode": "none", "note": "Pending."},
                    {"objective": "O003", "state": "pending", "mode": "none", "note": "Pending."},
                ],
            )
            report = validate_handoff(handoff, repo_root=root, check_draft=False)
            self.assertIsNotNone(report.document)
            assert report.document is not None
            self.assertFalse(
                can_mechanically_rebuild_same_lesson(
                    report.document,
                    primary_target="CC-DL-01",
                    primary_paths={"materials/lesson.md"},
                )
            )

    def test_active_pass_with_current_hashes_is_ready(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "fresh-reviewer")])
            report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertTrue(report.ok, report.errors)

    def test_non_actionable_planner_states_never_form_a_lesson_handoff(self) -> None:
        for target_state in ("NEED_DIAGNOSTIC", "NO_ACTIONABLE_TARGET"):
            with self.subTest(target_state=target_state), self.make_root() as directory:
                root = Path(directory)
                contract = CONTRACT.replace(
                    "- target_state: START_TARGET",
                    f"- target_state: {target_state}",
                )
                handoff, _ = build_handoff(
                    root,
                    contract=contract,
                    status="active",
                    reviews=[("pass", "fresh-reviewer")],
                )
                for mode in ({}, {"ready": True}, {"capture_ready": True}):
                    report = validate_handoff(handoff, repo_root=root, **mode)
                    self.assertFalse(report.ok)
                    self.assert_code(report, "TARGET_DECISION")

    def test_endpoint_must_be_ordered_and_contain_the_primary_target(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            contract = CONTRACT.replace(
                "- endpoint: TR-SYS-03",
                "- endpoint: NOT-A-ROADMAP-ENDPOINT",
            )
            handoff, _ = build_handoff(root, contract=contract)
            self.assert_code(validate_handoff(handoff, repo_root=root), "TARGET_DECISION")

        with self.make_root() as directory:
            root = Path(directory)
            (root / "CURRICULUM.md").write_text(
                "# Curriculum\n\n"
                "| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| CC-DL-01 | Tensor contracts | D2 | — | explain | — | 없음 | 별도 자료 확보 | Fixture. |\n"
                "| TR-EVAL-02 | Evaluation endpoint | D3 | — | design | — | 없음 | 트랙 선택 시 확보 | Fixture. |\n",
                encoding="utf-8",
            )
            (root / "ROADMAP.md").write_text(
                "# Roadmap\n\n## 정적 목표 endpoint\n\n"
                "| 우선순위 | 단계 | 방향 | Endpoint |\n"
                "| ---: | ---: | --- | --- |\n"
                "| 2 | `2B` | Evaluation | `TR-EVAL-02` |\n",
                encoding="utf-8",
            )
            contract = CONTRACT.replace(
                "- endpoint: TR-SYS-03",
                "- endpoint: TR-EVAL-02",
            )
            handoff, _ = build_handoff(root, contract=contract)
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "TARGET_DECISION")
            self.assertTrue(
                any("outside endpoint route" in error.message for error in report.errors)
            )

    def test_user_directed_is_for_user_modes_only(self) -> None:
        for selection_mode in ("user-named-target", "user-named-source"):
            with self.subTest(selection_mode=selection_mode), self.make_root() as directory:
                root = Path(directory)
                user_contract = CONTRACT.replace(
                    "- selection_mode: user-named-target",
                    f"- selection_mode: {selection_mode}",
                ).replace("- endpoint: TR-SYS-03", "- endpoint: user-directed")
                handoff, _ = build_handoff(root, contract=user_contract)
                self.assertTrue(validate_handoff(handoff, repo_root=root).ok)

        with self.make_root() as directory:
            root = Path(directory)
            user_contract = CONTRACT.replace(
                "- endpoint: TR-SYS-03", "- endpoint: user-directed"
            )
            planner_contract = user_contract.replace(
                "- selection_mode: user-named-target", "- selection_mode: planner"
            )
            handoff, _ = build_handoff(root, contract=planner_contract)
            self.assert_code(
                validate_handoff(handoff, repo_root=root), "TARGET_DECISION"
            )

    def test_planner_mode_accepts_an_exact_endpoint_route(self) -> None:
        for selection_mode in ("planner", "user-named-target", "user-named-source"):
            with self.subTest(selection_mode=selection_mode), self.make_root() as directory:
                root = Path(directory)
                contract = CONTRACT.replace(
                    "- selection_mode: user-named-target",
                    f"- selection_mode: {selection_mode}",
                )
                handoff, _ = build_handoff(root, contract=contract)
                self.assertTrue(validate_handoff(handoff, repo_root=root).ok)

    def test_bridge_must_belong_to_the_primary_prerequisite_closure(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            contract = CONTRACT.replace(
                "- target_state: START_TARGET",
                "- target_state: BRIDGE_PREREQUISITE",
            ).replace("- bridge_target: none", "- bridge_target: TR-SYS-03")
            handoff, _ = build_handoff(root, contract=contract)
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "TARGET_DECISION")
            self.assertTrue(
                any("is not a prerequisite" in error.message for error in report.errors)
            )


    def test_capture_ready_accepts_a_completed_confirmed_session(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="completed",
                reviews=[("pass", "fresh-reviewer")],
            )
            report = validate_handoff(handoff, repo_root=root, capture_ready=True)
            self.assertTrue(report.ok, report.errors)
            self.assertTrue(report.as_json()["capture_ready"])
            self.assertEqual(report.as_json()["workflow_action"], "CAPTURE_SESSION")

    def test_capture_ready_rejects_uncertain_or_uncaptured_learning(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="paused",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[
                    {
                        "concept_ids": "C01",
                        "objective_ids": "O001",
                        "verdict": "partial",
                        "capture_state": "not_eligible",
                    }
                ],
                delivery=[
                    {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis meaning was taught."},
                    {"objective": "O002", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                    {"objective": "O003", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                ],
                coverage=[
                    {"concept": "C01", "state": "uncertain", "evidence_ids": "E001", "note": "Explanation must continue."},
                    {"concept": "C02", "state": "deferred", "evidence_ids": "none", "note": "Not taught."},
                    {"concept": "C03", "state": "deferred", "evidence_ids": "none", "note": "Not taught."},
                ],
            )
            report = validate_handoff(handoff, repo_root=root, capture_ready=True)
            self.assert_code(report, "SESSION_CONCEPT_INCOMPLETE")

            handoff, _ = build_handoff(
                root,
                status="completed",
                reviews=[("pass", "fresh-reviewer")],
            )
            handoff.write_text(
                handoff.read_text(encoding="utf-8").replace(
                    "- capture_state: captured", "- capture_state: pending", 1
                ),
                encoding="utf-8",
            )
            self.assert_code(
                validate_handoff(handoff, repo_root=root, capture_ready=True),
                "EVIDENCE_STATE",
            )

    def test_handoff_has_no_til_composition_or_scratchpad_state(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8")
            self.assertNotIn("TIL Composition", text)
            self.assertNotIn("til_finalize_policy", text)
            self.assertNotIn("draft_path", text)
            self.assertNotIn("til/today.md", text)

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

    def test_targeted_recheck_requires_the_original_reviewer(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("repair_required", "reviewer-one"), ("pass", "reviewer-one")],
            )
            self.assertTrue(validate_handoff(handoff, repo_root=root, ready=True).ok)
            text = handoff.read_text(encoding="utf-8").replace(
                "- reviewer_id: reviewer-one",
                "- reviewer_id: reviewer-two",
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "REVIEW_NOT_PASS")

    def test_true_blocker_blocks_but_second_repair_remains_resumable(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="blocked", reviews=[("blocked", "reviewer-one")])
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)
            self.assert_code(validate_handoff(handoff, repo_root=root, ready=True), "REVIEW_NOT_PASS")

            handoff, _ = build_handoff(
                root,
                status="repair_pending",
                reviews=[("repair_required", "reviewer-one"), ("repair_required", "reviewer-one")],
            )
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)
            self.assert_code(validate_handoff(handoff, repo_root=root, ready=True), "REVIEW_NOT_PASS")
            report = validate_handoff(handoff, repo_root=root)
            self.assertEqual(report.as_json()["workflow_action"], "REPAIR_CONTRACT")

    def test_reviewer_unavailability_cannot_be_recorded_as_a_semantic_blocker(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="blocked",
                reviews=[("blocked", "reviewer-one")],
            )
            text = handoff.read_text(encoding="utf-8").replace(
                "| B001 | source-access | materials/lesson.md | Required source is unavailable. |",
                "| B001 | reviewer-unavailable | semantic-reviewer | Required reviewer is unavailable. |",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(
                validate_handoff(handoff, repo_root=root),
                "REVIEW_NOT_PASS",
            )

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

    def test_review_iteration_cannot_exceed_two(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="blocked",
                reviews=[
                    ("repair_required", "reviewer-one"),
                    ("repair_required", "reviewer-one"),
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
                "| CC-DL-01 | Tensor contracts | D2 | — | explain | primary:SRC-TEST-00-01 | 부분 | 수업 내 보충 | Fixture row. |\n"
                "| TR-SYS-03 | Systems endpoint | D3 | CC-DL-01 | design | — | 없음 | 트랙 선택 시 확보 | Fixture endpoint. |\n",
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
                    f"| CC-DL-01 | Tensor contracts | D2 | — | explain | {relation} | 충분 | 그대로 사용 | Fixture row. |\n"
                    "| TR-SYS-03 | Systems endpoint | D3 | CC-DL-01 | design | — | 없음 | 트랙 선택 시 확보 | Fixture endpoint. |\n\n"
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
            capture_ready_requested=False,
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
                "### Repair Findings\n\n| Finding ID | Location | Detail |\n| --- | --- | --- |\n| none | none | none |",
                "### Repair Findings\n\n| Finding ID | Location | Detail |\n| --- | --- | --- |\n| R001 | lesson-contract | Softmax mechanics are missing. |",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "REVIEW_NOT_PASS")

            handoff, _ = build_handoff(root, status="repair_pending", reviews=[("repair_required", "another-reviewer")])
            text = handoff.read_text(encoding="utf-8").replace(
                "| R001 | lesson-contract | Revise the named contract point. |",
                "| none | none | none |",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "REVIEW_NOT_PASS")

            handoff, _ = build_handoff(root, status="repair_pending", reviews=[("repair_required", "mixed-reviewer")])
            text = handoff.read_text(encoding="utf-8").replace(
                "| none | none | none | none |",
                "| B001 | source-access | reviewer | Unexpected blocker. |",
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "REVIEW_NOT_PASS")

    def test_mutable_draft_cannot_be_a_manifest_input(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            draft.write_text("learner scratch\n", encoding="utf-8")
            text = handoff.read_text(encoding="utf-8")
            draft_hash = sha256(draft.read_bytes())
            text = text.replace(
                "<!-- lesson-contract:start -->",
                f"| I004 | til | til/today.md | {draft_hash} |\n\n<!-- lesson-contract:start -->",
                1,
            )
            manifest_hash = sha256(
                "".join(
                    sorted(
                        [
                            f"primary\tmaterials/lesson.md\t{sha256((root / 'materials/lesson.md').read_bytes())}\n",
                            f"curriculum\tCURRICULUM.md\t{sha256((root / 'CURRICULUM.md').read_bytes())}\n",
                            f"roadmap\tROADMAP.md\t{sha256((root / 'ROADMAP.md').read_bytes())}\n",
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

    def test_schema_v8_and_earlier_are_rejected_with_rebuild_error(self) -> None:
        for old_version in ("8", "7", "6", "5", "4"):
            with self.subTest(old_version=old_version), self.make_root() as directory:
                root = Path(directory)
                handoff, _ = build_handoff(root)
                handoff.write_text(
                    handoff.read_text(encoding="utf-8").replace(
                        "- schema_version: 9", f"- schema_version: {old_version}"
                    ),
                    encoding="utf-8",
                )
                report = validate_handoff(handoff, repo_root=root)
                self.assert_code(report, "SCHEMA")
                self.assertTrue(
                    any(
                        "rebuild older handoffs" in error.message
                        for error in report.errors
                    )
                )

    def test_standard_rejects_three_step_micro_but_short_accepts_it(self) -> None:
        contract = self.short_three_step_contract()
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, contract=contract, session_profile="standard")
            self.assert_code(validate_handoff(handoff, repo_root=root), "SESSION_DEPTH")

            handoff, _ = build_handoff(root, contract=contract, session_profile="short")
            report = validate_handoff(handoff, repo_root=root)
            self.assertTrue(report.ok, report.errors)

    def test_standard_requires_two_distinct_example_fixtures(self) -> None:
        duplicated_fixture = "A 2 by 3 matrix with row and feature labels."
        contract = re.sub(
            r"(?m)^(\| X00[2-4] \| [^|]+ \| )[^|]+(?= \| O)",
            rf"\g<1>{duplicated_fixture}",
            CONTRACT,
        )
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, contract=contract)
            self.assert_code(validate_handoff(handoff, repo_root=root), "SESSION_DEPTH")

    def test_completed_standard_requires_integrated_exit_attempt(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="completed", reviews=[("pass", "fresh-reviewer")])
            report = validate_handoff(handoff, repo_root=root)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.document.evidence["E001"].values["concept_ids"], "C01, C02, C03")

            handoff.write_text(
                handoff.read_text(encoding="utf-8").replace("- kind: transfer", "- kind: explain_back", 1),
                encoding="utf-8",
            )
            self.assert_code(validate_handoff(handoff, repo_root=root), "SESSION_EXIT_EVIDENCE")


    def test_v8_to_v9_paused_migration_preserves_every_learner_content_byte(self) -> None:
        answer = "기존 답변의 바이트를 그대로 보존한다.\n\n아직 확신할 수 없는 이유도 평가와 분리한다."
        with self.make_root() as directory:
            root = Path(directory)
            replacement, _ = build_handoff(
                root,
                status="paused",
                reviews=[("pass", "fresh-reviewer")],
                lesson_id="recovery-fixture",
                evidence=[
                    {
                        "concept_ids": "C01",
                        "objective_ids": "O001",
                        "content": answer,
                        "verdict": "partial",
                        "capture_state": "not_eligible",
                    }
                ],
                delivery=[
                    {"objective": "O001", "state": "delivered", "mode": "full", "note": "The earlier explanation was delivered."},
                    {"objective": "O002", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                    {"objective": "O003", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
                ],
                coverage=[
                    {"concept": "C01", "state": "uncertain", "evidence_ids": "E001", "note": "Preserved unresolved evidence."},
                    {"concept": "C02", "state": "deferred", "evidence_ids": "none", "note": "Not taught."},
                    {"concept": "C03", "state": "deferred", "evidence_ids": "none", "note": "Not taught."},
                ],
            )
            report = validate_handoff(replacement, repo_root=root)
            self.assertTrue(report.ok, report.errors)
            current = replacement.read_bytes()
            legacy = root / "tmp/legacy-v8.md"
            legacy.write_bytes(current.replace(b"- schema_version: 9", b"- schema_version: 8", 1))
            prepared = root / "tmp/prepared-v9.md"
            prepared.write_bytes(current)
            before = tuple(
                match.group(1)
                for match in re.finditer(
                    rb"(?ms)^<!-- learner-content:start -->\n(.*?)\n<!-- learner-content:end -->$",
                    legacy.read_bytes(),
                )
            )

            migrate_paused_v8_handoff(legacy, prepared, repo_root=root)
            after = tuple(
                match.group(1)
                for match in re.finditer(
                    rb"(?ms)^<!-- learner-content:start -->\n(.*?)\n<!-- learner-content:end -->$",
                    legacy.read_bytes(),
                )
            )
            self.assertEqual(after, before)
            migrated = validate_handoff(legacy, repo_root=root)
            self.assertTrue(migrated.ok, migrated.errors)
            self.assertEqual(migrated.document.metadata["status"], "paused")

            tampered = current.replace(answer.encode("utf-8"), b"changed", 1)
            prepared.write_bytes(tampered)
            legacy.write_bytes(current.replace(b"- schema_version: 9", b"- schema_version: 8", 1))
            with self.assertRaisesRegex(MigrationError, "learner-content bytes"):
                migrate_paused_v8_handoff(legacy, prepared, repo_root=root)

    def test_source_coverage_requires_every_primary_in_manifest_order(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| I001 | D001, D002, D003 | O001, O002 | G001 |",
                "| I999 | D001, D002, D003 | O001, O002 | G001 |",
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "OBJECTIVE_COVERAGE")

    def test_registered_focused_slice_ignores_global_goals_and_backmatter(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_focused_private_handoff(root)
            report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(
                report.document.lesson_source_scopes["I001"].scope_id,
                "SCOPE-TEST-00-01-01",
            )
            self.assertNotIn("book-goal", report.document.contract)
            self.assertNotIn("appendix", report.document.contract)

    def test_focused_slice_rejects_boundary_and_outside_objectives(self) -> None:
        for anchor, expected in (
            ("orientation", "LESSON_SCOPE_BOUNDARY"),
            ("book-goal", "LESSON_SCOPE_RELATION"),
        ):
            with self.subTest(anchor=anchor), self.make_root() as directory:
                root = Path(directory)
                handoff = self.build_focused_private_handoff(root)
                text = handoff.read_text(encoding="utf-8").replace(
                    "#shape-propagation | Predict the output shape",
                    f"#{anchor} | Predict the output shape",
                    1,
                )
                handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
                self.assert_code(validate_handoff(handoff, repo_root=root), expected)

    def test_registered_scope_must_exactly_match_index_row(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_focused_private_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "Tensor axes [materials/private/example-course/00-01_lesson.md#axes]; Broadcast propagation [materials/private/example-course/00-01_lesson.md#shape-propagation]",
                "Tensor axes [materials/private/example-course/00-01_lesson.md#axes]",
                1,
            )
            handoff.write_text(refresh_contract_hash(text), encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "LESSON_SCOPE")

    def test_ephemeral_focused_slice_is_valid_without_a_registered_scope_id(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_focused_private_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| I001 | registered-slice | SCOPE-TEST-00-01-01 |",
                "| I001 | ephemeral-slice | none |",
                1,
            )
            text = refresh_contract_hash(text)
            contract_start = text.index("<!-- lesson-contract:start -->") + len(
                "<!-- lesson-contract:start -->\n"
            )
            contract_end = text.index("\n<!-- lesson-contract:end -->")
            text = re_sub_field(
                text,
                "reviewed_contract_sha256",
                sha256(text[contract_start:contract_end]),
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertTrue(report.ok, report.errors)

    def test_large_pdf_focused_review_stays_bounded_to_the_selected_pages(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_large_pdf_focused_handoff(root)
            report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertTrue(report.ok, report.errors)
            assert report.document is not None
            scope = report.document.lesson_source_scopes["I001"]
            self.assertEqual(1, len(scope.included_units))
            self.assertEqual(2, len(scope.boundary_units))
            self.assertNotIn("page-630", report.document.contract)
            self.assertNotIn("appendix", report.document.contract.lower())
            self.assertLess(len(report.document.contract), 15_000)

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
            text = handoff.read_text(encoding="utf-8").replace("| C01 | deferred | none | Not taught yet. |", "| C01 | deferred | none | G001 was not taught. |")
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "SESSION_CONCEPT_INCOMPLETE")

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
                "| CC-DL-01 | Tensor contracts | D2 | — | explain | primary:SRC-TEST-00-01 | 부분 | 별도 자료 확보 | Fixture row. |\n"
                "| TR-SYS-03 | Systems endpoint | D3 | CC-DL-01 | design | — | 없음 | 트랙 선택 시 확보 | Fixture endpoint. |\n",
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
            block_one = text[start_one:start_two]
            reordered = (
                block_one.replace("- concept_ids: C01", "- concept_ids: C02")
                .replace("- objective_ids: O001", "- objective_ids: O002")
                .replace("- example_id: X001", "- example_id: X002")
            )
            text = text[:start_one] + reordered + text[start_two:]
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
                "| C01 | uncertain | none | Taught but not demonstrated. |",
                "| C01 | deferred | none | Not taught yet. |",
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
                "| CC-DL-01 | Tensor contracts | D2 | — | explain | primary:SRC-TEST-00-01 | 충분 | 그대로 사용 | Fixture row. |\n"
                "| TR-SYS-03 | Systems endpoint | D3 | CC-DL-01 | design | — | 없음 | 트랙 선택 시 확보 | Fixture endpoint. |\n\n"
                "## exact-location\n",
                encoding="utf-8",
            )
            source_hash = sha256(source.read_bytes())
            curriculum_hash = sha256(curriculum.read_bytes())
            roadmap = root / "ROADMAP.md"
            roadmap.write_text(
                "# Roadmap\n\n## 정적 목표 endpoint\n\n"
                "| 우선순위 | 단계 | 방향 | Endpoint |\n"
                "| ---: | ---: | --- | --- |\n"
                "| 1 | `1A` | Systems | `TR-SYS-03` |\n",
                encoding="utf-8",
            )
            roadmap_hash = sha256(roadmap.read_bytes())
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
            text = text.replace("| I004 | roadmap |", "| I003 | roadmap |")
            text = text.replace(
                "| I001 | primary | materials/lesson.md | replace-with-file-sha256 |",
                f"| I001 | primary | materials/lesson.md | {source_hash} |",
            )
            text = text.replace(
                "| I002 | curriculum | CURRICULUM.md | replace-with-file-sha256 |",
                f"| I002 | curriculum | CURRICULUM.md | {curriculum_hash} |",
            )
            text = text.replace(
                "| I003 | roadmap | ROADMAP.md | replace-with-file-sha256 |",
                f"| I003 | roadmap | ROADMAP.md | {roadmap_hash} |",
            )
            manifest_hash = sha256(
                "".join(
                    sorted(
                        [
                            f"primary\tmaterials/lesson.md\t{source_hash}\n",
                            f"curriculum\tCURRICULUM.md\t{curriculum_hash}\n",
                            f"roadmap\tROADMAP.md\t{roadmap_hash}\n",
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
            self.assertIsNotNone(report.document.semantic_review)
            self.assertEqual(report.document.semantic_review.iteration, 0)
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
            roadmap_hash = sha256((REPO / "ROADMAP.md").read_bytes())
            import re

            text = re.sub(
                r"\| I002 \| curriculum \| CURRICULUM\.md \| [0-9a-f]{64} \|",
                f"| I002 | curriculum | CURRICULUM.md | {curriculum_hash} |",
                text,
                count=1,
            )
            text = re.sub(
                r"\| I003 \| roadmap \| ROADMAP\.md \| [0-9a-f]{64} \|",
                f"| I003 | roadmap | ROADMAP.md | {roadmap_hash} |",
                text,
                count=1,
            )
            manifest_hash = sha256(
                "".join(
                    sorted(
                        [
                            f"primary\t{relative_directory.as_posix()}/materials/lesson.md\t{source_hash}\n",
                            f"curriculum\tCURRICULUM.md\t{curriculum_hash}\n",
                            f"roadmap\tROADMAP.md\t{roadmap_hash}\n",
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
                "--capture-ready",
                "tmp/active-lesson-handoff.md",
            ],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(conflict.returncode, 2)
        self.assertEqual(conflict.stdout, "")
        self.assertRegex(conflict.stderr, r"^ERROR <cli>:1 \[SCHEMA\] argument --capture-ready: not allowed with argument --ready\n$")


def re_sub_field(text: str, key: str, value: str) -> str:
    import re

    return re.sub(rf"^- {re.escape(key)}: .*$", f"- {key}: {value}", text, count=1, flags=re.MULTILINE)


def refresh_contract_hash(text: str) -> str:
    start = text.index("<!-- lesson-contract:start -->") + len("<!-- lesson-contract:start -->\n")
    end = text.index("\n<!-- lesson-contract:end -->")
    return re_sub_field(text, "contract_sha256", sha256(text[start:end]))


if __name__ == "__main__":
    unittest.main()
