from __future__ import annotations

import re
import tomllib
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
    assert "follow one connected segment of the approved original course" in agents
    assert "Do not start ordinary study with a new readiness diagnostic or roadmap review" in agents
    assert "Do not enter a new course or assignment automatically" in agents
    assert "Never invent video content, timestamps, or learner viewing progress" in agents


def test_study_route_does_not_restore_fixed_entry_gates() -> None:
    for path in ("AGENTS.md", "README.md", "USAGE.md"):
        text = _normalized(path)
        for obsolete in (
            "The pilot spine is",
            "at most two focused bridge modules",
            "Before proposing Assignment 1 entry, run",
            "최대 두 번",
            "현재 첫 행동은",
            "Pilot의 주축은",
        ):
            assert obsolete not in text
    for path in ("README.md", "USAGE.md"):
        text = _normalized(path)
        assert "현재 주강의 단원으로 연결" in text
        assert "공식 API 문서" in text
    agents = _normalized("AGENTS.md")
    assert "then return to the same course" in agents
    assert "Do not require completing the entire KANT assignment, all CS224N lectures" in agents


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
    assert "승인된 주강의 순서를 강제 변경하거나" in curriculum
    assert "`CC-SEQ-01`을 필수 연결 역량으로 먼저 완료" not in roadmap


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
    for label in ("현재 주강의", "현재 강의", "현재 범위"):
        values = re.findall(rf"^- {label}:[ \t]*(\S[^\n]*)$", state, re.MULTILINE)
        assert len(values) == 1, f"Expected one nonempty {label}"
    assert len(re.findall(r"^## 다음 독립 행동$", state, re.MULTILINE)) == 1
    next_action = re.search(
        r"^## 다음 독립 행동\n(.*?)(?=^## |\Z)", state, re.MULTILINE | re.DOTALL
    )
    assert next_action is not None and next_action.group(1).strip()
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


def test_cs336_uses_a_separate_python_environment() -> None:
    pyproject = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["requires-python"] == ">=3.14,<3.15"

    agents = _normalized("AGENTS.md")
    readme = _normalized("README.md")
    usage = _normalized("USAGE.md")
    assert "learning lab's Python 3.14 environment" in agents
    assert "separate sibling clone" in agents
    assert "Python 3.12 or 3.13" in agents
    for text in (readme, usage):
        assert "learning-lab의 Python 3.14 환경" in text
        assert "별도 sibling clone" in text
        assert "Python 3.12 또는 3.13" in text
        assert "현재 `.venv`" in text


def test_private_material_count_and_registry_snapshot_do_not_claim_live_validation() -> None:
    materials = _normalized("materials/README.md")
    curriculum = _normalized("CURRICULUM.md")
    assert "딥러닝 기초 18강" not in materials
    assert "정확한 목록은 로컬 INDEX.md 기준" in materials
    assert "아래 수치는 2026-08-27 당시" in curriculum
    assert "검증으로 대조한 snapshot" in curriculum
    assert "이후 자료 변경은 실제 파일과 각 과정 `INDEX.md`를 수동으로 교차 확인한다" in curriculum


def test_cs336_command_policy_is_consistent() -> None:
    agents = _normalized("AGENTS.md")
    assert "The learner writes the assignment code, runs the provided tests, and runs every bash command" in agents
    assert "must not execute bash commands in the assignment repository" in agents
    assert "already shown in the official handout" in agents
    assert "must not create a new command sequence to solve or automate the assignment" in agents
    assert "Do not provide code, pseudocode, patches, or TODO solutions, even after an explicit request" in agents
    assert "a158843b20107949f1a8d7df1b05cd33b9166712" in agents

    for path in ("README.md", "USAGE.md"):
        text = _normalized(path)
        assert "학습자가 과제 코드를 직접 작성하고 제공된 테스트를 실행" in text
        assert "학습자가 모든 bash command를 직접 실행" in text
        assert "assignment repo에서 command를 실행하지 않습니다" in text
        assert "공식 handout에 이미 나온 command의 의미와 학습자가 제공한 실행 결과" in text
        assert "과제 해결·자동화를 위한 새로운 command sequence" in text
        assert "코드, pseudocode, patch, TODO 해답" in text
        assert "a158843b20107949f1a8d7df1b05cd33b9166712" in text


def test_error_hypothesis_is_required_only_after_an_error() -> None:
    agents = _normalized("AGENTS.md")
    assert "if an error occurs" in agents
    assert "before changing the code and how it was checked" in agents

    korean_docs = [_normalized(path) for path in ("README.md", "USAGE.md")]
    for text in korean_docs:
        assert "오류가 발생했다면" in text
        assert "수정 전에 세운 첫 원인 가설" in text
        assert "이를 확인한 방법" in text
        assert "첫 오류 가설" not in text
