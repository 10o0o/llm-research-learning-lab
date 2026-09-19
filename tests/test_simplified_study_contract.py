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
    assert "Readiness does not cancel unfinished CS224N assignments or its project" in agents


def test_official_practice_is_preserved_across_teaching_media() -> None:
    agents = _normalized("AGENTS.md")
    for rule in (
        "Video, text, and source-grounded dialogue are allowed",
        "KANT is only for topic/progress comparison, not default practice or a completion criterion",
        "Follow along with the full lecture implementation",
        "attempt separate exercises independently",
        "Completed instructor notebooks are references",
        "Supplementary AI examples cannot replace official practice",
        "Read the actual exercise requirements when assigning it",
        "leave affected work incomplete",
        "local tests or reviews are not official university grading",
    ):
        assert rule in agents
    assert "must not replace viewing it" not in agents
    assert "existing KANT practice for application" not in agents

    for path in ("README.md", "USAGE.md", "practice/README.md", "ROADMAP.md"):
        text = _normalized(path)
        assert "KANT는 진도·주제 대조용" in text
        assert "기본 실습이나 완료 기준으로 사용하지 않습니다" in text
        assert "영상·문서·공식 자료 기반 대화" in text
        assert "완성 노트북 실행이나 AI 보충 예제로 공식 실습을 대체하지 않습니다" in text
        assert "Optional·Bonus" in text
        assert "미완료" in text
        assert "기존 KANT 과제가 실습 역할" not in text
        assert "기존 KANT 실습에 연결" not in text
    for path in ("README.md", "USAGE.md"):
        assert "기준 자료·판본 → 직접 링크 → 이번 설명 범위 → 수행할 공식 실습 → 확인할 결과" in _normalized(path)


def test_cs224n_assignments_are_performed_with_the_official_ai_policy() -> None:
    """A1-A4 are back on the route in P3; only the final project stays on hold."""
    agents = _normalized("AGENTS.md")
    assert "CS224N Spring 2024 A1-A4 are performed in full in `P3`" in agents
    assert "AI collaboration is allowed but direct answer solicitation, copying answers, and substantial completion by AI are prohibited" in agents
    assert "Only the CS224N Final Project is held" in agents
    assert "Only the user may change or omit agreed practice" in agents
    for path in ("README.md", "USAGE.md", "practice/README.md"):
        text = _normalized(path)
        assert "A1~A4" in text
        assert "`P3`" in text
        assert "직접 답 요구·복사와 AI의 실질적 과제 대행을 금지합니다" in text
        assert "DEFERRED.md" in text


def test_foundations_first_route_is_pinned() -> None:
    roadmap = _normalized("ROADMAP.md")
    for phase in ("`P0`", "`P1`", "`P2`", "`P3`", "`P4`", "`P5`"):
        assert phase in roadmap
    assert "마감이 아니라 **예산**" in roadmap
    # The budget is planned below the learner's stated hours on purpose.
    assert "주 60시간(실효)" in roadmap
    # Every phase owes a deliverable; attending a course is not one.
    assert "강의 수강 자체는" in roadmap
    # CS336 prerequisites are covered in order rather than skipped.
    assert "memory hierarchy" in roadmap
    assert "이 순서를 앞당기지 않습니다" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Foundations are not optional here" in agents
    assert "do not propose reordering a later Phase forward" in agents
    assert "stay comparison-only" in agents


def test_blank_page_implementation_is_a_standing_track() -> None:
    """Official exercises follow a lecture; writing from nothing is a separate skill."""
    roadmap = _normalized("ROADMAP.md")
    assert "빈 파일 구현 트랙" in roadmap
    assert "모든 Phase에 상시로" in roadmap
    for practice in ("재구현", "deep-ml 챌린지", "시간 제한 구현", "알고리즘 코딩 테스트"):
        assert practice in roadmap
    assert "통과하지 못한 항목은 완료로 기록하지 않습니다" in roadmap
    assert _normalized("challenges/deep-ml/README.md").count("빈 파일 구현 트랙") == 1
    agents = _normalized("AGENTS.md")
    assert "Code is rebuilt from an empty file" in agents
    assert "not even an import list or a function signature" in agents
    assert "is not recorded as passed" in agents


def test_public_curricula_are_credited_with_what_they_changed() -> None:
    """Borrowed structure has to name its source and what it altered."""
    roadmap = _normalized("ROADMAP.md")
    for source in ("fast.ai", "Made With ML", "Full Stack Deep Learning", "roadmap.sh"):
        assert source in roadmap
    assert "top-down" in roadmap
    # The top-down front-end supplements the bottom-up route, it does not replace it.
    assert "앞에 짧게 붙이는** 구성입니다" in roadmap
    # Dated sources must be flagged rather than followed for current APIs.
    assert "판본 주의" in roadmap
    # ML system design was the gap these curricula exposed.
    assert "ML 시스템 설계" in roadmap


def test_job_ladder_is_marked_as_assessment_not_fact() -> None:
    roadmap = _normalized("ROADMAP.md")
    assert "직무 사다리와 최종 목표" in roadmap
    assert "LLM Research Engineer" in roadmap
    for rung in ("ML Engineer / AI Engineer (주니어)", "LLM Application Engineer",
                 "LLM Systems / Inference Engineer", "LLM Research Engineer"):
        assert rung in roadmap
    # The ladder is a judgement call and must not read as a quote from postings.
    assert "저자의 판단이지" in roadmap
    assert "실제 공고의 요구사항으로 다시" in roadmap
    # Applying to an earlier rung is not a failure.
    assert "포기**로 기록하지 않습니다" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Treat the ladder as an assessment to re-check against real postings" in agents


def test_competitions_and_papers_are_tracks_that_cannot_be_fabricated() -> None:
    roadmap = _normalized("ROADMAP.md")
    assert "실전 competition 트랙" in roadmap
    assert "논문 읽기 트랙" in roadmap
    # No specific competition is pinned, because the live list changes.
    assert "이 문서에 특정 대회를 고정하지 않습니다" in roadmap
    assert "3-pass" in roadmap
    # A failed reproduction with a diagnosed cause still counts.
    assert "재현 실패도 원인을 규명했다면 유효한 산출물" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Competitions and papers are proposed, never invented" in agents
    assert "do not name a specific Kaggle competition without checking" in agents
    assert "never cite a title, venue, year, or result you have not verified" in agents
    assert "never fill a gap in a reproduction with a plausible number" in agents
    assert "The learner writes the paper summary" in agents


def test_phase_check_and_hardware_prerequisite_are_pinned() -> None:
    roadmap = _normalized("ROADMAP.md")
    assert "중간 점검" in roadmap
    assert "지금 당장 찔러볼 수 있는 공고는 무엇인가" in roadmap
    # A real posting outranks the author's ladder.
    assert "공고가 맞고 사다리가 틀린 것" in roadmap
    assert "불합격을 학습 실패로 기록하지" in roadmap
    # No GPU was available when this route was written; P4/P5 depend on one.
    assert "NVIDIA GPU가 없습니다" in roadmap
    assert "지금 시작하는 데는 장애가 없습니다" in roadmap
    assert "대체 과제로" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Run the phase-transition check before closing a Phase" in agents
    assert "Never state that a company is hiring" in agents
    assert "the posting is right and the ladder needs fixing" in agents


def test_graded_coursework_stays_out_of_the_public_repository() -> None:
    agents = _normalized("AGENTS.md")
    assert "This repository is public and part of it is published as a site" in agents
    assert "CS224N and CS336 assignment solutions live in separate private clones" in agents
    assert "never assignment code, official problem statements, or copyrighted course material" in agents


def test_operating_documents_stay_tool_neutral() -> None:
    """The rules travel as files, so they must not name one tool's commands."""
    for path in ("AGENTS.md", "README.md", "USAGE.md", "practice/README.md"):
        text = _normalized(path)
        assert "apply_patch" not in text
        assert "Codex" not in text
    agents = _normalized("AGENTS.md")
    assert "More than one assistant" in agents
    assert "`STATE.md` is the only handoff" in agents
    assert "One session at a time" in agents
    assert "not a second chance to be handed an answer" in agents
    assert "the official source settles it, not the more confident assistant" in agents
    usage = _normalized("USAGE.md")
    assert "AI 도구를 두 개 쓸 때" in usage
    assert "동시에 두 개를 돌리지 않습니다" in usage
    assert "답을 받아낼 두 번째 기회가 아닙니다" in usage


def test_usage_documents_the_session_loop() -> None:
    usage = _normalized("USAGE.md")
    assert "하루 세션 운영" in usage
    assert "한 세션은 **모듈 하나**입니다" in usage
    # Nothing is written without approval, so an interrupted session is safe.
    assert "승인하지 않으면 파일은 바뀌지 않으므로" in usage
    for standing in ("빈 파일 재구현", "deep-ml", "논문", "무보조 구술", "전환 점검"):
        assert standing in usage


def test_state_is_never_written_without_approval() -> None:
    """The bookmark is the one place the learner, not an assistant, decides."""
    agents = _normalized("AGENTS.md")
    assert "`STATE.md` is never written automatically, at any checkpoint" in agents
    assert "decided by the learner rather than inferred by an assistant" in agents
    # The proposal is automatic even though the write is not.
    assert "Offer the replacement without being asked whenever the resume point moved" in agents
    assert "at a Phase transition" in agents
    assert "자동으로 쓰이지 않으며" in _normalized("ROADMAP.md")


def test_phase_id_in_state_does_not_reopen_progress_tracking() -> None:
    agents = _normalized("AGENTS.md")
    assert "The Phase ID is a static pointer into `ROADMAP.md`" in agents
    assert "Never add a percentage, a score, a readiness judgement, an hour tally" in agents
    assert "a Phase ID is not an opening to bring them back" in agents
    # The old blanket ban listed "phases"; it must not contradict the new field.
    assert "hashes, readiness scores, session history, or metrics" in agents


def test_understanding_is_verified_by_unassisted_recall() -> None:
    """Coverage is not evidence; the repo needs a mechanism that tests recall."""
    agents = _normalized("AGENTS.md")
    assert "Verifying understanding, not coverage" in agents
    assert "Knowledge notes are drafted unassisted, then compared" in agents
    assert "Never draft the note first and have the learner confirm it" in agents
    assert "blank-page explanation" in agents
    assert "three concepts from the previous week, cold" in agents
    assert "explains the whole Phase without notes" in agents
    assert "reuses your own earlier phrasing is not evidence" in agents


def test_deferred_material_keeps_a_return_condition() -> None:
    """A hold without a return condition is a deletion, so every entry needs one."""
    deferred = _normalized("DEFERRED.md")
    assert "미완료 보류" in deferred
    assert "복귀 조건" in deferred
    assert "어떤 조건도 자동으로 학습을 시작하지 않습니다" in deferred
    for item in ("Final Project", "WaveNet", "Assignment 3", "Hugging Face"):
        assert item in deferred
    # CS224N A1-A4 came off the hold list and must not read as deferred.
    assert "CS224N A1~A4는 **`P3`에서 정식 수행합니다.**" in deferred


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


def test_standalone_utilities_keep_their_explicit_no_commit_contract() -> None:
    expected = {"save-today-til", "update-learning-knowledge"}
    actual = {
        path.parent.name for path in (REPO / ".agents/skills").glob("*/SKILL.md")
    }
    assert actual == expected | {"finish-chapter"}

    for name in expected:
        entrypoint = _normalized(f".agents/skills/{name}/SKILL.md")
        manifest = _normalized(f".agents/skills/{name}/agents/openai.yaml")
        assert "Use only when the learner" in entrypoint
        assert "Commit and push each require a separate explicit request" in entrypoint
        assert "allow_implicit_invocation: false" in manifest


def test_chapter_wrap_up_is_separate_from_ordinary_study() -> None:
    entrypoint = _normalized(".agents/skills/finish-chapter/SKILL.md")
    manifest = _normalized(".agents/skills/finish-chapter/agents/openai.yaml")
    assert "allow_implicit_invocation: true" in manifest
    assert "Do not activate for 완료, 이해했어, or 오늘 학습 종료 alone" in entrypoint
    assert "Do not execute the learner's notebooks during wrap-up" in entrypoint
    assert "After approval, apply the exact replacement" in entrypoint
    assert "Never amend or push automatically" in entrypoint
    assert "unrelated staged changes" in entrypoint
    assert "never run commands or this helper in a CS336 assignment checkout" in entrypoint
    for path in ("AGENTS.md", "README.md", "USAGE.md"):
        assert "$finish-chapter" in _normalized(path)


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
