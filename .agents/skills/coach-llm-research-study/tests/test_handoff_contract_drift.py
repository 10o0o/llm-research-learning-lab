from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
REFERENCE = SKILL / "references/lesson-handoff.md"
TEMPLATE = SKILL / "assets/active-lesson-handoff-template.md"
FIXTURE = SKILL / "tests/handoff_fixture.py"
VALIDATOR = SKILL / "scripts/validate_lesson_handoff.py"

SPEC = importlib.util.spec_from_file_location("handoff_validator_drift_test", VALIDATOR)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class HandoffContractDriftTests(unittest.TestCase):
    def test_schema_version_is_shared_by_code_reference_template_and_fixture(self) -> None:
        version = MODULE.SCHEMA_VERSION
        self.assertEqual(version, "9")
        self.assertIn(f"currently `{version}`", REFERENCE.read_text(encoding="utf-8"))
        self.assertIn(f"- schema_version: {version}", TEMPLATE.read_text(encoding="utf-8"))
        self.assertIn(f"- schema_version: {version}", FIXTURE.read_text(encoding="utf-8"))

    def test_all_three_consumer_skills_link_to_the_single_contract(self) -> None:
        expected = {
            SKILL / "SKILL.md": "(references/lesson-handoff.md)",
            REPO / ".agents/skills/teach-course-material/SKILL.md": "(../coach-llm-research-study/references/lesson-handoff.md)",
            REPO / ".agents/skills/suggest-learning-practice/SKILL.md": "(../coach-llm-research-study/references/lesson-handoff.md)",
        }
        for path, link in expected.items():
            with self.subTest(path=path):
                self.assertIn(link, path.read_text(encoding="utf-8"))

    def test_consumer_guides_do_not_redeclare_normative_handoff_sections(self) -> None:
        consumers = [
            SKILL / "SKILL.md",
            REPO / ".agents/skills/teach-course-material/SKILL.md",
            REPO / ".agents/skills/suggest-learning-practice/SKILL.md",
            REPO / "AGENTS.md",
            REPO / "USAGE.md",
        ]
        forbidden = (
            "## Semantic Review",
            "## Current Position",
            "## Objective Delivery",
            "## Session Concept Coverage",
            "schema_version:",
            "review_iteration:",
            "--ready",
            "--capture-ready",
        )
        for path in consumers:
            text = path.read_text(encoding="utf-8")
            for detail in forbidden:
                with self.subTest(path=path, detail=detail):
                    self.assertNotIn(detail, text)

    def test_reference_declares_itself_the_only_normative_contract(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("sole normative specification", text)


if __name__ == "__main__":
    unittest.main()
