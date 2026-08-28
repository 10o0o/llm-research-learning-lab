from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
COACH_TESTS = REPO / ".agents/skills/coach-llm-research-study/tests"
for path in (SKILL / "scripts", COACH_TESTS):
    sys.path.insert(0, str(path))

from compose_lesson_til import CompositionError, compose_lesson_til  # noqa: E402
from finalize_lesson_til import FinalizationError, finalize_lesson_til  # noqa: E402
from handoff_fixture import build_handoff, draft_envelope  # noqa: E402
from validate_lesson_handoff import (  # noqa: E402
    can_replace_with_new_lesson,
    validate_handoff,
)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def _init_repository(root: Path, *, existing_til: str | None = None) -> None:
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.name", "Fixture Learner")
    _git(root, "config", "user.email", "fixture@example.com")
    (root / ".gitignore").write_text("tmp/\ntil/today.md\n", encoding="utf-8")
    if existing_til is not None:
        destination = root / "til/2026/08/2026-08-20.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(existing_til, encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "fixture baseline")


def _completed_handoff(root: Path) -> tuple[Path, str]:
    answer = "축 의미와 broadcast 조건을 연결하고 attention 입력으로 전이했다."
    draft = root / "til/today.md"
    draft.parent.mkdir(parents=True, exist_ok=True)
    draft.write_text(draft_envelope("tensor-shape-lesson", "E001", answer), encoding="utf-8")
    handoff, _ = build_handoff(
        root,
        status="completed",
        reviews=[("pass", "fresh-reviewer")],
        evidence=[
            {
                "concept_ids": "C01, C02, C03",
                "objective_ids": "O001, O002, O003",
                "kind": "transfer",
                "content": answer,
                "append_state": "drafted",
            }
        ],
        coverage=[
            {
                "concept": concept,
                "state": "confirmed",
                "evidence_ids": "E001",
                "representation": "learning",
                "note": "The integrated learner attempt covers every delivered objective.",
            }
            for concept in ("C01", "C02", "C03")
        ],
    )
    return handoff, answer


def _compose(handoff: Path, root: Path, answer: str) -> None:
    compose_lesson_til(
        handoff,
        [
            {
                "section": "오늘의 학습",
                "evidence_ids": ["E001"],
                "representation": "learning",
                "text": answer,
            }
        ],
        repo_root=root,
        composed_at="2026-08-20T02:00:00Z",
    )


def test_raw_evidence_composes_then_commits_only_the_dated_til(tmp_path: Path) -> None:
    handoff, answer = _completed_handoff(tmp_path)
    _init_repository(tmp_path)
    _compose(handoff, tmp_path, answer)

    ready = validate_handoff(handoff, repo_root=tmp_path, til_ready=True)
    assert ready.ok, ready.errors
    assert not can_replace_with_new_lesson(ready.document)
    result = finalize_lesson_til(handoff, repo_root=tmp_path)

    destination = tmp_path / str(result["dated_til_path"])
    text = destination.read_text(encoding="utf-8")
    assert answer in text
    assert "lesson-til-item:" not in text
    assert "- 관련 역량: `CC-DL-01`" in text
    assert "../../../materials/lesson.md" in text
    assert _git(tmp_path, "show", "--pretty=format:", "--name-only", "HEAD").stdout.splitlines() == [
        "til/2026/08/2026-08-20.md"
    ]
    committed = validate_handoff(handoff, repo_root=tmp_path)
    assert committed.ok, committed.errors
    assert committed.as_json()["workflow_action"] == "COMPLETE"
    assert can_replace_with_new_lesson(committed.document)


def test_same_day_session_merges_and_deduplicates_provenance(tmp_path: Path) -> None:
    existing = (
        "# 2026-08-20\n\n"
        "## 오늘의 학습\n\n기존 세션 기록.\n\n"
        "## 관련 기록\n\n- [lesson.md](../../../materials/lesson.md)\n"
        "- 관련 역량: `CC-DL-01`\n"
    )
    handoff, answer = _completed_handoff(tmp_path)
    _init_repository(tmp_path, existing_til=existing)
    _compose(handoff, tmp_path, answer)
    result = finalize_lesson_til(handoff, repo_root=tmp_path)

    text = (tmp_path / str(result["dated_til_path"])).read_text(encoding="utf-8")
    assert "기존 세션 기록." in text and answer in text
    assert text.count("- [lesson.md](../../../materials/lesson.md)") == 1
    assert text.count("- 관련 역량: `CC-DL-01`") == 1
    assert result["merged_existing"] is True


def test_commit_failure_preserves_composed_state_and_retry_succeeds(tmp_path: Path) -> None:
    handoff, answer = _completed_handoff(tmp_path)
    _init_repository(tmp_path)
    _compose(handoff, tmp_path, answer)
    draft_before = (tmp_path / "til/today.md").read_bytes()
    handoff_before = handoff.read_bytes()
    hook = tmp_path / ".git/hooks/pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    hook.chmod(0o755)

    with pytest.raises(FinalizationError, match="git commit"):
        finalize_lesson_til(handoff, repo_root=tmp_path)
    assert (tmp_path / "til/today.md").read_bytes() == draft_before
    assert handoff.read_bytes() == handoff_before
    assert validate_handoff(handoff, repo_root=tmp_path).as_json()["workflow_action"] == "FINALIZE_TIL"

    hook.unlink()
    result = finalize_lesson_til(handoff, repo_root=tmp_path)
    assert result["commit_sha"] == _git(tmp_path, "rev-parse", "HEAD").stdout.strip()


def test_handoff_generated_rejects_untracked_manual_text_without_mutation(tmp_path: Path) -> None:
    handoff, answer = _completed_handoff(tmp_path)
    draft = tmp_path / "til/today.md"
    draft.write_text(draft.read_text(encoding="utf-8") + "수동 메모\n", encoding="utf-8")
    before = (draft.read_bytes(), handoff.read_bytes())
    with pytest.raises(CompositionError, match="manual_text_sha256"):
        _compose(handoff, tmp_path, answer)
    assert (draft.read_bytes(), handoff.read_bytes()) == before


def test_mixed_composition_requires_exact_manual_hash_and_review_pass(tmp_path: Path) -> None:
    handoff, answer = _completed_handoff(tmp_path)
    draft = tmp_path / "til/today.md"
    manual = "수동으로 추가한 자율학습 메모"
    draft.write_text(draft.read_text(encoding="utf-8") + manual + "\n", encoding="utf-8")
    manual_hash = hashlib.sha256(manual.encode("utf-8")).hexdigest()
    compose_lesson_til(
        handoff,
        [
            {
                "section": "오늘의 학습",
                "evidence_ids": ["E001"],
                "representation": "learning",
                "text": answer,
            },
            {
                "section": "남은 질문",
                "evidence_ids": [],
                "representation": "remaining-question",
                "text": manual,
            },
        ],
        repo_root=tmp_path,
        mode="mixed",
        review="pass",
        manual_text_sha256=manual_hash,
        composed_at="2026-08-20T02:00:00Z",
    )
    report = validate_handoff(handoff, repo_root=tmp_path, til_ready=True)
    assert report.ok, report.errors


def test_mixed_pending_review_and_explicit_save_have_distinct_workflow_actions(tmp_path: Path) -> None:
    handoff, answer = _completed_handoff(tmp_path)
    draft = tmp_path / "til/today.md"
    manual = "검토가 필요한 수동 메모"
    draft.write_text(draft.read_text(encoding="utf-8") + manual + "\n", encoding="utf-8")
    compose_lesson_til(
        handoff,
        [
            {
                "section": "오늘의 학습",
                "evidence_ids": ["E001"],
                "representation": "learning",
                "text": answer,
            },
            {
                "section": "남은 질문",
                "evidence_ids": [],
                "representation": "remaining-question",
                "text": manual,
            },
        ],
        repo_root=tmp_path,
        mode="mixed",
        review="pending",
        manual_text_sha256=hashlib.sha256(manual.encode("utf-8")).hexdigest(),
        composed_at="2026-08-20T02:00:00Z",
    )
    report = validate_handoff(handoff, repo_root=tmp_path)
    assert report.ok, report.errors
    assert report.as_json()["workflow_action"] == "REVIEW_MIXED_DRAFT"

    explicit_root = tmp_path / "explicit"
    explicit_root.mkdir()
    explicit_handoff, explicit_answer = _completed_handoff(explicit_root)
    text = explicit_handoff.read_text(encoding="utf-8").replace(
        "- til_finalize_policy: auto-commit",
        "- til_finalize_policy: explicit-request",
        1,
    )
    explicit_handoff.write_text(text, encoding="utf-8")
    _compose(explicit_handoff, explicit_root, explicit_answer)
    explicit_report = validate_handoff(explicit_handoff, repo_root=explicit_root)
    assert explicit_report.ok, explicit_report.errors
    assert explicit_report.as_json()["workflow_action"] == "AWAIT_TIL_SAVE"


def test_corrected_attempt_is_classified_as_changed_understanding(tmp_path: Path) -> None:
    wrong = "분모는 발생한 사건의 수라고 생각했다."
    corrected = "분모는 표본공간에 있는 가능한 결과의 수라고 고쳐 설명했다."
    draft = tmp_path / "til/today.md"
    draft.parent.mkdir(parents=True, exist_ok=True)
    draft.write_text(draft_envelope("tensor-shape-lesson", "E002", corrected), encoding="utf-8")
    handoff, _ = build_handoff(
        tmp_path,
        status="paused",
        reviews=[("pass", "fresh-reviewer")],
        evidence=[
            {
                "concept_ids": "C01",
                "objective_ids": "O001",
                "content": wrong,
                "verdict": "misconception",
                "append_state": "not_eligible",
            },
            {
                "concept_ids": "C01",
                "objective_ids": "O001",
                "content": corrected,
                "append_state": "drafted",
            },
        ],
        coverage=[
            {"concept": "C01", "state": "confirmed", "evidence_ids": "E002", "representation": "learning", "note": "The corrected learner explanation is confirmed."},
            {"concept": "C02", "state": "deferred", "evidence_ids": "none", "representation": "not-required", "note": "Not taught."},
            {"concept": "C03", "state": "deferred", "evidence_ids": "none", "representation": "not-required", "note": "Not taught."},
        ],
        delivery=[
            {"objective": "O001", "state": "delivered", "mode": "full", "note": "The distinction was taught."},
            {"objective": "O002", "state": "pending", "mode": "none", "note": "Not taught."},
            {"objective": "O003", "state": "pending", "mode": "none", "note": "Not taught."},
        ],
    )
    compose_lesson_til(
        handoff,
        [
            {
                "section": "배운 점",
                "evidence_ids": ["E001", "E002"],
                "representation": "changed-understanding",
                "text": "처음에는 분모를 발생한 사건 수로 보았지만, 표본공간의 가능한 결과 수라는 점으로 고쳐 이해했다.",
            }
        ],
        repo_root=tmp_path,
        composed_at="2026-08-20T02:00:00Z",
    )
    report = validate_handoff(handoff, repo_root=tmp_path, til_ready=True)
    assert report.ok, report.errors
