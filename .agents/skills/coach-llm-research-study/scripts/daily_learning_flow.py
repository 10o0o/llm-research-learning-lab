#!/usr/bin/env python3
"""Manage the single ignored daily learning-flow cursor atomically.

The cursor is resumable operational state.  It records only enough information
to resume an authorized day flow and later compose an evidence-grounded TIL;
it is not a progress database and never infers mastery from files or checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from zoneinfo import ZoneInfo


FLOW_SCHEMA_VERSION = 1
FLOW_TIMEZONE = "Asia/Seoul"
DEFAULT_CURSOR_PATH = "tmp/active-learning-flow.json"
DEFAULT_HANDOFF_PATH = "tmp/active-lesson-handoff.md"

PHASES = {
    "SELECT_TARGET",
    "PREPARE_LESSON",
    "TEACH",
    "DECIDE_PRACTICE",
    "AWAIT_PRACTICE",
    "UPDATE_KNOWLEDGE",
    "PLAN_NEXT",
    "PAUSED",
}
AUTHORIZATION_MODES = {"none", "lesson-only", "full-day"}
CYCLE_STATUSES = {"active", "paused", "completed"}
PRACTICE_STATES = {"pending", "awaiting", "completed", "no-extra-practice"}
KNOWLEDGE_STATES = {"pending", "committed", "no-change"}
PRACTICE_ACTIONS = {
    "CONTINUE_EXISTING_PRACTICE",
    "CREATE_LOCAL_PRACTICE",
    "PROPOSE_EXTERNAL_PRACTICE",
    "NO_EXTRA_PRACTICE",
}
PRACTICE_MODES = {
    "NOTEBOOK",
    "BENCHMARK",
    "DATASET_PROJECT",
    "EXTERNAL_CHALLENGE",
    "EXTERNAL_COMPETITION",
    "NONE",
}
TARGET_RE = re.compile(r"(?:CC|TR)-[A-Z]+-\d{2}\Z")
CYCLE_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{2,95}\Z")
HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-f]{7,64}\Z")

ALLOWED_TRANSITIONS = {
    "SELECT_TARGET": {"PREPARE_LESSON", "PAUSED"},
    "PREPARE_LESSON": {"TEACH", "PAUSED"},
    "TEACH": {"DECIDE_PRACTICE", "PAUSED"},
    "DECIDE_PRACTICE": {"AWAIT_PRACTICE", "UPDATE_KNOWLEDGE", "PAUSED"},
    "AWAIT_PRACTICE": {"UPDATE_KNOWLEDGE", "PAUSED"},
    "UPDATE_KNOWLEDGE": {"PLAN_NEXT", "PAUSED"},
    "PLAN_NEXT": {"SELECT_TARGET", "PAUSED"},
    "PAUSED": PHASES - {"PAUSED"},
}


class FlowError(RuntimeError):
    """Raised when the daily cursor cannot make a safe state transition."""


@dataclass(frozen=True)
class CommitRecord:
    sha: str
    committer_date: str
    subject: str
    paths: tuple[str, ...]

    def as_json(self) -> dict[str, Any]:
        return {
            "sha": self.sha,
            "committer_date": self.committer_date,
            "subject": self.subject,
            "paths": list(self.paths),
        }


def _repo_root_from_script() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / ".git").exists() or (candidate / "AGENTS.md").is_file():
            return candidate.resolve()
    raise FlowError("could not locate repository root")


def _now(now: datetime | None = None) -> datetime:
    if now is None:
        return datetime.now(ZoneInfo(FLOW_TIMEZONE))
    if now.tzinfo is None:
        raise FlowError("timestamps must include a timezone")
    return now.astimezone(ZoneInfo(FLOW_TIMEZONE))


def _timestamp(now: datetime | None = None) -> str:
    return _now(now).replace(microsecond=0).isoformat()


def _today(now: datetime | None = None) -> str:
    return _now(now).date().isoformat()


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _safe_relative_path(raw: str, root: Path, *, allow_missing: bool = True) -> Path:
    if not raw or raw.startswith("/") or "\\" in raw:
        raise FlowError(f"path must be repository-relative POSIX syntax: {raw!r}")
    pure = PurePosixPath(raw)
    if pure.as_posix() != raw or any(part in {"", ".", ".."} for part in pure.parts):
        raise FlowError(f"path is not canonical repository-relative POSIX syntax: {raw!r}")
    candidate = root.joinpath(*pure.parts)
    try:
        candidate.resolve(strict=False).relative_to(root.resolve())
    except (OSError, ValueError) as error:
        raise FlowError(f"path escapes repository: {raw!r}") from error
    if not allow_missing and not candidate.is_file():
        raise FlowError(f"required file is missing: {raw}")
    return candidate


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old_mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, old_mode)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
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


def empty_flow(*, now: datetime | None = None) -> dict[str, Any]:
    stamp = _timestamp(now)
    return {
        "schema_version": FLOW_SCHEMA_VERSION,
        "timezone": FLOW_TIMEZONE,
        "flow_date": _today(now),
        "authorization": {
            "mode": "none",
            "authorized_on": None,
        },
        "phase": "SELECT_TARGET",
        "resume_phase": None,
        "active_cycle_id": None,
        "handoff_path": None,
        "practice_path": None,
        "cycles": [],
        "learner_evidence_sha256": sha256_bytes(_canonical_json([])),
        "learning_commit_shas": [],
        "til_saves": [],
        "created_at": stamp,
        "updated_at": stamp,
    }


def cursor_path(repo_root: Path | str, raw: str = DEFAULT_CURSOR_PATH) -> Path:
    return _safe_relative_path(raw, Path(repo_root).resolve())


def load_flow(
    repo_root: Path | str,
    *,
    path: str = DEFAULT_CURSOR_PATH,
    create: bool = False,
    now: datetime | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    candidate = cursor_path(root, path)
    if not candidate.exists():
        if not create:
            raise FlowError(f"daily learning cursor does not exist: {path}")
        return empty_flow(now=now)
    if not candidate.is_file():
        raise FlowError(f"daily learning cursor is not a regular file: {path}")
    try:
        state = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FlowError(f"daily learning cursor is unreadable: {error}") from error
    errors = validate_flow(state, repo_root=root, verify_commits=False)
    if errors:
        raise FlowError("invalid daily learning cursor: " + "; ".join(errors))
    return state


def save_flow(
    state: dict[str, Any],
    repo_root: Path | str,
    *,
    path: str = DEFAULT_CURSOR_PATH,
    now: datetime | None = None,
) -> Path:
    root = Path(repo_root).resolve()
    state = deepcopy(state)
    state["updated_at"] = _timestamp(now)
    _recompute_aggregates(state)
    errors = validate_flow(state, repo_root=root, verify_commits=False)
    if errors:
        raise FlowError("refusing to save invalid daily learning cursor: " + "; ".join(errors))
    candidate = cursor_path(root, path)
    _atomic_write(candidate, _canonical_json(state))
    return candidate


def authorization_is_active(state: dict[str, Any], *, now: datetime | None = None) -> bool:
    authorization = state.get("authorization", {})
    return (
        authorization.get("mode") in {"lesson-only", "full-day"}
        and authorization.get("authorized_on") == _today(now)
    )


def _require_authorization(
    state: dict[str, Any],
    *,
    allowed_modes: set[str],
    now: datetime | None = None,
) -> None:
    mode = state.get("authorization", {}).get("mode")
    if mode not in allowed_modes or not authorization_is_active(state, now=now):
        rendered = " or ".join(sorted(allowed_modes))
        raise FlowError(
            f"this operation requires active {rendered} authorization for the current Asia/Seoul date"
        )


def start_flow(
    state: dict[str, Any] | None,
    *,
    mode: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    if mode not in {"lesson-only", "full-day"}:
        raise FlowError("mode must be lesson-only or full-day")
    current = deepcopy(state) if state is not None else empty_flow(now=now)
    current["flow_date"] = _today(now)
    current["authorization"] = {"mode": mode, "authorized_on": _today(now)}
    if current.get("phase") == "PAUSED":
        current["phase"] = current.get("resume_phase") or (
            "TEACH" if current.get("active_cycle_id") else "SELECT_TARGET"
        )
        current["resume_phase"] = None
        active = _active_cycle(current)
        if active is not None and active.get("status") == "paused":
            active["status"] = "active"
    _recompute_aggregates(current)
    return current


def pause_flow(state: dict[str, Any], *, now: datetime | None = None) -> dict[str, Any]:
    current = deepcopy(state)
    if current.get("phase") != "PAUSED":
        current["resume_phase"] = current.get("phase")
    current["phase"] = "PAUSED"
    active = _active_cycle(current)
    if active is not None and active.get("status") != "completed":
        active["status"] = "paused"
    current["authorization"] = {"mode": "none", "authorized_on": None}
    current["flow_date"] = _today(now)
    _recompute_aggregates(current)
    return current


def transition_phase(
    state: dict[str, Any],
    phase: str,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    if phase not in PHASES:
        raise FlowError(f"unknown daily-flow phase: {phase}")
    current = deepcopy(state)
    source = current.get("phase")
    if phase == source:
        return current
    if phase not in ALLOWED_TRANSITIONS.get(source, set()):
        raise FlowError(f"invalid daily-flow transition: {source} -> {phase}")
    if phase != "PAUSED" and not authorization_is_active(current, now=now):
        raise FlowError("daily-flow authorization is not active for the current Asia/Seoul date")
    if phase == "PAUSED":
        return pause_flow(current, now=now)
    current["phase"] = phase
    current["resume_phase"] = None
    _recompute_aggregates(current)
    return current


def _active_cycle(state: dict[str, Any]) -> dict[str, Any] | None:
    active_id = state.get("active_cycle_id")
    if active_id is None:
        return None
    return next((cycle for cycle in state.get("cycles", []) if cycle.get("cycle_id") == active_id), None)


def begin_cycle(
    state: dict[str, Any],
    *,
    cycle_id: str,
    primary_target: str,
    bridge_target: str | None = None,
    handoff_path: str = DEFAULT_HANDOFF_PATH,
    now: datetime | None = None,
) -> dict[str, Any]:
    _require_authorization(state, allowed_modes={"lesson-only", "full-day"}, now=now)
    if state.get("phase") != "SELECT_TARGET":
        raise FlowError("a cycle may begin only at SELECT_TARGET")
    if not CYCLE_ID_RE.fullmatch(cycle_id):
        raise FlowError(f"invalid cycle_id: {cycle_id}")
    if not TARGET_RE.fullmatch(primary_target):
        raise FlowError(f"invalid primary target: {primary_target}")
    if bridge_target is not None and not TARGET_RE.fullmatch(bridge_target):
        raise FlowError(f"invalid bridge target: {bridge_target}")
    current = deepcopy(state)
    existing = next((item for item in current["cycles"] if item["cycle_id"] == cycle_id), None)
    if existing is not None:
        if (
            existing.get("primary_target") != primary_target
            or existing.get("bridge_target") != bridge_target
            or existing.get("handoff_path") != handoff_path
        ):
            raise FlowError(f"cycle_id already identifies different work: {cycle_id}")
        current["active_cycle_id"] = cycle_id
        current["handoff_path"] = handoff_path
        if existing.get("status") == "paused":
            existing["status"] = "active"
        return current
    if _active_cycle(current) is not None:
        raise FlowError("an unfinished active cycle must be completed or paused before another begins")
    started = _timestamp(now)
    current["cycles"].append(
        {
            "cycle_id": cycle_id,
            "status": "active",
            "started_at": started,
            "completed_on": None,
            "primary_target": primary_target,
            "bridge_target": bridge_target,
            "handoff_path": handoff_path,
            "handoff_sha256": None,
            "lesson_id": None,
            "concepts": [],
            "learner_evidence": [],
            "learner_evidence_sha256": sha256_bytes(_canonical_json([])),
            "source_provenance": [],
            "practice": {
                "state": "pending",
                "action": None,
                "mode": None,
                "path": None,
                "sha256": None,
                "interpretation_evidence": [],
                "commit_sha": None,
            },
            "knowledge": {"state": "pending", "paths": [], "commit_sha": None},
            "learning_commits": [],
            "next_target_preview": None,
            "til_consumed": False,
            "til_path": None,
            "til_commit_sha": None,
        }
    )
    current["active_cycle_id"] = cycle_id
    current["handoff_path"] = handoff_path
    current["practice_path"] = None
    _recompute_aggregates(current)
    return current


def _concept_titles(contract: str) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for line in contract.splitlines():
        match = re.fullmatch(
            r"\d+\. (C\d{2}) \| (?:none|\[선수개념\]|\[정정\]|\[보충\]) \| (.+?) \| source: (.+)",
            line.strip(),
        )
        if match:
            result[match.group(1)] = (match.group(2), match.group(3))
    return result


def record_lesson_evidence(
    state: dict[str, Any],
    *,
    cycle_id: str,
    lesson_id: str,
    handoff_path: str,
    evidence: dict[str, Any],
    now: datetime | None = None,
) -> dict[str, Any]:
    """Idempotently record one already-assessed learner evidence item."""

    _require_authorization(state, allowed_modes={"lesson-only", "full-day"}, now=now)
    if state.get("phase") != "TEACH":
        raise FlowError("learner evidence may be captured only during TEACH")
    current = deepcopy(state)
    cycle = next((item for item in current.get("cycles", []) if item.get("cycle_id") == cycle_id), None)
    if cycle is None:
        raise FlowError(f"daily cursor has no cycle for learner evidence: {cycle_id}")
    if cycle.get("handoff_path") != handoff_path:
        raise FlowError("learner evidence handoff path differs from the cursor cycle")
    if evidence.get("verdict") != "confirmed" or evidence.get("provenance") != "learner":
        raise FlowError("only confirmed learner-authored evidence enters the daily cursor")
    content = evidence.get("content")
    content_hash = evidence.get("content_sha256")
    if not isinstance(content, str) or content_hash != sha256_bytes(content.encode("utf-8")):
        raise FlowError("learner evidence content/hash mismatch")
    normalized = {
        "evidence_id": evidence.get("evidence_id"),
        "concept_ids": list(evidence.get("concept_ids", [])),
        "objective_ids": list(evidence.get("objective_ids", [])),
        "kind": evidence.get("kind"),
        "content": content,
        "content_sha256": content_hash,
        "captured_at": evidence.get("captured_at"),
    }
    existing = next(
        (item for item in cycle.get("learner_evidence", []) if item.get("evidence_id") == normalized["evidence_id"]),
        None,
    )
    if existing is not None:
        if existing != normalized:
            raise FlowError(f"cursor evidence differs for {normalized['evidence_id']}")
        return current
    cycle["lesson_id"] = lesson_id
    cycle["learner_evidence"].append(normalized)
    cycle["learner_evidence_sha256"] = sha256_bytes(_canonical_json(cycle["learner_evidence"]))
    _recompute_aggregates(current)
    return current


def capture_completed_session(
    state: dict[str, Any],
    handoff_path: Path | str,
    *,
    repo_root: Path | str,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Capture exact v9 session evidence into the cursor without inferring it."""

    _require_authorization(state, allowed_modes={"lesson-only", "full-day"}, now=now)
    if state.get("phase") != "TEACH":
        raise FlowError("a completed session may be captured only from TEACH")
    root = Path(repo_root).resolve()
    coach_scripts = Path(__file__).resolve().parent
    if str(coach_scripts) not in sys.path:
        sys.path.insert(0, str(coach_scripts))
    from validate_lesson_handoff import validate_handoff  # noqa: PLC0415

    report = validate_handoff(handoff_path, repo_root=root, capture_ready=True)
    if not report.ok or report.document is None:
        messages = "; ".join(f"{item.code}: {item.message}" for item in report.errors)
        raise FlowError(f"cannot capture an invalid handoff: {messages}")
    doc = report.document
    if doc.metadata.get("schema_version") != "9":
        raise FlowError("daily flow accepts only a schema-v9 handoff")
    if doc.metadata.get("status") != "completed":
        raise FlowError("only a completed session may advance to practice")
    cycle_id = doc.metadata.get("cycle_id")
    current = deepcopy(state)
    cycle = next((item for item in current.get("cycles", []) if item.get("cycle_id") == cycle_id), None)
    if cycle is None:
        raise FlowError(f"handoff cycle is absent from the daily cursor: {cycle_id}")
    if cycle.get("primary_target") != doc.target_decision.primary_target:
        raise FlowError("handoff primary target differs from the cursor cycle")
    if cycle.get("handoff_path") != Path(handoff_path).as_posix():
        try:
            relative_handoff = Path(handoff_path).resolve().relative_to(root).as_posix()
        except (OSError, ValueError):
            relative_handoff = Path(handoff_path).as_posix()
        if cycle.get("handoff_path") != relative_handoff:
            raise FlowError("handoff path differs from the cursor cycle")

    evidence: list[dict[str, Any]] = []
    for item in doc.evidence.values():
        if item.values.get("verdict") != "confirmed":
            continue
        evidence.append(
            {
                "evidence_id": item.evidence_id,
                "concept_ids": [value.strip() for value in item.values["concept_ids"].split(",")],
                "objective_ids": [value.strip() for value in item.values["objective_ids"].split(",")],
                "kind": item.values["kind"],
                "content": item.content,
                "content_sha256": item.values["content_sha256"],
                "captured_at": item.values["captured_at"],
            }
        )
    titles = _concept_titles(doc.contract)
    concepts: list[dict[str, Any]] = []
    for concept_id, coverage in doc.learning_coverage.items():
        if coverage.today_state == "deferred":
            continue
        title, source_location = titles.get(concept_id, (concept_id, "none"))
        objective_ids = [
            objective.objective_id
            for objective in doc.objectives.values()
            if objective.concept_id == concept_id and objective.treatment != "deferred"
        ]
        concepts.append(
            {
                "concept_id": concept_id,
                "title": title,
                "source_location": source_location,
                "objective_ids": objective_ids,
                "observable_outcomes": [doc.objectives[item].outcome for item in objective_ids],
                "evidence_ids": list(coverage.evidence_ids),
            }
        )
    evidence_hash = sha256_bytes(_canonical_json(evidence))
    manifest_by_id = {item.item_id: item for item in doc.manifest}
    sources: list[dict[str, Any]] = []
    for item in doc.manifest:
        if item.role not in {"primary", "external-primary"}:
            continue
        source: dict[str, Any] = {
            "primary_id": item.item_id,
            "role": item.role,
            "path": item.path,
            "sha256": item.sha256,
        }
        identity = doc.external_identities.get(item.item_id)
        if identity is not None:
            source.update(
                {
                    "provider": identity.provider,
                    "course": identity.course,
                    "offering_or_edition": identity.offering_or_edition,
                    "artifact": identity.artifact,
                    "official_url": identity.official_url,
                    "final_url": identity.final_url,
                    "scope": identity.scope,
                    "receipt_path": identity.receipt_path,
                }
            )
        scope = doc.lesson_source_scopes.get(item.item_id)
        if scope is not None:
            source.update(
                {
                    "scope_kind": scope.scope_kind,
                    "scope_id": None if scope.scope_id == "none" else scope.scope_id,
                    "included_units": list(scope.included_units),
                }
            )
        sources.append(source)
    del manifest_by_id  # the explicit primary iteration above is authoritative

    handoff_candidate = Path(handoff_path)
    if not handoff_candidate.is_absolute():
        handoff_candidate = root / handoff_candidate
    cycle.update(
        {
            "status": "active",
            "lesson_id": doc.metadata["lesson_id"],
            "handoff_sha256": sha256_file(handoff_candidate),
            "concepts": concepts,
            "learner_evidence": evidence,
            "learner_evidence_sha256": evidence_hash,
            "source_provenance": sources,
        }
    )
    current["learner_evidence_sha256"] = _aggregate_evidence_hash(current["cycles"])
    if current["authorization"]["mode"] == "lesson-only":
        current["phase"] = "PAUSED"
        current["resume_phase"] = "DECIDE_PRACTICE"
        current["authorization"] = {"mode": "none", "authorized_on": None}
        cycle["status"] = "paused"
    else:
        current["phase"] = "DECIDE_PRACTICE"
    return current


def record_practice_decision(
    state: dict[str, Any],
    *,
    action: str,
    mode: str,
    path: str | None,
    now: datetime | None = None,
) -> dict[str, Any]:
    _require_authorization(state, allowed_modes={"full-day"}, now=now)
    if state.get("phase") != "DECIDE_PRACTICE":
        raise FlowError("practice may be decided only at DECIDE_PRACTICE")
    current = deepcopy(state)
    cycle = _active_cycle(current)
    if cycle is None:
        raise FlowError("no active cycle is available for a practice decision")
    if action not in PRACTICE_ACTIONS or mode not in PRACTICE_MODES:
        raise FlowError("practice decision uses an unknown action or mode")
    previous = cycle.get("practice", {})
    if previous.get("state") != "pending":
        expected = (previous.get("action"), previous.get("mode"), previous.get("path"))
        if expected == (action, mode, path):
            return current
        raise FlowError("an existing practice decision cannot be silently replaced")
    if action == "NO_EXTRA_PRACTICE":
        if mode != "NONE" or path is not None:
            raise FlowError("NO_EXTRA_PRACTICE requires mode NONE and no path")
        cycle["practice"].update(
            {"state": "no-extra-practice", "action": action, "mode": "NONE", "path": None}
        )
        current["practice_path"] = None
        current["phase"] = "UPDATE_KNOWLEDGE"
    else:
        if not path:
            raise FlowError("a concrete practice or challenge path is required")
        pure_path = PurePosixPath(path)
        if (
            path.startswith("/")
            or "\\" in path
            or pure_path.as_posix() != path
            or any(part in {"", ".", ".."} for part in pure_path.parts)
        ):
            raise FlowError("practice path must use safe repository-relative POSIX syntax")
        if mode in {"NOTEBOOK", "BENCHMARK", "DATASET_PROJECT", "EXTERNAL_COMPETITION"}:
            if not path.startswith("practice/") or not path.endswith(".ipynb"):
                raise FlowError(f"{mode} requires one practice/*.ipynb path")
        elif mode == "EXTERNAL_CHALLENGE" and not path.startswith("challenges/"):
            raise FlowError("EXTERNAL_CHALLENGE requires an exact challenges/ path")
        cycle["practice"].update(
            {"state": "awaiting", "action": action, "mode": mode, "path": path}
        )
        current["practice_path"] = path
        current["phase"] = "AWAIT_PRACTICE"
    return current


def record_practice_completion(
    state: dict[str, Any],
    *,
    path: str,
    interpretation_evidence: Iterable[str],
    artifact_sha256: str,
    commit_sha: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    _require_authorization(state, allowed_modes={"full-day"}, now=now)
    if state.get("phase") != "AWAIT_PRACTICE":
        raise FlowError("practice may complete only at AWAIT_PRACTICE")
    current = deepcopy(state)
    cycle = _active_cycle(current)
    if cycle is None or cycle["practice"].get("path") != path:
        raise FlowError("practice completion does not match the active cycle")
    evidence = [item.strip() for item in interpretation_evidence if item.strip()]
    if not evidence:
        raise FlowError("practice completion requires learner interpretation evidence")
    if not HASH_RE.fullmatch(artifact_sha256) or not COMMIT_RE.fullmatch(commit_sha):
        raise FlowError("practice completion requires exact artifact and commit hashes")
    recorded = {item.get("sha") for item in cycle.get("learning_commits", [])}
    if commit_sha not in recorded:
        raise FlowError("practice completion commit must be recorded and path-verified first")
    cycle["practice"].update(
        {
            "state": "completed",
            "sha256": artifact_sha256,
            "interpretation_evidence": evidence,
            "commit_sha": commit_sha,
        }
    )
    current["phase"] = "UPDATE_KNOWLEDGE"
    return current


def record_knowledge_result(
    state: dict[str, Any],
    *,
    paths: Iterable[str] = (),
    commit_sha: str | None = None,
    no_change: bool = False,
    now: datetime | None = None,
) -> dict[str, Any]:
    _require_authorization(state, allowed_modes={"full-day"}, now=now)
    if state.get("phase") != "UPDATE_KNOWLEDGE":
        raise FlowError("knowledge may be finalized only at UPDATE_KNOWLEDGE")
    current = deepcopy(state)
    cycle = _active_cycle(current)
    if cycle is None:
        raise FlowError("no active cycle is available for a knowledge result")
    normalized_paths = sorted(set(path for path in paths if path))
    if no_change:
        if normalized_paths or commit_sha is not None:
            raise FlowError("NO_CHANGE must not claim knowledge paths or a commit")
        cycle["knowledge"] = {"state": "no-change", "paths": [], "commit_sha": None}
    else:
        if not normalized_paths or commit_sha is None or not COMMIT_RE.fullmatch(commit_sha):
            raise FlowError("a knowledge update requires exact paths and commit SHA")
        if len(normalized_paths) > 3 or any(not path.startswith("knowledge/") for path in normalized_paths):
            raise FlowError("knowledge updates are limited to one to three knowledge/ paths")
        recorded = {item.get("sha") for item in cycle.get("learning_commits", [])}
        if commit_sha not in recorded:
            raise FlowError("knowledge commit must be recorded and path-verified first")
        cycle["knowledge"] = {
            "state": "committed",
            "paths": normalized_paths,
            "commit_sha": commit_sha,
        }
    current["phase"] = "PLAN_NEXT"
    return current


def complete_cycle(
    state: dict[str, Any],
    *,
    next_target_preview: dict[str, Any],
    now: datetime | None = None,
) -> dict[str, Any]:
    _require_authorization(state, allowed_modes={"full-day"}, now=now)
    current = deepcopy(state)
    cycle = _active_cycle(current)
    if cycle is None:
        raise FlowError("no active cycle is available to complete")
    if current.get("phase") != "PLAN_NEXT":
        raise FlowError("a cycle completes only after knowledge handling reaches PLAN_NEXT")
    if cycle["practice"].get("state") not in {"completed", "no-extra-practice"}:
        raise FlowError("practice is not complete or explicitly unnecessary")
    if cycle["knowledge"].get("state") not in {"committed", "no-change"}:
        raise FlowError("knowledge handling is not terminal")
    if not cycle.get("concepts") or not cycle.get("learner_evidence"):
        raise FlowError("a cycle cannot complete without captured confirmed session evidence")
    cycle["status"] = "completed"
    cycle["completed_on"] = _today(now)
    cycle["next_target_preview"] = deepcopy(next_target_preview)
    current["active_cycle_id"] = None
    current["handoff_path"] = None
    current["practice_path"] = None
    current["phase"] = "SELECT_TARGET"
    _recompute_aggregates(current)
    return current


def _run_git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise FlowError(completed.stderr.strip() or f"git {' '.join(args)} failed")
    return completed.stdout


def inspect_commit(
    repo_root: Path | str,
    sha: str,
    *,
    expected_subject: str | None = None,
    expected_paths: Iterable[str] | None = None,
) -> CommitRecord:
    root = Path(repo_root).resolve()
    if not COMMIT_RE.fullmatch(sha):
        raise FlowError(f"invalid commit SHA: {sha}")
    raw = _run_git(root, "show", "-s", "--format=%H%x00%cI%x00%s", sha).rstrip("\n")
    fields = raw.split("\x00")
    if len(fields) != 3:
        raise FlowError(f"cannot parse commit metadata: {sha}")
    full_sha, committer_date, subject = fields
    paths = tuple(
        sorted(
            line
            for line in _run_git(root, "diff-tree", "--no-commit-id", "--name-only", "-r", full_sha).splitlines()
            if line
        )
    )
    for path in paths:
        _safe_relative_path(path, root)
    if expected_subject is not None and subject != expected_subject:
        raise FlowError(f"commit subject differs: expected {expected_subject!r}, got {subject!r}")
    if expected_paths is not None:
        expected = tuple(sorted(set(expected_paths)))
        if paths != expected:
            raise FlowError(f"commit path set differs: expected {expected}, got {paths}")
    return CommitRecord(full_sha, committer_date, subject, paths)


def record_learning_commit(
    state: dict[str, Any],
    *,
    repo_root: Path | str,
    sha: str,
    expected_subject: str,
    expected_paths: Iterable[str],
    now: datetime | None = None,
) -> dict[str, Any]:
    _require_authorization(state, allowed_modes={"full-day"}, now=now)
    if state.get("phase") not in {"AWAIT_PRACTICE", "UPDATE_KNOWLEDGE"}:
        raise FlowError("learning commits are accepted only for practice or knowledge phases")
    record = inspect_commit(
        repo_root,
        sha,
        expected_subject=expected_subject,
        expected_paths=expected_paths,
    )
    current = deepcopy(state)
    cycle = _active_cycle(current)
    if cycle is None:
        raise FlowError("no active cycle is available for a learning commit")
    existing = next((item for item in cycle["learning_commits"] if item["sha"] == record.sha), None)
    if existing is not None:
        if existing != record.as_json():
            raise FlowError("the cursor already records different metadata for this commit")
        return current
    cycle["learning_commits"].append(record.as_json())
    _recompute_aggregates(current)
    return current


def eligible_til_cycles(
    state: dict[str, Any],
    *,
    study_date: str | None = None,
) -> list[dict[str, Any]]:
    cycles = [
        deepcopy(cycle)
        for cycle in state.get("cycles", [])
        if cycle.get("status") == "completed" and not cycle.get("til_consumed", False)
    ]
    if study_date is not None:
        date.fromisoformat(study_date)
        cycles = [cycle for cycle in cycles if cycle.get("completed_on") == study_date]
    return cycles


def mark_til_consumed(
    state: dict[str, Any],
    *,
    cycle_ids: Iterable[str],
    til_path: str,
    til_sha256: str,
    commit_sha: str,
    study_date: str,
) -> dict[str, Any]:
    current = deepcopy(state)
    wanted = list(dict.fromkeys(cycle_ids))
    if not wanted:
        raise FlowError("at least one completed cycle is required")
    if not HASH_RE.fullmatch(til_sha256) or not COMMIT_RE.fullmatch(commit_sha):
        raise FlowError("TIL consumption requires exact file and commit hashes")
    matched: list[dict[str, Any]] = []
    for cycle_id in wanted:
        cycle = next((item for item in current["cycles"] if item["cycle_id"] == cycle_id), None)
        if cycle is None or cycle.get("status") != "completed":
            raise FlowError(f"TIL may consume completed cycles only: {cycle_id}")
        if cycle.get("til_consumed"):
            raise FlowError(f"cycle is already recorded in a TIL: {cycle_id}")
        if cycle.get("completed_on") != study_date:
            raise FlowError(f"cycle completion date differs from the TIL date: {cycle_id}")
        matched.append(cycle)
    for cycle in matched:
        cycle["til_consumed"] = True
        cycle["til_path"] = til_path
        cycle["til_commit_sha"] = commit_sha
    current["til_saves"].append(
        {
            "study_date": study_date,
            "path": til_path,
            "sha256": til_sha256,
            "cycle_ids": wanted,
            "commit_sha": commit_sha,
        }
    )
    return current


def _aggregate_evidence_hash(cycles: list[dict[str, Any]]) -> str:
    rows = [
        {"cycle_id": cycle.get("cycle_id"), "sha256": cycle.get("learner_evidence_sha256")}
        for cycle in cycles
        if cycle.get("learner_evidence")
    ]
    return sha256_bytes(_canonical_json(rows))


def _recompute_aggregates(state: dict[str, Any]) -> None:
    state["learner_evidence_sha256"] = _aggregate_evidence_hash(state.get("cycles", []))
    state["learning_commit_shas"] = list(
        dict.fromkeys(
            record["sha"]
            for cycle in state.get("cycles", [])
            for record in cycle.get("learning_commits", [])
        )
    )


def validate_flow(
    state: Any,
    *,
    repo_root: Path | str,
    verify_commits: bool = False,
) -> list[str]:
    errors: list[str] = []
    root = Path(repo_root).resolve()
    if not isinstance(state, dict):
        return ["cursor root must be a JSON object"]
    if state.get("schema_version") != FLOW_SCHEMA_VERSION:
        errors.append(f"schema_version must be {FLOW_SCHEMA_VERSION}")
    if state.get("timezone") != FLOW_TIMEZONE:
        errors.append(f"timezone must be {FLOW_TIMEZONE}")
    try:
        date.fromisoformat(str(state.get("flow_date")))
    except ValueError:
        errors.append("flow_date must be YYYY-MM-DD")
    authorization = state.get("authorization")
    if not isinstance(authorization, dict) or authorization.get("mode") not in AUTHORIZATION_MODES:
        errors.append("authorization mode is invalid")
    elif authorization.get("mode") == "none":
        if authorization.get("authorized_on") is not None:
            errors.append("none authorization must use authorized_on null")
    else:
        try:
            date.fromisoformat(str(authorization.get("authorized_on")))
        except ValueError:
            errors.append("active authorization requires authorized_on YYYY-MM-DD")
    phase = state.get("phase")
    if phase not in PHASES:
        errors.append("phase is invalid")
    resume_phase = state.get("resume_phase")
    if phase == "PAUSED" and resume_phase not in PHASES - {"PAUSED"}:
        errors.append("PAUSED requires a concrete non-PAUSED resume_phase")
    if phase != "PAUSED" and resume_phase is not None:
        errors.append("resume_phase must be null outside PAUSED")
    cycles = state.get("cycles")
    if not isinstance(cycles, list):
        return errors + ["cycles must be a list"]
    seen_cycles: set[str] = set()
    active_ids: list[str] = []
    observed_commits: list[str] = []
    for cycle in cycles:
        if not isinstance(cycle, dict):
            errors.append("every cycle must be an object")
            continue
        cycle_id = cycle.get("cycle_id")
        if not isinstance(cycle_id, str) or not CYCLE_ID_RE.fullmatch(cycle_id):
            errors.append(f"invalid cycle_id: {cycle_id!r}")
            continue
        if cycle_id in seen_cycles:
            errors.append(f"duplicate cycle_id: {cycle_id}")
        seen_cycles.add(cycle_id)
        status = cycle.get("status")
        if status not in CYCLE_STATUSES:
            errors.append(f"invalid cycle status: {cycle_id}")
        if status in {"active", "paused"}:
            active_ids.append(cycle_id)
        if not TARGET_RE.fullmatch(str(cycle.get("primary_target", ""))):
            errors.append(f"invalid cycle primary target: {cycle_id}")
        bridge = cycle.get("bridge_target")
        if bridge is not None and not TARGET_RE.fullmatch(str(bridge)):
            errors.append(f"invalid cycle bridge target: {cycle_id}")
        try:
            _safe_relative_path(str(cycle.get("handoff_path")), root)
        except FlowError as error:
            errors.append(str(error))
        evidence = cycle.get("learner_evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"learner_evidence must be a list: {cycle_id}")
            evidence = []
        for item in evidence:
            content = item.get("content") if isinstance(item, dict) else None
            digest = item.get("content_sha256") if isinstance(item, dict) else None
            if not isinstance(content, str) or digest != sha256_bytes(content.encode("utf-8")):
                errors.append(f"learner evidence content/hash mismatch: {cycle_id}")
        expected_evidence_hash = sha256_bytes(_canonical_json(evidence))
        if cycle.get("learner_evidence_sha256") != expected_evidence_hash:
            errors.append(f"learner evidence aggregate hash mismatch: {cycle_id}")
        if status == "completed":
            try:
                date.fromisoformat(str(cycle.get("completed_on")))
            except ValueError:
                errors.append(f"completed cycle requires completed_on: {cycle_id}")
            if not cycle.get("concepts") or not evidence:
                errors.append(f"completed cycle requires captured concepts and evidence: {cycle_id}")
            if cycle.get("practice", {}).get("state") not in {"completed", "no-extra-practice"}:
                errors.append(f"completed cycle has non-terminal practice: {cycle_id}")
            if cycle.get("knowledge", {}).get("state") not in {"committed", "no-change"}:
                errors.append(f"completed cycle has non-terminal knowledge: {cycle_id}")
        practice = cycle.get("practice", {})
        if practice.get("state") not in PRACTICE_STATES:
            errors.append(f"invalid practice state: {cycle_id}")
        if practice.get("action") is not None and practice.get("action") not in PRACTICE_ACTIONS:
            errors.append(f"invalid practice action: {cycle_id}")
        if practice.get("mode") is not None and practice.get("mode") not in PRACTICE_MODES:
            errors.append(f"invalid practice mode: {cycle_id}")
        knowledge = cycle.get("knowledge", {})
        if knowledge.get("state") not in KNOWLEDGE_STATES:
            errors.append(f"invalid knowledge state: {cycle_id}")
        for record in cycle.get("learning_commits", []):
            if not isinstance(record, dict) or not COMMIT_RE.fullmatch(str(record.get("sha", ""))):
                errors.append(f"invalid learning commit record: {cycle_id}")
                continue
            observed_commits.append(record["sha"])
            paths = record.get("paths")
            if not isinstance(paths, list) or paths != sorted(set(paths)):
                errors.append(f"learning commit paths must be a sorted unique list: {cycle_id}")
                continue
            if verify_commits:
                try:
                    actual_record = inspect_commit(
                        root,
                        record["sha"],
                        expected_subject=record.get("subject"),
                        expected_paths=paths,
                    )
                    if actual_record.as_json() != record:
                        errors.append(
                            f"learning commit metadata differs from Git: {cycle_id} {record['sha']}"
                        )
                except FlowError as error:
                    errors.append(str(error))
        recorded_shas = {
            record.get("sha")
            for record in cycle.get("learning_commits", [])
            if isinstance(record, dict)
        }
        if practice.get("state") == "completed" and practice.get("commit_sha") not in recorded_shas:
            errors.append(f"practice completion commit is not an exact learning commit: {cycle_id}")
        if knowledge.get("state") == "committed" and knowledge.get("commit_sha") not in recorded_shas:
            errors.append(f"knowledge commit is not an exact learning commit: {cycle_id}")
    if len(active_ids) > 1:
        errors.append("at most one unfinished cycle may be active or paused")
    active_id = state.get("active_cycle_id")
    if active_id is not None and active_id not in active_ids:
        errors.append("active_cycle_id does not name the unfinished cycle")
    if active_id is None and phase not in {"SELECT_TARGET", "PAUSED"} and cycles:
        errors.append("an operational phase requires active_cycle_id")
    if state.get("learner_evidence_sha256") != _aggregate_evidence_hash(cycles):
        errors.append("top-level learner_evidence_sha256 is stale")
    if state.get("learning_commit_shas") != list(dict.fromkeys(observed_commits)):
        errors.append("top-level learning_commit_shas is stale")
    saves = state.get("til_saves")
    if not isinstance(saves, list):
        errors.append("til_saves must be a list")
        saves = []
    cycles_by_id = {
        cycle.get("cycle_id"): cycle
        for cycle in cycles
        if isinstance(cycle, dict) and isinstance(cycle.get("cycle_id"), str)
    }
    saved_cycle_ids: set[str] = set()
    for item in saves:
        if not isinstance(item, dict):
            errors.append("every til_saves item must be an object")
            continue
        study_date = str(item.get("study_date", ""))
        try:
            date.fromisoformat(study_date)
        except ValueError:
            errors.append("TIL save study_date must be YYYY-MM-DD")
        expected_path = (
            f"til/{study_date[:4]}/{study_date[5:7]}/{study_date}.md"
            if len(study_date) == 10
            else ""
        )
        if item.get("path") != expected_path:
            errors.append(f"TIL save path differs from its study date: {study_date}")
        if not HASH_RE.fullmatch(str(item.get("sha256", ""))):
            errors.append(f"TIL save hash is invalid: {study_date}")
        if not COMMIT_RE.fullmatch(str(item.get("commit_sha", ""))):
            errors.append(f"TIL save commit is invalid: {study_date}")
        cycle_ids = item.get("cycle_ids")
        if (
            not isinstance(cycle_ids, list)
            or not cycle_ids
            or len(cycle_ids) != len(set(cycle_ids))
        ):
            errors.append(f"TIL save cycle_ids must be a nonempty unique list: {study_date}")
            continue
        for cycle_id in cycle_ids:
            cycle = cycles_by_id.get(cycle_id)
            if cycle is None or cycle.get("status") != "completed":
                errors.append(f"TIL save references a non-completed cycle: {cycle_id}")
                continue
            if cycle_id in saved_cycle_ids:
                errors.append(f"completed cycle appears in more than one TIL save: {cycle_id}")
            saved_cycle_ids.add(cycle_id)
            if (
                cycle.get("completed_on") != study_date
                or not cycle.get("til_consumed")
                or cycle.get("til_path") != item.get("path")
                or cycle.get("til_commit_sha") != item.get("commit_sha")
            ):
                errors.append(f"TIL save and cycle consumption metadata differ: {cycle_id}")
    for cycle_id, cycle in cycles_by_id.items():
        consumed = bool(cycle.get("til_consumed"))
        if consumed and cycle_id not in saved_cycle_ids:
            errors.append(f"consumed cycle is absent from til_saves: {cycle_id}")
        if not consumed and (
            cycle.get("til_path") is not None or cycle.get("til_commit_sha") is not None
        ):
            errors.append(f"unconsumed cycle must not claim a TIL path or commit: {cycle_id}")
    return errors


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cursor", default=DEFAULT_CURSOR_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)
    start = subparsers.add_parser("start")
    start.add_argument("--mode", choices=("lesson-only", "full-day"), required=True)
    subparsers.add_parser("show")
    subparsers.add_parser("pause")
    validate = subparsers.add_parser("validate")
    validate.add_argument("--verify-commits", action="store_true")
    transition = subparsers.add_parser("transition")
    transition.add_argument("phase", choices=sorted(PHASES - {"PAUSED"}))
    candidates = subparsers.add_parser("til-candidates")
    candidates.add_argument("--date")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    root = _repo_root_from_script()
    try:
        if args.command == "start":
            state = load_flow(root, path=args.cursor, create=True)
            state = start_flow(state, mode=args.mode)
            save_flow(state, root, path=args.cursor)
        elif args.command == "pause":
            state = pause_flow(load_flow(root, path=args.cursor))
            save_flow(state, root, path=args.cursor)
        elif args.command == "transition":
            state = transition_phase(load_flow(root, path=args.cursor), args.phase)
            save_flow(state, root, path=args.cursor)
        elif args.command == "validate":
            state = load_flow(root, path=args.cursor)
            errors = validate_flow(state, repo_root=root, verify_commits=args.verify_commits)
            if errors:
                for error in errors:
                    print(f"ERROR {args.cursor} [FLOW_STATE] {error}", file=sys.stderr)
                return 1
        elif args.command == "til-candidates":
            state = load_flow(root, path=args.cursor)
            print(json.dumps(eligible_til_cycles(state, study_date=args.date), ensure_ascii=False, indent=2))
            return 0
        state = load_flow(root, path=args.cursor)
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0
    except FlowError as error:
        print(f"ERROR {args.cursor} [FLOW_STATE] {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
