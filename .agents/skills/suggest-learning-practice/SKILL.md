---
name: suggest-learning-practice
description: Decide and execute one authentic practice modality from either a completed schema-v9 lesson session or an exact finalized TIL, create one guided-fading metadata-v4 Notebook, propose a verified external challenge or competition, or coach an exact saved attempt. Use after CAPTURE_SESSION in the daily full flow or for legacy TIL-based practice. Do not perform learner work, submit externally, infer an input, or treat platform/checker success without interpretation as completion.
---

# Decide and Run Authentic Practice

Read the [v9 lesson contract](../coach-llm-research-study/references/lesson-handoff.md),
[practice design](references/practice-design.md), and
[practice metadata v4](references/practice-audit-metadata.md) before creation.

## Decide first

Return both axes:

- `practice_action`: `SESSION_REPAIR_REQUIRED | TIL_REPAIR_REQUIRED | CONTINUE_EXISTING_PRACTICE | CREATE_LOCAL_PRACTICE | PROPOSE_EXTERNAL_PRACTICE | NO_EXTRA_PRACTICE`;
- `practice_mode`: `NOTEBOOK | BENCHMARK | DATASET_PROJECT | EXTERNAL_CHALLENGE | EXTERNAL_COMPETITION | NONE`.

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

## Resolve one exact input

Creation accepts exactly one of:

- `lesson-session`: the active cycle ID, completed handoff path/hash, exact
  primary and bridge, concept IDs/hash, and confirmed evidence IDs/hash;
- `finalized-til`: one named validated `til/YYYY/MM/YYYY-MM-DD.md` path/hash.

Schema v4 stores this union under `learning_input`. Session Outcomes link
`concept_ids`, `evidence_ids`, and one performance action. Finalized-TIL
Outcomes retain exact `til_location`. Existing schema-v3 notebooks remain valid
without migration; all new artifacts use v4.

Return `SESSION_REPAIR_REQUIRED` for missing or drifted session input and
`TIL_REPAIR_REQUIRED` for a broken legacy TIL input. A live handoff/hash is
required for creation and strict completion; learner-state validation may warn
when a cleaned-up handoff or external cache is offline.

## Create or continue one artifact

Local modes use exactly one `practice/<area>/<topic>.ipynb`. Keep one unexecuted
setup cell, then adjacent brief, learner-owned implementation, deterministic
fixture, `check_e##()`, and required reflection cells. Disclose every fixed
contract before the TODO, keep internal IDs in metadata only, and put folded
hints next to the relevant blank. Do not overwrite learner work or include a
complete answer.

Validate and obtain one fresh read-only learner-surface/source-fidelity review:

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
