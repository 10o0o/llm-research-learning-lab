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
        "START_TARGET",
        "CONTINUE_TARGET",
        "BRIDGE_PREREQUISITE",
        "NEED_DIAGNOSTIC",
        "NO_ACTIONABLE_TARGET",
        "REPAIR_REQUIRED",
        "NONE",
        "CONTINUE_EXISTING_PRACTICE",
        "CONTINUE_LOCAL_SOURCE",
        "USE_TEMPORARY_EXTERNAL_SOURCE",
        "AWAIT_SOURCE_APPROVAL",
        "NO_NEW_SOURCE_NEEDED",
        "LOCAL_REGISTERED",
        "EPHEMERAL",
        "REGISTRATION_RECOMMENDED",
        "satisfied",
        "bridgeable",
        "blocking",
        "unknown",
    ):
        assert f"`{value}`" in text


def test_target_selection_is_source_independent_and_stat110_is_conditional() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    scenarios = SCENARIOS.read_text(encoding="utf-8")
    assert "Source availability never changes target priority" in text
    assert "only when `CC-PROB-01` is the selected target" in text
    assert "CONTINUE_LOCAL_SOURCE" in scenarios
    assert "Systems variant does not choose probability" in scenarios


def test_forward_scenarios_are_complete_and_non_persistent() -> None:
    text = SCENARIOS.read_text(encoding="utf-8")
    headings = re.findall(r"^## (F\d{2}) ", text, re.MULTILINE)
    assert headings == ["F01", "F02", "F03", "F04", "F05", "F06"]
    for scenario_id in headings:
        start = text.index(f"## {scenario_id} ")
        next_match = re.search(r"^## F\d{2} ", text[start + 1 :], re.MULTILINE)
        end = start + 1 + next_match.start() if next_match else len(text)
        body = text[start:end]
        assert "- Prompt:" in body
        assert "- Fixture" in body
        assert "- Expected invariants:" in body
    assert "do not save its generated answer" in text


def test_target_first_ranking_and_practice_reuse_invariants_are_explicit() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    ranking = [
        "an exact target named by the user",
        "a blocking prerequisite on the path",
        "the active target when it still lacks required learner evidence",
        "unlocks the greatest number of downstream targets",
    ]
    positions = [text.index(item) for item in ranking]
    assert positions == sorted(positions)
    for condition in (
        "directly names the primary target or bridge target",
        "still-required execution evidence token",
        "not paused or explicitly deferred",
        "no unresolved conceptual blocker",
        "frontier prerequisite",
        "merely `bridgeable` prerequisite",
        "Curriculum row order only as a reproducible final ordering",
    ):
        assert condition in text


def test_diagnostic_action_and_evidence_aggregation_are_unambiguous() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "For `NEED_DIAGNOSTIC`" in text
    assert "`learning_action: NO_NEW_SOURCE_NEEDED`" in text
    assert "`source_persistence: NONE`" in text
    assert "`NEED_DIAGNOSTIC` retains the tentative" in text
    assert "`bridge_target: none`" in text
    assert "materially distinct behaviors named by that target row" in text


def test_repository_rules_keep_planner_target_first_and_read_only() -> None:
    text = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "select one primary Curriculum target" in text
    assert "one blocking bridge" in text
    assert "Source availability affects executability after selection, not target priority" in text
    assert "The planner remains read-only" in text
