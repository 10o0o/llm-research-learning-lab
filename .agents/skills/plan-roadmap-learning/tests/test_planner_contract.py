from __future__ import annotations

import re
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
ENTRYPOINT = SKILL / "SKILL.md"
CONTRACT = SKILL / "references/planner-contract.md"
SCENARIOS = SKILL / "references/forward-test-scenarios.md"


def test_skill_routes_runtime_and_maintenance_references() -> None:
    text = ENTRYPOINT.read_text(encoding="utf-8")
    assert "references/planner-contract.md" in text
    assert "references/forward-test-scenarios.md" in text
    assert "read-only reviewer" in text


def test_action_and_prerequisite_contract_is_complete() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    for value in (
        "REPAIR_REQUIRED",
        "NONE",
        "CONTINUE_EXISTING_PRACTICE",
        "CONTINUE_LOCAL_SOURCE",
        "PROPOSE_EXTERNAL_SOURCE",
        "NO_NEW_SOURCE_NEEDED",
        "satisfied",
        "bridgeable",
        "blocking",
        "unknown",
    ):
        assert f"`{value}`" in text


def test_stat110_pilot_is_retired_after_registration() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    scenarios = SCENARIOS.read_text(encoding="utf-8")
    assert "Temporary Stat110 pilot" not in text
    assert "Pending Stat110 artifact" not in scenarios
    assert "Registered Stat110 artifact" in scenarios
    assert "CONTINUE_LOCAL_SOURCE" in scenarios
    assert "registered but stale" in scenarios
    assert "not to propose an alternative source" in scenarios
    assert "retired external-source pilot" in scenarios
    assert "persisting candidate state" in scenarios


def test_forward_scenarios_are_complete_and_non_persistent() -> None:
    text = SCENARIOS.read_text(encoding="utf-8")
    headings = re.findall(r"^## (F\d{2}) ", text, re.MULTILINE)
    assert headings == ["F01", "F02", "F03", "F04"]
    for scenario_id in headings:
        start = text.index(f"## {scenario_id} ")
        next_match = re.search(r"^## F\d{2} ", text[start + 1 :], re.MULTILINE)
        end = start + 1 + next_match.start() if next_match else len(text)
        body = text[start:end]
        assert "- Prompt:" in body
        assert "- Fixture" in body
        assert "- Expected invariants:" in body
    assert "do not save its generated answer" in text


def test_repository_rules_route_only_undecided_requests_through_planner() -> None:
    text = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "when the next target or source is undecided" in text
    assert "Use `$plan-roadmap-learning` first only when" in text
