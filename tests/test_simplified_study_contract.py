from __future__ import annotations

import hashlib
import re
import runpy
import tomllib
from pathlib import Path
from urllib.parse import unquote

import pytest


REPO = Path(__file__).resolve().parents[1]
_EXTRACT_LINK_TARGETS = runpy.run_path(
    str(REPO / ".agents/skills/update-learning-knowledge/scripts/validate_knowledge.py")
)["extract_link_targets"]

OPERATING_DOCS = (
    "AGENTS.md", "STATE.md", "README.md", "USAGE.md",
    "ROADMAP.md", "CURRICULUM.md", "DEFERRED.md",
    ".agents/references/learning-policies.md",
    ".agents/references/official-course-policies.md",
    ".agents/references/recordkeeping-policies.md",
    ".agents/skills/study-session/SKILL.md",
    ".agents/skills/study-session/references/tutor-cases.md",
    ".agents/skills/finish-chapter/SKILL.md",
    ".agents/skills/finish-chapter/references/chapter-review.md",
    ".agents/skills/save-today-til/SKILL.md",
    ".agents/skills/update-learning-knowledge/SKILL.md",
    ".specify/README.md", ".specify/memory/constitution.md",
    "practice/README.md", "practice/ai-apps/README.md",
    "materials/README.md", "challenges/README.md",
    "challenges/deep-ml/README.md", "knowledge/README.md",
    "knowledge/template.md", "til/README.md", "til/template.md",
)


def _raw(path: str) -> str:
    return (REPO / path).read_text(encoding="utf-8")


def _normalized(path: str) -> str:
    return re.sub(r"\s+", " ", _raw(path))


def _markdown_cells(line: str) -> list[str]:
    stripped = line.strip()
    assert stripped.startswith("|") and stripped.endswith("|")
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _contract() -> str:
    # Inspect canonical contracts; this is not a loader or a study reading list.
    sources = (
        "AGENTS.md",
        ".agents/references/learning-policies.md",
        ".agents/references/official-course-policies.md",
        ".agents/references/recordkeeping-policies.md",
    )
    return " ".join(_normalized(path) for path in sources)



def _doc_lines(path: Path) -> list[tuple[int, str]]:
    """Markdown lines outside fenced/inline examples; never execute examples."""
    visible = []
    fence = ""
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = ""
            continue
        if marker:
            fence = marker[1]
            continue
        visible.append((number, line))
    return visible


def _doc_heading_ids(path: Path) -> set[str]:
    """GitHub-style ATX heading IDs used by this repository, including duplicates."""
    ids: set[str] = set()
    for _, line in _doc_lines(path):
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*$", line)
        if not heading:
            continue
        text = re.sub(r"<[^>]+>", "", heading[1])
        text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
        slug = re.sub(r"[^\w\s-]", "", text.lower())
        slug = re.sub(r"\s", "-", slug.strip())
        candidate, suffix = slug, 0
        while candidate in ids:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        ids.add(candidate)
    return ids


def _doc_link_errors(path: Path) -> list[str]:
    """Check local inline link files/headings; external URLs and templates are inert."""
    if not path.is_file():
        return [f"{path}: document missing"]
    errors = []
    for number, line in _doc_lines(path):
        line = re.sub(r"`+[^`]*`+", "", line)
        for raw in _EXTRACT_LINK_TARGETS(line):
            target = raw.strip()
            if target.startswith("<") and ">" in target:
                target = target[1:target.index(">")]
            else:
                target = target.split(maxsplit=1)[0] if target else ""
            if re.match(r"[a-zA-Z][\w+.-]*:", target) or target.startswith("//"):
                continue
            file_part, _, fragment = target.partition("#")
            file_part = re.sub(r"\\([\\()])", r"\1", unquote(file_part))
            fragment = unquote(fragment)
            if re.search(r"[<>{}]", file_part):
                continue  # e.g. knowledge/<area>/<concept>.md, not a real file.
            linked = (path.parent / file_part).resolve() if file_part else path.resolve()
            prefix = f"{path}:{number}: {raw}"
            if not linked.exists():
                errors.append(f"{prefix}: target missing")
                continue
            if linked.is_dir():
                linked = linked / "README.md"
            if fragment and linked.suffix.lower() == ".md":
                if not linked.is_file() or fragment not in _doc_heading_ids(linked):
                    errors.append(f"{prefix}: heading missing")
    return errors


def _unit(unit: str) -> str:
    return re.split(r"^## ", _raw("ROADMAP.md").split(f"## {unit} —", 1)[1], maxsplit=1, flags=re.M)[0]


def test_plain_study_phrases_use_state() -> None:
    agents = _contract()
    for phrase in ("오늘 학습 시작", "오늘 전체 학습 흐름 시작", "전체 학습 흐름 시작", "계속", "오늘 학습 종료", "이번 주 회상", "$study-session"):
        assert phrase in agents
    for rule in ("resume the next independent action in `STATE.md`", "Do not begin with a new readiness diagnostic or roadmap review", "Never invent source content, timestamps, or learner viewing progress"):
        assert rule in agents


def test_study_route_does_not_restore_fixed_entry_gates() -> None:
    for path in ("AGENTS.md", "README.md", "USAGE.md"):
        content = _normalized(path)
        for obsolete in ("The pilot spine is", "at most two focused bridge modules",
                         "Before proposing Assignment 1 entry, run", "최대 두 번",
                         "현재 첫 행동은", "Pilot의 주축은"):
            assert obsolete not in content
    agents = _contract()
    assert "Do not impose a second full tokenizer/Transformer implementation as an entry test" in agents
    assert "Entry does not cancel unfinished work" in agents


def test_study_entrypoints_do_not_end_at_one_module() -> None:
    """Guard obsolete routing text; actual continuation needs response evaluation."""
    for path in ("AGENTS.md", ".agents/skills/study-session/SKILL.md",
                 "README.md", "USAGE.md"):
        content = _normalized(path)
        for request in ("오늘 학습 시작", "오늘 전체 학습 흐름 시작", "전체 학습 흐름 시작"):
            assert request in content, (path, request)
        for obsolete in ("one connected module in the current approved course",
                         "연결된 모듈 하나", "한 모듈에서 멈춥니다"):
            assert obsolete not in content, (path, obsolete)


def test_tutoring_contract_teaches_before_requesting_an_attempt() -> None:
    agents = _contract()
    skill = _normalized(".agents/skills/study-session/SKILL.md")
    assert "Do not require direct textbook reading before starting or resuming" in agents
    assert "givens, conditions, and required output in the conversation" in agents
    assert "not learner-visible givens: include the actual values and shapes" in agents
    assert "withholding formulas and derived shapes whose reconstruction is the learning target" in agents
    assert "reuse verified source details and instructions" in agents
    assert "when uncertainty arises" in agents
    assert "not just a source link or section number" in skill
    assert "never claim the learner read a source unless they confirm it" in skill
    assert "During cold recall, do not prefill answer cues" in skill
    assert "Do not replace the missing segment with a lesson inferred from its title or general recollection" in agents


def test_tutoring_contract_distinguishes_support_progress_and_mastery() -> None:
    agents = _contract()
    skill = _normalized(".agents/skills/study-session/SKILL.md")
    assert "unrelated inputs and a separate toy task" in agents
    assert "Explain the relevant parameters and their values; generic API signatures and calls are allowed" in agents
    assert "Never adapt that example into the target exercise's code, answer, or scaffold" in agents
    assert "including spelling out the target's exact API call, inputs, and chosen arguments in prose" in agents
    assert "the same solution under renamed variables is still a target answer" in agents
    assert "Ask at most one clarifying follow-up seeking the same answer" in skill
    assert "change the explanation or representation instead of repeating the question" in skill
    assert "Briefly correct nonblocking gaps in wording or reasoning and continue" in skill
    assert "Incomplete independent evidence alone does not stop ordinary progress" in skill
    assert "Finishing an ordinary explanation or feedback response does not trigger a checkpoint" in skill
    assert "Keep components already accepted in the current activity out of the next quiz" in skill
    assert "preserve unanswered formal requirements" in skill
    assert "teach any genuine prerequisite before its dependent activity" in skill


def test_selected_official_practice_keeps_requirements_without_becoming_an_ax_gate() -> None:
    contract = _contract()
    for rule in ("inspect actual requirements before assigning them", "KANT is supporting context", "limits as incomplete", "Preserve Optional/Bonus labels", "do not describe dialogue as video viewing or local checks as official university grading"):
        assert rule in contract
    for path in ("practice/README.md", "ROADMAP.md"):
        text = _normalized(path)
        for boundary in ("Optional·Bonus", "미완료", "공식", "KANT"):
            assert boundary in text, (path, boundary)
    assert "공식 과제를 선택하면" in _raw("ROADMAP.md")


def test_reselected_cs224n_keeps_edition_and_ai_policy() -> None:
    agents = _contract()
    for rule in ("CS224N is Spring 2024, archive 1246", "A3 Q1(i) and A4 Q1-Q2 written", "Never mix Winter 2024 archive 1244", "AI collaboration is allowed but direct answer solicitation, copying answers, and substantial completion by AI are prohibited"):
        assert rule in agents
    deferred = _raw("DEFERRED.md")
    assert all(term in deferred for term in ("1246", "Q1(i)", "written", "programming", "Final Project", "보류"))


def test_ax_then_re_units_have_complete_context_and_source_mapping() -> None:
    roadmap = _raw("ROADMAP.md")
    expected = [f"{track}-{i:02}" for track in ("AX", "RE") for i in range(1, 5)]
    units = re.findall(r"^## ((?:AX|RE)-\d{2}) —", roadmap, re.M)
    assert units == expected
    fields = ("사용자 문제", "구현 목적", "이전·다음 연결", "입력·출력", "전체 데이터 흐름", "학습자 직접 작업", "관찰 결과", "완료 기준", "최소 선수", "작업 중 보강 개념")
    for unit in expected:
        section = _unit(unit)
        rows = [_markdown_cells(line) for line in section.splitlines() if line.startswith("|")]
        labels = [row[0] for row in rows]
        assert all(labels.count(field) == 1 for field in fields), unit
        assert "자료·근거" in section, unit
    assert "한 서비스" in roadmap
    assert "LLM Research Engineer" in roadmap
    assert "사용자 지정 필수 순서가 아니다" in roadmap


def test_old_hours_and_phase_quotas_are_not_active_gates() -> None:
    roadmap = _raw("ROADMAP.md")
    assert not re.search(r"^## P[0-5] |^\| 개인 학습 활동 \|", roadmap, re.M)
    assert "의무 시간표" in roadmap
    assert "18/27/9/6" in _raw("DEFERRED.md")
    assert not re.search(r"^\| `P[0-5]` \|", roadmap, re.M)


def test_no_fixed_calendar_or_automatic_curriculum_engine() -> None:
    for path in ("ROADMAP.md", "AGENTS.md", "STATE.md"):
        text = _raw(path)
        assert "2880" not in text
    assert "자동 커리큘럼 선택기" in _raw("AGENTS.md")
    assert "고정" in _raw("ROADMAP.md") and "보장" in _raw("ROADMAP.md")


def test_first_baseline_has_its_own_completion_boundary() -> None:
    first = _unit("AX-01")
    for term in ("정상", "누락", "범위 밖", "baseline", "실제", "미실행", "Python", "JSON/HTTP"):
        assert term in first
    assert "긴 선행 수강 없이 시작" in first
    assert "식별자·본문" in first
    assert "모델 접근 미해결은 미실행" in first


def test_representative_recall_is_distinct_from_api_practical_work() -> None:
    text = _contract()
    for rule in ("Separate API-doc-assisted practical implementation from closed-book recall", "not even an import list or a function signature", "Do not require rewriting every module's full implementation or entire assignments", "is not recorded as passed"):
        assert rule in text
    deepml = _raw("challenges/deep-ml/README.md")
    assert "별도 필수 트랙" in deepml
    assert "공백" in deepml
    assert "현재 Phase의" not in deepml


def test_prerequisites_have_use_sites_and_observed_repair_conditions() -> None:
    text = _raw("CURRICULUM.md").split("## 4. 공통 핵심 역량", 1)[0]
    for term in ("조건부확률", "LLN·CLT", "likelihood", "gradient", "Jacobian", "bootstrap", "검정력", "사용처", "공백", "AX-01", "RE-01"):
        assert term in text
    for line in text.splitlines():
        if re.match(r"^\| (?:AX|RE)-\d", line):
            cells = _markdown_cells(line)
            assert len(cells) >= 5 and all(cell.strip() for cell in cells)
    assert "R을 요구" in _contract()


def test_lm_and_specialization_are_alternatives_with_resource_limits() -> None:
    lm, specialization = _unit("RE-02"), _unit("RE-03")
    assert "대체" in lm and "A1" in lm and "자체" in lm
    assert "post-training/evaluation" in specialization and "inference/systems" in specialization
    assert "둘 다" in specialization and "의무" in specialization
    contract = _contract()
    for term in ("v26.0.3", "a158843b20107949f1a8d7df1b05cd33b9166712", "v26.1.3", "ca8bc81a59b70516f7ebb2da4808daade877c736", "CPU/MPS", "TinyStories", "B200", "OPTIONAL", "TTFT", "ITL", "queueing", "EOS"):
        assert term in contract
    assert "ablation" in _unit("RE-04")


def test_historical_catalog_registry_and_audit_body_are_byte_preserved() -> None:
    raw = _raw("CURRICULUM.md")
    historical = raw.split("## 4. 공통 핵심 역량", 1)[1].split("## 9. 갱신 규칙", 1)[0]
    assert hashlib.sha256(historical.encode()).hexdigest() == "26b9580670fae3017abecde4b873034b274db6941ff7e295d0614af1d7efc2e9"
    active = raw.split("## 4. 공통 핵심 역량", 1)[0]
    assert "역사적 참고" in active and "현재 지시가 아니다" in active
    assert "새 자료를 다운로드하거나 전체 감사한 것으로 기록하지 않는다" in active


def test_source_observation_is_distinct_from_design_and_current_access() -> None:
    active = _raw("CURRICULUM.md").split("## 4. 공통 핵심 역량", 1)[0]
    for ref in ("MIT 6.S191", "2026", "CS336", "Hugging Face", "Full Stack Deep Learning", "2023", "판본", "접근", "설계 판단"):
        assert ref in active
    for target in ("research/jd-evidence.md", "research/reference-curricula.md", "research/trend-evidence.md", "research/decision-matrix.md"):
        assert target in active


def test_minimum_portfolio_has_six_fields_and_does_not_certify_eligibility() -> None:
    text = _raw("ROADMAP.md")
    for item in ("사용자 문제", "직접 작동 기능", "평가·실패 사례", "재현 조건", "자기 기여·도움", "주장 한계"):
        assert f"| {item} |" in text
    assert "조기" in text and "주 포트폴리오" in text
    for term in ("필수·우대", "연차·학위", "보장하지", "다른 언어"):
        assert term in text


def test_competitions_and_papers_cannot_be_fabricated_or_become_quotas() -> None:
    agents = _contract()
    for rule in ("Competitions and papers are proposed, never invented", "do not name a specific kaggle competition without checking", "never cite a title, venue, year, or result you have not verified", "never fill a gap in a reproduction with a plausible number", "The learner writes the paper summary"):
        assert rule.lower() in agents.lower()
    assert "월별" in _raw("DEFERRED.md")


def test_all_competitions_are_optional() -> None:
    deferred = _raw("DEFERRED.md")
    assert "P1 Kaggle" in deferred and "모든 대회" in deferred
    assert "의무 해제" in deferred
    assert "Kaggle은 P1만 필수" not in _raw("ROADMAP.md")


def test_comparison_failure_and_unavailable_resources_remain_distinct() -> None:
    roadmap = _raw("ROADMAP.md")
    assert "미개선" in roadmap and "미실행" in roadmap
    assert "가능한 로컬" in _contract()
    assert "유료" in _contract() and "별도" in _contract()
    assert "실제 배포" in roadmap and "로컬" in roadmap


def test_graded_coursework_stays_out_of_the_public_repository() -> None:
    agents = _contract()
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
    agents = _contract()
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


def test_state_updates_without_reapproval_within_authorized_scope() -> None:
    agents = _contract()
    assert "Update `STATE.md` without prior proposal or approval" in agents
    assert "distinguish completed work, planned work, and unverified claims" in agents
    assert "does not authorize a new course, a sequence change" in agents
    for path in ("README.md", "USAGE.md"):
        assert "STATE 승인 후" not in _raw(path)


def test_unit_reference_does_not_reopen_progress_tracking() -> None:
    agents = _contract()
    assert "static reference" in agents
    assert "Never add a percentage, a score, a readiness judgement, an hour tally" in agents
    assert "hashes, readiness scores, session history, or metrics" in agents


def test_evidence_contract_separates_practical_work_and_unassisted_recall() -> None:
    """Evidence and artifact permissions stay in the shared contract.

    These assertions check the published evidence contract only. Actual tutor
    behavior requires separate response review or resumed-study observation;
    matching prose in several guides cannot establish tutor compliance.
    """
    agents = _contract()
    assert "Tutor explanations, assent, file existence, successful execution, and green tests alone do not establish understanding" in agents
    assert "Confirm the learner's unassisted concept drafts before knowledge edits or workspace reset" in agents
    assert "Separate API-doc-assisted practical implementation from closed-book recall" in agents
    assert "Same-day success does not establish delayed recall or transfer" in agents
    assert "representative implementation units" in agents.lower()
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


def test_setup_responsibility_defines_distinct_starting_states() -> None:
    """This checks the documented contract, not actual tutor compliance."""
    agents = _raw(".agents/references/learning-policies.md")
    setup = agents.split("## Learning setup and starting materials", 1)[1].split(
        "## Learner ownership and evidence", 1
    )[0]
    rows = [_markdown_cells(line) for line in setup.splitlines()
            if line.startswith("|") and not line.startswith("|---")]
    assert len(rows) == 4
    states = {row[0]: row[1] for row in rows[1:]}
    assert "unfinished" in states["Work using a supplied starter"]
    reproduction = states["Fresh-kernel reproduction of existing code"]
    for requirement in ("unchanged", "working copy", "outputs", "execution counts"):
        assert requirement in reproduction
    recall = states["Representative unassisted reconstruction or cold recall"]
    for requirement in ("blank", "no code", "imports", "signatures", "skeletons"):
        assert requirement in recall


def test_setup_authorization_preserves_targets_and_restricted_actions() -> None:
    agents = _contract()
    setup = agents.split("## Learning setup and starting materials", 1)[1].split(
        "## Learner ownership and evidence", 1
    )[0]
    assert "A study-start or resume request includes this routine preparation" in setup
    assert "do not ask the learner to choose its scope or manually copy preparation cells" in setup
    assert "do not overwrite a nonempty working space without authorization" in setup
    assert "Preserve original starters, archives, and existing learner-owned cells" in setup
    for restriction in ("Course-specific AI", "command-execution", "acquisition",
                        "separate-environment", "paid-resource", "publication"):
        assert restriction in setup
    assert "unfinished learner-target portions" in setup
    assert "silently repair existing learner code" in setup
    assert "changing learner-owned implementation or executing a learner's notebook needs explicit authorization" in agents
    assert "not by running learner cells" in agents
    assert "not by itself prohibit permitted preparation" in setup
    assert "ask only for those missing facts" in setup
    assert "Do not assign package installation, configuration creation, or kernel repair to the learner as their next action" in setup
    assert "do not make learner-owned diagnosis or adaptation a new approval gate" in setup
    assert "distinguish any learner-adapted run from unchanged-code reproduction" in setup
    skill = _normalized(".agents/skills/study-session/SKILL.md")
    assert "without handing installation, configuration, or kernel repair to the learner" in skill
    assert "do not add a setup-scope approval gate or write the fix" in skill
    assert "repair that responsibility from the verified source and actual artifacts" in agents


def test_setup_policy_is_shared_without_blanket_cell_or_notebook_bans() -> None:
    obsolete = (
        "Do not write exercise code, answer lines, cells, skeletons",
        "Never supply exercise code, answer lines, cells, skeletons",
        "Do not provide target exercise code or setup skeletons to either mode",
        "Ordinary study does not create a Notebook",
        "Never silently fill a learner gap in setup",
    )
    for path in ("AGENTS.md", ".agents/skills/study-session/SKILL.md"):
        content = _normalized(path)
        for blanket in obsolete:
            assert blanket not in content, (path, blanket)
    for path in ("README.md", "USAGE.md", "practice/README.md"):
        assert "learning-policies.md#learning-setup-and-starting-materials" in _raw(path)
    practice = _normalized("practice/README.md")
    assert "위 준비 범위 외의 파일 생성·수정" in practice
    assert "정확한 파일 생성·수정 요청이나 확인된 챕터 전환" not in practice
    claude = REPO / "CLAUDE.md"
    assert claude.is_symlink()
    assert claude.resolve() == (REPO / "AGENTS.md").resolve()


def test_behavior_cases_separate_response_judgments_from_artifact_checks() -> None:
    cases = _normalized(".agents/skills/study-session/references/tutor-cases.md")
    for family in ("Supplied incomplete starter", "Existing-code fresh-kernel reproduction",
                   "Unassisted reconstruction starting state",
                   "Learner responsibility correction across turns",
                   "Incorrect preparation action in STATE",
                   "Preparation support and evidence classification",
                   "Missing source or real overwrite conflict",
                   "Preparation does not expand restricted authorization"):
        assert family in cases
    for boundary in ("actual resumed conversations", "actor's own response",
                     "Tool-enabled preparation checks", "synthetic inputs",
                     "rubric", "outside the actor's workspace and prompt",
                     "byte-identical", "do not execute notebook cells",
                     "failed or unsupported runs remain incomplete evidence"):
        assert boundary in cases


def test_tutoring_flow_cases_cover_the_approved_behavior_comparison() -> None:
    """Check evaluation coverage, not whether a tutor followed the contract."""
    cases = _normalized(".agents/skills/study-session/references/tutor-cases.md")
    for family in ("Normal resume and continuous study",
                   "Missing prerequisite and repeated uncertainty",
                   "Partial answer, misconception, and grounding",
                   "Assisted exercise and missing transfer",
                   "API-assisted implementation versus delayed recall",
                   "Teaching without direct textbook reading",
                   "Quiet bookmarks and verified-context reuse",
                   "Unavailable source, course boundary, and unknown chronology",
                   "Manual weekly follow-up, pause, and explicit end"):
        assert family in cases, family
    for method in ("baseline and candidate in fresh, empty contexts",
                   "same user-approved model and reasoning effort",
                   "Change only the instruction bundle",
                   "Prohibit tool use and exclude any run that used tools",
                   "without injecting a replacement assistant response",
                   "new directory for each revision rather than overwriting failures",
                   "none establishes delayed learner memory"):
        assert method in cases, method


def test_deferred_entries_cover_old_and_new_holds_with_reasons() -> None:
    text = _raw("DEFERRED.md")
    rows = [_markdown_cells(line) for line in text.splitlines() if line.startswith("| ")][2:]
    assert len(rows) >= 20
    for row in rows:
        assert len(row) == 4 and all(cell and cell != "—" for cell in row)
    for term in ("MML", "MIT 18.05", "makemore", "fast.ai", "CS229", "ISLP", "CS231n", "CS224N", "CS336", "Kaggle", "18/27/9/6", "multi-agent", "TF-IDF", "MCP", "WaveNet", "Final Project", "Assignment 3", "Hugging Face"):
        assert term in text
    assert "조건이 생겨도 자동으로 시작하지 않고" in text
    assert "미완료 보류" in text


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
    roadmap, curriculum = _raw("ROADMAP.md"), _raw("CURRICULUM.md")
    assert "현재 학습 범위와 다음 행동은 [`STATE.md`](./STATE.md)만 정합니다" in roadmap
    assert "현재 학습 범위와 다음 행동은 `STATE.md`만 정하며" in curriculum
    assert "실제 파일과 `INDEX.md`를 수동으로 교차 확인한다" in curriculum
    assert "자동" in _raw("AGENTS.md")


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
    assert "Default chapter-transition wrap-up" in _contract()
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


def _assert_public_bookmark(state: str) -> None:
    """Check the bookmark's structure and privacy, without grading its prose.

    Whether unnumbered sentences share one purpose needs a manual semantic
    review. This guard must accept connected steps without requiring particular
    verbs or refer-back words, and never selects a lesson or writes STATE.
    """
    fields = {}
    for label in ("현재 경로", "현재 단위", "현재 범위", "확인된 근거", "재확인"):
        values = re.findall(rf"^- {label}: ([^\n]*)$", state, re.M)
        assert len(values) == 1 and values[0].strip(), label
        fields[label] = values[0].strip()
    valid_units = set(re.findall(r"^## ((?:AX|RE)-\d{2}) —", _raw("ROADMAP.md"), re.M))
    current = re.match(r"((?:AX|RE)-\d{2})(?:\s|$)", fields["현재 단위"])
    assert current and current[1] in valid_units, "유효한 현재 단위"
    assert re.match(rf"{current[1][:2]}(?:\s|$)", fields["현재 경로"]), "경로/단위 일치"
    assert "재개 북마크" in state
    assert len(re.findall(r"^## 다음 독립 행동$", state, re.M)) == 1
    action = state.split("## 다음 독립 행동\n", 1)[1].strip()
    assert action and not re.fullmatch(r"(?:계속|다음|미정|TODO|진행|확인)(?:한다)?[.! ]*", action, re.I)
    assert not re.search(r"(?m)^#{1,6}\s+", action), "다음 행동 뒤의 별도 구간"
    bullets = re.findall(r"(?m)^\s*[-*+]\s+(?=\S)", action)
    numbered = re.findall(r"(?:^|\s)\d+[.)]\s+(?=\S)|[①-⑳]", action)
    assert len(bullets) + len(numbered) <= 1, "나열된 독립 목표"
    decoded = unquote(state).replace("\\", "/")
    for forbidden in ("schema_version", "evidence_id", "sha256", "materials/private",
                      "practice/private", "tmp/", "/home/", "/Users/", "C:/Users/", "- [ ]", "dprobs"):
        assert forbidden.casefold() not in decoded.casefold(), forbidden
    assert not re.search(r"(?im)^- (?:점수|진도율|누적 시간|이력|transcript):|(?:api[_ -]?key|password|access[_ -]?token)\s*[:=]", decoded)


def _sample_bookmark(unit: str, action: str) -> str:
    return f"""# Study State

현재 범위와 다음 행동의 재개 북마크다. 숙달 기록이 아니다.

- 현재 경로: {unit[:2]} — 승인 경로
- 현재 단위: {unit} — 현재 단위
- 현재 범위: 권리 확인 자료의 작은 기능/평가
- 확인된 근거: 제공 도구와 학습자 변경·실행/해석의 근거를 구분한다.
- 재확인: 다른 환경 재현·독립 수행·지연 기억은 미확인이다.

## 다음 독립 행동

{action}
"""


@pytest.mark.parametrize(("unit", "action"), [
    ("AX-01", "저장된 응답을 원문/추가 확인 기준과 비교하고 내용 오류를 첫 해석한다."),
    ("AX-02", "sparse 검색 baseline의 질의→근거→기권 기능을 작성·실행하고 실패를 해석한다."),
    ("AX-03", "로컬 조회 함수의 오류 반환을 구현한다. 같은 입력으로 실행하고 그 결과를 해석한다."),
    ("AX-03", "로컬 조회 함수를 작성한다. 저장하고 실행한다."),
    ("RE-02", "checkpoint를 불러와 이어 학습한다."),
    ("RE-03", "같은 모델과 요청 길이에서 지연을 재고 결과의 차이를 해석한다."),
    ("AX-04", "한 API 경계의 요청 검증을 작성한다. 그리고 같은 기능의 정상/실패 응답을 비교한다."),
    ("RE-01", "한 모델의 학습/검증 흐름을 작성→실행→첫 해석하여 손실 격차를 진단한다."),
    ("RE-04", "실제로 읽은 주장과 baseline의 부정 결과를 비교해 해석의 한계를 설명한다."),
])
def test_bookmark_accepts_later_units_and_connected_evaluation_actions(unit: str, action: str) -> None:
    _assert_public_bookmark(_sample_bookmark(unit, action))


@pytest.mark.parametrize("state", [
    _sample_bookmark("AX-99", "저장된 응답의 실패 원인을 해석한다."),
    _sample_bookmark("AX-01", ""),
    _sample_bookmark("AX-01", "계속"),
    _sample_bookmark("AX-01", "- 검색 baseline을 작성한다.\n- 새 모델의 학습을 구현한다."),
    _sample_bookmark("AX-01", "1) 검색 baseline을 작성한다. 2) 새 모델의 학습을 구현한다."),
    _sample_bookmark("AX-01", "① 검색 baseline을 작성한다. ② 새 모델의 학습을 구현한다."),
    _sample_bookmark("AX-01", "저장 응답을 /home/synthetic-user/run.json과 비교한다."),
    _sample_bookmark("AX-01", r"저장 응답을 C:\Users\synthetic-user\run.json과 비교한다."),
    _sample_bookmark("AX-01", "materials/private/source의 저장 응답을 비교한다."),
    _sample_bookmark("AX-01", "materials%2Fprivate%2Fsource의 저장 응답을 비교한다."),
    _sample_bookmark("AX-01", "저장 응답을 비교한다. api_key=synthetic-example"),
    _sample_bookmark("AX-01", "저장 응답을 비교한다.").replace("현재 경로: AX", "현재 경로: RE"),
    _sample_bookmark("AX-01", "저장 응답을 비교한다.").replace("- 확인된 근거:", "- 없는 필드:"),
    _sample_bookmark("AX-01", "저장 응답을 비교한다.").replace("- 재확인:", "- 없는 필드:"),
    _sample_bookmark("AX-01", "저장 응답을 비교한다.").replace("권리 확인 자료의 작은 기능/평가", " "),
])
def test_bookmark_rejects_invalid_empty_multiple_or_private_state(state: str) -> None:
    with pytest.raises(AssertionError):
        _assert_public_bookmark(state)


def test_state_is_a_public_bookmark_with_one_next_action_and_preserved_original() -> None:
    state = _raw("STATE.md")
    _assert_public_bookmark(state)
    archive = _raw("practice/reviews/curriculum-transition.md")
    original = archive.split("````text\n", 1)[1].rsplit("````\n", 1)[0]
    assert hashlib.sha256(original.encode()).hexdigest() == "bab21404447e173855853a825bbb4e987622036c496563b3f585b782711ba127"
    assert "당시 북마크 인용·현재 재개 사용 금지" in archive
    assert "curriculum-transition.md" in state
    for word in ("dprobs", "도움", "미확인", "미완료"):
        assert word in original


def test_state_update_is_edit_only_except_explicit_study_stop() -> None:
    agents = _contract()
    assert "Updating `STATE.md`, automatically or on request, authorizes only the file edit" in agents
    assert "An explicit study-stop request is the standing exception" in agents
    assert "authorized a scoped commit and push without another confirmation" in agents


def test_routine_bookmarks_are_quiet_and_pause_is_not_session_end() -> None:
    agents = _contract()
    assert "Do not edit it for each corrected answer when the resume action stays the same" in agents
    assert "Keep routine edits quiet" in agents
    assert "user asks for status, at an explicit study stop" in agents
    for path in ("AGENTS.md", ".agents/skills/study-session/SKILL.md"):
        content = _normalized(path)
        assert "does not trigger the closing commit or push procedure" in content, path
    for path in ("USAGE.md", "ROADMAP.md"):
        content = _normalized(path)
        for obsolete in ("수정하고 알린다", "수정하고 변경을 알립니다",
                         "의미 있는 재개 지점 변경만 알"):
            assert obsolete not in content, (path, obsolete)


def test_cs336_uses_a_separate_python_environment() -> None:
    pyproject = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["requires-python"] == ">=3.14,<3.15"

    agents = _contract()
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
    agents = _contract()
    assert "The learner writes the assignment code, runs the provided tests, and runs every bash command" in agents
    assert "must not execute bash commands in the assignment repository" in agents
    assert "already shown in the official handout" in agents
    assert "must not create a new command sequence to solve or automate the assignment" in agents
    assert "Do not provide code, pseudocode, patches, or TODO solutions, even after an explicit request" in agents
    assert "a158843b20107949f1a8d7df1b05cd33b9166712" in agents

def test_error_hypothesis_is_required_only_after_an_error() -> None:
    agents = _contract()
    assert "If an error occurred" in agents
    assert "first cause hypothesis formed before changing the code and how they checked it" in agents
    assert "do not require an error when none occurred" in agents


def test_root_size_mandatory_reads_and_core_safety_are_reachable() -> None:
    root = _raw("AGENTS.md")
    assert len(root.encode()) <= 12 * 1024
    for path in (".agents/skills/study-session/SKILL.md", ".agents/references/learning-policies.md", "STATE.md"):
        assert path in root[:5000]
        assert (REPO / path).is_file()
    for core in ("CS336", "pseudocode", "private", "nbpeek.py", "커밋", "푸시", "web/", "학습자"):
        assert core in root
    skill = _raw(".agents/skills/study-session/SKILL.md")
    assert "learning-policies.md" in skill and "read" in skill.lower()
    assert "@import" not in root


def test_research_and_learning_ids_are_static_references_with_full_mapping() -> None:
    mapping = _raw("specs/001-employment-project-curriculum/research/decision-matrix.md")
    sources = {name: _raw(f"specs/001-employment-project-curriculum/research/{name}.md") for name in ("jd-evidence", "reference-curricula", "trend-evidence")}
    assert len(re.findall(r"^\| JD-KR-0\d", sources["jd-evidence"], re.M)) >= 4
    assert len(re.findall(r"^\| JD-US-0\d", sources["jd-evidence"], re.M)) >= 4
    assert len(re.findall(r"^\| REF-\d", sources["reference-curricula"], re.M)) >= 6
    assert len(re.findall(r"^\| TREND-.*?2026-", sources["trend-evidence"], re.M)) >= 2
    for unit in [f"{track}-{i:02}" for track in ("AX", "RE") for i in range(1, 5)]:
        row = next(line for line in mapping.splitlines() if line.startswith(f"| **{unit} "))
        cells = _markdown_cells(row)
        assert len(cells) == 5 and all(cells)
        assert "JD-" in cells[1] and "REF-" in cells[3]


def test_unit_completion_does_not_trigger_wrap_up_or_new_learning_files() -> None:
    for path in ("AGENTS.md", ".agents/skills/study-session/SKILL.md", ".agents/skills/finish-chapter/SKILL.md"):
        text = _raw(path)
        assert "AX/RE" in text and "finish-chapter" in text
    assert "단위 완료" in _raw("AGENTS.md")
    assert "학습자 초안" in _raw("AGENTS.md")


def test_evaluation_separates_corpus_final_test_and_actual_outcome() -> None:
    text = _raw("ROADMAP.md")
    for term in ("독립 표본", "qrels", "train/dev", "최종 평가", "중복", "실제 상태", "판정기", "미사용 test", "반복 시도"):
        assert term in text


def test_conditional_search_and_workflow_choices_keep_their_purpose() -> None:
    """Guard changed scope; static documents alone cannot prove tutor behavior."""
    search, workflow = _unit("AX-02"), _unit("AX-03")
    assert "sparse baseline 하나" in search and "사전 학습 질문" in search
    assert "비교" in search and "선택" in search and "qrels" in search
    assert "Python 고정" in workflow
    for condition in ("상태 보존", "중단/재개", "승인", "모델 주도 선택", "단계 제한", "실제 상태"):
        assert condition in workflow
    assert "LangGraph 하나로 책임을 표현" not in workflow
    deferred = _raw("DEFERRED.md")
    for term in ("sparse baseline 하나부터", "Python 고정 흐름 우선", "옛 전체", "미수행"):
        assert term in deferred


def test_current_delegation_preserves_default_ownership_and_restricted_work() -> None:
    """Check the documented distinctions; V-B judges actual response excerpts."""
    policy = _normalized(".agents/references/learning-policies.md")
    ownership = policy.split("## Learner ownership and evidence", 1)[1].split("## Evidence and long-term review", 1)[0]
    for term in ("기본 학습", "현재 명시적으로 위임한 수정·작성·필요 검증", "요청 범위", "중복 승인", "일괄 거절", "보조 수행", "상시 대행 권한", "공식 과제", "무보조 확인", "백지 재작성"):
        assert term in ownership, term
    assert "even when asked" not in ownership
    # The strict official policy and cold-recall protections remain separate.
    assert "Do not provide code, pseudocode, patches, or TODO solutions, even after an explicit request" in _normalized(".agents/references/official-course-policies.md")
    assert "not even an import list or a function signature" in policy
    skill = _normalized(".agents/skills/study-session/SKILL.md")
    assert "현재 명시적으로 위임한 수정·작성·필요 검증" in skill
    assert "Prior help is not standing delegation" in skill


def test_validation_boundaries_cover_the_eight_cases_without_claiming_learning_effects() -> None:
    policy = _normalized(".agents/references/learning-policies.md")
    for level in ("V-A", "V-B", "V-C"):
        assert level in policy
    for limit in ("별도 학습 재개 요청", "첫 해석", "⑥기여/재현 설명", "미수행", "개선율"):
        assert limit in policy
    cases = _raw(".agents/skills/study-session/references/tutor-cases.md")
    audited = cases.split("## Approved audit scenarios", 1)[1]
    assert re.findall(r"^\| (B[1-8]) ", audited, re.M) == [f"B{i}" for i in range(1, 9)]
    # Inspect scenario/evidence coverage, not a frozen past execution status.
    for limit in ("합성 수동", "교육 효과", "첫 원인 가설"):
        assert limit in audited


def test_doc_link_errors_handle_real_and_example_targets(tmp_path: Path) -> None:
    target = tmp_path / "참고 문서(1).md"
    target.write_text("## 절 하나\n", encoding="utf-8")
    page = tmp_path / "guide.md"
    page.write_text(
        "[정상](<참고 문서(1).md#절-하나>)\n\n"
        "```md\n[예시](missing-example.md)\n```\n",
        encoding="utf-8",
    )
    assert _doc_link_errors(page) == []
    page.write_text("[누락](missing.md)\n", encoding="utf-8")
    assert any("missing.md" in error for error in _doc_link_errors(page))
    page.write_text("[없는 절](<참고 문서(1).md#없는-절>)\n", encoding="utf-8")
    assert any("없는-절" in error for error in _doc_link_errors(page))


@pytest.mark.parametrize("relative", OPERATING_DOCS)
def test_operating_doc_links_resolve(relative: str) -> None:
    assert _doc_link_errors(REPO / relative) == []


def test_doc_links_normalize_escapes_fragments_and_duplicate_headings(tmp_path: Path) -> None:
    target = tmp_path / "한 글(1).md"
    target.write_text("## API `find` / Set\n## API `find` / Set\n", encoding="utf-8")
    page = tmp_path / "guide.md"
    page.write_text(
        "# Local\n"
        "[self](#local)\n"
        "[encoded](%ED%95%9C%20%EA%B8%80%281%29.md#api-find--set-1)\n"
        "[escaped](<한 글\\(1\\).md#api-find--set>)\n",
        encoding="utf-8",
    )
    assert _doc_link_errors(page) == []
    page.write_text("[missing self](#absent)\n", encoding="utf-8")
    assert any("#absent" in error for error in _doc_link_errors(page))


def test_doc_links_ignore_urls_templates_and_nested_fenced_examples(tmp_path: Path) -> None:
    page = tmp_path / "guide.md"
    page.write_text(
        "[web](https://example.invalid/doc#missing)\n"
        "[email](mailto:example@example.invalid)\n"
        "[template](knowledge/<area>/<concept>.md)\n"
        "`[inline example](absent-inline.md)`\n"
        "~~~~md\n[example](absent-tilde.md)\n~~~~\n"
        "````md\n```md\n[example](absent-nested.md)\n```\n````\n",
        encoding="utf-8",
    )
    assert _doc_link_errors(page) == []


@pytest.mark.parametrize("fragment", (
    "course-specific-scope-and-assistance", "cs336-return-and-boundaries",
    "default-chapter-transition-wrap-up", "standalone-writing-and-sources",
))
def test_moved_policy_anchors_remain_reachable(tmp_path: Path, fragment: str) -> None:
    page = tmp_path / "compatibility.md"
    target = REPO / ".agents/references/learning-policies.md"
    page.write_text(f"[old link](<{target}#{fragment}>)\n", encoding="utf-8")
    assert _doc_link_errors(page) == []
