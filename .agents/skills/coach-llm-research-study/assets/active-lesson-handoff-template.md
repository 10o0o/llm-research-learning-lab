# Active Lesson Handoff

> Codex-generated temporary operational cache. This file is not a durable
> learner note and is not evidence of learner understanding.

## Metadata

- schema_version: 5
- lesson_id: replace-with-stable-lesson-id
- title: Replace with lesson title
- status: preparing
- study_date: YYYY-MM-DD
- created_at: YYYY-MM-DDTHH:MM:SSZ
- updated_at: YYYY-MM-DDTHH:MM:SSZ
- author_id: replace-with-contract-author-id
- draft_path: til/today.md
- input_manifest_sha256: replace-with-64-lowercase-hex
- contract_sha256: replace-with-64-lowercase-hex

## Input Manifest

| ID | Role | Path | SHA-256 |
| --- | --- | --- | --- |
| I001 | primary | materials/private/course/NN-NN_lesson.md | replace-with-file-sha256 |
| I002 | course-index | materials/private/course/INDEX.md | replace-with-file-sha256 |
| I003 | curriculum | CURRICULUM.md | replace-with-file-sha256 |
| I004 | roadmap | ROADMAP.md | replace-with-file-sha256 |

<!-- lesson-contract:start -->
### Objective

Replace with one observable lesson objective.

### Coverage Mode

- mode: full-source

### Curriculum Targets

- CC-DL-01

### Target Decision

- selection_mode: planner
- target_state: START_TARGET
- primary_target: CC-DL-01
- bridge_target: none
- evidence_gap: explain
- completion_evidence: Replace with the observable evidence that closes this target for the current cycle.
- endpoint: TR-SYS-03
- why_now: Replace with the target-first graph and learner-evidence reason.

### Curriculum Treatment Map

| Target ID | Coverage | Gap action | Lesson treatment | Objective IDs | Note |
| --- | --- | --- | --- | --- | --- |
| CC-DL-01 | 충분 | 그대로 사용 | source-only | O001, O002 | Replace with the reviewed reason this treatment matches the current Curriculum row. |

### External Source Identity

| Primary ID | Provider | Course | Offering/Edition | Artifact | Official URL | Final URL | Retrieved at | Media type | Scope | Receipt path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | none | none | none | none | none | none | none | none | none | none |

### External Target Relation

| Target ID | Primary ID | Relation | Objective IDs | Audit basis |
| --- | --- | --- | --- | --- |
| none | none | none | none | none |

### Learner Evidence Baseline

- No demonstrated learner evidence has been found yet.

### Audited Findings

| Finding ID | Type | Source location | Linked IDs | Note |
| --- | --- | --- | --- | --- |
| F001 | prerequisite | materials/private/course/NN-NN_lesson.md#exact-location | O001 | Replace with the exact prerequisite finding. |
| F002 | supplement | CURRICULUM.md#exact-location | O003 | Replace with the exact roadmap-linked supplement finding. |

### Source Coverage Index

| Primary ID | Declared Goal IDs | Objective IDs | Guidance IDs | Excluded locations | Reason |
| --- | --- | --- | --- | --- | --- |
| I001 | none | O001, O002 | none | none | none |

### Declared Goal Alignment

| Goal ID | Primary ID | Goal location | Disposition | Linked IDs | Body support | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| none | none | none | none | none | none | This source has no explicit declared goals. |

### Guidance Map

| Guidance ID | Kind | Source location | Summary | Trigger |
| --- | --- | --- | --- | --- |
| none | none | none | none | none |

### Observable Objective Map

| Objective ID | Requirement | Marker | Source location | Observable outcome | Concept ID | Treatment | Teaching move | Baseline evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O001 | source-core | prerequisite | materials/private/course/NN-NN_lesson.md#exact-location | Replace with one observable source-core outcome. | C01 | full | Replace with the concrete explanation or demonstration move. | none |
| O002 | source-core | none | materials/private/course/NN-NN_lesson.md#exact-location | Replace with another observable source-core outcome. | C02 | full | Replace with the concrete explanation or demonstration move. | none |
| O003 | optional-added | supplement | CURRICULUM.md#exact-location | Replace with one direct roadmap connection. | C03 | full | Replace with the short supplement move. | none |

### Concept Path

1. C01 | [선수개념] | First concept | source: materials/private/course/NN-NN_lesson.md#exact-location
2. C02 | none | Second concept | source: materials/private/course/NN-NN_lesson.md#exact-location
3. C03 | [보충] | Third concept | source: CURRICULUM.md#exact-location

### Prepared Teaching Steps

#### T001

- concept_id: C01
- objective_ids: O001
- delivery_outline: Replace with the ordered explanation outline for O001.
- tiny_example: Replace with a tiny concrete example.
- check_policy: adaptive
- check_basis: if the answer shows the prerequisite -> continue to T002; else -> reteach the prerequisite with the tiny example
- check_question: Replace with one diagnostic question.

#### T002

- concept_id: C02
- objective_ids: O002
- delivery_outline: Replace with the ordered explanation outline for O002.
- tiny_example: Replace with a tiny concrete example.
- check_policy: none
- check_basis: The worked trace exposes this outcome directly and no branch in the next explanation depends on a learner answer.
- check_question: none

#### T003

- concept_id: C03
- objective_ids: O003
- delivery_outline: Replace with the ordered explanation outline for O003.
- tiny_example: Replace with a tiny concrete example.
- check_policy: none
- check_basis: This short supplement reuses the established axis language and does not change the next explanation.
- check_question: none

### Deferred

| Objective ID | Source location | Reason |
| --- | --- | --- |
| none | none | No objectives are deferred. |
<!-- lesson-contract:end -->

## Semantic Review

- review_attempt: 0

> Add at most two contiguous semantic-review attempt blocks using the schema in
> `references/lesson-handoff.md`. Do not leave an example block in the live
> handoff because marker-looking examples are parsed as operational state.

## Current Position

- last_completed_step: none
- current_step: T001
- next_action: teach
- target_objectives: O001
- basis: none
- resume_note: Teach T001 from its reviewed delivery outline.

## Objective Delivery

| Objective ID | State | Mode | Basis/Note |
| --- | --- | --- | --- |
| O001 | pending | none | Awaiting instruction. |
| O002 | pending | none | Awaiting instruction. |
| O003 | pending | none | Awaiting instruction. |

## Daily Learning Coverage

- pre_save_verdict: pending
- reviewed_at: pending
- reviewed_draft_sha256: pending

> For an `uncertain` row, write `draft-anchor: <exact excerpt>` in `Note`.
> The excerpt must occur under the reviewed draft's non-empty `## 남은 질문`.

| Concept ID | Today state | Evidence IDs | TIL representation | Note |
| --- | --- | --- | --- | --- |
| C01 | deferred | none | not-required | Update after this concept is taught. |
| C02 | deferred | none | not-required | Update after this concept is taught. |
| C03 | deferred | none | not-required | Update after this concept is taught. |

## Learner Evidence

> Add learner-evidence blocks only after the learner answers. Use the exact
> block schema in `references/lesson-handoff.md`; do not pre-create evidence.
