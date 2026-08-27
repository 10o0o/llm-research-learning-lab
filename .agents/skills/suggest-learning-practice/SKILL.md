---
name: suggest-learning-practice
description: Decide the practice action and modality for one selected Curriculum target and its exact finalized TIL, then create one mode-specific guided-fading local Notebook, propose one verified external challenge or competition, continue a directly linked artifact, or return no extra practice. Also coach an attempt from an exact practice path and real failure output. Do not infer the latest TIL or artifact, repair an incomplete TIL, perform learner work, submit externally, reveal a full solution, or treat green checks as mastery.
---

# Build and Coach Authentic Practice

Practice turns the major outcomes of a complete daily TIL into performance. It
is not limited to gaps or misconceptions. A concept the learner can explain is
still a practice target when they have not independently recalled,
implemented, tested, debugged, transferred, or interpreted it.

Read [the practice design contract](references/practice-design.md) completely
before generating or reviewing an artifact. In creation mode also read
[practice audit metadata v3](references/practice-audit-metadata.md) completely.
Use exactly one of the modes below.

## Decide before executing

Return both axes before creating or proposing anything:

- `practice_action`: `TIL_REPAIR_REQUIRED`, `CONTINUE_EXISTING_PRACTICE`, `CREATE_LOCAL_PRACTICE`, `PROPOSE_EXTERNAL_PRACTICE`, or `NO_EXTRA_PRACTICE`;
- `practice_mode`: `NOTEBOOK`, `BENCHMARK`, `DATASET_PROJECT`, `EXTERNAL_CHALLENGE`, `EXTERNAL_COMPETITION`, or `NONE`.

Use `scripts/route_practice.py` as the deterministic baseline, then verify the exact target, TIL outcomes, learner evidence, and artifact state. Choose modality by the performance evidence needed:

- mathematics, Tensor mechanics, small algorithms, or model mechanisms -> `NOTEBOOK`;
- latency, throughput, memory, batching, KV cache, or quantization measurements -> `BENCHMARK`;
- data handling, validation, metrics, or error analysis -> `DATASET_PROJECT`, or a genuinely valuable current competition;
- a short algorithm or API contract with a useful verified platform item -> `EXTERNAL_CHALLENGE`;
- equivalent independent implementation, execution, and interpretation evidence, or no practice-capable outcome -> `NONE`.

Local modes all preserve the one-Notebook boundary; their scenario, fixtures, measurements, and metadata must reflect the selected modality. Search and verify the current exact item before naming an external challenge or competition. Account access, participation, and submission require approval and are never implied by practice planning or the full learning flow.
If no exact current external item has material value, return a typed local
fallback (`NOTEBOOK` for a short algorithm/API or `DATASET_PROJECT` for data and
evaluation) instead of raising an error or naming an unverified item. When an
external proposal is selected, state the approval scope as account access,
participation, and submission; the read-only proposal itself does not perform
any of them.

## Resolve the mode and exact input

- **Creation mode** requires exactly one named finalized
  `til/YYYY/MM/YYYY-MM-DD.md`.
- **Attempt-feedback mode** requires exactly one named artifact under `practice/`.
- Never infer today's, latest, or most likely file. Never accept
  `til/today.md` for creation. If the user says only “continue,” resume an exact
  practice artifact already established in the current conversation; otherwise
  ask for its path. This resume phrase does not authorize a commit.
- A decision-only request remains read-only. Creation mode otherwise authorizes exactly one unexecuted Notebook-only artifact. In an explicitly authorized full learning flow, the exact newly finalized TIL is the creation input and the selected local artifact is generated immediately without another prompt; it remains uncommitted.

## Creation mode: establish the complete practice input

1. Read the exact TIL and validate it:

   ```bash
   python3 .agents/skills/save-today-til/scripts/validate_til.py \
     til/YYYY/MM/YYYY-MM-DD.md
   ```

2. Require a resolvable exact source link for source-based study. Read every
   linked source needed to interpret the TIL. Do not guess from filenames,
   dates, lesson numbers, nearby files, or the course directory.
3. Respect the coach completeness gate. If the TIL validator or a known coach
   completeness review failed, return **TIL 수정 우선** and create nothing. If
   a major claim is visibly unsupported or an actual studied boundary is
   recoverable and missing, ask the coach to repair it before practice. Do not
   silently complete the TIL yourself.
4. For each exact linked course lesson, open that course's `INDEX.md`. Use an
   instructor practice only when a row explicitly maps its `Related lesson
   path` to that exact lesson. Validate the index first:

   ```bash
   python3 .agents/skills/suggest-learning-practice/scripts/validate_practice_index.py \
     materials/private/<course>/INDEX.md
   ```

   Read the mapped `basic` and `advanced` variants when both exist. Audit their
   starter, TODO, fixture, check, and solution boundaries before designing the
   generated Exercise. Preserve or minimally adapt a sound instructor starter
   before inventing a new public API. Use solutions only to verify the public
   specification and in an ephemeral reference run; never copy learner-core
   answers or claimed output. Do not load an unlisted, neighboring, or
   same-numbered practice. Instructor practice is source scaffolding, not
   learner evidence, and remains unchanged.
5. Search `practice/` for learner artifacts that explicitly link the same TIL
   outcomes. Do not overwrite executed work, answers, outputs, or reflections.

## Convert the whole TIL into practice outcomes

Identify the TIL's major learning outcomes, not only its gaps. A major outcome
is a mechanism, calculation, Shape or dtype contract, implementation flow,
debugging rule, evaluation judgment, or limitation that materially represents
what the learner studied. Do not turn incidental prose into busywork.

Create this map in the Notebook's internal practice metadata. It must not appear
in learner-facing cells. The map plus explicitly cited equivalent completed
learner evidence must cover the TIL's major outcomes:

```text
Outcome ID | TIL location | Practice action | Artifact/Exercise | Required evidence
```

- IDs are contiguous `O01`, `O02`, and so on.
- `TIL location` names an exact heading and identifying phrase.
- `Practice action` is exactly `implement`, `test`, `debug`, `interpret`, or
  `design`.
- Every major TIL outcome without equivalent completed evidence maps to at
  least one exercise. Combine outcomes when one realistic flow naturally
  exercises them together.
- A conceptual outcome may use prediction, API or experiment design, failure
  diagnosis, or output interpretation; do not force meaningless coding.
- Already explaining an outcome is not grounds to omit it. Equivalent prior
  evidence must include independent implementation or execution **and**
  interpretation of the relevant state or result.

Choose exactly one result:

- `TIL_REPAIR_REQUIRED`: validation or the coach completeness gate failed.
- `CONTINUE_EXISTING_PRACTICE`: an unfinished learner artifact already exercises the
  same outcomes; name that exact path and do not replace it.
- `CREATE_LOCAL_PRACTICE`: the normal local result, including when evidence is thin. Begin
  with the smallest Core task instead of withholding practice.
- `PROPOSE_EXTERNAL_PRACTICE`: one exact current external challenge or competition has material value for the selected evidence. Await approval before account access, participation, or submission.
- `NO_EXTRA_PRACTICE`: exceptional; every major outcome already has equivalent
  implemented, executed, and interpreted evidence, or there is no
  practice-capable learning outcome. Cite that evidence.

## Select depth and one-Notebook boundary

- **Core**: recall and implement one mechanism on deterministic tiny data, then
  test and interpret it. This is the default when implementation evidence is
  absent.
- **Applied**: preserve a baseline and add one realistic data, validation,
  metric, or integration condition.
- **Advanced**: add one controlled research question, ablation, sensitivity,
  failure analysis, efficiency tradeoff, or reproducibility check only after
  Core mechanics are demonstrated.

Match the task to the outcome: use small NumPy or PyTorch calculations for
mathematics and Tensor mechanics, controlled validation and error analysis for
classical ML, minimal modules and debugging for DL or Transformer mechanics,
and controlled latency, throughput, memory, batching, or KV-cache comparisons
for systems. Use Kaggle only when the learning outcome is the end-to-end data,
validation, metric, or error-analysis workflow; verify any current competition,
dataset, library, model, or tool before naming it, and never optimize for rank.

Use one whole-task flow when outcomes share inputs and completion evidence.
Creation always produces one `practice/<area>/<topic>.ipynb`; keep independent
questions as separate exercises in that Notebook instead of splitting files.
This includes small training, validation, checkpoint-selection, API-shape, and
debugging workflows: their state can be represented by deterministic fixtures
and local `check_e##()` checks. Do not create `src/`, `tests/`, a package, or a
project directory unless the user explicitly requests a reusable multi-file
project outside this default practice flow.

Never overwrite an existing learner artifact; choose a narrower new Notebook or
continue the existing one.

## Build an authentic but small task

### Keep the Notebook self-contained

The learner must be able to complete every TODO and understand every check by
reading the Notebook alone. Source links provide provenance and optional review;
they are never required reading for discovering a task rule. Before the TODO,
state every arbitrary value or convention that a fixture or test depends on,
including policy thresholds and precedence, exact return tokens and dictionary
keys, dtype or device representation, axis and inclusive-boundary conventions,
aggregation formulas, and required error behavior.

Do not turn this requirement into an answer leak or an authoring rubric on the
learner surface. State fixed requirements in natural prose and bullets, then
state what the learner must implement or infer. Internally, keep contiguous
Requirement IDs and `source-given`, `practice-given`, or `derive` kinds in
`metadata.llm_research_lab.practice` only.

- A source-given Requirement faithfully names a precise source location and
  identifies a source-specific threshold as a local policy, not a universal
  fact.
- A practice-given Requirement is allowed only for a useful local interface or
  failure boundary and records its rationale internally.
- A derive Requirement states what must be calculated or checked without
  putting the completed algorithm or derived answer in the brief.
- Each Requirement points to a same-exercise brief cell before implementation,
  and its complete normalized natural-language claim must occur there. Isolated
  word matches are not evidence that the relation was disclosed.
- Each `np.testing` or `torch.testing` assertion and expected-exception block is
  traced internally by AST ordinal and fingerprint. Never put Requirement IDs
  or trace markers in Markdown or code.
- Do not invent a callable or token assertion for a prose-only concept. A
  learner-owned design or interpretation Requirement may instead terminate in
  the adjacent reflection cell, with its exact prompt and unresolved
  placeholder tracked as the learner target.
- Track every required reflection response as a learner target. A reflection
  that has no target must be phrased as optional and state that it is not a
  completion condition; never hide a fourth required action in prose after an
  Exercise has reached its three-target limit.

If two reasonable implementations satisfy the visible Notebook but only one
passes its checks, the artifact is defective. A test may verify a derived
consequence; it may not be the first disclosure of an arbitrary rule.

Use guided fading. Choose `guided` when the learner is meeting a mechanism for
the first time, `partial` when they can complete a familiar core inside a
provided boundary, and `independent` only when their evidence supports writing
the whole small mechanism. In every stage, provide signatures, repetitive
validation, return assembly, fixture wiring, and bookkeeping unless one of
those is itself a mapped learning outcome. The learner owns the decisive
operation, reasoning, diagnosis, or design choice.

Keep one primary concept per Exercise and no more than three learner targets.
Split independent concepts into adjacent Exercises in the same Notebook. A
completed learner Exercise may be preserved as an explicit migration exception;
do not erase it merely to restore a creation-ready state.

Provide setup and scaffolding that do not solve the declared learner targets:

- a realistic scenario and requirements;
- public signatures, type hints, and docstrings;
- deterministic tiny fixtures, imports, and environment boilerplate;
- exactly one unexecuted setup-role code cell before the first exercise;
- tests expressing already disclosed normal, edge, and failure contracts;
- commands and values to observe.

Every created artifact is a Notebook-only artifact:

- keep the setup cell to dependency imports, type aliases, and non-solution
  helpers;
- give every cell a stable nbformat cell ID and one internal role;
- for each Exercise, keep one brief, implementation, fixture, `check_e01()`, and
  reflection cell in that order;
- use natural comments such as `# 예제 입력으로 동작을 살펴보세요` and
  `# 잘못된 입력`; never expose setup, fixture, check, Outcome, Requirement, or
  trace role markers;
- keep normal, edge, and failure categories in check metadata while presenting
  learner-friendly comments in code;
- use lightweight local assertions such as `numpy.testing`; do not add path
  manipulation, module reload, subprocess, pytest, package imports, or hidden
  test files.

Imports, fixtures, calls, prints, comparison assertions, routine validation,
dict or tuple assembly, and API bookkeeping are normally scaffolding, not the
learner's answer. Keep the runnable fixture beside its TODO; do not make the
learner copy it by hand. A practice-added API rule defaults to provided
scaffolding and may become learner-owned only when an exact TIL outcome makes
that rule the concept being practised.

Leave these to the learner at the selected scaffold stage:

- core algorithms and Tensor operations;
- the decisive train/validation ordering;
- metric, checkpoint, batching, and validation judgments;
- result interpretation and design justification.

Track each learner-owned boundary as an internal learner target. A guided or
partial function may contain completed provided code around an explicit
unresolved `NotImplementedError`; only the target operation must remain blank.
An implementation cell may also contain complete helpers or top-level
prediction/design work and need not expose a public learner function. Do not
prefill the declared core and leave cosmetic blanks. Tests may verify the
observable contract, never introduce a hidden requirement or reveal an
implementation strategy. Use only production
features that serve the outcome: explicit Shape/dtype contracts, separated
public interfaces, deterministic config, train/eval boundaries, meaningful
return values, input validation, or normal/edge/failure tests. Avoid Docker,
cloud, large downloads, elaborate packaging, and other decorative complexity.

Do not prescribe exact learner-facing headings. Write a polished exercise that
reads like finished courseware: a natural title and short purpose, the functions
to implement, exact fixed requirements, a tiny analogous example when useful,
folded progressive hints, starter code, local observations, and an
interpretation prompt. The metadata roles establish order without leaking the
authoring schema. Never create a global hint section.

Put folded hints in the brief immediately before the implementation cell.

- Hint 1 points to the state or concept to inspect.
- Hint 2 gives a tiny trace, Shape flow, or pseudocode.
- Add Hint 3 only when a minimal API skeleton is necessary; never give the
  completed core.

Store the exact TIL, all used lessons, every mapped instructor-practice file,
their hashes, Outcome coverage, and source-versus-practice findings in the
internal metadata. The learner surface may contain one concise optional TIL or
course-index review link, but never an exhaustive audit list or coverage table.
Leave every code cell unexecuted with `execution_count: null` and empty outputs.
Do not invent success, output, metric, or experiment results.

The initial run is expected to fail only at declared unresolved learner targets;
syntax errors, import errors, provided-scaffold failures, fixture failures, and
test cell-order errors are artifact defects.

## Validate and obtain an independent review

Run the artifact validator on the Notebook:

```bash
python3 .agents/skills/suggest-learning-practice/scripts/validate_practice_artifact.py \
  practice/<area>/<topic>.ipynb
```

Use `--learner-state` only when validating an existing Notebook that already
contains learner implementations or execution state. It preserves specification
and trace audits but does not certify the artifact as newly created and blank.

Use `--strict-external-sources` before deleting a lesson's temporary cache. Use `--completion-ready` only after the learner has implemented, run, and interpreted the whole artifact. A completion-ready pass permits a commit of exactly that Notebook path with `practice: complete <artifact-stem>` when the current request authorizes it; creation never does. Do not replace learner work to make this gate pass.

Also run Notebook JSON and metadata validation, the setup-role cell from the
repository root, code-cell compilation, source hash and link checks, and
`git diff --check`. Read the final Notebook.

Then give the Notebook to a fresh read-only reviewer that did not author it.
First provide only the rendered learner surface: the reviewer checks that it
reads like polished courseware, contains no internal audit language, and makes
every check behavior determinable without another file. Only after that pass,
provide the exact TIL, metadata, linked sources, and mapped instructor practice
for source fidelity, full outcome coverage, appropriate scaffold ownership,
useful
non-solution local checks, adjacent sufficient hints, single-file simplicity,
and absence of fake output. A source-only requirement, a hidden test convention,
audit leakage, or a source-specific policy presented as universal is blocking.
Permit one revision and one second fresh reviewer only. If review is unavailable
or the second review does not pass, do not call the artifact ready.

Do not execute learner TODOs or push. Commit only under an explicit request or the exact full-flow completion authorization described in the repository rules.

## Attempt-feedback mode

1. Read the exact saved Notebook or legacy bundle, including learner code, outputs,
   traceback, and actual test result. If the reported failure is not saved or
   reproducible from supplied output, ask for that exact evidence; do not
   invent it.
2. Distinguish inputs, model outputs, targets, parameters, gradients, metrics,
   and persisted artifacts. Trace the smallest relevant state or Shape.
3. Address one blocker at a time. Start with the smallest concept hint, then a
   partial trace, then the provided API boundary. Do not complete the core
   implementation without explicit authorization.
4. After tests pass, require the learner to explain the decisive state change,
   output, or contract. A green test alone is not completion evidence.
5. Record only results that actually ran. Preserve the learner artifact and do
   not rewrite unrelated cells or files.

## Report

For creation, report the decision, TIL and mapped source basis, covered
outcomes, artifact path(s) and depth, independent-review result, validation
commands, and the first prediction to make. For attempt feedback, report the
observed blocker, smallest next action, and exact rerun command. Do not provide
a menu, score, mandatory schedule, hidden answer, or unsupported success claim.
