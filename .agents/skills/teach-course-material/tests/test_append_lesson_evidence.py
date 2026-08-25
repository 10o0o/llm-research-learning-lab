from __future__ import annotations

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
from handoff_fixture import build_handoff, draft_envelope  # noqa: E402
from validate_lesson_handoff import validate_handoff  # noqa: E402


def delivered_o001() -> list[dict[str, str]]:
    return [
        {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis meaning was taught."},
        {"objective": "O002", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
        {"objective": "O003", "state": "pending", "mode": "none", "note": "Awaiting instruction."},
    ]


class AppendLessonEvidenceTests(unittest.TestCase):
    def test_confirmed_evidence_is_appended_once_and_state_becomes_drafted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
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
            self.assertIn("APPENDED", message)
            draft = root / "til/today.md"
            first_draft = draft.read_text(encoding="utf-8")
            first_handoff = handoff.read_text(encoding="utf-8")
            self.assertIn(content, first_draft)
            self.assertNotIn("학습자가 두 축을 정확히 구분했다.", first_draft)
            self.assertIn("- append_state: drafted", first_handoff)
            self.assertEqual(first_draft.count("<!-- lesson-evidence:tensor-shape-lesson:E001:"), 1)

            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 0, message)
            self.assertIn("ALREADY_APPENDED", message)
            self.assertEqual(draft.read_text(encoding="utf-8"), first_draft)
            self.assertEqual(handoff.read_text(encoding="utf-8"), first_handoff)

    def test_crash_between_draft_and_handoff_writes_is_recovered_without_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = "결과 shape는 두 입력의 broadcast 가능한 축을 합쳐 얻는다."
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"content": content}],
                delivery=delivered_o001(),
            )
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            existing = "내 기존 메모\n\n" + draft_envelope("tensor-shape-lesson", "E001", content)
            draft.write_text(existing, encoding="utf-8")

            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 0, message)
            self.assertIn("RECOVERED", message)
            self.assertEqual(draft.read_text(encoding="utf-8"), existing)
            self.assertIn("- append_state: drafted", handoff.read_text(encoding="utf-8"))

    def test_partial_or_tutor_authored_evidence_is_never_appended(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"verdict": "partial", "append_state": "not_eligible"}],
            )
            original = handoff.read_text(encoding="utf-8")
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 1)
            self.assertIn("EVIDENCE_STATE", message)
            self.assertFalse((root / "til/today.md").exists())
            self.assertEqual(handoff.read_text(encoding="utf-8"), original)

            text = original.replace("- provenance: learner", "- provenance: tutor")
            handoff.write_text(text, encoding="utf-8")
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertNotEqual(code, 0)
            self.assertIn("EVIDENCE_STATE", message)
            self.assertFalse((root / "til/today.md").exists())

    def test_existing_draft_content_and_multiline_learner_answer_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = "첫 줄\n\n```python\nx = (2, 3)\n```\n\n마지막 줄"
            handoff, _ = build_handoff(
                root,
                status="paused",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"content": content}],
                delivery=delivered_o001(),
            )
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            prefix = "# 오늘 메모\n\n기존 내용\n"
            draft.write_text(prefix, encoding="utf-8")
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 0, message)
            written = draft.read_text(encoding="utf-8")
            self.assertTrue(written.startswith(prefix))
            self.assertIn("\n" + content + "\n<!-- /lesson-evidence", written)
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)

    def test_mismatched_existing_envelope_is_rejected_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = "올바른 학습자 답변"
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"content": content}],
            )
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            draft.write_text(
                draft_envelope("tensor-shape-lesson", "E001", content).replace(content, "변조된 답변"),
                encoding="utf-8",
            )
            original_handoff = handoff.read_text(encoding="utf-8")
            original_draft = draft.read_text(encoding="utf-8")
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 1)
            self.assertIn("DRAFT_CONTENT", message)
            self.assertEqual(draft.read_text(encoding="utf-8"), original_draft)
            self.assertEqual(handoff.read_text(encoding="utf-8"), original_handoff)

    def test_drafted_state_without_marker_is_not_silently_reappended(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"append_state": "drafted"}],
            )
            code, message = append_evidence(handoff, "E001", repo_root=root)
            self.assertEqual(code, 1)
            self.assertIn("DRAFT_MARKER", message)
            self.assertFalse((root / "til/today.md").exists())


if __name__ == "__main__":
    unittest.main()
