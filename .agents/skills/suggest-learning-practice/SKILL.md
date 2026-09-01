---
name: suggest-learning-practice
description: Decide and execute one authentic practice modality from captured schema-v10 lesson cycles or exact finalized TILs, create one guided-fading metadata-v5 pre-lab, module assignment, or phase capstone, defer practice to a named milestone, propose a verified external item, or coach an exact saved attempt. Use after CAPTURE_SESSION in the daily full flow or for legacy TIL-based practice. Do not perform learner work, submit externally, infer an input, grant milestone credit to legacy artifacts, or treat platform/checker success without interpretation as completion.
---

# Decide and Run Authentic Practice

Read the [v10 lesson contract](../coach-llm-research-study/references/lesson-handoff.md),
[practice design](references/practice-design.md), and
[practice metadata v5](references/practice-audit-metadata.md) before creation.

## Decide first

Return both axes:

- `practice_action`: `SESSION_REPAIR_REQUIRED | TIL_REPAIR_REQUIRED | CONTINUE_EXISTING_PRACTICE | CREATE_LOCAL_PRACTICE | PROPOSE_EXTERNAL_PRACTICE | DEFER_TO_MILESTONE | NO_EXTRA_PRACTICE`;
- `practice_mode`: `NOTEBOOK | BENCHMARK | DATASET_PROJECT | EXTERNAL_CHALLENGE | EXTERNAL_COMPETITION | NONE`.
- `practice_layer`: `PRE_LAB | MODULE_ASSIGNMENT | PHASE_CAPSTONE | NONE`;
- `implementation_depth`: `I1_MECHANISM | I2_COMPONENT | I3_WORKFLOW | I4_EXPERIMENT | I5_RESEARCH | I0_NONE`, plus an exact milestone ID when applicable.

Use `scripts/route_practice.py`, then verify exact evidence and artifact state.

- math, Tensor mechanics, small mechanisms or implementations → `NOTEBOOK`;
- latency, throughput, memory, batching or KV cache → `BENCHMARK`;
- data, validation, metrics or error analysis → `DATASET_PROJECT`, or a current
  valuable competition;
- short algorithm or API contract → a verified external challenge;
- equivalent implementation, execution and interpretation evidence, or no
  practice-capable outcome → `NONE`.

External items must be verified on their current official page at recommendation
time. Account access, participation, and submission need separate approval.
Store a Kaggle execution Notebook under `practice/`; store short external
submission code under `challenges/`. A platform pass is never enough without
the learner's result interpretation.

Choose the deepest ready cumulative layer before a smaller one:

1. a ready `PHASE_CAPSTONE` at `I5_RESEARCH`;
2. a ready `MODULE_ASSIGNMENT` at `I3_WORKFLOW` or deeper;
3. a `PRE_LAB / I1_MECHANISM` only for one concrete concept blocker;
4. otherwise `DEFER_TO_MILESTONE` with an exact later `MA-*` or `PC-*` ID
   that occurs exactly once in the current `CURRICULUM.md` milestone table.

Every supplied module, capstone, or deferred milestone ID must occur exactly
once in that current table; module selections use `MA-*` and capstone selections
use `PC-*`.

`PRE_LAB` never has a milestone ID and never earns milestone credit. Do not
create another micro-Notebook merely because a lesson completed.

## Resolve exact same-kind inputs

Schema v5 accepts one or more same-kind `learning_inputs`, with exactly one
`primary` and the rest `supporting`:

- `captured-cycle`: the cycle ID and exact `captured_session_sha256`, targets,
  concept IDs, and confirmed evidence IDs from cursor schema v2;
- `finalized-til`: one named validated `til/YYYY/MM/YYYY-MM-DD.md` path/hash.

Captured-cycle Outcomes use input-namespaced `concept_ids` and `evidence_ids`
and one performance action. Finalized-TIL Outcomes retain exact `til_location`.
Validate the cursor's immutable `captured_session` projection and its self-hash;
never reopen the live handoff for v5 provenance. Existing schema-v3/v4
Notebooks remain valid as `legacy-unclassified` without milestone credit. All
new artifacts use v5.

Return `SESSION_REPAIR_REQUIRED` for missing or drifted captured input and
`TIL_REPAIR_REQUIRED` for a broken legacy TIL input. A live handoff/hash is
only a v4 legacy requirement; v5 creation and strict completion use the cursor
capture. Learner-state validation may warn when deliberate operational cleanup
makes a captured cycle or external cache unavailable.

## Create or continue one artifact

Local modes use exactly one `practice/<area>/<topic>.ipynb`. Keep one unexecuted
setup cell, then adjacent brief, learner-owned implementation, deterministic
fixture, `check_e##()`, and required reflection cells. Disclose every fixed
contract before the TODO, keep internal IDs in metadata only, and put folded
hints next to the relevant blank. Do not overwrite learner work or include a
complete answer.

Put a concise `Local contract` comment block immediately above each code
target's editable region. Even with the brief folded, that implementation cell
must state the input and output roles, shapes or other invariants, and the next
semantic step. It must not disclose a complete right-hand side or loop that can
be copied as the answer. Fresh schema-v5 code targets declare non-overlapping
`editable_region.start_marker` and `end_marker` boundaries; preserve those
markers while learner code between them grows from one placeholder into
multiple statements. Static validation owns only boundary structure. The fresh
learner-surface reviewer owns contract sufficiency and answer-leakage judgment.

Every v5 artifact records result cells and any required interpretation's exact
result-cell links. A `MODULE_ASSIGNMENT` contains a reusable component plus a
bounded data → model → loss → train/eval workflow. Each workflow stage has a
stage-exclusive learner-visible code cell, and training and evaluation have
distinct observed result cells. A `PHASE_CAPSTONE` references at least two exact
completed module artifacts whose completion commits each change only that one
Notebook. It adds learner-visible, structurally distinct baseline, controlled
comparison or ablation, and error-analysis results plus reproducibility
conditions and limitations.

Validate and obtain one fresh independent read-only learner-surface then
metadata/source-fidelity review. Record at most one repair and one second fresh
review in `creation_reviews`:

```bash
python3 .agents/skills/suggest-learning-practice/scripts/validate_practice_artifact.py \
  practice/<area>/<topic>.ipynb
```

During an attempt, inspect the exact saved path and actual failure, address one
blocker at a time, and leave learner-owned implementation to the learner.
Completion requires `--completion-ready`, current source/session provenance,
actual setup/implementation/fixture/check execution order, no error output,
resolved reflections, and learner interpretation. In an authorized full-day
flow, commit only that exact completed path as
`practice: complete <artifact-stem>`; creation remains uncommitted.

Use `scripts/migrate_practice_v4_to_v5.py` only to classify an existing v4
attempt conservatively as `PRE_LAB / I1_MECHANISM / preserved_attempt`. It is
atomic, preserves `.cells`, grants no milestone, and never fabricates a review.
For a superseded captured attempt it also binds the old handoff and external
source identities to their exact files and receipts under
`tmp/lesson-attempts/<cycle-id>/`. The captured form owns exactly one input
cycle; archive bindings cannot cross cycles or use symlinks. Re-running the
migration may repair only those bindings on an already-v5 preserved attempt.
It never rewrites a fresh v5 artifact.
After an independent review actually occurs, use
`scripts/record_practice_creation_review.py` to record its two surface verdicts
and current contract hash without changing learner cells.
