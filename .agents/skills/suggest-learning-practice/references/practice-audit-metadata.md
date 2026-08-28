# Practice audit metadata v4

Read this reference when creating or validating a practice Notebook. Metadata at
`metadata.llm_research_lab.practice` is an internal provenance and authoring
layer, not a mastery record or learner-facing specification.

All newly generated artifacts use schema v4. Existing schema-v3 notebooks remain
valid without migration. Schema v2 requires the existing explicit metadata-only
migration; learner cells, outputs, execution counts, IDs, and answers must not
change.

## Learning input union

Schema v4 replaces the mandatory TIL input with exactly one `learning_input`.

### Completed lesson session

The full day flow uses:

```json
{
  "kind": "lesson-session",
  "cycle_id": "cycle-example",
  "lesson_id": "example-lesson",
  "handoff_path": "tmp/active-lesson-handoff.md",
  "handoff_sha256": "<64 lowercase hex>",
  "primary_target": "CC-DL-01",
  "bridge_target": null,
  "concept_ids": ["C01", "C02"],
  "evidence_ids": ["E001", "E002"],
  "concept_sha256": "<canonical confirmed concept projection hash>",
  "learner_evidence_sha256": "<canonical confirmed learner evidence hash>"
}
```

The handoff must be a completed schema-v9 session. Its exact cycle, lesson,
targets, ordered confirmed concepts, ordered confirmed learner evidence, and
both canonical hashes must match. Creation and strict completion require the
live handoff and exact file hash. Learner-state validation may emit an offline
warning after deliberate downstream cleanup; hash or identity drift is
`SESSION_REPAIR_REQUIRED`.

Session Outcomes do not use `til_location`. They link non-empty subsets of the
input's `concept_ids` and `evidence_ids`, one performance action, exercises,
required evidence, and relevant Curriculum targets.

### Exact finalized TIL

Manual or historical study may use:

```json
{
  "kind": "finalized-til",
  "path": "til/2026/08/2026-08-28.md",
  "sha256": "<64 lowercase hex>"
}
```

This form names one validated dated TIL. Its Outcomes retain exact
`til_location` values. Missing or drifted input is `TIL_REPAIR_REQUIRED`.
Do not infer the latest TIL.

## Complete Notebook example

```json
{
  "schema_version": 4,
  "artifact_kind": "standalone-practice",
  "scaffold_mode": "guided-fading",
  "practice_mode": "NOTEBOOK",
  "curriculum_targets": ["CC-DL-01"],
  "learning_input": {
    "kind": "lesson-session",
    "cycle_id": "cycle-example",
    "lesson_id": "example-lesson",
    "handoff_path": "tmp/active-lesson-handoff.md",
    "handoff_sha256": "<64 lowercase hex>",
    "primary_target": "CC-DL-01",
    "bridge_target": null,
    "concept_ids": ["C01"],
    "evidence_ids": ["E001"],
    "concept_sha256": "<64 lowercase hex>",
    "learner_evidence_sha256": "<64 lowercase hex>"
  },
  "sources": [
    {
      "id": "S001",
      "kind": "lesson",
      "path": "materials/private/course/01-01_lesson.md",
      "sha256": "<64 lowercase hex>"
    }
  ],
  "outcomes": [
    {
      "id": "O01",
      "concept_ids": ["C01"],
      "evidence_ids": ["E001"],
      "action": "implement",
      "exercise_ids": ["E01"],
      "required_evidence": "구현, 실행, 결과 해석",
      "curriculum_target_ids": ["CC-DL-01"]
    }
  ],
  "exercises": [
    {
      "id": "E01",
      "primary_outcome_id": "O01",
      "supporting_outcome_ids": [],
      "scaffold_stage": "guided",
      "learner_target_ids": ["T-E01-01"]
    }
  ],
  "requirements": [
    {
      "id": "C-E01-01",
      "exercise_id": "E01",
      "kind": "source-given",
      "claim": "반환된 shape는 일반 tuple로 기록해야 합니다.",
      "owner": "learner",
      "source_locations": [
        {
          "source_id": "S001",
          "locator": "Tensor 카드 요구사항",
          "anchor": "shape를 일반 tuple로 변환한다"
        }
      ],
      "rationale": "",
      "visible_cell_id": "e01-brief",
      "target_ids": ["T-E01-01"]
    }
  ],
  "learner_targets": [
    {
      "id": "T-E01-01",
      "exercise_id": "E01",
      "kind": "code",
      "cell_id": "e01-implementation",
      "marker": "# TODO: Tensor 속성을 채우세요",
      "placeholder": "raise NotImplementedError(\"Tensor 속성을 채우세요\")",
      "symbol": "tensor_card",
      "outcome_ids": ["O01"],
      "requirement_ids": ["C-E01-01"]
    }
  ]
}
```

`practice_mode` is `NOTEBOOK`, `BENCHMARK`, or `DATASET_PROJECT` for
local notebooks. The artifact-level Curriculum targets are the exact union of
Outcome target IDs. These are relevance links only.

## Source records

Source IDs are contiguous `S001`, `S002`, and so on. Requirement locations
reference stable source IDs, not paths as identity.

Local kinds are `course-index`, `lesson`, `instructor-practice`, and
`reference`; each stores the exact repository-relative path and current hash.
Instructor practice also records its explicit related lesson and variant.

A temporary external source stores provider, course, offering or edition,
artifact, official and final HTTPS URLs, retrieval time, media type, exact
scope, byte hash, cache path, and receipt path. Cache and receipt identity must
match the reviewed lesson. Normal learner-state validation warns if deliberate
cleanup made them offline. Strict external validation requires the bytes and
receipt. Never fabricate durable coverage from a temporary receipt.

## Graph invariants

- Outcome IDs and Exercise IDs are contiguous.
- Outcome action is `implement`, `test`, `debug`, `interpret`, or
  `design`.
- Each Exercise has one primary Outcome, optional supporting Outcomes, one
  scaffold stage, and one to three learner targets.
- Requirements are atomic, learner-visible contracts. Source-given requirements
  need an exact source ID, locator, and normalized anchor.
- Requirements and learner targets reference each other in both directions
  within the same Exercise.
- Learner-target kinds are `code`, `debug`, `prediction`, `design`, and
  `interpretation`. Required reflections are tracked learner targets.

Every cell has a stable nbformat ID and internal role. There is exactly one
unexecuted setup cell, followed by adjacent brief, implementation, fixture,
check, and reflection cells per Exercise. Check metadata records assertion or
expected-exception kind, AST ordinal, fingerprint, category, and atomic
Requirement. Internal IDs never appear on the learner surface.

## Validation states and completion

Creation validation requires an unexecuted artifact and unresolved learner
targets. Learner-state validation permits saved work and output while retaining
schema, ownership, source, disclosure, and check traceability.

Completion requires every code and reflection target resolved; setup,
implementation, fixture, and checker cells actually executed in current order;
no error output or non-empty stderr; live strict session/source provenance; and
learner-authored result interpretation. A checker or platform pass alone is not
completion and cannot update knowledge.

After completion, only the exact Notebook path may be committed. A short
external submission uses its exact `challenges/` path instead; a Kaggle
execution remains a Notebook under `practice/`.
