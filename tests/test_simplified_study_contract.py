from __future__ import annotations

import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def _normalized(path: str) -> str:
    return re.sub(r"\s+", " ", (REPO / path).read_text(encoding="utf-8"))


def test_plain_study_phrases_use_state() -> None:
    agents = _normalized("AGENTS.md")
    for phrase in (
        "`오늘 학습 시작`: teach one connected module",
        "`오늘 전체 학습 흐름 시작` or `전체 학습 흐름 시작`",
        "`계속`: resume the next independent action written in `STATE.md`",
        "`오늘 학습 종료`: stop",
    ):
        assert phrase in agents
    assert "There is no fallback route" in agents


def test_removed_learning_management_skills_do_not_return() -> None:
    removed = (
        "plan-roadmap-learning",
        "coach-llm-research-study",
        "teach-course-material",
        "suggest-learning-practice",
    )
    for name in removed:
        assert not (REPO / ".agents/skills" / name).exists()

    active_docs = " ".join(
        _normalized(path)
        for path in ("AGENTS.md", "README.md", "USAGE.md", "ROADMAP.md", "CURRICULUM.md")
    )
    for dead_surface in (
        "active-learning-flow",
        "active-lesson-handoff",
        "lesson-handoff",
        "legacy daily-flow",
    ):
        assert dead_surface not in active_docs


def test_roadmap_and_curriculum_cannot_select_the_current_target() -> None:
    roadmap = _normalized("ROADMAP.md")
    curriculum = _normalized("CURRICULUM.md")
    assert "현재 학습 범위와 다음 행동은 [`STATE.md`](./STATE.md)만 정합니다" in roadmap
    assert "어떤 기록도 새 강의나 추가 실습을 자동으로 선택하지 않습니다" in roadmap
    assert "현재 학습 범위와 다음 행동은 `STATE.md`만 정하며" in curriculum
    assert "실제 파일과 `INDEX.md`를 수동으로 교차 확인한다" in curriculum


def test_remaining_utilities_are_explicit_and_never_commit() -> None:
    expected = {"save-today-til", "update-learning-knowledge"}
    actual = {
        path.parent.name for path in (REPO / ".agents/skills").glob("*/SKILL.md")
    }
    assert actual == expected

    for name in expected:
        entrypoint = _normalized(f".agents/skills/{name}/SKILL.md")
        manifest = _normalized(f".agents/skills/{name}/agents/openai.yaml")
        assert "Use only when the learner" in entrypoint
        assert "Commit and push each require a separate explicit request" in entrypoint
        assert "allow_implicit_invocation: false" in manifest


def test_state_is_a_public_bookmark_with_one_next_action() -> None:
    state = (REPO / "STATE.md").read_text(encoding="utf-8")
    assert "재개 북마크" in state
    assert state.count("## 다음 독립 행동") == 1
    assert "https://cs336.stanford.edu/" in state
    assert "a158843b20107949f1a8d7df1b05cd33b9166712" in state
    for forbidden in (
        "schema_version",
        "evidence_id",
        "sha256",
        "active-learning-flow",
        "active-lesson-handoff",
        "materials/private",
        "tmp/",
    ):
        assert forbidden not in state


def test_state_approval_is_edit_only() -> None:
    agents = _normalized("AGENTS.md")
    usage = _normalized("USAGE.md")
    assert "`STATE 반영해` or equivalent approval authorizes only replacement of `STATE.md`" in agents
    assert "It does not authorize a commit or push" in agents
    assert "이 문장은 `STATE.md` 수정만 허용합니다" in usage
