# Practice audit metadata v3

Read this reference when creating, migrating, or validating a Notebook. The metadata is an internal authoring and provenance layer inside the same `.ipynb`; it is not a security boundary and never replaces learner-visible requirements.

Schema v3 connects five separate identities without recording mastery:

- artifact-level Curriculum targets and practice modality;
- TIL Outcomes and the targets each Outcome practises;
- stable source IDs for local or temporary external provenance;
- atomic Requirements and their exact source locations;
- exact learner-owned targets and execution evidence.

## Notebook metadata

Store the audit at `metadata.llm_research_lab.practice`:

```json
{
  "schema_version": 3,
  "artifact_kind": "standalone-practice",
  "scaffold_mode": "guided-fading",
  "practice_mode": "NOTEBOOK",
  "curriculum_targets": ["CC-DL-01"],
  "til": {
    "path": "til/2026/08/2026-08-24.md",
    "sha256": "<64 lowercase hex>"
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
      "til_location": "오늘의 학습 > 식별 문구",
      "action": "implement",
      "exercise_ids": ["E01"],
      "required_evidence": "구현, 공개 검사, 결과 해석",
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
      "claim": "반환된 `shape`는 Tensor shape를 일반 tuple로 기록해야 합니다.",
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
      "marker": "# TODO: Tensor 속성 네 가지를 채우세요",
      "placeholder": "raise NotImplementedError(\"Tensor 속성을 채우세요\")",
      "symbol": "tensor_card",
      "outcome_ids": ["O01"],
      "requirement_ids": ["C-E01-01"]
    }
  ]
}
```

`practice_mode` is `NOTEBOOK`, `BENCHMARK`, or `DATASET_PROJECT` for a local Notebook. These modes share the one-Notebook boundary but use different tasks: mechanisms and small calculations, controlled systems measurements, or data/validation/error-analysis work. External challenge and competition proposals are not local artifacts and therefore do not use this Notebook schema until an exact learner artifact is saved locally.

Artifact `curriculum_targets` contains the union of every Outcome's non-empty `curriculum_target_ids`. The links are relevance and provenance only; they do not change Curriculum coverage or establish mastery.

## Stable source records

Source IDs are contiguous `S001`, `S002`, and so on. A Requirement source location uses `source_id`, never a mutable path as its identity.

Local source kinds are `course-index`, `lesson`, `instructor-practice`, and `reference`; they retain exact repository-relative `path` and current SHA-256. Instructor practice also records `related_lesson` and `variant: basic | advanced | single`.

A temporary external source uses `kind: external-reference` and this identity:

```json
{
  "id": "S002",
  "kind": "external-reference",
  "provider": "Provider",
  "course": "Course",
  "offering_or_edition": "2026 offering",
  "artifact": "Lecture 1 notes",
  "url": "https://official.example/course/lecture-1",
  "final_url": "https://official.example/course/lecture-1.html",
  "retrieved_at": "2026-08-27T01:02:03Z",
  "media_type": "text/html",
  "sha256": "<retrieved bytes hash>",
  "scope": "Sections 1-3",
  "cache_path": "tmp/active-lesson-sources/<lesson-id>/<sha>.html",
  "receipt_path": "tmp/active-lesson-sources/<lesson-id>/<sha>.receipt.json"
}
```

The cache and receipt paths use the same exact content SHA under one valid
`tmp/active-lesson-sources/<lesson-id>/` directory. The receipt must say
`status: CACHED`, the same lesson ID, and `kind: primary`, and must match both
URLs, media type, retrieval time, paths, byte count, and hash.

Normal learner-state validation warns, but exits successfully, when this temporary cache is offline. `--strict-external-sources` requires the cache and receipt and checks every identity field and hash. Preserve the exact lesson cache through this strict practice-provenance check; delete only that lesson directory after the check succeeds. Never fabricate a receipt or durable coverage when the bytes are unavailable.

## Outcomes, Exercises, Requirements, and Learner Targets

- Outcome IDs are contiguous `O01`, `O02`, and so on. `action` is `implement`, `test`, `debug`, `interpret`, or `design`.
- Exercise IDs are contiguous and match learner-flow cells. `primary_outcome_id` is singular, `supporting_outcome_ids` may reuse connected knowledge, and `scaffold_stage` is `guided`, `partial`, or `independent`.
- Each Exercise has one to three learner targets. A migrated completed Exercise still lists them; learner-state validation permits resolved placeholders.
- Requirement IDs are contiguous within the Exercise. `kind` is `source-given`, `practice-given`, or `derive`; `owner` is `provided` or `learner`.
- A Requirement `claim` is one complete learner-visible behavior. A source-given Requirement has at least one exact `source_id`, `locator`, and normalized `anchor`.
- A practice-given Requirement needs a concrete rationale. If learner-owned, its `learner_outcome_ids` must be shared by every linked target.
- Requirement and learner target records reference each other in both directions within the same Exercise.
- Learner Target `kind` is `code`, `debug`, `prediction`, `design`, or `interpretation`. `marker` and exact unresolved `placeholder` occur in its implementation or reflection cell. Optional `symbol` names the top-level learner API.

## Cell and check metadata

Every cell retains a stable nbformat `id` and `metadata.llm_research_lab.practice.role`. There is exactly one `intro` and one `setup`, then one `brief`, `implementation`, `fixture`, `check`, and `reflection` per Exercise in that order. Required reflection answers have learner targets; an untracked reflection must explicitly be optional and not a completion condition.

The `check` cell records every `np.testing.*` or `torch.testing.*` call and expected-exception block with its AST ordinal, kind, fingerprint, `normal|edge|failure` category, and exactly one atomic Requirement ID. The trace must match code order. Do not expose these internal IDs or roles to the learner.

## Validation states

Default creation-ready validation requires unexecuted code cells and unresolved learner targets. `--learner-state` permits learner implementations, saved outputs, and resolved placeholders while retaining schema, source, disclosure, ownership, surface, and check-trace validation.

`--completion-ready` implies learner-state and additionally requires:

- every learner target placeholder, including required reflections, is resolved;
- setup and every implementation, fixture, and check cell has a positive saved execution count;
- each check ran after its Exercise's latest implementation and fixture;
- no code cell retains an error output or non-empty stderr stream;
- TIL and source provenance is current, including strict external receipts.

Completion does not create learner evidence by itself: the learner must still interpret the relevant state or output. Once the completion gate and that interpretation are confirmed, only the exact Notebook path is eligible for the path-limited completion commit.

Schema v2 is rejected with an explicit mechanical migration message. Use `scripts/migrate_practice_v2_to_v3.py` with an explicit Outcome-to-Curriculum mapping. The migration may change audit metadata only; cell source, output, execution count, stable ID, and learner answers must remain identical.
