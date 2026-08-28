from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


TEACH_SKILL = Path(__file__).resolve().parents[1]
COACH_SKILL = TEACH_SKILL.parent / "coach-llm-research-study"
sys.path.insert(0, str(TEACH_SKILL / "scripts"))
sys.path.insert(0, str(COACH_SKILL / "scripts"))
sys.path.insert(0, str(COACH_SKILL / "tests"))

from append_lesson_evidence import append_evidence  # noqa: E402
from daily_learning_flow import (  # noqa: E402
    begin_cycle,
    empty_flow,
    save_flow,
    start_flow,
    transition_phase,
)
from handoff_fixture import build_handoff  # noqa: E402
from validate_lesson_handoff import validate_handoff  # noqa: E402


def delivered_o001() -> list[dict[str, str]]:
    return [
        {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis meaning was taught."},
        {"objective": "O002", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
        {"objective": "O003", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
    ]


def initialize_cursor(root: Path) -> None:
    state = start_flow(empty_flow(), mode="full-day")
    state = begin_cycle(
        state,
        cycle_id="cycle-tensor-shape-lesson",
        primary_target="CC-DL-01",
    )
    state = transition_phase(state, "PREPARE_LESSON")
    state = transition_phase(state, "TEACH")
    save_flow(state, root)


class AppendLessonEvidenceTests(unittest.TestCase):
    def test_confirmed_evidence_is_captured_once_without_touching_manual_scratchpad(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_cursor(root)
            scratch = root / "til/today.md"
            scratch.parent.mkdir(parents=True)
            scratch.write_text("# 수동 메모\n", encoding="utf-8")
            content = "배치 축은 예시 두 개를, 특성 축은 각 예시의 세 값을 나타낸다."
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"content": content, "assessment": "학습자가 두 축을 정확히 구분했다."}],
                delivery=delivered_o001(),
            )

            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 0, message)
            self.assertIn("CAPTURED", message)
            self.assertEqual(scratch.read_text(encoding="utf-8"), "# 수동 메모\n")
            cursor = json.loads((root / "tmp/active-learning-flow.json").read_text(encoding="utf-8"))
            self.assertEqual(cursor["cycles"][0]["learner_evidence"][0]["content"], content)
            first_cursor = (root / "tmp/active-learning-flow.json").read_bytes()
            first_handoff = handoff.read_bytes()
            self.assertIn(b"- capture_state: captured", first_handoff)

            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 0, message)
            self.assertIn("ALREADY_CAPTURED", message)
            self.assertEqual((root / "tmp/active-learning-flow.json").read_bytes(), first_cursor)
            self.assertEqual(handoff.read_bytes(), first_handoff)

    def test_cursor_first_retry_recovers_a_pending_handoff_without_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_cursor(root)
            content = "결과 shape는 두 입력의 broadcast 가능한 축을 합쳐 얻는다."
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"content": content}],
                delivery=delivered_o001(),
            )
            original = handoff.read_text(encoding="utf-8")
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 0, message)
            handoff.write_text(original, encoding="utf-8")

            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 0, message)
            self.assertIn("CAPTURED", message)
            cursor = json.loads((root / "tmp/active-learning-flow.json").read_text(encoding="utf-8"))
            self.assertEqual(len(cursor["cycles"][0]["learner_evidence"]), 1)

    def test_partial_or_tutor_authored_evidence_never_enters_cursor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_cursor(root)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"verdict": "partial", "capture_state": "not_eligible"}],
            )
            original_cursor = (root / "tmp/active-learning-flow.json").read_bytes()
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 1)
            self.assertIn("EVIDENCE_STATE", message)
            self.assertEqual((root / "tmp/active-learning-flow.json").read_bytes(), original_cursor)

            text = handoff.read_text(encoding="utf-8").replace(
                "- provenance: learner", "- provenance: tutor"
            )
            handoff.write_text(text, encoding="utf-8")
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertNotEqual(code, 0)
            self.assertIn("EVIDENCE_STATE", message)
            self.assertEqual((root / "tmp/active-learning-flow.json").read_bytes(), original_cursor)

    def test_missing_or_mismatched_cycle_is_rejected_without_handoff_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"content": "축을 구분했다."}],
                delivery=delivered_o001(),
            )
            original = handoff.read_bytes()
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 1)
            self.assertIn("FLOW_STATE", message)
            self.assertEqual(handoff.read_bytes(), original)

            state = start_flow(empty_flow(), mode="full-day")
            state = begin_cycle(state, cycle_id="different-cycle", primary_target="CC-DL-01")
            state = transition_phase(state, "PREPARE_LESSON")
            state = transition_phase(state, "TEACH")
            save_flow(state, root)
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 1)
            self.assertIn("no cycle", message)
            self.assertEqual(handoff.read_bytes(), original)

    def test_multiline_answer_is_preserved_byte_for_byte_in_cursor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize_cursor(root)
            content = "첫 줄\n\n```python\nx = (2, 3)\n```\n\n마지막 줄"
            handoff, _ = build_handoff(
                root,
                status="paused",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"content": content}],
                delivery=delivered_o001(),
            )
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 0, message)
            cursor = json.loads((root / "tmp/active-learning-flow.json").read_text(encoding="utf-8"))
            self.assertEqual(cursor["cycles"][0]["learner_evidence"][0]["content"].encode(), content.encode())
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)


if __name__ == "__main__":
    unittest.main()
