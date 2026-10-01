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


def _budget_table() -> tuple[list[str], dict[str, int], int]:
    lines = _raw("ROADMAP.md").splitlines()
    header_index = next(index for index, line in enumerate(lines)
                        if line.startswith("| 개인 학습 활동 |"))
    headers = _markdown_cells(lines[header_index])
    activities: dict[str, int] = {}
    total: int | None = None
    for line in lines[header_index + 2:]:
        if not line.startswith("|"):
            break
        cells = _markdown_cells(line)
        assert len(cells) == len(headers), f"Malformed budget row: {line}"
        hours = _hours(cells[1])
        if cells[0] == "합계":
            assert total is None
            total = hours
        else:
            assert cells[0] not in activities
            activities[cells[0]] = hours
    assert total is not None
    return headers, activities, total


def test_plain_study_phrases_use_state() -> None:
    agents = _normalized("AGENTS.md")
    for phrase in (
        "`오늘 학습 시작`",
        "`오늘 전체 학습 흐름 시작` or `전체 학습 흐름 시작`",
        "`계속`",
        "`오늘 학습 종료`",
        "`이번 주 회상`",
        "$study-session",
    ):
        assert phrase in agents
    assert "resume the next independent action in `STATE.md`" in agents
    assert "never enter another course automatically" in agents
    assert "Do not begin with a new readiness diagnostic or roadmap review" in agents
    assert "Never invent source content, timestamps, or learner viewing progress" in agents


def test_study_route_does_not_restore_fixed_entry_gates() -> None:
    for path in ("AGENTS.md", "README.md", "USAGE.md"):
        content = _normalized(path)
        for obsolete in ("The pilot spine is", "at most two focused bridge modules",
                         "Before proposing Assignment 1 entry, run", "최대 두 번",
                         "현재 첫 행동은", "Pilot의 주축은"):
            assert obsolete not in content
    agents = _normalized("AGENTS.md")
    assert "Do not impose a second full tokenizer/Transformer implementation as an entry test" in agents
    assert "Entry does not cancel unfinished work" in agents


def test_official_practice_is_preserved_across_teaching_media() -> None:
    agents = _normalized("AGENTS.md")
    for rule in ("Use official course implementations, exercises, and assignments as primary practice",
                 "inspect actual requirements before assigning them", "KANT is supporting context",
                 "supplementary examples and completed instructor notebooks do not replace official practice",
                 "limits as incomplete", "Preserve Optional/Bonus labels",
                 "do not describe dialogue as video viewing or local checks as official university grading"):
        assert rule in agents
    for path in ("practice/README.md", "ROADMAP.md"):
        content = _normalized(path)
        for rule in ("KANT는 진도·주제 대조용", "기본 실습이나 완료 기준으로 사용하지 않습니다",
                     "영상·문서·공식 자료 기반 대화", "Optional·Bonus", "미완료"):
            assert rule in content, (path, rule)
    assert "독립 품질" in _normalized("ROADMAP.md")
    assert "공식 필수 과제 완료를 대신하지 않는다" in _normalized("ROADMAP.md")


def test_selected_cs224n_scope_keeps_edition_and_ai_policy() -> None:
    agents = _normalized("AGENTS.md")
    for rule in ("CS224N is Spring 2024, archive 1246", "A3 Q1(i) and A4 Q1-Q2 written",
                 "Never mix Winter 2024 archive 1244",
                 "AI collaboration is allowed but direct answer solicitation, copying answers, and substantial completion by AI are prohibited"):
        assert rule in agents
    for path in ("practice/README.md", "ROADMAP.md", "DEFERRED.md"):
        content = _normalized(path)
        assert "1246" in content and "Q1(i)" in content
        assert "written" in content and "programming" in content
        assert "보류" in content and "Final Project" in content


def test_foundations_first_route_is_pinned() -> None:
    roadmap = _normalized("ROADMAP.md")
    headings = [roadmap.index(f"## P{index} ") for index in range(6)]
    assert headings == sorted(headings)
    for phase in ("`P0`", "`P1`", "`P2`", "`P3`", "`P4`", "`P5`"):
        assert phase in roadmap
    assert "개인 LLM Research Engineer" in roadmap
    assert "잠정 **Systems / Inference**" in roadmap
    assert "평가를 P5까지 미루지 않는다" in roadmap
    assert "강의 수강 자체는" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Foundations are not optional here" in agents
    assert "Do not propose reordering a later Phase forward" in agents


def test_personal_budget_example_has_no_hidden_activity_hours() -> None:
    headers, activities, total = _budget_table()
    assert headers == ["개인 학습 활동", "예시"]
    assert activities == {"공식 읽기·수학·통계": 18, "학습자 구현·디버깅": 27,
                          "실험·평가·해석": 9, "지연 회상·전이·정리": 6}
    assert sum(activities.values()) == total == 60


def test_budget_is_an_excluded_activity_intent_not_a_fixed_calendar() -> None:
    roadmap = _normalized("ROADMAP.md")
    for rule in ("개인 학습 주 60시간 이상", "KANT 수업 주 40시간",
                 "알고리즘 약 2시간/일, 취업 준비는 제외", "초기 배분 가설",
                 "첫 1~2주", "확정 기본값으로 계승하지 않는다"):
        assert rule in roadmap
    assert not re.search(r"^\| `P[0-5]` \| \d+~\d+ \|", _raw("ROADMAP.md"), re.MULTILINE)
    assert "Use 52 calendar weeks with 48 effective study weeks" not in _normalized("AGENTS.md")


def test_approved_course_scope_and_phase_boundary_are_explicit() -> None:
    roadmap = _normalized("ROADMAP.md")
    for scope in ("MIT 18.05 Spring 2022", "PS1~PS11", "R 요구까지 모두 수행",
                  "CS229 Summer 2020", "PS1, PS2, PS3의 필수 written과 coding을 모두 수행",
                  "PS3 Q1 RL와 Q6 ICA는 기존 필수 범위로 유지",
                  "공식 문제를 임의 NumPy 연습으로 대체하지 않습니다",
                  "CS231n Spring 2024 Lecture 2~6", "A2 Q1~Q3",
                  "CS224N Spring 2024", "Q1(i)", "Q1 Attention Exploration",
                  "Q2 Position Embeddings Exploration", "GPT bridge"):
        assert scope in roadmap
    agents = _normalized("AGENTS.md")
    assert "NumPy reimplementations cannot replace official problem sets" in agents
    assert "PS3 Q1 RL and Q6 ICA stay required" in agents


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


def test_lm_training_systems_and_inference_have_distinct_scope() -> None:
    roadmap = _normalized("ROADMAP.md")
    p3 = roadmap.split("## P3 —", 1)[1].split("## P4 —", 1)[0]
    for scope in ("Assignment 1 Basics", "v26.0.3",
                  "a158843b20107949f1a8d7df1b05cd33b9166712", "교육용 핵심 구현",
                  "임의 축소 실험", "공식 A1 수행", "CPU/MPS", "TinyStories"):
        assert scope in p3
    p4 = roadmap.split("## P4 —", 1)[1].split("## P5 —", 1)[0]
    for scope in ("v26.1.3", "ca8bc81a59b70516f7ebb2da4808daade877c736",
                  "학습 성능·분산 학습 과제", "B200", "2/4/6 GPU", "OPTIONAL",
                  "prefill", "decode", "TTFT", "ITL", "queueing", "EOS"):
        assert scope in p4
    assert "공식 전체 A2는 현재 필수 관문이 아니다" in p4
    p5 = roadmap.split("## P5 —", 1)[1].split("## 평가와 대표 관문", 1)[0]
    assert "프로젝트와 논문 재현을 따로 만들지 않습니다" in p5
    for item in ("baseline", "통제 조건", "ablation", "실패 사례", "claim limits", "최대 세 산출물"):
        assert item in p5


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
    roadmap = _normalized("ROADMAP.md")
    for source in ("fast.ai", "Made With ML", "Full Stack Deep Learning", "roadmap.sh",
                   "CMU", "smol-course", "Raschka"):
        assert source in roadmap
    for rule in ("top-down", "판본 주의", "ML 시스템 설계",
                 "전체 과정을 별도 졸업 조건으로 추가하지 않습니다"):
        assert rule in roadmap


def test_job_ladder_is_marked_as_assessment_not_fact() -> None:
    roadmap = _normalized("ROADMAP.md")
    assert "LLM Research Engineer" in roadmap
    assert "특정 Phase가 취업이나 지원 자격을 보장하지 않습니다" in roadmap
    assert "실제 공고 3~5건" in roadmap
    assert "공고가 경로와 다르면 공고를 기준으로 경로를 재검토합니다" in roadmap
    agents = _normalized("AGENTS.md")
    assert "Treat the job-role comparisons as an assessment to re-check against real postings" in agents
    assert "without promising employability at any Phase or date" in agents
    assert "an earlier rung is not a failure" in agents


def test_competitions_and_papers_are_tracks_that_cannot_be_fabricated() -> None:
    roadmap = _normalized("ROADMAP.md")
    assert "Kaggle은 P1만 필수입니다" in roadmap
    assert "P0·P2·P3은 선택" in roadmap
    assert "실제 목록" in roadmap
    assert "한 연구 질문" in roadmap and "논문 주장 하나" in roadmap
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


def test_phase_check_does_not_require_paid_gpu_for_available_local_work() -> None:
    roadmap = _normalized("ROADMAP.md")
    for scope in ("로컬 필수 검증", "축소·추가 자원 검증의 경계", "공식 저자원 경로",
                  "VRAM뿐 아니라 연산시간·장치 수·공식 지정 hardware", "가능한 로컬 학습을 계속",
                  "필수 항목이 비면 Phase를 닫지 않는다", "교육적 타당성 검토와 다르며"):
        assert scope in roadmap
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
    for path in ("practice/README.md", "ROADMAP.md"):
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


def test_usage_documents_the_session_loop() -> None:
    # User guides expose the requests and link to the authoritative procedure;
    # they need not repeat every course or permission rule verbatim.
    for path in ("README.md", "USAGE.md"):
        text = _raw(path)
        for request in ("오늘 학습 시작", "계속", "오늘 학습 종료", "이번 주 회상", "$study-session"):
            assert request in text, (path, request)
        for target in ("AGENTS.md", "STATE.md", "ROADMAP.md", ".agents/skills/study-session/SKILL.md"):
            assert re.search(r"\]\(\.?/?" + re.escape(target) + r"(?:#[^)]*)?\)", text), (path, target)


def test_state_updates_without_prior_approval_from_confirmed_evidence() -> None:
    agents = _normalized("AGENTS.md")
    assert "Update `STATE.md` without prior proposal or approval" in agents
    assert "distinguish completed work, planned work, and unverified claims" in agents
    assert "does not authorize a new course, a sequence change" in agents
    assert "At a Phase transition, run the `ROADMAP.md` check first" in agents
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
    assert "The Phase ID is a static pointer into `ROADMAP.md`" in agents
    assert "Never add a percentage, a score, a readiness judgement, an hour tally" in agents
    assert "a Phase ID is not an opening to bring them back" in agents
    assert "hashes, readiness scores, session history, or metrics" in agents


def test_understanding_is_verified_by_unassisted_recall() -> None:
    """Evidence and artifact permissions stay in the shared contract.

    Tutoring behavior is exercised separately with isolated response cases;
    matching prose in several guides cannot establish tutor compliance.
    """
    agents = _normalized("AGENTS.md")
    assert "Tutor explanations, assent, file existence, successful execution, and green tests alone do not establish understanding" in agents
    assert "Confirm the learner's unassisted concept drafts before knowledge edits or workspace reset" in agents
    assert "Separate API-doc-assisted practical implementation from closed-book recall" in agents
    assert "Same-day success does not establish delayed recall or transfer" in agents
    assert "explains the whole Phase without notes" in agents
    assert "representative implementation units" in agents
    assert "Do not require rewriting every module's full implementation or entire assignments" in agents

    knowledge = _normalized("knowledge/README.md")
    assert "교정할 knowledge 초안은 대화·강의·기존 노트를 닫고 학습자가 기억으로 먼저" in knowledge
    assert "그 초안 이후에만 공식 자료와 대조" in knowledge
    assert "AI가 면접 답변집이나 완성 노트를 먼저 작성하지 않습니다" in knowledge
    for path in ("ROADMAP.md",):
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
    assert "기존 A1~A4 전체 의무를 이번 승인 재설계로 줄였으며" in deferred
    assert "나머지 written·programming·Final Project" in deferred


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
    # Utility permissions do not depend on the number of unrelated skills.
    assert expected | {"finish-chapter"} <= actual

    for name in expected:
        entrypoint = _normalized(f".agents/skills/{name}/SKILL.md")
        manifest = _normalized(f".agents/skills/{name}/agents/openai.yaml")
        assert "Use only when the learner" in entrypoint
        assert "Commit and push each require a separate explicit request" in entrypoint
        assert "allow_implicit_invocation: false" in manifest


def test_study_skill_is_reachable_through_the_shared_contract() -> None:
    skill = REPO / ".agents/skills/study-session/SKILL.md"
    assert skill.is_file()
    assert ".agents/skills/study-session/SKILL.md" in _raw("AGENTS.md")
    claude = REPO / "CLAUDE.md"
    assert claude.is_symlink()
    assert claude.resolve() == REPO / "AGENTS.md"

    content = skill.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", content, re.DOTALL)
    assert frontmatter is not None
    assert re.search(r"^name: study-session$", frontmatter.group(1), re.MULTILINE)
    assert re.search(r"^description:.*\S", frontmatter.group(1), re.MULTILINE)
    manifest = _normalized(".agents/skills/study-session/agents/openai.yaml")
    assert "allow_implicit_invocation: true" in manifest
    assert "$study-session" in manifest

    # These are resolvable instruction resources, not a learning-state engine.
    assert not (skill.parent / "scripts").exists()
    reference = skill.parent / "references/tutor-cases.md"
    assert reference.is_file()
    assert "references/tutor-cases.md" in content
    for target in re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", content):
        if "://" in target or target.startswith("#"):
            continue
        assert (skill.parent / target.split("#", 1)[0]).resolve().exists(), target


def test_chapter_wrap_up_defaults_to_confirmed_transitions_only() -> None:
    entrypoint = _normalized(".agents/skills/finish-chapter/SKILL.md")
    manifest = _normalized(".agents/skills/finish-chapter/agents/openai.yaml")
    assert "allow_implicit_invocation: true" in manifest
    assert "confirmed chapter transition" in entrypoint
    assert "standing chapter-transition authorization" in entrypoint
    assert "Default chapter-transition wrap-up" in _normalized("AGENTS.md")
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


def test_state_update_is_edit_only_except_explicit_study_stop() -> None:
    agents = _normalized("AGENTS.md")
    assert "Updating `STATE.md`, automatically or on request, authorizes only the file edit" in agents
    assert "An explicit study-stop request is the standing exception" in agents
    assert "authorized a scoped commit and push without another confirmation" in agents


def test_cs336_uses_a_separate_python_environment() -> None:
    pyproject = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["requires-python"] == ">=3.14,<3.15"

    agents = _normalized("AGENTS.md")
    assert "learning lab's Python 3.14 environment" in agents
    assert "separate sibling clone" in agents
    assert "Python 3.12 or 3.13" in agents


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

def test_error_hypothesis_is_required_only_after_an_error() -> None:
    agents = _normalized("AGENTS.md")
    assert "If an error occurred" in agents
    assert "first cause hypothesis formed before changing the code and how they checked it" in agents
    assert "do not require an error when none occurred" in agents
