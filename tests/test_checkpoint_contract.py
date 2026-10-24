"""Static scenario-to-instruction contracts, NOT an agent behavior or save-engine test.

Synthetic prompts never become real STATE. Each fixture requires the active guide
 to cover the response obligation; this cannot prove an LLM follows it at runtime.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'AGENTS.md'

class CheckpointContractTests(unittest.TestCase):
    def test_synthetic_scenarios_have_active_instructions(self):
        guide = (ROOT / SOURCE).read_text(encoding="utf-8")
        cases = json.loads((ROOT / "tests/fixtures/checkpoint_scenarios.json").read_text(encoding="utf-8"))
        self.assertEqual({case["id"] for case in cases}, {
            "end_incomplete", "mid_session", "resume", "failed_save", "no_new_evidence"
        })
        for case in cases:
            with self.subTest(scenario=case["id"]):
                self.assertTrue(case["scenario"])
                for phrase in case["required"]:
                    self.assertIn(phrase, guide)
                for phrase in case["forbidden"]:
                    self.assertNotIn(phrase, guide)

    def test_no_fake_learning_or_new_state_store(self):
        guide = (ROOT / SOURCE).read_text(encoding="utf-8")
        for phrase in ("STATE는 하나만", "완료·AC·독립 해결·숙달 판정과 북마크 저장은 별개", "로컬 저장·커밋·원격 반영"):
            self.assertIn(phrase, guide)
        state = (ROOT / "STATE.md").read_text(encoding="utf-8")
        self.assertNotIn("합성 과제", state)

if __name__ == "__main__":
    unittest.main()
