# Practice design contract

Use this reference to design and independently review generated practice. The
research motivates the sequence; it does not justify inflating every lesson
into a large project.

## Learning-design basis

- **Authentic whole task**: 4C/ID organizes complex-skill learning around
  meaningful whole tasks, supported information, procedural information, and
  part-task practice. Here that means shrinking one real ML workflow while
  preserving its input contract, core implementation, tests, failure
  diagnosis, and interpretation. It does not mean adding production scale.
  See [4C/ID in the context of instructional design and the learning
  sciences](https://research.ou.nl/en/publications/4cid-in-the-context-of-instructional-design-and-the-learning-scie/).
- **Deliberate practice**: practice needs a concrete performance target,
  effortful learner execution, observable error, and feedback focused on
  improvement. Repetition alone and a generic project do not meet this bar.
  See [Ericsson, Krampe, and Tesch-Römer
  (1993)](https://doi.org/10.1037/0033-295X.100.3.363). Do not turn this into a
  “10,000 hours” claim or claim practice explains all expertise.
- **Retrieval practice**: ask for a prediction or reconstruction before showing
  setup-specific cues. Retrieval can strengthen later retention more than
  restudy alone, so an already well-written TIL still benefits from a blank
  implementation attempt. See [Roediger and Karpicke
  (2006)](https://doi.org/10.1111/j.1467-9280.2006.01693.x).
- **Fading**: progress from a tiny analogous trace to pseudocode and only then
  a minimal API skeleton. Never jump directly from no help to a full answer.
  See [Renkl et al. (2002)](https://eric.ed.gov/?id=EJ658398).
- **Avoid split attention**: put the hint beside the TODO it explains. A global
  hint appendix forces the learner to alternate between separate information
  sources and adds irrelevant search work. See [Chandler and Sweller
  (1992)](https://doi.org/10.1111/j.2044-8279.1992.tb01017.x).

## Whole-task sizing

Keep the smallest workflow that still exposes the professional boundary:

1. deterministic input or fixture;
2. explicit public contract;
3. learner-owned core logic;
4. normal, edge, and failure observation;
5. diagnosis from the actual failure;
6. explanation of system meaning and limitation.

For a Tensor lesson this might be a boundary function plus tests, not a model
service. For a training-loop lesson it might be `train_step`, validation, and
checkpoint selection on a fixed CPU batch, not distributed training.

## Standalone specification boundary

The generated Notebook is the learner's complete task interface. Linked TIL,
lesson, and instructor-practice files establish provenance and fidelity but are
not prerequisites for discovering a threshold, token, representation, axis,
boundary convention, aggregation, or failure rule.

Keep two distinct layers inside the same `.ipynb`:

- **Learner surface**: natural purpose, exact implementation requirements,
  small examples, starter code, fixtures, checks, hints, and interpretation.
- **Audit metadata**: the exact completed lesson session or finalized TIL,
  source hashes, Outcome coverage, Requirement kinds, cell roles, and assertion
  traceability under `metadata.llm_research_lab.practice`.

Read [practice audit metadata v5](practice-audit-metadata.md) when creating or
validating a Notebook. The internal IDs and audit kinds must never be rendered
in Markdown or code. Hiding an ID does not hide its requirement: every fixed
value and convention still appears naturally before the learner implementation.
Do not make a source link, hint, fixture output, or failing check the first place
an arbitrary choice becomes visible.

## Cumulative progression

Choose one progression layer before designing exercises:

- `PRE_LAB / I1_MECHANISM` removes one concrete mechanism blocker. It has no
  milestone ID and cannot satisfy a module or phase milestone.
- `MODULE_ASSIGNMENT / I3_WORKFLOW` or deeper implements at least one reusable
  component and a bounded data → model → loss → train/eval workflow. Its
  Outcomes include `implement`, `interpret`, and at least one of `test` or
  `debug`.
- `PHASE_CAPSTONE / I5_RESEARCH` integrates at least two exact completed module
  artifacts. It adds a baseline, controlled comparison or ablation, error
  analysis, reproducibility conditions, and limitations.

Prefer a ready phase capstone over a module assignment and a ready module
assignment over a pre-lab. If no concrete blocker remains and the cumulative
assignment is not ready, use `DEFER_TO_MILESTONE` instead of generating another
small Notebook. The deferred ID must be a well-formed, case-sensitive `MA-*` or
`PC-*` ID with exactly one current row in `CURRICULUM.md`; a plausible-looking
or future prose label is not enough. Apply the same exact-row check to ready
module and capstone IDs, with `MA-*` restricted to module assignments and
`PC-*` restricted to phase capstones.

This is a semantic boundary, not merely a formatting rule. If multiple sensible
implementations fit the prose and only an undisclosed convention passes, the
artifact fails review even when all structural checks pass. Conversely, a
derived numeric answer need not be printed in the specification when the visible
fixture and contract determine it.

Put exactly one unexecuted cell with the internal `setup` role before the first
Exercise. It contains only dependencies, shared types, and non-solution helpers.
Use a natural learner-facing comment if one is helpful; do not expose the role
as `# setup-check`. The artifact validator executes this cell from the
repository root.

## Choose the smallest useful artifact boundary

Choose the modality before the artifact. Use `NOTEBOOK` for mathematics,
Tensor mechanics, model mechanisms, and small implementations; `BENCHMARK` for
latency, throughput, memory, batching, and KV-cache measurements; and
`DATASET_PROJECT` for data handling, validation, metrics, and error analysis.
All three local modes keep the one-Notebook boundary but must use mode-specific
tasks and metadata. A verified external challenge or competition is a proposal,
not a local Notebook, and requires approval before account access,
participation, or submission. If the current item or its material value cannot
be verified, keep the decision typed and use the corresponding local fallback
instead of emitting an exception or an unverified external name.

Create exactly one `practice/<area>/<topic>.ipynb` for each generated practice.
Use exercises inside that Notebook for every part of the whole task, including
small training, validation, checkpoint-selection, shape, and output-contract
work. A production-looking directory, import boundary, reload loop, or pytest
process is not useful authenticity for this learning flow; it creates
bookkeeping the learner did not ask to practise. A reusable multi-file project
is a different, explicitly requested deliverable.

Before writing those roles, compare every mapped instructor-practice variant.
Treat a sound starter/TODO boundary as the default scaffold: preserve the
provided API and routine code, adapt it only enough to fit the single Notebook,
and use the solution only for specification auditing and an ephemeral reference
run. When a basic variant has no concrete starter, recover the public boundary
from the advanced variant without copying its completed core.

Within a Notebook-only exercise, keep five learner-flow roles adjacent:

1. a brief with purpose, requirements, a small example, and nearby hints;
2. an implementation cell with provided scaffold and explicit unresolved
   learner targets;
3. a deterministic observation fixture;
4. a self-contained `check_e01()` with normal, edge, and failure observations;
5. the learner's interpretation prompt.

Keep the deterministic fixture and normal, edge, and failure checks beside the
exercise. This prevents split attention and lets the learner follow one short
loop: implement, run the fixture, run `check_e##()`, and interpret the resulting
state. Cell roles and check mappings live in metadata, not source markers. Do
not create a hidden source module or test file.

## Guided-fading ownership

Choose the scaffold by evidence and by the concept's role:

- `guided`: provide the public API, validation, assembly, and a narrow blank at
  the decisive operation;
- `partial`: provide the boundary and repeated plumbing, leaving a familiar
  multi-step core blank;
- `independent`: provide only the public contract and deterministic fixture
  when the learner has already demonstrated the mechanism.

Use one primary concept and at most three learner targets per Exercise. Do not
turn return-token memorization, dict construction, repeated shape guards, or a
generator-created helper into learner work unless the exact lesson session or
finalized TIL studies that operation. A design or interpretation target may be
a structured written response and does not need an artificial callable.

Every required written response is a learner target too. If an Exercise has
already reached three targets, any additional reflection must be clearly
optional and say that it is not needed for completion; an imperative untracked
prompt is hidden workload and fails review.

The metadata ownership decision is part of review. A `practice-given`
Requirement defaults to `provided`; making it learner-owned requires a direct
link to a named session or TIL Outcome and a concrete reason. Fading removes
support for later Exercises, not required task information.

## Coverage-map review

For every major session or TIL Outcome, ask:

1. Is the cited session concept/evidence relation or TIL location exact enough
   to find the learner's demonstrated statement?
2. Does the action test performance rather than recognition?
3. Is required evidence observable in code, a test, a trace, or an interpreted
   result?
4. Is the outcome naturally part of this whole task? If not, split only when a
   separate environment or interpretation is necessary.
5. Does prior evidence include independent execution and interpretation? A
   correct written explanation alone does not remove the outcome.

## Artifact review rubric

A fresh reviewer returns `pass` only when all are true:

- the exact captured session or finalized TIL is valid and all major Outcomes
  are represented;
- the v5 layer, implementation depth, and milestone definition are current;
- a captured-cycle input matches the cursor-v2 immutable captured session and
  does not depend on a live handoff;
- the practice modality matches the evidence the selected Curriculum target
  requires, and every Outcome declares a relevant target;
- exact lesson links resolve and instructor practice comes from an explicit
  `INDEX.md` mapping;
- each learner target is a genuine blank core operation or response while
  routine scaffold is already usable;
- the Notebook alone discloses every fixed requirement needed by its TODOs and
  checks, while source links remain optional provenance;
- each internal Requirement points to natural learner-visible prose before the
  implementation, and every check has a same-exercise metadata trace with no
  hidden test-only convention;
- source-specific policies are labeled as local rather than universal, and
  practice-added rules are useful rather than arbitrary busywork;
- tests cover meaningful normal, edge, and failure behavior without inventing
  an error boundary merely to fill a category;
- each exercise begins with a natural purpose and exact requirements and ends
  with failure diagnosis and interpretation;
- progressive hints are folded and adjacent to the relevant implementation;
- code cells are unexecuted and contain no fabricated output;
- setup and conventions remain smaller than the concept being learned;
- the single Notebook has adjacent implementation, fixture, and local
  normal/edge/failure checks;
- the learner surface contains no coverage table, internal ID, audit kind,
  source-audit prose, or cell-role/test-trace marker;
- each Exercise has one primary concept and no more than three learner targets;
- initial execution fails only at explicit learner-owned unresolved boundaries.
- module assignments expose a real data → model → loss → train/eval workflow,
  and phase capstones expose the required baseline/comparison/error-analysis
  research cycle with prior module evidence;
- every workflow stage owns at least one learner-visible code cell not reused
  as every other stage, data owns a deterministic fixture and check,
  model/loss/train own distinct learner code targets tied to their Requirements
  and expose their component, computation, and update/control-flow boundaries,
  and distinct training and evaluation result cells are interpreted;
- capstone baseline, controlled comparison or ablation, and error analysis are
  grounded in structurally distinct learner-visible result cells rather than
  three metadata labels over one observation;
- every required interpretation names the result cell or cells it interprets;
- one fresh independent review passes both the learner surface and the metadata
  inspection, with at most one repair and one second reviewer.

The completion gate is separate from creation review. `--completion-ready`
requires every learner target and required reflection to be resolved, setup,
implementation, fixture, and checker cells to have actually executed in the
current order, no error output, and current session-or-TIL/source provenance. A green
checker without the learner's interpretation is still not learning evidence.

The reviewer first receives only the rendered learner surface and performs a
specification inversion: for every public assertion or expected exception, it
identifies the exact earlier sentence that determines the expected behavior.
Any required guess is blocking. The same pass checks natural commercial-quality
presentation, absence of audit leakage, the boundary between provided scaffold
and learner work, and concept overload. Only then does the reviewer inspect
metadata and sources for coverage, anchor fidelity, ownership, and check
traceability. The reviewer identifies concrete blocking findings, not stylistic
preferences.
One revision and one second fresh review are the maximum. Never replace an
unavailable independent reviewer with the author's self-approval.
