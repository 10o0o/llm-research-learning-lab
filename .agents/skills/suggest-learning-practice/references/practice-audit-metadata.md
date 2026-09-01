# Practice audit metadata v5

Read this reference when creating or validating a practice Notebook. Metadata at
`metadata.llm_research_lab.practice` is an internal provenance and authoring
layer, not a mastery or progress record.

All newly generated artifacts use schema v5. Existing schema-v3 and schema-v4
Notebooks remain valid as `legacy-unclassified`; they receive no practice-layer,
implementation-depth, or milestone credit. Do not add v5 credit fields while
leaving an older schema number.

## Progression header

Every v5 artifact records:

```json
{
  "schema_version": 5,
  "artifact_kind": "standalone-practice",
  "scaffold_mode": "guided-fading",
  "practice_mode": "NOTEBOOK",
  "practice_layer": "MODULE_ASSIGNMENT",
  "implementation_depth": "I3_WORKFLOW",
  "lifecycle": "fresh",
  "milestone_id": "MA-SEQUENCE-01",
  "milestone_definition_sha256": "<hash of the current canonical Curriculum row>"
}
```

Allowed layers are `PRE_LAB`, `MODULE_ASSIGNMENT`, and `PHASE_CAPSTONE`.
Implementation depth is ordered from `I1_MECHANISM` through `I5_RESEARCH`.

- `PRE_LAB` is exactly `I1_MECHANISM`; both milestone fields are `null`.
- `MODULE_ASSIGNMENT` is at least `I3_WORKFLOW` and names one current `MA-*`
  Curriculum milestone.
- `PHASE_CAPSTONE` is exactly `I5_RESEARCH` and names one current `PC-*`
  Curriculum milestone.

`lifecycle` is `fresh` or `preserved_attempt`. A preserved attempt remains a
`PRE_LAB`, cannot claim a milestone, and is not retroactive evidence for a new
Curriculum target.

## Learning inputs

Schema v5 stores a non-empty `learning_inputs` list. IDs are contiguous `L001`,
`L002`, and so on. Exactly one input has role `primary`; the others are
`supporting`. One artifact uses captured cycles or finalized TILs, not a mixture.

### Captured cycle

```json
{
  "id": "L001",
  "role": "primary",
  "kind": "captured-cycle",
  "cycle_id": "2026-08-31-rnn-lstm-sequence-module-10",
  "lesson_id": "rnn-lstm-sequence-module-10",
  "primary_target": "CC-SEQ-01",
  "bridge_target": null,
  "concept_ids": ["C01", "C02"],
  "evidence_ids": ["E001", "E004"],
  "captured_session_sha256": "<64 lowercase hex>"
}
```

The validator reads cursor schema v2 and locates the cycle's immutable
`captured_session`. That object contains exactly `schema_version`,
`cycle_id`, `lesson_id`, `primary_target`, `bridge_target`, `handoff_sha256`,
`concepts`, `learner_evidence`, `learner_evidence_sha256`,
`source_provenance`, and `projection_sha256`. Its `projection_sha256` hashes the
canonical object without that self-hash field. The input hash and all declared
identities must match this projection. Mutable top-level cycle fields and the
live handoff are not v5 provenance.

Outcome concept and evidence references are input-namespaced, for example
`L001:C01` and `L001:E004`. This prevents collisions when a cumulative artifact
uses more than one captured cycle.

### Exact finalized TIL

```json
{
  "id": "L001",
  "role": "primary",
  "kind": "finalized-til",
  "path": "til/2026/08/2026-08-28.md",
  "sha256": "<64 lowercase hex>"
}
```

This form names an exact validated dated TIL. Its Outcomes retain exact
`til_location` values. Never infer the latest TIL.

## Workflow and research contracts

A module assignment or capstone records a bounded `workflow_contract`:

```json
{
  "data_contract": "fixed delayed-information train and evaluation splits",
  "component_contract": "ManualRNNCell, ManualLSTMCell, and SequenceClassifier",
  "loss_contract": "cross-entropy from sequence-level logits",
  "training_contract": "learner-owned zero_grad to backward to step loop",
  "evaluation_contract": "same split, seed, budget, and metric for all models",
  "stage_cell_ids": {
    "data": ["e01-fixture", "e01-check"],
    "model": ["e02-implementation"],
    "loss": ["e03-implementation"],
    "train": ["e04-implementation"],
    "evaluation": ["e05-fixture", "e05-check"]
  }
}
```

All stage IDs resolve to code cells with implementation, fixture, or check
roles. Each stage has at least one stage-exclusive learner-visible code cell;
the data stage includes a deterministic fixture and check, while model, loss,
and train each include a distinct learner-owned code target whose reciprocal
Requirement matches that stage contract. Their code skeletons expose a
component definition/call boundary, a loss computation boundary, and an update
or optimization control/data-flow boundary respectively. Training and
evaluation each link a different declared result cell, and learner
interpretation targets link both. Repeating one component cell under several
stage names, putting five workflow sentences beside one tensor exercise, or
using five empty TODO shells is invalid.
Module-assignment Outcomes include `implement`, `interpret`, and at least one of
`test` or `debug`.

A phase capstone additionally records non-empty `research_contract` fields for
`hypothesis`, `baseline`, `control_or_ablation`, `error_analysis`,
`reproducibility`, and `limitations`. Its Outcomes include `implement`, `debug`,
`interpret`, and `design`. Learner-owned requirements and design or
interpretation targets ground `baseline`, `control_or_ablation`, and
`error_analysis` in distinct declared result cells from distinct learner-visible
exercises. Reusing one output for all three labels is not research evidence.

## Prior-practice evidence

`prior_practice_evidence` is always a list. A capstone needs at least two unique
metadata-v5 module assignments:

```json
{
  "id": "P001",
  "path": "practice/deep-learning/rnn-lstm-sequence-modeling.ipynb",
  "sha256": "<current artifact hash>",
  "commit_sha": "<exact completion commit>",
  "practice_layer": "MODULE_ASSIGNMENT",
  "implementation_depth": "I3_WORKFLOW",
  "milestone_id": "MA-SEQUENCE-01"
}
```

The path, current hash, and declared layer/depth/milestone must match the
referenced Notebook. Its completion commit must exist, contain the declared
Notebook bytes, and change exactly that one Notebook path—no second practice
artifact or unrelated file. A pre-lab cannot claim cumulative prior-practice
evidence.

## Result and interpretation links

`result_cell_ids` is a unique list of fixture or check cell IDs whose outputs
are interpreted. Module assignments and capstones require at least one. Every
required interpretation target has its own non-empty `result_cell_ids` subset.
Creation keeps code unexecuted; `--completion-ready` requires actual non-error
output in every declared result cell.

## Creation review

Fresh v5 practice records one or two `creation_reviews`. A preserved migration
may keep an empty list because no review may be invented.

Every code target in a fresh v5 artifact declares its learner-owned span:

```json
{
  "kind": "code",
  "symbol": "SequenceClassifier.forward",
  "editable_region": {
    "start_marker": "# 학습자 편집 구간 시작 — 경계 주석은 남겨 두세요.",
    "end_marker": "# 학습자 편집 구간 끝"
  }
}
```

Each boundary is a distinct, non-empty whole-line marker occurring exactly once
in the target cell. Start precedes end, both are inside the declared symbol, and
regions in one cell do not overlap. Schema-v3/v4 artifacts and schema-v5
`preserved_attempt` artifacts are exempt so migration remains cell-exact.

```json
{
  "iteration": 1,
  "reviewer_id": "independent-reviewer",
  "reviewed_at": "2026-08-31T12:00:00+09:00",
  "learner_surface_verdict": "pass",
  "metadata_verdict": "pass",
  "verdict": "pass",
  "contract_sha256": "<reviewed practice contract hash>",
  "recheck_of": null
}
```

The first reviewer inspects only the rendered learner surface, then the metadata
and source fidelity. A pass requires both surfaces to pass. With the brief
folded, the implementation cell must still disclose inputs, outputs, invariants,
and the next semantic step without offering complete code to copy. Static
validation does not infer that quality from line counts or fixed wording. One
repair and one second fresh reviewer are the maximum; iteration 2 has
`recheck_of: 1`.

The contract hash excludes learner-editable implementation/reflection bodies,
execution counts, outputs, and the review records themselves, but includes the
briefs, fixtures, checks, topology, and all other audit metadata. For fresh-v5
code targets it masks every complete line strictly between the editable-region
markers. The signature, `Local contract`, both markers, and any provided suffix,
postlude, return assembly, or later scaffold remain hashed. Therefore deleting
a TODO and replacing one placeholder with multiple learner statements does not
stale a review; changing the public API, local contract, boundaries, or provided
suffix does. Legacy and preserved targets retain their prior compatibility
behavior.

## Existing graph metadata

Schema v5 retains the schema-v4 source, Outcome, Exercise, Requirement, learner
target, cell-role, and check-observable graph:

- Outcome actions are `implement`, `test`, `debug`, `interpret`, or `design`.
- Each Exercise has one primary Outcome, optional supporting Outcomes, one
  scaffold stage, and one to three learner targets.
- Requirements are atomic learner-visible contracts with exact source anchors.
- Requirements and learner targets reference each other in both directions.
- Learner-target kinds are `code`, `debug`, `prediction`, `design`, and
  `interpretation`; every required reflection is a learner target.
- Every cell has a stable nbformat ID and internal role. There is exactly one
  setup cell followed by adjacent brief, implementation, fixture, check, and
  reflection cells for each Exercise.

The artifact-level Curriculum targets are the exact Outcome target union. For
captured cycles they also equal the primary/bridge target union across inputs.
These are relevance and provenance links, not mastery claims.

## Validation and migration

Creation validation requires a fresh reviewed artifact with unexecuted code and
unresolved learner targets. Learner-state validation permits saved learner work
and output while retaining structure and provenance. Completion requires every
learner target and required reflection resolved; setup, implementation, fixture,
and checker cells executed in current order; no error output; current strict
input/source/milestone provenance; and learner-authored result interpretation.

`migrate_practice_v4_to_v5.py` is a conservative metadata-only migration. It
classifies one v4 artifact as `PRE_LAB / I1_MECHANISM / preserved_attempt`, sets
both milestone fields to `null`, preserves `.cells` exactly, and writes
atomically. A v4 lesson session migrates only when its identity matches cursor
v2's immutable captured session. Running the migration again is a no-op. Do not
bulk-migrate legacy artifacts or use migration to grant milestone credit.

When a captured attempt has been superseded, the migration binds the lesson
source to `tmp/lesson-attempts/<cycle-id>/active-lesson-handoff.md`. For each
captured external source, `cache_path` and `receipt_path` name the archived
bytes under that attempt's `source-cache/`, while `captured_path` and
`captured_receipt_path` preserve the immutable active-cache identity stored in
the captured session and archived receipt. Learner-state validation accepts
this equivalence only for a `preserved_attempt` backed by exactly one captured
cycle, only in the archive owned by that source's input cycle, and only when
the symlink-free archive path, content SHA-256, receipt identity, and byte count
all match. Re-running the
migration may repair these bindings on an already-migrated preserved attempt;
it leaves every fresh v5 artifact byte-for-byte unchanged.

After an independent review actually finishes, record it without touching
learner cells:

```bash
uv run python .agents/skills/suggest-learning-practice/scripts/record_practice_creation_review.py \
  practice/<area>/<topic>.ipynb --repo-root . \
  --reviewer-id <independent-reviewer> --reviewed-at <RFC3339> \
  --learner-surface-verdict pass --metadata-verdict pass
```
