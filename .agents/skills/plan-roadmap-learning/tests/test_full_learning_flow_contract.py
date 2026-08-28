from __future__ import annotations

import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]


def _text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


def test_full_flow_is_one_explicit_cycle_with_exact_commit_boundaries() -> None:
    agents = _text(REPO / "AGENTS.md")
    usage = _text(REPO / "USAGE.md")
    for phrase in (
        "full learning flow",
        "one complete cycle",
        "practice: complete <artifact-stem>",
        "zero to three evidence-backed knowledge notes",
        "preview the next target",
    ):
        assert phrase in agents
    for phrase in (
        "전체 흐름으로 진행해줘",
        "현재 대화의 한 학습 사이클",
        "practice: complete <artifact-stem>",
        "다음 target preview",
    ):
        assert phrase in usage


def test_full_flow_never_substitutes_learner_work_or_broadens_external_authority() -> None:
    agents = _text(REPO / "AGENTS.md")
    usage = _text(REPO / "USAGE.md")
    for phrase in (
        "never permits the agent to supply learner answers",
        "permanent source registration",
        "paid or authenticated downloads",
        "external participation or submission",
        "do not authorize practice, knowledge, or next-target continuation",
    ):
        assert phrase in agents
    for phrase in (
        "learner-owned 구현·실행 대행",
        "permanent source 등록",
        "외부 challenge·competition 참여나 제출",
        "전체 흐름 권한으로 넓어지지는 않습니다",
    ):
        assert phrase in usage


def test_no_new_orchestration_skill_or_progress_snapshot_contract() -> None:
    skill_names = {
        path.parent.name
        for path in (REPO / ".agents/skills").glob("*/SKILL.md")
    }
    assert not any("orchestrat" in name or "full-flow" in name for name in skill_names)
    agents = _text(REPO / "AGENTS.md")
    assert "do not create an orchestration skill, snapshot, or progress database" in agents
