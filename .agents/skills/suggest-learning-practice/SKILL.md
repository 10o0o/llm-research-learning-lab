---
name: suggest-learning-practice
description: Turn one explicitly supplied finalized dated TIL and its exactly linked course sources into one self-contained hands-on Notebook for recall, from-scratch implementation, testing, debugging, interpretation, and design, or coach an attempt from an explicitly supplied practice artifact and real failure output. Use when the user invokes $suggest-learning-practice with an exact til/YYYY/MM/YYYY-MM-DD.md path to create one Notebook under practice, or with an exact existing practice path for stepwise feedback. Automatically use only instructor practice explicitly mapped to the TIL's lesson in that course INDEX.md. Do not infer the latest TIL or artifact, repair an incomplete TIL, execute a new workbook, reveal a complete solution, or treat tutor prose as learner evidence.
---

# Build and Coach Authentic Practice

Practice turns the major outcomes of a complete daily TIL into performance. It
is not limited to gaps or misconceptions. A concept the learner can explain is
still a practice target when they have not independently recalled,
implemented, tested, debugged, transferred, or interpreted it.

Read [the practice design contract](references/practice-design.md) completely
before generating or reviewing an artifact. Use exactly one of the modes below.

## Resolve the mode and exact input

- **Creation mode** requires exactly one named finalized
  `til/YYYY/MM/YYYY-MM-DD.md`.
- **Attempt-feedback mode** requires exactly one named artifact under `practice/`.
- Never infer today's, latest, or most likely file. Never accept
  `til/today.md` for creation. If the user says only “continue,” ask for the
  exact artifact path.
- A decision-only request remains read-only. Creation mode otherwise authorizes
  exactly one unexecuted Notebook-only artifact.

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

   Read the mapped `basic` and `advanced` variants when both exist. Do not load
   an unlisted, neighboring, or same-numbered practice. Instructor practice is
   source scaffolding, not learner evidence; keep it unchanged and never copy
   its full answer or claimed output.
5. Search `practice/` for learner artifacts that explicitly link the same TIL
   outcomes. Do not overwrite executed work, answers, outputs, or reflections.

## Convert the whole TIL into practice outcomes

Identify the TIL's major learning outcomes, not only its gaps. A major outcome
is a mechanism, calculation, Shape or dtype contract, implementation flow,
debugging rule, evaluation judgment, or limitation that materially represents
what the learner studied. Do not turn incidental prose into busywork.

Create this exact map in the generated Notebook. The map plus explicitly cited
equivalent completed learner evidence must cover the TIL's major outcomes:

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

- **TIL 수정 우선**: validation or the coach completeness gate failed.
- **기존 실습 계속**: an unfinished learner artifact already exercises the
  same outcomes; name that exact path and do not replace it.
- **실습 생성**: the normal result, including when evidence is thin. Begin
  with the smallest Core task instead of withholding practice.
- **추가 실습 없음**: exceptional; every major outcome already has equivalent
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

Do not turn this requirement into an answer leak. Separate fixed requirements
from results the learner must derive. In every exercise, put this exact table
inside `### 작은 유사 사례와 계약`, followed by a non-empty
`#### 학습자가 구현·판단할 것` subsection:

```text
| Contract ID | Kind | Learner-visible requirement |
| --- | --- | --- |
| C-E01-01 | source-given | An exact requirement retained from a linked source. |
| C-E01-02 | practice-given | An exact local API or failure requirement added by this practice. |
| C-E01-03 | derive | An observable result or invariant the learner derives from visible inputs. |
```

- Contract IDs are contiguous within each exercise: `C-E01-01`,
  `C-E01-02`, and so on.
- `source-given` must faithfully state the linked source's rule and identify
  source-specific thresholds as local policies rather than universal facts.
- `practice-given` is allowed only for a useful local interface or failure
  boundary and must state the choice explicitly.
- `derive` states what must be calculated or checked without supplying the
  completed algorithm or derived answer.
- Put `# contract: C-E01-01` immediately before every assertion group or
  expected-exception block in `check_e01()`. Every declared contract must be
  exercised and every assertion or expected exception must have a same-exercise
  contract marker.

If two reasonable implementations satisfy the visible Notebook but only one
passes its checks, the artifact is defective. A test may verify a derived
consequence; it may not be the first disclosure of an arbitrary rule.

Provide only setup that does not solve the learning target:

- a realistic scenario and requirements;
- public signatures, type hints, and docstrings;
- deterministic tiny fixtures, imports, and environment boilerplate;
- exactly one unexecuted `# setup-check` code cell before the first exercise,
  so it precedes every learner TODO;
- tests expressing already disclosed normal, edge, and failure contracts;
- commands and values to observe.

Every created artifact is a Notebook-only artifact:

- keep the setup cell to dependency imports, type aliases, and non-solution
  helpers;
- put learner-owned functions in one `# TODO: E01` implementation cell;
- put deterministic calls and observations in a separate
  `# provided-fixture: E01` cell;
- put a self-contained `check_e01()` definition and call in one
  `# test-check: E01` cell, with explicit `# normal`, `# edge`, and `# failure`
  cases;
- use lightweight local assertions such as `numpy.testing`; do not add path
  manipulation, module reload, subprocess, pytest, package imports, or hidden
  test files.

Imports, fixtures, calls, prints, and comparison assertions are scaffolding,
not the learner's answer. Keep the runnable fixture beside its TODO; do not
make the learner copy it by hand. Keep the core algorithm, target-specific
validation, and interpretation learner-owned.

Leave these to the learner from scratch:

- core algorithms and Tensor operations;
- the decisive train/validation ordering;
- metric, checkpoint, batching, and validation judgments;
- implementation of explicitly specified target-specific error handling;
- result interpretation and design justification.

Every public learner function starts with `raise NotImplementedError`. Do not
prefill most of the algorithm and leave cosmetic blanks. Tests may verify the
observable contract, never introduce a hidden requirement or reveal an
implementation strategy. Use only production
features that serve the outcome: explicit Shape/dtype contracts, separated
public interfaces, deterministic config, train/eval boundaries, meaningful
return values, input validation, or normal/edge/failure tests. Avoid Docker,
cloud, large downloads, elaborate packaging, and other decorative complexity.

Each exercise uses this exact order:

```text
## E01. <title>
### 실제 사용 맥락
### 실행 전 회상·예측
### 작은 유사 사례와 계약
### 구현
<folded Hint 1 and Hint 2 beside the TODO>
### 테스트와 실패 진단
### 결과 해석
```

Put the folded hints in the Markdown cell immediately before the code cell
containing `# TODO: E01`. Never create a global hint section.

- Hint 1 points to the state or concept to inspect.
- Hint 2 gives a tiny trace, Shape flow, or pseudocode.
- Add Hint 3 only when a minimal API skeleton is necessary; never give the
  completed core.

Link the exact TIL, all used lessons, and every mapped instructor-practice file
from the workbook. State what was retained from course scaffolding and what was
added as scenario, test, or failure case. Leave every code cell unexecuted with
`execution_count: null` and empty outputs. Do not invent success, output,
metric, or experiment results.

The initial run is expected to fail only because learner functions remain
`NotImplementedError`; syntax errors, import errors, fixture failures, and test
cell-order errors are artifact defects.

## Validate and obtain an independent review

Run the artifact validator on the Notebook:

```bash
python3 .agents/skills/suggest-learning-practice/scripts/validate_practice_artifact.py \
  practice/<area>/<topic>
```

Also run Notebook JSON validation, the `# setup-check` from the repository root,
code-cell compilation, link checks, and `git diff --check`. Read the final
Notebook.

Then give the exact TIL, linked sources, mapped instructor practice, Practice
Coverage Map, and Notebook to a fresh read-only reviewer that did not author it.
The reviewer first reads only the Notebook and checks that every test behavior
is determinable without opening a source. The reviewer then compares the TIL,
linked lessons, and mapped instructor practice for source fidelity, full outcome
coverage, from-scratch core work, useful non-solution local checks, adjacent
sufficient hints, single-file simplicity, and absence of decorative complexity
or fake output. A source-only requirement, a hidden test convention, or a
source-specific policy presented as a universal fact is blocking. Permit one
revision and a second fresh reviewer only. If review is unavailable or the
second review does not pass, do not call the artifact ready or deliver it as
completed.

Do not execute learner TODOs or commit/push unless the user separately asks.

## Attempt-feedback mode

1. Read the exact saved Notebook or legacy bundle, including learner code, outputs,
   traceback, and actual test result. If the reported failure is not saved or
   reproducible from supplied output, ask for that exact evidence; do not
   invent it.
2. Distinguish inputs, model outputs, targets, parameters, gradients, metrics,
   and persisted artifacts. Trace the smallest relevant state or Shape.
3. Address one blocker at a time. Start with the smallest concept hint, then a
   partial trace, then a minimal API skeleton. Do not complete the core
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
