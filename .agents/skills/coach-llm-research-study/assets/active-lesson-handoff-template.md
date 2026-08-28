# Active Lesson Handoff

> Codex-generated temporary operational cache. This file is not a durable
> learner note and is not evidence of learner understanding.

## Metadata

- schema_version: 9
- cycle_id: replace-with-daily-flow-cycle-id
- lesson_id: replace-with-stable-lesson-id
- title: Replace with lesson title
- status: preparing
- session_profile: standard
- flow_mode: day-full
- study_date: YYYY-MM-DD
- created_at: YYYY-MM-DDTHH:MM:SSZ
- updated_at: YYYY-MM-DDTHH:MM:SSZ
- author_id: replace-with-contract-author-id
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

### Source Scope Map

| Primary ID | Scope kind | Scope ID | Included locations | Boundary context | Outside-scope disposition |
| --- | --- | --- | --- | --- | --- |
| I001 | entire-source | none | entire-source | none | none |

### Source Coverage Index

| Primary ID | Declared Goal IDs | Objective IDs | Guidance IDs |
| --- | --- | --- | --- |
| I001 | none | O001, O002 | none |

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

### Module Plan

| Module ID | Topic | Concept IDs | Source locators | Application step | Expected minutes |
| --- | --- | --- | --- | --- | ---: |
| M01 | Why the first concept is needed | C01 | materials/private/course/NN-NN_lesson.md#exact-location | T002 | 15 |
| M02 | Core mechanism and assumptions | C02 | materials/private/course/NN-NN_lesson.md#exact-location | T003 | 20 |
| M03 | Failure boundary and correction | C02, C03 | materials/private/course/NN-NN_lesson.md#exact-location; CURRICULUM.md#exact-location | T004 | 15 |
| M04 | Integrated transfer to the target | C01, C02, C03 | materials/private/course/NN-NN_lesson.md#exact-location; CURRICULUM.md#exact-location | T005 | 20 |

### Session Plan

- session_goal: Connect the motivating problem, concept model, worked example, limitation, and one integrated transfer.
- exit_step: T005
- exit_evidence_kind: transfer

### Example Map

| Example ID | Purpose | Fixture | Objective IDs |
| --- | --- | --- | --- |
| X001 | Motivate the first concept | Replace with the concrete motivating fixture. | O001 |
| X002 | Work the core mechanism | Replace with a different deterministic worked fixture. | O002 |
| X003 | Expose a limitation | Replace with a failure or counterexample fixture. | O002, O003 |
| X004 | Transfer across concepts | Replace with one integrated application fixture. | O001, O002, O003 |

### Prepared Teaching Steps

#### T001

- step_role: motivation
- concept_ids: C01
- objective_ids: O001
- example_id: X001
- delivery_outline: Replace with the ordered explanation outline for O001.
- tiny_example: Replace with a tiny concrete example.
- check_policy: none
- check_basis: The motivating fixture makes the problem concrete before a branch is useful.
- check_question: none

#### T002

- step_role: concept-model
- concept_ids: C01
- objective_ids: O001
- example_id: X001
- delivery_outline: Replace with the concept model that explains O001.
- tiny_example: Replace with a tiny concrete example.
- check_policy: adaptive
- check_basis: if the answer shows the prerequisite -> continue to T003; else -> reteach the prerequisite with the tiny example
- check_question: Replace with one diagnostic question.

#### T003

- step_role: worked-example
- concept_ids: C02
- objective_ids: O002
- example_id: X002
- delivery_outline: Work the core mechanism for O002 from inputs to result.
- tiny_example: Replace with a tiny concrete example.
- check_policy: adaptive
- check_basis: if the learner applies the mechanism correctly -> continue to the limitation; else -> retrace the smallest failed step with a different fixture
- check_question: Replace with one learner calculation, prediction, or trace.

#### T004

- step_role: contrast-limit
- concept_ids: C02, C03
- objective_ids: O002, O003
- example_id: X003
- delivery_outline: Contrast the valid mechanism with one failure or limitation.
- tiny_example: Replace with a distinct counterexample or boundary case.
- check_policy: none
- check_basis: The explicit contrast prepares the final transfer without requiring a separate quiz.
- check_question: none

#### T005

- step_role: synthesis-transfer
- concept_ids: C01, C02, C03
- objective_ids: O001, O002, O003
- example_id: X004
- delivery_outline: Integrate the three concepts in one small transfer task.
- tiny_example: Replace with a new fixture that requires the learner to connect at least two concepts.
- check_policy: adaptive
- check_basis: if the learner integrates the concepts -> finish the session; else -> revisit the smallest failed link before retrying
- check_question: Replace with one integrated transfer or explain-back question.

### Deferred

| Objective ID | Source location | Reason |
| --- | --- | --- |
| none | none | No objectives are deferred. |
<!-- lesson-contract:end -->

## Semantic Review

- initial_reviewer_id: none
- reviewer_id: none
- review_iteration: 0
- review_phase: none
- recheck_of: none
- reviewed_at: pending
- verdict: pending
- reviewed_input_manifest_sha256: pending
- reviewed_contract_sha256: pending

### Repair Findings

| Finding ID | Location | Detail |
| --- | --- | --- |
| none | none | none |

### Blocking Findings

| Finding ID | Kind | Location | Detail |
| --- | --- | --- | --- |
| none | none | none | none |

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

## Teaching Step Delivery

| Step ID | State | Basis/Note |
| --- | --- | --- |
| T001 | pending | Awaiting teaching. |
| T002 | pending | Awaiting teaching. |
| T003 | pending | Awaiting teaching. |
| T004 | pending | Awaiting teaching. |
| T005 | pending | Awaiting teaching. |

## Session Concept Coverage

| Concept ID | Session state | Evidence IDs | Note |
| --- | --- | --- | --- |
| C01 | deferred | none | Update after this concept is taught. |
| C02 | deferred | none | Update after this concept is taught. |
| C03 | deferred | none | Update after this concept is taught. |

## Learner Evidence

> Add learner-evidence blocks only after the learner answers. Use the exact
> block schema in `references/lesson-handoff.md`; do not pre-create evidence.
