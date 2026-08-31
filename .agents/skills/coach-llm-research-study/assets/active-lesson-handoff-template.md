# Active Lesson Handoff

> Codex-generated temporary operational cache. This file is not a durable
> learner note and is not evidence of learner understanding.

## Metadata

- schema_version: 10
- cycle_id: replace-with-daily-flow-cycle-id
- lesson_id: replace-with-stable-lesson-id
- title: Replace with lesson title
- status: preparing
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

### Session Profile Decision

- profile: standard
- basis: default-standard
- requested_constraint: none
- planned_minutes: 70

### Coverage Mode

- mode: full-source

### Curriculum Targets

- CC-DL-01

### Target Decision

- selection_mode: planner
- target_state: START_TARGET
- primary_target: CC-DL-01
- bridge_target: none
- target_evidence_requirements: explain
- target_evidence_basis: Replace with the exact Curriculum evidence-requirement basis.
- target_evidence_gap: explain
- lesson_evidence_scope: explain
- lesson_scope_basis: Replace with why this lesson directly covers this exact subset.
- residual_target_evidence: none
- residual_practice_basis: Replace with why the residual belongs in practice or why no target-level residual remains.
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

| Primary ID | Scope kind | Scope ID | Included units | Boundary units | Outside-scope disposition |
| --- | --- | --- | --- | --- | --- |
| I001 | entire-source | none | entire-source | none | none |

### Boundary Decision Map

| Boundary ID | Primary ID | Unit locator | Relation | Disposition | Reason |
| --- | --- | --- | --- | --- | --- |
| none | none | none | none | none | none |

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

| Objective ID | Requirement | Marker | Source location | Observable outcome | Concept ID | Prerequisite Concept IDs | Treatment | Teaching move | Baseline evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O001 | source-core | prerequisite | materials/private/course/NN-NN_lesson.md#exact-location | Replace with one observable source-core outcome. | C01 | none | full | Replace with the concrete explanation or demonstration move. | none |
| O002 | source-core | none | materials/private/course/NN-NN_lesson.md#exact-location | Replace with another observable source-core outcome. | C02 | C01 | full | Replace with the concrete explanation or demonstration move. | none |
| O003 | optional-added | supplement | CURRICULUM.md#exact-location | Replace with one direct roadmap connection. | C03 | C01, C02 | full | Replace with the short supplement move. | none |

### Concept Path

1. C01 | [선수개념] | First concept | source: materials/private/course/NN-NN_lesson.md#exact-location
2. C02 | none | Second concept | source: materials/private/course/NN-NN_lesson.md#exact-location
3. C03 | [보충] | Third concept | source: CURRICULUM.md#exact-location

### Module Plan

| Module ID | Topic | Concept IDs | Source locators | Representation | Learner action | Teaching Step IDs | Application step | Expected minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| M01 | Why the first concept is needed | C01 | materials/private/course/NN-NN_lesson.md#exact-location | numeric | explain | T001, T002, T003 | T003 | 15 |
| M02 | Core mechanism and assumptions | C01, C02 | materials/private/course/NN-NN_lesson.md#exact-location | tensor | shape | T004, T005 | T005 | 20 |
| M03 | Failure boundary and correction | C01, C02, C03 | materials/private/course/NN-NN_lesson.md#exact-location; CURRICULUM.md#exact-location | code-api | debug | T006, T007 | T007 | 15 |
| M04 | Integrated transfer to a new task | C01, C02, C03 | materials/private/course/NN-NN_lesson.md#exact-location; CURRICULUM.md#exact-location | task-experiment | transfer | T008, T009 | T009 | 20 |

### Session Plan

- session_goal: Connect the motivating problem, concept model, worked example, limitation, and one integrated transfer.
- exit_step: T009
- exit_evidence_kind: transfer

### Example Map

| Example ID | Purpose | Fixture | Objective IDs |
| --- | --- | --- | --- |
| X001 | Motivate the first concept | Replace with the concrete motivating fixture. | O001 |
| X002 | Work the first representation | Replace with a deterministic numeric worked fixture. | O001 |
| X003 | Work the core mechanism | Replace with a distinct Tensor worked fixture. | O001, O002 |
| X004 | Expose and diagnose a limitation | Replace with an actual `class Name(nn.Module):`, `def forward(...):`, concrete `nn.*(...)` call, and Tensor/shape-flow fixture when implementation or debugging is in scope. | O001, O002, O003 |
| X005 | Transfer across concepts | Replace with one novel task, code, or system fixture whose normalized content is not used in any earlier fixture or context. | O001, O002, O003 |

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
- check_policy: none
- check_basis: Explain the prerequisite fully before its module application.
- check_question: none

#### T003

- step_role: worked-example
- concept_ids: C01
- objective_ids: O001
- example_id: X002
- delivery_outline: Walk the first representation, then let the learner apply it to a changed fixture.
- tiny_example: Replace with a deterministic numeric trace.
- check_policy: adaptive
- check_basis: if the learner applies C01 -> continue to the core mechanism; else -> retrace the smallest failed part before retrying
- check_question: Replace with one learner application of C01.

#### T004

- step_role: concept-model
- concept_ids: C01, C02
- objective_ids: O001, O002
- example_id: X003
- delivery_outline: Explain the core mechanism and walk every intermediate Tensor or state shape.
- tiny_example: Replace with a distinct Tensor trace.
- check_policy: none
- check_basis: Complete the mechanism and trace before asking the learner to apply it.
- check_question: none

#### T005

- step_role: worked-example
- concept_ids: C01, C02
- objective_ids: O001, O002
- example_id: X003
- delivery_outline: Walk a changed fixture, then let the learner predict or calculate the result.
- tiny_example: Replace with a second worked fixture in a representation different from X002.
- check_policy: adaptive
- check_basis: if the learner applies the mechanism -> continue to its failure boundary; else -> retrace the first failed transition
- check_question: Replace with one core-mechanism application.

#### T006

- step_role: contrast-limit
- concept_ids: C01, C02, C03
- objective_ids: O001, O002, O003
- example_id: X004
- delivery_outline: Explain a real limitation or counterexample; when implementation/debugging is in scope, name an actual `class Name(nn.Module):`, `def forward(...):`, and concrete `nn.*(...)` call.
- tiny_example: Replace with a distinct Tensor/shape trace containing at least three labeled stages joined by arrows, such as `x: (B,T,D) -> hidden: (B,T,H) -> logits: (B,C)`.
- check_policy: none
- check_basis: Explain the failure mechanism before asking the learner to diagnose it.
- check_question: none

#### T007

- step_role: worked-example
- concept_ids: C01, C02, C03
- objective_ids: O001, O002, O003
- example_id: X004
- delivery_outline: Walk the failure from input through the failing state, then let the learner diagnose a changed case.
- tiny_example: Replace with a concrete class/API/forward/Tensor or data-flow trace when required.
- check_policy: adaptive
- check_basis: if the learner diagnoses the causal failure -> continue to the new task; else -> expose the smallest intermediate state and retry
- check_question: Replace with one authentic diagnosis or correction.

#### T008

- step_role: concept-model
- concept_ids: C01, C02, C03
- objective_ids: O001, O002, O003
- example_id: none
- delivery_outline: Summarize the reusable strategy without revealing or rehearsing the final novel fixture.
- tiny_example: Re-state the general decision procedure that will be reused in a new context.
- check_policy: none
- check_basis: Set up the novel context before the integrated transfer.
- check_question: none

#### T009

- step_role: synthesis-transfer
- concept_ids: C01, C02, C03
- objective_ids: O001, O002, O003
- example_id: X005
- delivery_outline: Integrate every non-deferred concept and objective in the novel task, code, or system context.
- tiny_example: Replace with a new fixture that requires every non-deferred concept.
- check_policy: adaptive
- check_basis: if the learner integrates all non-deferred concepts and objectives -> finish the session; else -> revisit the smallest failed link before retrying
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
- scope_breadth: pending
- teaching_order: pending
- authentic_application: pending
- assessment_load: pending
- exit_integration: pending

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
| T006 | pending | Awaiting teaching. |
| T007 | pending | Awaiting teaching. |
| T008 | pending | Awaiting teaching. |
| T009 | pending | Awaiting teaching. |

## Session Concept Coverage

| Concept ID | Session state | Evidence IDs | Note |
| --- | --- | --- | --- |
| C01 | deferred | none | Update after this concept is taught. |
| C02 | deferred | none | Update after this concept is taught. |
| C03 | deferred | none | Update after this concept is taught. |

## Learner Evidence

> Add learner-evidence blocks only after the learner answers. Use the exact
> block schema in `references/lesson-handoff.md`; do not pre-create evidence.
