# Practice audit metadata v2

Read this reference when creating, migrating, or validating a Notebook. The
metadata is an internal authoring and review layer inside the same `.ipynb`; it
is not a security boundary and never replaces learner-visible requirements.

Schema v2 separates four things that v1 conflated:

- an Outcome says what performance from the TIL needs practice;
- an Exercise says which one primary concept is practised and how much support
  is provided;
- a Requirement states one observable behavior and who owns it;
- a Learner Target identifies the exact operation or response left unfinished.

## Notebook metadata

Store the audit at `metadata.llm_research_lab.practice`:

```json
{
  "schema_version": 2,
  "artifact_kind": "standalone-practice",
  "scaffold_mode": "guided-fading",
  "til": {
    "path": "til/2026/08/2026-08-24.md",
    "sha256": "<64 lowercase hex>"
  },
  "sources": [
    {
      "kind": "lesson",
      "path": "materials/private/course/01-01_lesson.md",
      "sha256": "<64 lowercase hex>"
    },
    {
      "kind": "instructor-practice",
      "path": "materials/private/course/course-provided-practice/01-01_basic.md",
      "sha256": "<64 lowercase hex>",
      "related_lesson": "materials/private/course/01-01_lesson.md",
      "variant": "basic"
    }
  ],
  "outcomes": [
    {
      "id": "O01",
      "til_location": "오늘의 학습 > 식별 문구",
      "action": "implement",
      "exercise_ids": ["E01"],
      "required_evidence": "구현, 공개 검사, 결과 해석"
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
      "claim": "반환된 `shape`는 Tensor shape를 일반 tuple로 기록해야 합니다.",
      "owner": "learner",
      "source_locations": [
        {
          "path": "materials/private/course/01-01_lesson.md",
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
      "marker": "# TODO: Tensor 속성 네 가지를 채우세요",
      "placeholder": "raise NotImplementedError(\"Tensor 속성을 채우세요\")",
      "symbol": "tensor_card",
      "outcome_ids": ["O01"],
      "requirement_ids": ["C-E01-01"]
    }
  ]
}
```

### Shared records

- Repository paths are relative, unique, existing files. Store current SHA-256
  values so source drift invalidates readiness.
- Source `kind` is `course-index`, `lesson`, `instructor-practice`, or
  `reference`. Instructor practice also records `related_lesson` and
  `variant: basic | advanced | single`.
- Outcome IDs are contiguous `O01`, `O02`, and so on. `action` is `implement`,
  `test`, `debug`, `interpret`, or `design`.

### Exercise records

- Exercise IDs are contiguous and match learner-flow cell metadata.
- `primary_outcome_id` is singular. `supporting_outcome_ids` may preserve
  naturally reused knowledge without creating another primary task.
- `scaffold_stage` is `guided`, `partial`, or `independent`.
- `learner_target_ids` is non-empty and contains at most three same-Exercise
  targets. A migrated completed Exercise still lists its targets; it is checked
  with learner-state validation rather than erased.

### Atomic Requirement records

- Requirement IDs are contiguous within each Exercise. `kind` is
  `source-given`, `practice-given`, or `derive`; `owner` is `provided` or
  `learner`.
- `claim` is one complete natural-language behavior. Its normalized full text
  must appear in `visible_cell_id`, a same-Exercise brief before implementation.
  Lists of isolated tokens are not a specification.
- A Requirement should describe one input-output relation or failure boundary.
  Multiple checks may reuse it, but each observable maps to exactly one atomic
  Requirement.
- A `source-given` Requirement has at least one source location. `anchor` is an
  exact normalized excerpt that must exist at the listed source path;
  `locator` is a short human navigation hint.
- A `practice-given` Requirement needs a concrete `rationale`. It defaults to
  `owner: provided`. If it is learner-owned, add `learner_outcome_ids`; these
  IDs must be shared by every linked target and explain why the local API rule
  is itself a TIL learning outcome.
- `target_ids` is empty for provided behavior and non-empty for learner-owned
  behavior. Requirement and Learner Target records reference each other in both
  directions, and every ID stays within the same Exercise.

### Learner Target records

- Target IDs are contiguous within each Exercise: `T-E01-01`, `T-E01-02`, ...
- `kind` is `code`, `debug`, `prediction`, `design`, or `interpretation`.
- `cell_id` names an implementation or reflection cell for the same Exercise.
- `marker` is a natural learner-facing TODO or response prompt. It must be
  present without exposing the target ID.
- `placeholder` is the exact unresolved text replaced by the learner. In
  creation-ready mode it must still exist in the target cell. In
  `--learner-state` it may be absent.
- `symbol` is optional. When present it names a top-level function or
  `Class.method` containing the placeholder in creation-ready mode. Complete
  helpers and scaffold may coexist in the cell.
- `outcome_ids` and `requirement_ids` must be known, same-Exercise links.

## Cell metadata

Every cell has a stable nbformat cell `id` and this custom metadata:

```json
{
  "llm_research_lab": {
    "practice": {
      "role": "brief",
      "exercise_id": "E01"
    }
  }
}
```

Roles are `intro` and `setup`, exactly once without `exercise_id`, followed by
`brief`, `implementation`, `fixture`, `check`, and `reflection`, exactly once
per Exercise and in that order. Role metadata, not visible markers, identifies
the cell. Every required response in a reflection cell has a Learner Target.
When a reflection cell has no target, its learner-facing text must explicitly
say that the note is optional and is not required for exercise completion.

## Check trace

The `check` cell records every `np.testing.*` or `torch.testing.*` call and every
expected-exception block detected by the validator:

```json
[
  {
    "ordinal": 1,
    "kind": "assertion",
    "fingerprint": "sha256:<normalized AST hash>",
    "category": "normal",
    "requirement_ids": ["C-E01-01"]
  }
]
```

- Ordinal, kind, AST fingerprint, and order must match the code.
- Category is `normal`, `edge`, or `failure`. Use the categories that represent
  meaningful behavior; do not invent an error contract merely to fill all
  three.
- Every observable maps to exactly one defined same-Exercise Requirement.
  Every machine-checkable Requirement is exercised at least once. A
  learner-owned Requirement may intentionally have no assertion only when all
  of its targets are `design` or `interpretation` responses in that Exercise's
  reflection cell; this prevents prose understanding from being disguised as
  a token-returning helper merely to satisfy the validator.

## Validation states

Default creation-ready validation requires all code cells to be unexecuted and
every declared target placeholder to remain. `--learner-state` permits resolved
targets and execution state while retaining schema, source, disclosure,
ownership, surface-leak, and check-trace validation. It does not certify a
Notebook as a fresh blank artifact.

Schema v1 is rejected with a migration message. Regenerate or deliberately
migrate it; do not silently reinterpret token lists as complete claims.

## Learner-surface boundary

The learner sees a natural title, purpose, implementation requirements, a small
example, adjacent folded hints, starter code, fixture, public checks, and an
interpretation prompt. Never render Outcome, Requirement, or Target IDs, audit
kinds, exhaustive source maps, cell-role markers, or check-trace markers.
