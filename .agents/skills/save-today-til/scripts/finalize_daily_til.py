#!/usr/bin/env python3
"""Compose and path-limit commit one dated TIL from completed v9 cycles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
COACH_SCRIPTS = SCRIPT_DIR.parents[1] / "coach-llm-research-study" / "scripts"
if str(COACH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(COACH_SCRIPTS))

from daily_learning_flow import (  # noqa: E402
    DEFAULT_CURSOR_PATH,
    FlowError,
    eligible_til_cycles,
    inspect_commit,
    load_flow,
    mark_til_consumed,
    save_flow,
    sha256_file,
    validate_flow,
)
from validate_til import validate_file  # noqa: E402


FLOW_FORBIDDEN = (
    "남은 질문",
    "내 말로 설명해야",
    "내 말로 정리해야",
    "학습자가 설명해야",
    "확인 질문",
    "평가 문구",
    "lesson-til-item",
    "lesson-evidence",
    "TODO",
)
CURRICULUM_ID_RE = re.compile(r"(?:CC|TR)-[A-Z]+-\d{2}\Z")


class DailyTilError(RuntimeError):
    """Raised when an explicit daily-TIL request cannot be finalized safely."""


def _repo_root_from_script() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / ".git").exists() or (candidate / "AGENTS.md").is_file():
            return candidate.resolve()
    raise DailyTilError("could not locate repository root")


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old_mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, old_mode)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def _run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode != 0:
        raise DailyTilError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result


def _run_git_bytes(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise DailyTilError(
            result.stderr.decode("utf-8", errors="replace").strip()
            or f"git {' '.join(args)} failed"
        )
    return result.stdout


def _relative_link(from_path: PurePosixPath, target: str, label: str) -> str:
    if target.startswith("https://"):
        return f"[{label}]({target})"
    relative = os.path.relpath(target, start=from_path.parent.as_posix())
    rendered = f"<{relative}>" if any(character in relative for character in " ()[]") else relative
    return f"[{label}]({rendered})"


def _cycle_by_id(state: dict[str, Any], cycle_id: str) -> dict[str, Any]:
    cycle = next((item for item in state["cycles"] if item["cycle_id"] == cycle_id), None)
    if cycle is None:
        raise DailyTilError(f"unknown cycle in TIL specification: {cycle_id}")
    return cycle


def _existing_til_parts(
    path: Path,
    *,
    study_date: str,
    mode: str,
) -> tuple[str, str, list[str], list[str]]:
    """Preserve dated history while removing obsolete operational sections."""

    if not path.exists():
        return "", "", [], []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise DailyTilError(f"existing dated TIL is not UTF-8: {path}") from error
    if not text.startswith(f"# {study_date}\n"):
        raise DailyTilError("existing dated TIL heading differs from its completion date")
    # Legacy v8 files may contain composition comments.  Preserve their visible
    # prose, but never carry an internal marker into the recomposed note.
    text = re.sub(r"(?s)<!--.*?-->", "", text)
    matches = list(re.finditer(r"(?m)^## ([^\n]+)\n", text))
    sections: dict[str, str] = {}
    ordered_other: list[str] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        if title in sections:
            raise DailyTilError(f"existing dated TIL repeats section: {title}")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end].strip()
        sections[title] = body
        if title not in {"오늘의 학습", "배운 점", "관련 기록"}:
            if mode == "mixed" and body:
                ordered_other.append(f"## {title}\n\n{body}")
    learning = sections.get("오늘의 학습", "")
    learned = sections.get("배운 점", "")
    related = [line.strip() for line in sections.get("관련 기록", "").splitlines() if line.strip()]
    # Flow-generated notes deliberately discard legacy remaining questions and
    # next-step instructions.  An explicitly reviewed mixed note may retain them.
    return learning, learned, ordered_other, related


def _validate_existing_saved_til(
    state: dict[str, Any],
    *,
    study_date: str,
    destination: Path,
) -> None:
    prior = [item for item in state.get("til_saves", []) if item.get("study_date") == study_date]
    if not prior:
        return
    if not destination.is_file():
        raise DailyTilError("a previously saved dated TIL is missing")
    expected = prior[-1].get("sha256")
    actual = hashlib.sha256(destination.read_bytes()).hexdigest()
    if actual != expected:
        raise DailyTilError("current dated TIL differs from the latest exact cursor save")


def _validate_commit_cross_checks(state: dict[str, Any], root: Path) -> None:
    errors = validate_flow(state, repo_root=root, verify_commits=True)
    if errors:
        raise DailyTilError("daily cursor commit verification failed: " + "; ".join(errors))
    for cycle in state["cycles"]:
        if cycle.get("status") != "completed":
            continue
        commit_shas = {record["sha"] for record in cycle.get("learning_commits", [])}
        practice = cycle.get("practice", {})
        if practice.get("state") == "completed":
            if practice.get("commit_sha") not in commit_shas:
                raise DailyTilError(f"practice commit is absent from exact cycle commit records: {cycle['cycle_id']}")
            path = root / practice["path"]
            if not path.is_file() or sha256_file(path) != practice.get("sha256"):
                raise DailyTilError(f"current practice artifact differs from the completed cycle: {cycle['cycle_id']}")
        knowledge = cycle.get("knowledge", {})
        if knowledge.get("state") == "committed":
            if knowledge.get("commit_sha") not in commit_shas:
                raise DailyTilError(f"knowledge commit is absent from exact cycle commit records: {cycle['cycle_id']}")
            for raw in knowledge.get("paths", []):
                if not (root / raw).is_file():
                    raise DailyTilError(f"current knowledge artifact is missing: {raw}")
                committed_blob = _run_git(
                    root,
                    "rev-parse",
                    f"{knowledge['commit_sha']}:{raw}",
                ).stdout.strip()
                current_blob = _run_git(root, "hash-object", raw).stdout.strip()
                if committed_blob != current_blob:
                    raise DailyTilError(f"current knowledge artifact differs from its cycle commit: {raw}")
    for save in state.get("til_saves", []):
        study_date = save["study_date"]
        try:
            record = inspect_commit(
                root,
                save["commit_sha"],
                expected_subject=f"til: {study_date} 학습 기록",
                expected_paths=[save["path"]],
            )
        except FlowError as error:
            raise DailyTilError(str(error)) from error
        committed = _run_git_bytes(root, "show", f"{record.sha}:{save['path']}")
        if hashlib.sha256(committed).hexdigest() != save["sha256"]:
            raise DailyTilError(
                f"recorded dated TIL hash differs from its exact commit: {save['path']}"
            )


def _validate_cycle_spec(
    cycle: dict[str, Any], raw: dict[str, Any]
) -> list[dict[str, Any]]:
    concepts = raw.get("concepts")
    if not isinstance(concepts, list) or not concepts:
        raise DailyTilError(f"{cycle['cycle_id']} needs concept-first composition items")
    expected = [item["concept_id"] for item in cycle.get("concepts", [])]
    observed = [item.get("concept_id") for item in concepts if isinstance(item, dict)]
    if observed != expected:
        raise DailyTilError(
            f"{cycle['cycle_id']} concept order must exactly match the completed session: {expected}"
        )
    known_evidence = {item["evidence_id"] for item in cycle.get("learner_evidence", [])}
    cited: set[str] = set()
    required_fields = (
        "title",
        "definition",
        "conditions_mechanism_limits",
        "learning_process",
        "evidence_ids",
    )
    for item in concepts:
        for field in required_fields:
            value = item.get(field)
            if value is None or value == "" or value == []:
                raise DailyTilError(f"{cycle['cycle_id']} {item.get('concept_id')} needs {field}")
        evidence_ids = item["evidence_ids"]
        if (
            not isinstance(evidence_ids, list)
            or len(evidence_ids) != len(set(evidence_ids))
            or not set(evidence_ids).issubset(known_evidence)
        ):
            raise DailyTilError(f"{cycle['cycle_id']} {item['concept_id']} has invalid evidence_ids")
        cited.update(evidence_ids)
    if cited != known_evidence:
        missing = sorted(known_evidence - cited)
        raise DailyTilError(f"{cycle['cycle_id']} omits confirmed learner evidence: {', '.join(missing)}")
    return concepts


def render_daily_til(
    state: dict[str, Any],
    spec: dict[str, Any],
    *,
    repo_root: Path | str,
) -> tuple[str, list[str], str]:
    """Render the complete concept-first note for one completion date."""

    root = Path(repo_root).resolve()
    mode = spec.get("mode", "flow-generated")
    if mode not in {"flow-generated", "mixed"}:
        raise DailyTilError("TIL mode must be flow-generated or mixed")
    if mode == "mixed" and spec.get("manual_review") != "pass":
        raise DailyTilError("mixed manual content requires one same-flow coach review pass")
    study_date = str(spec.get("study_date", ""))
    try:
        from datetime import date

        date.fromisoformat(study_date)
    except ValueError as error:
        raise DailyTilError("study_date must be YYYY-MM-DD") from error
    completed = [
        cycle
        for cycle in state.get("cycles", [])
        if cycle.get("status") == "completed"
        and cycle.get("completed_on") == study_date
        and not cycle.get("til_consumed", False)
    ]
    if not completed:
        raise DailyTilError(f"no unconsumed completed cycle exists for {study_date}")
    raw_cycles = spec.get("cycles")
    if not isinstance(raw_cycles, list):
        raise DailyTilError("TIL specification cycles must be a list")
    expected_ids = [cycle["cycle_id"] for cycle in completed]
    observed_ids = [item.get("cycle_id") for item in raw_cycles if isinstance(item, dict)]
    if observed_ids != expected_ids:
        raise DailyTilError(
            "the TIL specification must contain only unconsumed completed cycles in order: "
            + ", ".join(expected_ids)
        )

    destination = PurePosixPath(f"til/{study_date[:4]}/{study_date[5:7]}/{study_date}.md")
    destination_path = root / destination.as_posix()
    _validate_existing_saved_til(
        state,
        study_date=study_date,
        destination=destination_path,
    )
    existing_learning, existing_learned, existing_manual, existing_related = _existing_til_parts(
        destination_path,
        study_date=study_date,
        mode=mode,
    )
    sections: list[str] = [f"# {study_date}", "## 오늘의 학습"]
    related: list[str] = []
    targets: list[str] = []
    bridges: list[str] = []
    learned_blocks: list[str] = []
    practice_blocks: list[str] = []
    knowledge_blocks: list[str] = []

    for raw_cycle in raw_cycles:
        cycle = _cycle_by_id(state, raw_cycle["cycle_id"])
        concepts = _validate_cycle_spec(cycle, raw_cycle)
        for concept in concepts:
            learned_blocks.extend(
                [
                    f"### {concept['title']}",
                    str(concept["definition"]).strip(),
                    f"성립 조건·작동 원리·한계: {str(concept['conditions_mechanism_limits']).strip()}",
                    f"학습 과정과 확인: {str(concept['learning_process']).strip()}",
                ]
            )
        practice = cycle.get("practice", {})
        if practice.get("state") == "completed":
            practice_blocks.append(
                "- "
                + _relative_link(destination, practice["path"], "실습")
                + ": "
                + " ".join(practice.get("interpretation_evidence", []))
            )
        knowledge = cycle.get("knowledge", {})
        if knowledge.get("state") == "committed":
            knowledge_blocks.extend(
                "- " + _relative_link(destination, path, Path(path).stem)
                for path in knowledge.get("paths", [])
            )
        for source in cycle.get("source_provenance", []):
            if source.get("role") == "external-primary":
                url = source.get("official_url")
                if isinstance(url, str):
                    related.append(_relative_link(destination, url, str(source.get("artifact") or "공식 자료")))
                    related.append(
                        f"provider/course: {source.get('provider')} / {source.get('course')}; "
                        f"offering/edition: {source.get('offering_or_edition')}; scope: {source.get('scope')}"
                    )
            else:
                related.append(_relative_link(destination, source["path"], Path(source["path"]).name))
        target = cycle.get("primary_target")
        if isinstance(target, str) and CURRICULUM_ID_RE.fullmatch(target):
            targets.append(f"- 관련 역량: `{target}`")
        bridge = cycle.get("bridge_target")
        if isinstance(bridge, str) and CURRICULUM_ID_RE.fullmatch(bridge):
            bridges.append(f"- 보충 선수 역량: `{bridge}`")

    if existing_learning:
        sections.append(existing_learning)
    sections.extend(learned_blocks)
    if existing_learned or practice_blocks or knowledge_blocks:
        sections.append("## 배운 점")
        if existing_learned:
            sections.append(existing_learned)
        if practice_blocks:
            sections.extend(["### 실습에서 확인한 결과", *practice_blocks])
        if knowledge_blocks:
            sections.extend(["### 정리한 개념 노트", *knowledge_blocks])
    if mode == "mixed":
        manual_sections = spec.get("manual_sections")
        if not isinstance(manual_sections, list) or not all(
            isinstance(item, str) and item.strip() for item in manual_sections
        ):
            raise DailyTilError("mixed mode requires reviewed manual_sections")
        sections.extend(existing_manual)
        sections.extend(item.strip() for item in manual_sections)
    sections.append("## 관련 기록")
    sections.extend(
        "- " + item if not item.startswith("-") else item
        for item in dict.fromkeys([*existing_related, *related, *targets, *bridges])
    )
    text = "\n\n".join(section for section in sections if section).rstrip() + "\n"
    if "<!--" in text or "-->" in text:
        raise DailyTilError("final TIL must not contain internal markers")
    if mode == "flow-generated":
        forbidden = [phrase for phrase in FLOW_FORBIDDEN if phrase in text]
        if forbidden:
            raise DailyTilError("flow-generated TIL contains forbidden operational prose: " + ", ".join(forbidden))
    return text, expected_ids, destination.as_posix()


def finalize_daily_til(
    spec: dict[str, Any],
    *,
    repo_root: Path | str,
    cursor: str = DEFAULT_CURSOR_PATH,
) -> dict[str, Any]:
    """Recompose, validate, commit, and consume only newly completed cycles."""

    root = Path(repo_root).resolve()
    state = load_flow(root, path=cursor)
    _validate_commit_cross_checks(state, root)
    study_date = str(spec.get("study_date", ""))
    new_cycles = eligible_til_cycles(state, study_date=study_date)
    if not new_cycles:
        raise DailyTilError(f"no unconsumed completed cycle exists for {study_date}")
    text, rendered_cycle_ids, relative_path = render_daily_til(state, spec, repo_root=root)
    new_cycle_ids = [cycle["cycle_id"] for cycle in new_cycles]
    if rendered_cycle_ids != new_cycle_ids:
        raise DailyTilError("TIL specification differs from the exact unconsumed cycles")
    destination = root / relative_path
    _atomic_write(destination, text)
    validation_errors = validate_file(destination)
    if validation_errors:
        raise DailyTilError("dated TIL validation failed: " + "; ".join(validation_errors))
    diff_check = _run_git(root, "diff", "--check", "--", relative_path, check=False)
    if diff_check.returncode != 0:
        raise DailyTilError(diff_check.stderr.strip() or diff_check.stdout.strip())
    tracked = _run_git(root, "ls-files", "--error-unmatch", "--", relative_path, check=False)
    if tracked.returncode != 0:
        _run_git(root, "add", "--intent-to-add", "--", relative_path)
    subject = f"til: {study_date} 학습 기록"
    commit = _run_git(
        root,
        "commit",
        "--only",
        "-m",
        subject,
        "--",
        relative_path,
        check=False,
    )
    if commit.returncode != 0:
        raise DailyTilError(
            "git commit failed; the validated dated TIL and daily cursor were preserved for retry: "
            + (commit.stderr.strip() or commit.stdout.strip())
        )
    sha = _run_git(root, "rev-parse", "HEAD").stdout.strip()
    record = inspect_commit(
        root,
        sha,
        expected_subject=subject,
        expected_paths=[relative_path],
    )
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    updated = mark_til_consumed(
        state,
        cycle_ids=new_cycle_ids,
        til_path=relative_path,
        til_sha256=digest,
        commit_sha=record.sha,
        study_date=study_date,
    )
    save_flow(updated, root, path=cursor)
    return {
        "path": relative_path,
        "sha256": digest,
        "commit_sha": record.sha,
        "consumed_cycle_ids": new_cycle_ids,
        "included_cycle_ids": rendered_cycle_ids,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--cursor", default=DEFAULT_CURSOR_PATH)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        result = finalize_daily_til(
            spec,
            repo_root=_repo_root_from_script(),
            cursor=args.cursor,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, FlowError, DailyTilError) as error:
        print(f"ERROR {args.spec}:1 [DAILY_TIL] {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
