from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
SCRIPT = SKILL / "scripts/prepare_til_input.py"
COACH_TESTS = REPO / ".agents/skills/coach-llm-research-study/tests"
sys.path.insert(0, str(COACH_TESTS))
sys.path.insert(0, str(SKILL / "scripts"))

SPEC = importlib.util.spec_from_file_location("prepare_til_input_under_test", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

from handoff_fixture import build_handoff, draft_envelope, sha256  # noqa: E402
from compose_lesson_til import compose_lesson_til  # noqa: E402


class PrepareTilInputTests(unittest.TestCase):
    def test_standalone_canonical_draft_is_byte_preserving(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            original = b"# \xec\x98\xa4\xeb\x8a\x98\xec\x9d\x98 \xed\x95\x99\xec\x8a\xb5\r\n\r\n\xeb\x82\xb4 \xeb\xac\xb8\xec\x9e\xa5\r\n"
            draft.write_bytes(original)
            prepared = MODULE.prepare_til_input(repo_root=root)
            self.assertEqual(prepared.encode("utf-8"), original)

    def test_active_non_ready_handoff_blocks_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            draft.write_text("# 오늘의 학습\n\n진행 중\n", encoding="utf-8")
            handoff, _ = build_handoff(root)
            draft_before = draft.read_bytes()
            handoff_before = handoff.read_bytes()
            with self.assertRaisesRegex(MODULE.PreflightError, "not TIL-ready"):
                MODULE.prepare_til_input(repo_root=root)
            self.assertEqual(draft.read_bytes(), draft_before)
            self.assertEqual(handoff.read_bytes(), handoff_before)

    def test_til_ready_handoff_returns_marker_free_input_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = "배치 축과 특성 축을 구분해 설명했다."
            question = "오른쪽 축부터 비교하는 이유는 무엇인가?"
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            draft.write_text(
                draft_envelope("tensor-shape-lesson", "E001", content),
                encoding="utf-8",
            )
            handoff, _ = build_handoff(
                root,
                status="paused",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[
                    {"concept_ids": "C01", "objective_ids": "O001", "content": content, "append_state": "drafted"},
                    {
                        "concept_ids": "C02",
                        "objective_ids": "O002",
                        "content": question,
                        "verdict": "unconfirmed",
                        "append_state": "not_eligible",
                    },
                ],
                coverage=[
                    {"concept": "C01", "state": "confirmed", "evidence_ids": "E001", "representation": "learning", "note": "Learner answer is drafted."},
                    {"concept": "C02", "state": "uncertain", "evidence_ids": "E002", "representation": "remaining-question", "note": "The unresolved learner question is represented."},
                    {"concept": "C03", "state": "deferred", "evidence_ids": "none", "representation": "not-required", "note": "Not taught today."},
                ],
                delivery=[
                    {"objective": "O001", "state": "delivered", "mode": "full", "note": "Axis meaning was taught."},
                    {"objective": "O002", "state": "delivered", "mode": "full", "note": "Broadcasting was taught."},
                    {"objective": "O003", "state": "pending", "mode": "none", "note": "Not taught today."},
                ],
            )
            compose_lesson_til(
                handoff,
                [
                    {
                        "section": "오늘의 학습",
                        "evidence_ids": ["E001"],
                        "representation": "learning",
                        "text": content,
                    },
                    {
                        "section": "남은 질문",
                        "evidence_ids": ["E002"],
                        "representation": "remaining-question",
                        "text": question,
                    },
                ],
                repo_root=root,
                composed_at="2026-08-20T02:00:00Z",
            )
            draft_before = draft.read_bytes()
            handoff_before = handoff.read_bytes()
            prepared = MODULE.prepare_til_input(repo_root=root)
            self.assertIn(content, prepared)
            self.assertNotIn("lesson-evidence:", prepared)
            self.assertEqual(draft.read_bytes(), draft_before)
            self.assertEqual(handoff.read_bytes(), handoff_before)

            corrupted = draft.read_text(encoding="utf-8").replace(
                f":{sha256(content)} -->",
                f":{'0' * 64} -->",
                1,
            )
            draft.write_text(corrupted, encoding="utf-8")
            handoff_text = handoff.read_text(encoding="utf-8").replace(
                f"- draft_sha256: {sha256(draft_before)}",
                f"- draft_sha256: {sha256(draft.read_bytes())}",
            )
            handoff.write_text(handoff_text, encoding="utf-8")
            failed_draft = draft.read_bytes()
            failed_handoff = handoff.read_bytes()
            with self.assertRaisesRegex(MODULE.PreflightError, "not TIL-ready"):
                MODULE.prepare_til_input(repo_root=root)
            self.assertEqual(draft.read_bytes(), failed_draft)
            self.assertEqual(handoff.read_bytes(), failed_handoff)

    def test_marker_without_handoff_is_rejected_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            draft.write_text(
                draft_envelope("tensor-shape-lesson", "E001", "학습자 답변"),
                encoding="utf-8",
            )
            before = draft.read_bytes()
            with self.assertRaisesRegex(MODULE.PreflightError, "no active handoff"):
                MODULE.prepare_til_input(repo_root=root)
            self.assertEqual(draft.read_bytes(), before)

    def test_explicit_standalone_draft_ignores_active_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            standalone = root / "notes/rough.md"
            standalone.parent.mkdir(parents=True)
            standalone.write_text("# 독립 메모\n", encoding="utf-8")
            handoff, _ = build_handoff(root)
            handoff_before = handoff.read_bytes()
            self.assertEqual(
                MODULE.prepare_til_input("notes/rough.md", repo_root=root),
                "# 독립 메모\n",
            )
            self.assertEqual(handoff.read_bytes(), handoff_before)


if __name__ == "__main__":
    unittest.main()
