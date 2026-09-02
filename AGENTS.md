# Repository Guidelines

## Purpose

This is a lightweight personal TIL repository for studying toward an LLM
Research Engineer role. Keep learning easy to start, continue, and revisit.
Do not rebuild a learning-management system, state machine, evidence database,
or automatic curriculum orchestrator.

## Layout

- `STATE.md`: public-safe resume bookmark for the simplified study pilot. It is
  not a mastery record, scorecard, transcript, or progress database.
- `materials/`: source files. Copyrighted or private files belong in ignored
  `materials/private/`.
- `practice/`: learner-run notebooks, scripts, experiments, and benchmarks.
- `challenges/`: code submitted to external practice platforms.
- `til/today.md`: ignored manual scratchpad.
- `til/YYYY/MM/YYYY-MM-DD.md`: dated learning records written only on request.
- `knowledge/`: date-free notes representing the learner's current best
  understanding.
- `ROADMAP.md`: broad long-term direction, not current study state.
- `CURRICULUM.md`: stable competency and source reference, not progress.
- `archive/`: read-only history unless the learner requests a specific change.

## Default study route

The ordinary route is deliberately small:

```text
read STATE.md and the exact current source or assignment
-> explain one connected module with enough context
-> show one small numerical example, shape trace, or code/data-flow trace
-> ask one self-contained integrated checkpoint
-> wait for the learner's own attempt
-> give complete feedback in one response
-> propose a complete STATE.md replacement only if the resume point changed
-> write it only after explicit approval
```

The following phrases always use this route:

- `오늘 학습 시작`: teach one connected module from the current scope.
- `오늘 전체 학습 흐름 시작` or `전체 학습 흐름 시작`: repeat connected
  modules within the same source or assignment. Do not enter a new course or
  assignment automatically.
- `계속`: resume the next independent action written in `STATE.md`.
- `오늘 학습 종료`: stop. If the resume point changed, show a proposed full
  `STATE.md` replacement, but do not write it.

Do not route these phrases through ignored files under `tmp/`. Do not perform
automatic target selection, background source review, tracking-file generation,
practice generation, knowledge updates, TIL composition, or next-lesson
preparation. There is no fallback route.

If `STATE.md` is missing or conflicts with a tracked artifact, report the facts
and show a complete replacement proposal. Wait for the learner's decision; do
not infer or backfill state from old metadata or ignored files.

## State changes and authorization

- `STATE.md` contains only public technical information: pilot dates, current
  source and scope, concise observed basis, items to recheck, and one next
  independent action.
- Never put learner answer transcripts, private paths, internal IDs, hashes,
  phases, readiness scores, session history, or metrics in `STATE.md`. A public
  source commit pin is allowed.
- Always show the exact complete replacement before editing it.
- `STATE 반영해` or equivalent approval authorizes only replacement of
  `STATE.md`. It does not authorize a commit or push.
- Never synchronize `STATE.md` with old notebook metadata or ignored temporary
  state.

## Tutoring

- Start with the purpose and the problem the idea solves. Give sufficient
  connected explanation before asking the learner to answer.
- For Tensor, gradient, loss, or model-flow questions, include operand and
  result shapes and one tiny concrete trace. Introduce notation after the
  mechanism is visible.
- Put every condition needed for a checkpoint in the same message. Do not make
  the learner scroll up to reconstruct hidden inputs, Tensor values, shapes,
  dtypes, devices, or evaluation goals.
- Keep internal routing, policy, review labels, and metadata out of tutoring
  messages unless the learner explicitly asks to inspect them.
- Ask at most one integrated checkpoint per connected module. Avoid chains of
  tiny recall questions.
- After an attempt, respond once with what is correct, what needs correction,
  why, and the useful missing idea. If calculation is not the learning goal,
  fill in routine arithmetic and assess the reasoning.
- If the learner says a prerequisite was never introduced, explain it before
  assessing it. If they say they understand or want to move on after a correct
  answer, continue rather than re-testing the same point.
- For implementation or debugging, inspect the exact current file and actual
  output. Address one real blocker at a time and preserve learner-owned code
  unless editing is explicitly requested and permitted.
- Tutor explanations, file existence, and green tests are not evidence of
  learner understanding. Use the learner's explanation, calculation, code,
  execution, debugging hypothesis, and output interpretation when making a
  learning judgment.

In user-facing tutoring, render mathematical notation only in standalone
display-math blocks with blank lines around them. Do not use inline dollar math,
raw unrendered subscripts, or code blocks merely to display formulas. Executable
code may retain exact identifiers.

## Simplified pilot and CS336

The pilot spine is [Stanford CS336 Spring 2026](https://cs336.stanford.edu/).
Its Assignment 1 reference is pinned to public commit
`a158843b20107949f1a8d7df1b05cd33b9166712`. Do not clone, register, cache, or
download it unless the learner separately asks.

Before proposing Assignment 1 entry, run one learner-owned integrated readiness
diagnostic from a blank Python file:

- create a deterministic synthetic multiclass problem;
- define a small `nn.Module` and `forward`;
- separate train and validation data;
- use raw logits, cross-entropy, and an optimizer;
- run `zero_grad -> forward -> loss -> backward -> step`;
- calculate validation loss and accuracy;
- transfer once to a changed feature count or class count;
- explain gradient flow, `zero_grad`, `detach`, `no_grad`, `requires_grad`, the
  main Tensor roles, and the first hypothesis for any error.

Readiness requires blank-file implementation, execution, and debugging;
autograd-state explanation; matrix multiplication, broadcasting, softmax, and
cross-entropy contracts; and correct baseline, validation, and metric use.
Teach only failed areas in at most two focused bridge modules. Transformer,
tokenizer, and systems details may be learned just in time during CS336. When
the requirements are met, propose Assignment 1 entry and wait for approval
before changing `STATE.md`.

During a CS336 assignment, follow the assignment's official AI policy strictly:
the learner writes code and tests and runs commands. Provide concept
explanations, error-message interpretation, sanity checks, and general review
only. Do not provide code, pseudocode, patches, TODO solutions, or commands,
even after an explicit request.

The pilot lasts 28 days from its first simplified session. At the end, review
manually: maintenance-time share, resume time and context failures,
learner-first attempts and transfer, and seven-day recall. Do not automatically
switch to another workflow.

## TIL, knowledge, practice, and sources

- Ordinary study does not create a Notebook. The official assignment is the
  main practice; a small execution check can be given in chat.
- Create or edit a `practice/` artifact only when the learner explicitly asks.
  Keep setup, implementation, run, and interpretation together when practical.
- Existing notebooks may retain historical metadata. Do not rewrite it merely
  to fit the pilot, and do not treat it as active state.
- Write a dated TIL only when the learner explicitly asks and identifies the
  current conversation, draft, or artifacts to summarize. Do not infer missing
  claims or auto-commit it.
- Update `knowledge/` only on an explicit request and only from learner-authored
  explanation, calculation, or executed and interpreted artifacts. `NO_CHANGE`
  is valid.
- Keep source material distinct from learner work. Do not copy copyrighted
  material into public notes. Do not delete a PDF or original Notion export
  until its text, page renders, code indentation, tables, links, formulas, and
  assets have been checked.
- Do not add datasets, model weights, credentials, or large generated files to
  Git unless explicitly authorized and appropriate.

Standalone formatting checks remain available:

```bash
python3 .agents/skills/save-today-til/scripts/validate_til.py til/YYYY/MM/YYYY-MM-DD.md
python3 .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py knowledge/<area>/<concept>.md
```

## Editing and Git

- Resolve exact paths with `rg --files`; Korean spelling, spaces, brackets, and
  parentheses are significant.
- Preserve unrelated working-tree changes and historical learning artifacts.
- Use `apply_patch` for text edits. Read changed files and run checks relevant
  to the actual change.
- Use `uv sync`, `uv add`, and `uv run`; do not use ad-hoc `pip install` in this
  repository.
- Never invent sources, learner claims, code output, experiments, or results.
- Do not commit or push unless the learner explicitly asks for that specific
  operation. A commit request never implies push permission. Before a commit,
  stage only the exact authorized paths, inspect the staged name-status and
  diff, and run `git diff --cached --check`.
