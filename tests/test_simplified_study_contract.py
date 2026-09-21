from __future__ import annotations

import re
import tomllib
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def _raw(path: str) -> str:
    return (REPO / path).read_text(encoding="utf-8")


def _normalized(path: str) -> str:
    return re.sub(r"\s+", " ", _raw(path))


def _markdown_cells(line: str) -> list[str]:
    stripped = line.strip()
    assert stripped.startswith("|") and stripped.endswith("|")
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _hours(cell: str) -> int:
    match = re.fullmatch(r"\*{0,2}(\d[\d,]*)h\*{0,2}", cell.strip())
    assert match is not None, f"Expected an hour cell, got {cell!r}"
    return int(match.group(1).replace(",", ""))


def _budget_table() -> tuple[list[str], dict[str, list[int]], list[int]]:
    lines = _raw("ROADMAP.md").splitlines()
    header_index = next(
        index for index, line in enumerate(lines) if line.startswith("| Phase |")
    )
    headers = _markdown_cells(lines[header_index])
    assert _markdown_cells(lines[header_index + 1])

    phase_rows: dict[str, list[int]] = {}
    total_row: list[int] | None = None
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        cells = _markdown_cells(line)
        assert len(cells) == len(headers), f"Malformed budget row: {line}"
        phase = cells[0].replace("`", "").replace("*", "").strip()
        hours = [_hours(cell) for cell in cells[2:]]
        if phase in {f"P{index}" for index in range(6)}:
            assert phase not in phase_rows, f"Duplicate budget row: {phase}"
            phase_rows[phase] = hours
        elif phase == "합계":
            assert total_row is None, "Duplicate budget total"
            total_row = hours
        else:
            raise AssertionError(f"Unexpected budget label: {phase}")

    assert total_row is not None, "Budget table has no total row"
    return headers, phase_rows, total_row


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
    headings = [roadmap.index(f"## P{index} ") for index in range(6)]
    assert headings == sorted(headings)
    assert "48개 실효 학습주" in roadmap
    assert "합계 2,880시간" in roadmap
    assert "마감이 아니라 **예산**" in roadmap
    assert "주 60시간(실효)" in roadmap
    assert "강의 수강 자체는" in roadmap
    assert "공식 핵심 과제나 무보조 설명·해석 단계를 잘라" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Foundations are not optional here" in agents
    assert "do not propose reordering a later Phase forward" in agents
    assert "stay comparison-only" in agents


def test_roadmap_budget_table_has_the_approved_shape_and_sums() -> None:
    headers, phases, total = _budget_table()
    assert headers == [
        "Phase",
        "실효 주",
        "주과정·공식 과제·지정 독서",
        "프로젝트",
        "구술·재구현",
        "지원 활동",
        "작업 버퍼",
        "합계",
    ]
    expected = {
        "P0": [330, 30, 72, 0, 48, 480],
        "P1": [330, 120, 90, 0, 60, 600],
        "P2": [225, 45, 54, 0, 36, 360],
        "P3": [330, 0, 72, 30, 48, 480],
        "P4": [390, 0, 90, 60, 60, 600],
        "P5": [0, 120, 36, 168, 36, 360],
    }
    assert phases == expected
    for phase, row in phases.items():
        assert sum(row[:-1]) == row[-1], f"Activity sum differs for {phase}"
    assert total == [1605, 315, 414, 258, 288, 2880]
    assert [sum(phases[phase][column] for phase in expected) for column in range(5)] == total[:5]
    assert sum(total[:5]) == total[5]
    assert sum(row[-1] for row in phases.values()) == total[-1]


def test_relative_weeks_match_phase_hours_without_hidden_job_hours() -> None:
    _, phases, _ = _budget_table()
    rows = re.findall(
        r"^\| `(?P<phase>P[0-5])` \| (?P<start>\d+)~(?P<end>\d+) \|",
        _raw("ROADMAP.md"),
        re.MULTILINE,
    )
    assert len(rows) == 6
    next_week = 1
    for phase, start, end in rows:
        assert int(start) == next_week
        assert (int(end) - int(start) + 1) * 60 == phases[phase][-1]
        next_week = int(end) + 1
    assert next_week == 49
    roadmap = _normalized("ROADMAP.md")
    assert "52주 달력 안의 48개 실효 학습주" in roadmap
    assert "나머지 4주" in roadmap
    assert "초기 배분 가설" in roadmap
    assert "각 활동은 수행하는 Phase에 한 번만 계산" in roadmap
    assert "P5의 지정 독서만 통합 프로젝트 시간에 포함" in roadmap
    assert "지원 활동이 0인 Phase에 실제 지원하기로 하면" in roadmap


def test_approved_course_scope_and_phase_boundary_are_explicit() -> None:
    roadmap = _normalized("ROADMAP.md")
    assert "MIT 18.05 Spring 2022" in roadmap
    assert "PS1~PS11을 R 요구까지 모두 수행" in roadmap
    assert "CS229 Summer 2020" in roadmap
    assert "PS1, PS2, PS3의 필수 written과 coding을 모두 수행" in roadmap
    assert "공식 문제를 임의 NumPy 연습으로 대체하지 않습니다" in roadmap
    assert "CS231n Spring 2024" in roadmap
    assert "Lecture 2~6" in roadmap
    assert "Assignment 2" in roadmap and "Q1~Q5" in roadmap
    assert "P2 마지막에는" in roadmap
    assert "GPT와 BPE를 직접 구현합니다" in roadmap
    assert "P2 끝에서 GPT와 BPE 구현을 마친 것을 전제로" in roadmap
    assert "CS224N Spring 2024" in roadmap
    assert "Assignment 1~4를 **written·수학·programming 요구사항까지 전부 수행**" in roadmap

    agents = _normalized("AGENTS.md")
    assert "NumPy reimplementations cannot replace official problem sets" in agents
    assert "CS224N Spring 2024 A1-A4 are performed in full in `P3`" in agents


def test_blank_page_implementation_is_a_standing_track() -> None:
    """Official exercises follow a lecture; writing from nothing is a separate skill."""
    roadmap = _normalized("ROADMAP.md")
    assert "대표 무보조 재구현" in roadmap
    assert "공식 과제 수행과 무보조 재구현은 서로 다른 근거" in roadmap
    assert "전체 과제를 다시 쓰는 의무를 추가하지 않고" in roadmap
    assert "도움받은 구현을 무보조 성공으로 기록하지 않습니다" in roadmap
    assert "PCA, k-means" in roadmap
    assert "PCA 또는 k-means" not in roadmap
    assert _normalized("challenges/deep-ml/README.md").count("빈 파일 구현 트랙") == 1
    agents = _normalized("AGENTS.md")
    assert "Code is rebuilt from an empty file" in agents
    assert "at representative implementation units" in agents
    assert "Do not require rewriting every module's full implementation or entire assignments" in agents
    assert "not even an import list or a function signature" in agents
    assert "is not recorded as passed" in agents


def test_foundation_repair_preserves_math_scope_and_r_requirements() -> None:
    p0 = _normalized("ROADMAP.md").split("## P0 —", 1)[1].split("## P1 —", 1)[0]
    for scope in ("Chapter 2~5, 7", "공식 연습문제", "무보조 설명·계산",
                  "MIT 18.01SC Fall 2010", "PS1~PS11", "Lesson 1~2"):
        assert scope in p0
    assert "이미 설명·계산한 내용을 반복 수강하지 않습니다" in p0
    assert "R이 필요한 과제는 R로 수행하며 Python 대체로 완료 처리하지 않습니다" in p0
    assert "별도 수학 과정 전체를 추가하지 않습니다" in p0
    assert "Stat110과 OpenIntro는 다른 설명이 필요할 때만" in p0


def test_systems_training_and_single_inference_research_have_distinct_scope() -> None:
    roadmap = _normalized("ROADMAP.md")
    p4 = roadmap.split("## P4 —", 1)[1].split("## P5 —", 1)[0]
    assert "Assignment 1 Basics" in p4 and "Assignment 2 Systems 전체" in p4
    assert "P4 끝에 2026 Lecture 10 inference" in p4
    assert "training systems 과제이지 serving 과제가 아닙니다" in p4
    assert "a158843b20107949f1a8d7df1b05cd33b9166712" in p4
    p5 = roadmap.split("## P5 —", 1)[1].split("## 실전 competition", 1)[0]
    assert "프로젝트와 논문 재현을 따로 만들지 않습니다" in p5
    for item in ("고정 workload", "baseline", "통제 비교", "품질", "memory",
                 "latency", "throughput", "남은 한계"):
        assert item in p5
    assert "quantization은 baseline과 측정 계약이 안정된 뒤의 선택 항목" in p5


def test_current_explanation_criteria_do_not_relabel_historical_source_audits() -> None:
    curriculum = _normalized("CURRICULUM.md")
    criteria = curriculum.split("## 3. 핵심 개념과 설명 기준", 1)[1].split(
        "## 4. 공통 핵심 역량", 1
    )[0]
    for concept in ("선형변환", "SVD", "Jacobian", "convexity", "LLN·CLT",
                    "MLE·MAP", "검정력", "bootstrap·다중비교", "calibration",
                    "RNN·LSTM", "KV cache", "분산 통신"):
        assert concept in criteria
    assert "완료 체크·점수·답변집이 아니며" in criteria
    assert "새 자료를 다운로드하거나 전체 감사한 것으로 기록하지 않는다" in criteria
    assert "현재 경로에 강의가 없다는 뜻이 아니다" in curriculum
    assert "현재 P0~P5의 추가 졸업 조건이나 진입 시험으로 사용하지 않는다" in curriculum


def test_public_curricula_are_credited_with_what_they_changed() -> None:
    """Borrowed structure has to name its source and what it altered."""
    roadmap = _normalized("ROADMAP.md")
    for source in ("fast.ai", "Made With ML", "Full Stack Deep Learning", "roadmap.sh"):
        assert source in roadmap
    assert "top-down" in roadmap
    # The top-down front-end supplements the bottom-up route, it does not replace it.
    assert "fast.ai를 앞에 짧게 붙이는 구성은" in roadmap
    # Dated sources must be flagged rather than followed for current APIs.
    assert "판본 주의" in roadmap
    # ML system design was the gap these curricula exposed.
    assert "ML 시스템 설계" in roadmap
    assert "전체 과정을 별도 졸업 조건으로 추가하지 않습니다" in roadmap


def test_job_ladder_is_marked_as_assessment_not_fact() -> None:
    roadmap = _normalized("ROADMAP.md")
    assert "LLM Research Engineer" in roadmap
    assert "특정 Phase가 취업이나 지원 자격을 보장하지 않습니다" in roadmap
    assert "실제 공고 3~5건" in roadmap
    assert "공고가 경로와 다르면 공고를 기준으로 경로를 재검토합니다" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Treat the ladder as an assessment to re-check against real postings" in agents
    assert "without promising employability at any Phase or date" in agents
    assert "an earlier rung is not a failure" in agents


def test_competitions_and_papers_are_tracks_that_cannot_be_fabricated() -> None:
    roadmap = _normalized("ROADMAP.md")
    assert "Kaggle은 P1만 필수입니다" in roadmap
    assert "P0·P2·P3은 선택" in roadmap
    assert "실제 목록" in roadmap
    assert "P5만 논문 주장 하나를 독립 연구 질문 안에서 집중 재현합니다" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Competitions and papers are proposed, never invented" in agents
    assert "do not name a specific kaggle competition without checking" in agents.lower()
    assert "never cite a title, venue, year, or result you have not verified" in agents
    assert "never fill a gap in a reproduction with a plausible number" in agents
    assert "The learner writes the paper summary" in agents


def test_kaggle_recommendation_trigger_does_not_require_a_p0_submission() -> None:
    roadmap = _normalized("ROADMAP.md")
    agents = _normalized("AGENTS.md")
    deferred = _normalized("DEFERRED.md")
    assert "Kaggle은 P1만 필수입니다" in roadmap
    assert "Kaggle is required only in P1" in agents
    assert "P0는 예측을 만들 수 있으면 첫 제출 경험을 제안합니다" in roadmap
    assert "이전 제출 경험을 요구하지 않습니다" in roadmap
    assert "제출 결과가 다음 Phase의 선수조건은 아닙니다" in roadmap
    assert "P0 needs the ability to produce predictions, not a previous submission" in agents
    assert "the first submission is the proposed experience" in agents
    assert "P0·P2·P3 Kaggle competition" in deferred
    assert "다른 Phase의 competition은 선택입니다" in deferred
    assert "P0는 예측을 만들 수 있으면 첫 제출 경험을 제안하며 이전 제출 경험을 요구하지 않습니다" in deferred
    assert "P2·P3는 핵심 학습 이후" in deferred


def test_phase_check_and_hardware_prerequisite_are_pinned() -> None:
    roadmap = _normalized("ROADMAP.md")
    assert "P2 시작 전에 단일 GPU 환경에서 CS231n A2와 PyTorch workload가 실행되는지" in roadmap
    assert "P4 시작 전에는 CS336 A2 공식 요구를 수행할 유료 GPU 수단" in roadmap
    assert "과제를 미완료로 두며 대체 과제로 완료 처리하지 않습니다" in roadmap
    assert "실제 공고 3~5건" in roadmap
    assert "Phase 종료 전 아래를 확인하고 필수 항목이 비면 Phase를 닫지 않습니다" in roadmap
    assert "지정 범위의 직접 수행, 실행·해석과 재현 가능성" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Run the phase-transition check before closing a Phase" in agents
    assert "Never state that a company is hiring" in agents
    assert "the posting is right and the ladder needs fixing" in agents


def test_graded_coursework_stays_out_of_the_public_repository() -> None:
    agents = _normalized("AGENTS.md")
    assert "This repository is public and part of it is published as a site" in agents
    boundary = agents.split("This repository is public", 1)[1].split(
        "The KANT materials", 1
    )[0]
    for course in ("MIT 18.05", "CS229", "CS231n", "CS224N", "CS336"):
        assert course in boundary
    assert "separate private workspaces" in boundary
    for artifact in ("written answers", "code", "notebooks", "saved outputs"):
        assert artifact in boundary
    assert "never assignment code, official problem statements, or copyrighted course material" in boundary
    for path in ("README.md", "USAGE.md", "practice/README.md", "ROADMAP.md"):
        paragraphs = re.split(r"\n\s*\n", _raw(path))
        private_boundary = next(
            paragraph for paragraph in paragraphs
            if "MIT 18.05" in paragraph and "비공개 작업 공간" in paragraph
        )
        for course in ("CS229", "CS231n", "CS224N", "CS336"):
            assert course in private_boundary, path
        for artifact in ("written", "코드", "노트북", "저장 출력"):
            assert artifact in private_boundary, path


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
    # Confirmed resume changes do not need a separate approval turn.
    assert "STATE.md는 확인된 재개 위치에 맞춰 사전 승인 없이 갱신됩니다" in usage
    for standing in ("빈 파일 재구현", "deep-ml", "논문", "무보조 구술", "전환 점검"):
        assert standing in usage


def test_state_updates_without_prior_approval_from_confirmed_evidence() -> None:
    agents = _normalized("AGENTS.md")
    assert "Update `STATE.md` without prior proposal or approval" in agents
    assert "distinguish completed work, planned work, and unverified claims" in agents
    assert "does not authorize a new course, a sequence change" in agents
    assert "At a Phase transition, run the `ROADMAP.md` check first" in agents
    usage = _normalized("USAGE.md")
    assert "사전 제안이나 승인 없이 갱신" in usage
    assert "미실행 계획과 확인되지 않은 이해를 완료로 기록하지" in usage
    for path, obsolete in (
        ("AGENTS.md", "write it only after explicit approval"),
        ("README.md", "STATE 승인 후"),
        ("USAGE.md", "STATE 전체 교체안을 보여 주며, 승인 후"),
        (".agents/skills/finish-chapter/SKILL.md", "After approval, apply the exact replacement"),
        (".agents/skills/finish-chapter/agents/openai.yaml", "STATE 전체 교체안 승인 후"),
    ):
        assert obsolete not in _normalized(path)


def test_phase_id_in_state_does_not_reopen_progress_tracking() -> None:
    agents = _normalized("AGENTS.md")
    usage = _normalized("USAGE.md")
    assert "The Phase ID is a static pointer into `ROADMAP.md`" in agents
    assert "Never add a percentage, a score, a readiness judgement, an hour tally" in agents
    assert "a Phase ID is not an opening to bring them back" in agents
    assert "hashes, readiness scores, session history, or metrics" in agents
    assert "현재 `ROADMAP.md`의 정적 Phase ID 하나 (`P0`~`P5`)" in usage
    assert "Phase 변경은 ROADMAP 전환 점검과 기존 과정 선택 규칙을 따릅니다" in usage
    assert "자동 또는 요청에 따른 STATE 갱신은 `STATE.md` 수정만 허용합니다" in usage
    assert "hash, phase, 점수표" not in usage


def test_understanding_is_verified_by_unassisted_recall() -> None:
    """Coverage is not evidence; the repo needs a mechanism that tests recall."""
    agents = _normalized("AGENTS.md")
    assert "Verifying understanding, not coverage" in agents
    assert "Knowledge notes are drafted unassisted, then compared" in agents
    assert "Never draft the note first and have the learner confirm it" in agents
    assert "blank-page explanation" in agents
    assert "two concepts from the previous week and one older concept, cold" in agents
    assert "explains the whole Phase without notes" in agents
    assert "reuses your own earlier phrasing is not evidence" in agents
    assert "1-2 minute unassisted explanation" in agents
    assert "one changed-condition case" in agents
    assert "one complete response covering what is correct, incorrect, and missing" in agents
    assert "representative implementation units" in agents
    assert "Do not require rewriting every module's full implementation or entire assignments" in agents

    knowledge = _normalized("knowledge/README.md")
    assert "교정할 knowledge 초안은 대화·강의·기존 노트를 닫고 학습자가 기억으로 먼저" in knowledge
    assert "그 초안 이후에만 공식 자료와 대조" in knowledge
    assert "AI가 면접 답변집이나 완성 노트를 먼저 작성하지 않습니다" in knowledge
    for path in ("README.md", "USAGE.md", "ROADMAP.md"):
        text = _normalized(path)
        assert "지난주 개념 2개와 더 이전 개념 1개" in text, path
        assert "초안" in text, path
        assert "지난주 개념 3개" not in text, path


def test_deferred_material_keeps_a_return_condition() -> None:
    """A hold without a return condition is a deletion, so every entry needs one."""
    deferred = _normalized("DEFERRED.md")
    assert "미완료 보류" in deferred
    assert "복귀 조건" in deferred
    assert "조건이 생겨도 자동으로 시작하지 않고" in deferred
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
    assert "새 자료를 여기 연결하는 것은 다운로드·전체 감사·환경 설치 완료를 뜻하지 않습니다" in roadmap
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
    assert "Update STATE from confirmed evidence without prior proposal or approval" in entrypoint
    assert "Never amend or push automatically" in entrypoint
    assert "unrelated staged changes" in entrypoint
    assert "never run commands or this helper in a CS336 assignment checkout" in entrypoint
    draft_check = entrypoint.index("Before touching `knowledge/`")
    knowledge_update = entrypoint.index("update reusable concepts")
    reset = entrypoint.index("5. Validate notes and links before reset")
    assert draft_check < knowledge_update < reset
    assert "If they have not, stop and ask for it" in entrypoint
    assert "A wrap-up is not an exemption from this rule" in entrypoint
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


def test_state_update_is_edit_only() -> None:
    agents = _normalized("AGENTS.md")
    usage = _normalized("USAGE.md")
    assert "Updating `STATE.md`, automatically or on request, authorizes only the file edit" in agents
    assert "It does not authorize a commit or push" in agents
    assert "자동 또는 요청에 따른 STATE 갱신은 `STATE.md` 수정만 허용합니다" in usage


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
