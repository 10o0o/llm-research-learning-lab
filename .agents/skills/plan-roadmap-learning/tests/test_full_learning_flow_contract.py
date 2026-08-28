from __future__ import annotations

import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]


def _text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


def test_full_day_flow_repeats_cycles_with_exact_commit_boundaries() -> None:
    agents = _text(REPO / "AGENTS.md")
    usage = _text(REPO / "USAGE.md")
    for phrase in (
        "same-Asia/Seoul-day sequence of cycles",
        "exact completion-ready practice commit",
        "zero to three knowledge updates or `NO_CHANGE`",
        "next-target calculation",
        "preparation of the next reviewed lesson",
    ):
        assert phrase in agents
    for phrase in (
        "오늘 전체 학습 흐름 시작",
        "60~90분 표준 수업",
        "학습자가 직접 구현·실행·해석",
        "knowledge를 0~3개 갱신",
        "다음 target을 계산",
    ):
        assert phrase in usage


def test_full_day_flow_never_substitutes_learner_work_or_broadens_external_authority() -> None:
    agents = _text(REPO / "AGENTS.md")
    usage = _text(REPO / "USAGE.md")
    for phrase in (
        "Full-day authorization never permits learner answers",
        "learner-owned practice",
        "permanent source registration",
        "paid/authenticated downloads",
        "external participation or submission",
        "TIL saving, or push",
    ):
        assert phrase in agents
    for phrase in (
        "학습자 대신 답하거나 learner-owned practice를 구현하는 일",
        "permanent source 등록",
        "외부 계정 접근, 대회 참여 또는 제출",
        "TIL 자동 저장",
    ):
        assert phrase in usage


def test_no_new_orchestration_skill_or_progress_snapshot_contract() -> None:
    skill_names = {
        path.parent.name
        for path in (REPO / ".agents/skills").glob("*/SKILL.md")
    }
    assert not any("orchestrat" in name or "full-flow" in name for name in skill_names)
    agents = _text(REPO / "AGENTS.md")
    usage = _text(REPO / "USAGE.md")
    assert "Do not create an orchestration skill, snapshot, or progress database" in agents
    assert "하나의 거대 orchestration skill이나 별도 progress DB는 두지 않습니다" in usage
