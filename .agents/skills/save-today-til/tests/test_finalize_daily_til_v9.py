from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
COACH = REPO / ".agents/skills/coach-llm-research-study"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(COACH / "scripts"))
sys.path.insert(0, str(COACH / "tests"))

import finalize_daily_til as daily_til  # noqa: E402
from daily_learning_flow import (  # noqa: E402
    begin_cycle,
    capture_completed_session,
    complete_cycle,
    empty_flow,
    load_flow,
    record_knowledge_result,
    record_learning_commit,
    record_practice_completion,
    record_practice_decision,
    save_flow,
    start_flow,
    transition_phase,
)
from finalize_daily_til import DailyTilError, finalize_daily_til, render_daily_til  # noqa: E402
from handoff_fixture import build_handoff  # noqa: E402


SEOUL = ZoneInfo("Asia/Seoul")
NOW = datetime(2026, 8, 28, 10, 0, tzinfo=SEOUL)


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()


def _init_git(root: Path) -> None:
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.name", "Daily Flow Fixture")
    _git(root, "config", "user.email", "daily@example.com")
    (root / ".gitignore").write_text("tmp/\ntil/today.md\n", encoding="utf-8")


def _terminal_cycle(
    root: Path,
    *,
    state: dict[str, object] | None = None,
    lesson_id: str = "tensor-shape-lesson",
    completion_time: datetime = NOW,
) -> dict[str, object]:
    if state is None:
        state = start_flow(empty_flow(now=completion_time), mode="full-day", now=completion_time)
    cycle_id = f"cycle-{lesson_id}"
    state = begin_cycle(
        state,
        cycle_id=cycle_id,
        primary_target="CC-DL-01",
        now=completion_time,
    )
    state = transition_phase(state, "PREPARE_LESSON", now=completion_time)
    state = transition_phase(state, "TEACH", now=completion_time)
    handoff, _ = build_handoff(
        root,
        lesson_id=lesson_id,
        status="completed",
        reviews=[("pass", "fresh-reviewer")],
    )
    state = capture_completed_session(
        state,
        handoff,
        repo_root=root,
        now=completion_time,
    )
    state = record_practice_decision(
        state,
        action="NO_EXTRA_PRACTICE",
        mode="NONE",
        path=None,
        now=completion_time,
    )
    state = record_knowledge_result(state, no_change=True, now=completion_time)
    return complete_cycle(
        state,
        next_target_preview={"target_state": "START_TARGET", "primary_target": "CC-DL-02"},
        now=completion_time,
    )


def _cycle_spec(cycle: dict[str, object], *, title_suffix: str = "") -> dict[str, object]:
    return {
        "cycle_id": cycle["cycle_id"],
        "concepts": [
            {
                "concept_id": concept["concept_id"],
                "title": str(concept["title"]) + title_suffix,
                "definition": f"{concept['title']}의 핵심 개념을 확인한 학습 결과다.",
                "conditions_mechanism_limits": "적용 조건과 작동 원리를 구분하고 성립하지 않는 경계를 함께 확인했다.",
                "learning_process": "작은 예시를 추적하고 학습자의 통합 전이 설명으로 확인했다.",
                "evidence_ids": list(concept["evidence_ids"]),
            }
            for concept in cycle["concepts"]
        ],
    }


def _spec(state: dict[str, object], study_date: str = "2026-08-28") -> dict[str, object]:
    completed = [
        cycle
        for cycle in state["cycles"]
        if cycle["status"] == "completed"
        and cycle["completed_on"] == study_date
        and not cycle["til_consumed"]
    ]
    return {
        "mode": "flow-generated",
        "study_date": study_date,
        "cycles": [_cycle_spec(cycle) for cycle in completed],
    }


def _baseline(root: Path) -> None:
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "fixture baseline")


def test_explicit_request_composes_concept_first_and_commits_only_the_dated_til(
    tmp_path: Path,
) -> None:
    _init_git(tmp_path)
    state = _terminal_cycle(tmp_path)
    save_flow(state, tmp_path, now=NOW)
    _baseline(tmp_path)
    result = finalize_daily_til(_spec(state), repo_root=tmp_path)
    assert result["path"] == "til/2026/08/2026-08-28.md"
    assert result["consumed_cycle_ids"] == ["cycle-tensor-shape-lesson"]
    text = (tmp_path / result["path"]).read_text(encoding="utf-8")
    assert "## 오늘의 학습" in text
    assert "성립 조건·작동 원리·한계:" in text
    assert "남은 질문" not in text
    assert "lesson-evidence" not in text
    assert _git(tmp_path, "show", "--pretty=format:", "--name-only", "HEAD") == result["path"]
    cursor = load_flow(tmp_path)
    assert cursor["cycles"][0]["til_consumed"] is True
    assert cursor["til_saves"][0]["sha256"] == result["sha256"]


def test_unfinished_cycle_is_excluded_and_unrelated_git_history_is_not_summarized(
    tmp_path: Path,
) -> None:
    _init_git(tmp_path)
    state = _terminal_cycle(tmp_path)
    state = start_flow(state, mode="full-day", now=NOW)
    state = begin_cycle(
        state,
        cycle_id="cycle-unfinished-lesson",
        primary_target="CC-DL-02",
        now=NOW,
    )
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    save_flow(state, tmp_path, now=NOW)
    unrelated = tmp_path / "unrelated.md"
    unrelated.write_text("# unrelated\n", encoding="utf-8")
    _baseline(tmp_path)
    unrelated.write_text("# unrelated\n\nchanged\n", encoding="utf-8")
    _git(tmp_path, "add", "unrelated.md")
    _git(tmp_path, "commit", "-qm", "unrelated: do not summarize")

    spec = _spec(state)
    assert [item["cycle_id"] for item in spec["cycles"]] == ["cycle-tensor-shape-lesson"]
    result = finalize_daily_til(spec, repo_root=tmp_path)
    text = (tmp_path / result["path"]).read_text(encoding="utf-8")
    assert "unfinished" not in text
    assert "unrelated" not in text


def test_exact_practice_commit_and_current_artifact_are_cross_checked(tmp_path: Path) -> None:
    _init_git(tmp_path)
    state = start_flow(empty_flow(now=NOW), mode="full-day", now=NOW)
    state = begin_cycle(
        state,
        cycle_id="cycle-tensor-shape-lesson",
        primary_target="CC-DL-01",
        now=NOW,
    )
    state = transition_phase(state, "PREPARE_LESSON", now=NOW)
    state = transition_phase(state, "TEACH", now=NOW)
    handoff, _ = build_handoff(
        tmp_path,
        status="completed",
        reviews=[("pass", "fresh-reviewer")],
    )
    state = capture_completed_session(state, handoff, repo_root=tmp_path, now=NOW)
    practice = tmp_path / "practice/math/session.ipynb"
    practice.parent.mkdir(parents=True)
    practice.write_text('{"cells": [], "nbformat": 4, "nbformat_minor": 5}\n', encoding="utf-8")
    _baseline(tmp_path)
    practice.write_text('{"cells": [{"result": 4}], "nbformat": 4, "nbformat_minor": 5}\n', encoding="utf-8")
    _git(tmp_path, "add", practice.relative_to(tmp_path).as_posix())
    _git(tmp_path, "commit", "-qm", "practice: complete session")
    practice_sha = _git(tmp_path, "rev-parse", "HEAD")
    state = record_practice_decision(
        state,
        action="CREATE_LOCAL_PRACTICE",
        mode="NOTEBOOK",
        path="practice/math/session.ipynb",
        now=NOW,
    )
    state = record_learning_commit(
        state,
        repo_root=tmp_path,
        sha=practice_sha,
        expected_subject="practice: complete session",
        expected_paths=["practice/math/session.ipynb"],
        now=NOW,
    )
    state = record_practice_completion(
        state,
        path="practice/math/session.ipynb",
        interpretation_evidence=["결과 4가 예상한 유한 열거와 일치했다."],
        artifact_sha256=hashlib.sha256(practice.read_bytes()).hexdigest(),
        commit_sha=practice_sha,
        now=NOW,
    )
    state = record_knowledge_result(state, no_change=True, now=NOW)
    state = complete_cycle(
        state,
        next_target_preview={"target_state": "START_TARGET", "primary_target": "CC-DL-02"},
        now=NOW,
    )
    save_flow(state, tmp_path, now=NOW)

    practice.write_text("drift\n", encoding="utf-8")
    with pytest.raises(DailyTilError, match="practice artifact differs"):
        finalize_daily_til(_spec(state), repo_root=tmp_path)


def test_repeated_same_day_save_merges_only_new_cycles_without_duplication(
    tmp_path: Path,
) -> None:
    _init_git(tmp_path)
    state = _terminal_cycle(tmp_path)
    save_flow(state, tmp_path, now=NOW)
    _baseline(tmp_path)
    first = finalize_daily_til(_spec(state), repo_root=tmp_path)
    state = load_flow(tmp_path)
    state = start_flow(state, mode="full-day", now=NOW)
    state = _terminal_cycle(tmp_path, state=state, lesson_id="tensor-shape-second")
    save_flow(state, tmp_path, now=NOW)
    second = finalize_daily_til(_spec(state), repo_root=tmp_path)
    assert first["consumed_cycle_ids"] == ["cycle-tensor-shape-lesson"]
    assert second["consumed_cycle_ids"] == ["cycle-tensor-shape-second"]
    assert second["included_cycle_ids"] == ["cycle-tensor-shape-second"]
    text = (tmp_path / second["path"]).read_text(encoding="utf-8")
    assert text.count("- 관련 역량: `CC-DL-01`") == 1
    assert len(load_flow(tmp_path)["til_saves"]) == 2


def test_previous_til_commit_is_cross_checked_before_merge(tmp_path: Path) -> None:
    _init_git(tmp_path)
    state = _terminal_cycle(tmp_path)
    save_flow(state, tmp_path, now=NOW)
    _baseline(tmp_path)
    unrelated_sha = _git(tmp_path, "rev-parse", "HEAD")
    finalize_daily_til(_spec(state), repo_root=tmp_path)

    state = load_flow(tmp_path)
    state = start_flow(state, mode="full-day", now=NOW)
    state = _terminal_cycle(tmp_path, state=state, lesson_id="tensor-shape-second")
    state["til_saves"][0]["commit_sha"] = unrelated_sha
    state["cycles"][0]["til_commit_sha"] = unrelated_sha
    save_flow(state, tmp_path, now=NOW)

    with pytest.raises(DailyTilError, match="commit subject differs"):
        finalize_daily_til(_spec(state), repo_root=tmp_path)


def test_legacy_dated_til_is_recomposed_without_history_rewrite_or_remaining_question(
    tmp_path: Path,
) -> None:
    _init_git(tmp_path)
    legacy = tmp_path / "til/2026/08/2026-08-28.md"
    legacy.parent.mkdir(parents=True)
    legacy.write_text(
        "# 2026-08-28\n\n"
        "## 오늘의 학습\n\n"
        "기존에 확인한 표본공간 계산은 그대로 보존한다.\n\n"
        "<!-- lesson-evidence:legacy -->\n"
        "4면 주사위의 ordered pair 하나는 1/16이다.\n"
        "<!-- /lesson-evidence:legacy -->\n\n"
        "## 남은 질문\n\n"
        "내 말로 설명해야 한다.\n\n"
        "## 관련 기록\n\n"
        "- [기존 자료](../../../materials/lesson.md)\n"
        "- 관련 역량: `CC-DL-01`\n",
        encoding="utf-8",
    )
    _baseline(tmp_path)
    legacy_commit = _git(tmp_path, "rev-parse", "HEAD")
    state = _terminal_cycle(tmp_path)
    save_flow(state, tmp_path, now=NOW)
    result = finalize_daily_til(_spec(state), repo_root=tmp_path)
    text = legacy.read_text(encoding="utf-8")
    assert "기존에 확인한 표본공간 계산은 그대로 보존한다." in text
    assert "4면 주사위의 ordered pair 하나는 1/16이다." in text
    assert "남은 질문" not in text
    assert "내 말로" not in text
    assert "lesson-evidence" not in text
    assert text.count("- 관련 역량: `CC-DL-01`") == 1
    assert _git(tmp_path, "cat-file", "-t", legacy_commit) == "commit"
    assert result["consumed_cycle_ids"] == ["cycle-tensor-shape-lesson"]


def test_flow_generated_forbidden_prose_and_mixed_review_boundary(tmp_path: Path) -> None:
    state = _terminal_cycle(tmp_path)
    spec = _spec(state)
    spec["cycles"][0]["concepts"][0]["definition"] = "남은 질문을 남긴다."
    with pytest.raises(DailyTilError, match="forbidden operational prose"):
        render_daily_til(state, spec, repo_root=tmp_path)

    mixed = _spec(state)
    mixed.update({"mode": "mixed", "manual_sections": ["## 배운 점\n\n수동 메모를 함께 검토했다."]})
    with pytest.raises(DailyTilError, match="coach review pass"):
        render_daily_til(state, mixed, repo_root=tmp_path)
    mixed["manual_review"] = "pass"
    text, _, _ = render_daily_til(state, mixed, repo_root=tmp_path)
    assert "수동 메모를 함께 검토했다." in text


def test_commit_failure_preserves_unconsumed_cursor_and_retry_succeeds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _init_git(tmp_path)
    state = _terminal_cycle(tmp_path)
    save_flow(state, tmp_path, now=NOW)
    _baseline(tmp_path)
    real_run = daily_til._run_git

    def fail_commit(root: Path, *args: str, check: bool = True):
        if args and args[0] == "commit":
            return subprocess.CompletedProcess(["git", *args], 1, "", "hook rejected")
        return real_run(root, *args, check=check)

    monkeypatch.setattr(daily_til, "_run_git", fail_commit)
    with pytest.raises(DailyTilError, match="preserved for retry"):
        finalize_daily_til(_spec(state), repo_root=tmp_path)
    assert load_flow(tmp_path)["cycles"][0]["til_consumed"] is False
    assert (tmp_path / "til/2026/08/2026-08-28.md").is_file()

    monkeypatch.setattr(daily_til, "_run_git", real_run)
    result = finalize_daily_til(_spec(state), repo_root=tmp_path)
    assert result["consumed_cycle_ids"] == ["cycle-tensor-shape-lesson"]


def test_previous_date_pending_cycle_uses_its_completion_date(tmp_path: Path) -> None:
    previous = datetime(2026, 8, 27, 23, 30, tzinfo=SEOUL)
    _init_git(tmp_path)
    state = _terminal_cycle(tmp_path, completion_time=previous)
    save_flow(state, tmp_path, now=NOW)
    _baseline(tmp_path)
    result = finalize_daily_til(_spec(state, "2026-08-27"), repo_root=tmp_path)
    assert result["path"] == "til/2026/08/2026-08-27.md"
