from __future__ import annotations

import hashlib
import re
from pathlib import Path


def sha256(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


CONTRACT = """### Objective

Trace a tensor operation and explain its shape contract.

### Coverage Mode

- mode: full-source

### Curriculum Targets

- CC-DL-01

### Target Decision

- selection_mode: user-named-target
- target_state: START_TARGET
- primary_target: CC-DL-01
- bridge_target: none
- evidence_gap: explain
- completion_evidence: Explain both axes and predict the broadcast result shape.
- endpoint: TR-SYS-03
- why_now: The named tensor target is a prerequisite on the Systems route.

### Curriculum Treatment Map

| Target ID | Coverage | Gap action | Lesson treatment | Objective IDs | Note |
| --- | --- | --- | --- | --- | --- |
| CC-DL-01 | 충분 | 그대로 사용 | source-only | O001, O002 | The named source directly supports the selected tensor-shape target. |

### External Source Identity

| Primary ID | Provider | Course | Offering/Edition | Artifact | Official URL | Final URL | Retrieved at | Media type | Scope | Receipt path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | none | none | none | none | none | none | none | none | none | none |

### External Target Relation

| Target ID | Primary ID | Relation | Objective IDs | Audit basis |
| --- | --- | --- | --- | --- |
| none | none | none | none | none |

### Learner Evidence Baseline

- The learner has not yet demonstrated this shape trace.

### Audited Findings

| Finding ID | Type | Source location | Linked IDs | Note |
| --- | --- | --- | --- | --- |
| F001 | prerequisite | materials/lesson.md#axes | O001 | Axis meaning is required before shape propagation. |
| F002 | supplement | CURRICULUM.md#CC-DL-01 | O003 | The attention-axis connection is optional roadmap enrichment. |

### Source Scope Map

| Primary ID | Scope kind | Scope ID | Included locations | Boundary context | Outside-scope disposition |
| --- | --- | --- | --- | --- | --- |
| I001 | entire-source | none | entire-source | none | none |

### Source Coverage Index

| Primary ID | Declared Goal IDs | Objective IDs | Guidance IDs |
| --- | --- | --- | --- |
| I001 | D001, D002, D003 | O001, O002 | G001 |

### Declared Goal Alignment

| Goal ID | Primary ID | Goal location | Disposition | Linked IDs | Body support | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| D001 | I001 | materials/lesson.md#Identify the batch and feature axes. | learning | O001 | materials/lesson.md#axes | none |
| D002 | I001 | materials/lesson.md#Predict the output shape of a broadcast operation. | learning | O002 | materials/lesson.md#shape-propagation | none |
| D003 | I001 | materials/lesson.md#Review the course map only when it affects the current path. | guidance | G001 | materials/lesson.md#orientation | It is navigation guidance, not learner knowledge or skill. |

### Guidance Map

| Guidance ID | Kind | Source location | Summary | Trigger |
| --- | --- | --- | --- | --- |
| G001 | reference | materials/lesson.md#orientation | The course map is an on-demand navigation reference. | The learner asks where this tensor topic fits in the course. |

### Observable Objective Map

| Objective ID | Requirement | Marker | Source location | Observable outcome | Concept ID | Treatment | Teaching move | Baseline evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O001 | source-core | prerequisite | materials/lesson.md#axes | Identify the batch and feature axes in a small tensor. | C01 | full | Trace both axes before naming the operation. | none |
| O002 | source-core | none | materials/lesson.md#shape-propagation | Predict the output shape of a broadcast operation. | C02 | full | Compare aligned dimensions from the right. | none |
| O003 | optional-added | supplement | CURRICULUM.md#CC-DL-01 | Connect tensor axes to batch, token, and hidden axes. | C03 | full | Map one small tensor to an attention input. | none |

### Concept Path

1. C01 | [선수개념] | Axis meaning | source: materials/lesson.md#axes
2. C02 | none | Shape propagation | source: materials/lesson.md#shape-propagation
3. C03 | [보충] | Attention connection | source: CURRICULUM.md#CC-DL-01

### Prepared Teaching Steps

#### T001

- concept_id: C01
- objective_ids: O001
- delivery_outline: Establish axis meaning before tracing a shape-changing operation.
- tiny_example: Trace a 2 by 3 matrix by row and column.
- check_policy: adaptive
- check_basis: if learner identifies both axes -> continue to shape propagation; else -> reteach rows and columns with labels
- check_question: Which axis contains the three features?

#### T002

- concept_id: C02
- objective_ids: O002
- delivery_outline: Align dimensions from the right and explain each resulting axis.
- tiny_example: Broadcast a 2 by 1 tensor with a 1 by 3 tensor.
- check_policy: adaptive
- check_basis: if learner predicts both aligned dimensions -> continue to the attention connection; else -> trace the rightmost aligned dimensions again
- check_question: What is the result shape and why?

#### T003

- concept_id: C03
- objective_ids: O003
- delivery_outline: Reuse the same axis language for a small attention-shaped tensor.
- tiny_example: Map batch, token, and hidden axes for one small tensor.
- check_policy: none
- check_basis: This optional bridge reuses already checked axis language and does not change the next explanation.
- check_question: none

### Deferred

| Objective ID | Source location | Reason |
| --- | --- | --- |
| none | none | No objectives are deferred. |
"""


def build_handoff(
    root: Path,
    *,
    contract: str = CONTRACT,
    status: str = "preparing",
    reviews: list[tuple[str, str]] | None = None,
    evidence: list[dict[str, str]] | None = None,
    lesson_id: str = "tensor-shape-lesson",
    primary_role: str = "primary",
    primary_path: str = "materials/lesson.md",
    primary_bytes: bytes = (
        b"# Lesson\n\n"
        b"## learning-goals\n\n"
        b"- Identify the batch and feature axes.\n"
        b"- Predict the output shape of a broadcast operation.\n"
        b"- Review the course map only when it affects the current path.\n\n"
        b"## axes\n\nTensor axes.\n\n"
        b"## shape-propagation\n\nBroadcast shapes.\n\n"
        b"## orientation\n\nUse the course map when navigation is needed.\n"
    ),
    additional_manifest_inputs: list[tuple[str, str, bytes]] | None = None,
    course_index_path: str | None = None,
    coverage: list[dict[str, str]] | None = None,
    pre_save_verdict: str = "pending",
    reviewed_at: str = "pending",
    reviewed_draft_sha256: str = "pending",
    delivery: list[dict[str, str]] | None = None,
) -> tuple[Path, dict[str, str]]:
    reviews = reviews or []
    evidence = evidence or []
    (root / "materials").mkdir(parents=True, exist_ok=True)
    primary = root / primary_path
    if not primary.exists():
        primary.parent.mkdir(parents=True, exist_ok=True)
        primary.write_bytes(primary_bytes)
    source_hash = sha256(primary.read_bytes())
    curriculum = root / "CURRICULUM.md"
    if not curriculum.exists():
        curriculum.write_text(
            "# Curriculum\n\n"
            "| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
            "| CC-DL-01 | Tensor contracts | D2 | — | explain | primary:SRC-TEST-00-01 | 충분 | 그대로 사용 | Fixture row. |\n"
            "| TR-SYS-03 | Systems endpoint | D3 | CC-DL-01 | design | — | 없음 | 트랙 선택 시 확보 | Fixture endpoint. |\n\n"
            "| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            f"| SRC-TEST-00-01 | `{primary_path}` | HTML 토글 펼침 Markdown | `{source_hash}` | complete | complete | 2026-08-20 | Fixture source. |\n",
            encoding="utf-8",
        )
    curriculum_hash = sha256(curriculum.read_bytes())
    roadmap = root / "ROADMAP.md"
    if not roadmap.exists():
        roadmap.write_text(
            "# Roadmap\n\n## 정적 목표 endpoint\n\n"
            "| 우선순위 | 단계 | 방향 | Endpoint |\n"
            "| ---: | ---: | --- | --- |\n"
            "| 1 | `1A` | Systems | `TR-SYS-03` |\n",
            encoding="utf-8",
        )
    roadmap_hash = sha256(roadmap.read_bytes())
    manifest_inputs = [(primary_role, primary_path, source_hash)]
    for role, path, payload in additional_manifest_inputs or []:
        candidate = root / path
        candidate.parent.mkdir(parents=True, exist_ok=True)
        candidate.write_bytes(payload)
        manifest_inputs.append((role, path, sha256(payload)))
    if course_index_path is not None:
        course_index = root / course_index_path
        manifest_inputs.append(("course-index", course_index_path, sha256(course_index.read_bytes())))
    manifest_inputs.append(("curriculum", "CURRICULUM.md", curriculum_hash))
    manifest_inputs.append(("roadmap", "ROADMAP.md", roadmap_hash))
    manifest_rows = [
        (f"I{index:03d}", role, path, digest)
        for index, (role, path, digest) in enumerate(manifest_inputs, start=1)
    ]
    manifest_hash = sha256(
        "".join(sorted(f"{role}\t{path}\t{digest}\n" for _, role, path, digest in manifest_rows))
    )
    contract_hash = sha256(contract)

    review_iteration = len(reviews)
    latest_verdict, latest_reviewer = reviews[-1] if reviews else ("pending", "none")
    initial_reviewer = reviews[0][1] if reviews else "none"
    review_phase = (
        "none"
        if review_iteration == 0
        else "independent-slice"
        if review_iteration == 1
        else "targeted-recheck"
    )
    review_recheck = "R001" if review_iteration >= 2 else "none"
    review_time = "pending" if review_iteration == 0 else f"2026-08-20T01:00:0{min(review_iteration, 9)}Z"
    review_manifest = "pending" if review_iteration == 0 else manifest_hash
    review_contract = "pending" if review_iteration == 0 else contract_hash
    repair_row = (
        "| R001 | lesson-contract | Revise the named contract point. |"
        if latest_verdict == "repair_required"
        else "| none | none | none |"
    )
    blocker_row = (
        "| B001 | source-access | materials/lesson.md | Required source is unavailable. |"
        if latest_verdict == "blocked"
        else "| none | none | none | none |"
    )
    review_text = f"""- initial_reviewer_id: {initial_reviewer}
- reviewer_id: {latest_reviewer}
- review_iteration: {review_iteration}
- review_phase: {review_phase}
- recheck_of: {review_recheck}
- reviewed_at: {review_time}
- verdict: {latest_verdict}
- reviewed_input_manifest_sha256: {review_manifest}
- reviewed_contract_sha256: {review_contract}

### Repair Findings

| Finding ID | Location | Detail |
| --- | --- | --- |
{repair_row}

### Blocking Findings

| Finding ID | Kind | Location | Detail |
| --- | --- | --- | --- |
{blocker_row}
"""

    evidence_text = ""
    content_hashes: dict[str, str] = {}
    for index, item in enumerate(evidence, start=1):
        evidence_id = f"E{index:03d}"
        content = item.get("content", "배치 축과 특성 축을 구분해 결과 shape를 설명했다.")
        content_hash = sha256(content)
        content_hashes[evidence_id] = content_hash
        evidence_text += f"""
<!-- learner-evidence:{evidence_id}:start -->
### {evidence_id}

- concept: {item.get("concept", "C01")}
- objective_ids: {item.get("objective_ids", {"C01": "O001", "C02": "O002", "C03": "O003"}.get(item.get("concept", "C01"), "O001"))}
- kind: {item.get("kind", "explain_back")}
- provenance: {item.get("provenance", "learner")}
- verdict: {item.get("verdict", "confirmed")}
- append_state: {item.get("append_state", "pending")}
- captured_at: 2026-08-20T01:30:0{index}Z
- content_sha256: {content_hash}

#### Learner Content

<!-- learner-content:start -->
{content}
<!-- learner-content:end -->

#### Tutor Assessment

{item.get("assessment", "축의 의미와 결과 shape를 독립적으로 설명했다.")}
<!-- learner-evidence:{evidence_id}:end -->
"""

    if delivery is None:
        delivery = [
            {
                "objective": objective,
                "state": "delivered" if status == "completed" else "pending",
                "mode": "full" if status == "completed" else "none",
                "note": "Delivered in the completed fixture." if status == "completed" else "Awaiting instruction.",
            }
            for objective in ("O001", "O002", "O003")
        ]
    delivery_rows = "\n".join(
        "| {objective} | {state} | {mode} | {note} |".format(**row)
        for row in delivery
    )
    delivered_objectives = [row["objective"] for row in delivery if row["state"] == "delivered"]
    objective_concepts: dict[str, str] = {}
    for line in contract.splitlines():
        cells = [cell.strip() for cell in line.strip()[1:-1].split("|")] if line.startswith("|") and line.endswith("|") else []
        if len(cells) == 9 and re.fullmatch(r"O\d{3,}", cells[0]):
            objective_concepts[cells[0]] = cells[5]

    if coverage is None:
        coverage = [
            {
                "concept": concept,
                "state": "uncertain" if any(objective_concepts[item] == concept for item in delivered_objectives) else "deferred",
                "evidence_ids": "none",
                "representation": "missing" if any(objective_concepts[item] == concept for item in delivered_objectives) else "not-required",
                "note": "Taught but not demonstrated." if any(objective_concepts[item] == concept for item in delivered_objectives) else "Not taught yet.",
            }
            for concept in ("C01", "C02", "C03")
        ]
    coverage_rows = "\n".join(
        "| {concept} | {state} | {evidence_ids} | {representation} | {note} |".format(**row)
        for row in coverage
    )

    step_objectives = {
        match.group(1): [item.strip() for item in match.group(2).split(",")]
        for match in re.finditer(
            r"^#### (T\d{3,})\n\n(?:[^\n]*\n)*?- objective_ids: ([^\n]+)$",
            contract,
            re.MULTILINE,
        )
    }
    step_ids = list(step_objectives)
    current_step = next(
        (step_id for step_id in step_ids if any(item not in delivered_objectives for item in step_objectives[step_id])),
        "none",
    )
    if current_step == "none":
        last_completed_step = step_ids[-1]
        next_action = "complete"
        target_objectives = "none"
        resume_note = "All Teaching Steps are complete."
    else:
        current_index = step_ids.index(current_step)
        last_completed_step = step_ids[current_index - 1] if current_index else "none"
        next_action = "teach"
        target_objectives = ", ".join(
            item for item in step_objectives[current_step] if item not in delivered_objectives
        )
        resume_note = f"Teach {current_step} from its reviewed delivery outline."
    rows = "\n".join(f"| {item_id} | {role} | {path} | {digest} |" for item_id, role, path, digest in manifest_rows)
    text = f"""# Active Lesson Handoff

> Codex-generated temporary operational cache. This file is not a durable
> learner note and is not evidence of learner understanding.

## Metadata

- schema_version: 7
- lesson_id: {lesson_id}
- title: Tensor shape lesson
- status: {status}
- study_date: 2026-08-20
- created_at: 2026-08-20T00:00:00Z
- updated_at: 2026-08-20T01:30:00Z
- author_id: contract-author
- draft_path: til/today.md
- input_manifest_sha256: {manifest_hash}
- contract_sha256: {contract_hash}

## Input Manifest

| ID | Role | Path | SHA-256 |
| --- | --- | --- | --- |
{rows}

<!-- lesson-contract:start -->
{contract}
<!-- lesson-contract:end -->

## Semantic Review

{review_text}
## Current Position

- last_completed_step: {last_completed_step}
- current_step: {current_step}
- next_action: {next_action}
- target_objectives: {target_objectives}
- basis: none
- resume_note: {resume_note}

## Objective Delivery

| Objective ID | State | Mode | Basis/Note |
| --- | --- | --- | --- |
{delivery_rows}

## Daily Learning Coverage

- pre_save_verdict: {pre_save_verdict}
- reviewed_at: {reviewed_at}
- reviewed_draft_sha256: {reviewed_draft_sha256}

| Concept ID | Today state | Evidence IDs | TIL representation | Note |
| --- | --- | --- | --- | --- |
{coverage_rows}

## Learner Evidence
{evidence_text}
"""
    handoff = root / "tmp" / "active-lesson-handoff.md"
    handoff.parent.mkdir(parents=True, exist_ok=True)
    handoff.write_text(text, encoding="utf-8")
    return handoff, {
        "manifest_hash": manifest_hash,
        "contract_hash": contract_hash,
        **{f"{item_id}_hash": digest for item_id, digest in content_hashes.items()},
    }


def draft_envelope(lesson_id: str, evidence_id: str, content: str) -> str:
    return (
        f"<!-- lesson-evidence:{lesson_id}:{evidence_id}:{sha256(content)} -->\n"
        f"{content}\n"
        f"<!-- /lesson-evidence:{lesson_id}:{evidence_id} -->\n"
    )
