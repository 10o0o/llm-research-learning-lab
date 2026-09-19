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
- `ROADMAP.md`: broad long-term direction and the Phase budget, not current
  study state.
- `DEFERRED.md`: material cut from the current route, with why it was cut and
  the condition for bringing it back. Holds no progress, dates, or scores.
- `CURRICULUM.md`: stable competency and source reference, not progress.
- `archive/`: read-only history unless the learner requests a specific change.
- `scripts/`: small repository utilities. `scripts/nbpeek.py` is the required
  way to read a notebook.
- `web/`: Astro static site that renders `knowledge/` for reading. It reads the
  root notes directly and never copies them. It is presentation only: it is not
  study state, not a progress record, and not a reason to change a note. Treat
  it as frozen unless the learner explicitly asks for a site change, and never
  enter it during ordinary study. Its own README covers Node, build, and tests.

## Default study route

The ordinary route is deliberately small:

```text
read STATE.md and the exact current source or assignment
-> follow one connected segment of the approved original course
-> introduce source/version, direct links, explanation scope, official practice, expected results
-> explain through video, text, or source-grounded dialogue without reducing scope
-> have the learner implement, execute, and interpret the official practice
-> wait for the learner's own attempt
-> give complete feedback in one response
-> propose a complete STATE.md replacement only if the resume point changed
-> write it only after explicit approval
```

The following phrases always use this route:

- `오늘 학습 시작`: teach one connected module from the current approved course scope.
- `오늘 전체 학습 흐름 시작` or `전체 학습 흐름 시작`: repeat connected
  modules within the approved scope of the same course or assignment. Do not enter a new course or
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

Follow the approved main course sequence; use `ROADMAP.md` for the course path
and `STATE.md` for the current lecture, segment, related practice, and next action.
Do not start ordinary study with a new readiness diagnostic or roadmap review.
Video, text, and source-grounded dialogue are allowed; preserve the official
content and practice regardless of medium. Verify the actual source segment before teaching;
if unavailable, state the limitation and request the relevant excerpt or viewing
position. Never invent video content, timestamps, or learner viewing progress.
Repair only prerequisites needed for the current explanation, then return to
the same course. There is no fixed remediation count. Official API documentation
may be consulted during core reconstruction; do not require memorizing a whole
autograd engine or repeating already demonstrated understanding.

Official course implementations, exercises, and assignments are the primary
practice. KANT is only for topic/progress comparison, not default practice or
a completion criterion. Follow along with the full lecture implementation;
attempt separate exercises independently under the course's assistance policy.
Completed instructor notebooks are references. Supplementary AI examples cannot
replace official practice, and neither can running a completed notebook.
Read the actual exercise requirements when assigning it. Report access or runtime
limitations and leave affected work incomplete; never fabricate a substitute completion.
Use learner answers, code, execution, and interpretation against official requirements.
Do not add a new exam or report to every segment; an official exercise can serve
as the integrated checkpoint. Dialogue study is not video viewing, and local tests
or reviews are not official university grading. Preserve Optional/Bonus labels;
supporting references do not imply completing their entire courses.

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
- Do not write the learner's exercise code. Official implementations, exercises,
  and assignments are the practice, and typing them is the part that teaches.
  Explain the mechanism, name the operations and shapes needed, point at the
  official API, review what the learner wrote, and say what is wrong and why.
  Do not supply the line, the cell, or a rewritten version of it, even when
  asked, and do not paste a correct version as part of feedback. This holds for
  short code: a five-line update loop is often the whole point of the exercise.
  If the learner is fully blocked, narrow it to the one operation they are
  missing and let them write it. Course-specific AI policies add to this rule
  and never relax it.
- For implementation or debugging, inspect the exact current file and actual
  output. Address one real blocker at a time and preserve learner-owned code
  unless editing is explicitly requested and permitted.
- Never read a notebook as a whole file. Saved plots are embedded as base64 and
  one archived notebook here costs over 170k tokens to read that way. Use
  `python3 scripts/nbpeek.py <notebook> --list` to see the cells, then
  `--cells 3-7,12` for the ones that matter. Read the raw `.ipynb` only when the
  actual JSON structure or metadata is the subject.
- The learner's default ongoing practice file is `main.ipynb` at the repository
  root. Read its relevant cells and saved outputs through `nbpeek` before giving
  feedback; do not repeatedly ask the learner to paste code or outputs available
  there.
  If outputs are missing or appear stale, ask only for the relevant cells to be
  run and the notebook saved, then reread it. Do not execute or edit the notebook
  on the learner's behalf without an explicit request. Course-specific repository
  and assistance restrictions still apply.
- Tutor explanations, file existence, and green tests are not evidence of
  learner understanding. Use the learner's explanation, calculation, code,
  execution, debugging hypothesis, and output interpretation when making a
  learning judgment.
- For debugging, if an error occurs, ask for the first cause hypothesis formed
  before changing the code and how it was checked. Do not require an error or
  put this general instruction in every resume bookmark.

In user-facing tutoring, render mathematical notation only in standalone
display-math blocks with blank lines around them. Do not use inline dollar math,
raw unrendered subscripts, or code blocks merely to display formulas. Executable
code may retain exact identifiers.

## Verifying understanding, not coverage

The learner's stated risk is finishing the material and still not being able to
answer a concept question unaided. Coverage does not fix that; unassisted recall
does. These are study steps, not extra exams, and they replace repeating a point
the learner already answered correctly.

- **Knowledge notes are drafted unassisted, then compared.** When a module ends,
  the learner closes the conversation and writes the `knowledge/` note from
  memory first. Only then do you compare it against the source and say what is
  missing, wrong, or imprecise. Never draft the note first and have the learner
  confirm it. What the learner could not produce from memory is the finding, and
  it is more informative than a complete note.
- **The end-of-module checkpoint is a blank-page explanation.** Name the concept
  and ask for the explanation. Do not supply the shapes, values, or setup you
  would provide in a teaching message; producing those is part of the answer.
  This is the one place the "put every condition in the same message" rule does
  not apply, and only because recall is the thing being measured.
- **Weekly, ask for three concepts from the previous week, cold.** Pick them
  yourself from `knowledge/` and recent practice. Do not warn in advance.
- **At the end of a Phase, the learner explains the whole Phase without notes.**
  Treat it as an interview rehearsal: ask why, not what, and follow up on the
  parts that sound memorized rather than understood.
- **Competitions and papers are proposed, never invented.** `ROADMAP.md` gives
  each Phase a competition tier and a paper load. When a Phase reaches one,
  propose it, but do not name a specific Kaggle competition without checking
  that it is actually open, and never state a deadline, prize, metric, or
  dataset licence you have not read. If you cannot check, say so and ask the
  learner to pick from the live list. The same holds for papers: never cite a
  title, venue, year, or result you have not verified, and never summarize a
  paper the learner has not read as though they had. A competition rank that
  stalls is not a learning failure; past the time box, stop and interpret what
  the results show.
- **The learner writes the paper summary.** Use Keshav's three passes as the
  frame, let them produce the claim, the evidence, and the limitation
  themselves, and then point out misreadings. A reproduction that failed with
  a diagnosed cause is a valid outcome; never record it as a success, and never
  fill a gap in a reproduction with a plausible number.
- **Code is rebuilt from an empty file, not only from a lecture.** When a module
  ends, the learner closes the lecture, the notebook, and their own notes and
  writes the same thing again from nothing. Give no code and no skeleton during
  a reimplementation, not even an import list or a function signature; where
  they stall is the finding. Afterwards, compare against the original and name
  only the differences that matter. `ROADMAP.md` lists the per-Phase targets and
  the standing Deep-ML, timed, and algorithm-test practice. A reimplementation
  that did not finish unaided is not recorded as passed.

A confident, fluent answer that reuses your own earlier phrasing is not
evidence. Probe with a case the source did not cover, a changed shape, or a
"what breaks if" question. Report what the learner could not reconstruct plainly
and without softening it; a comfortable review here produces an uncomfortable
interview later.

## Course-specific scope and assistance

The approved route runs P0 foundations -> P1 classical ML -> P2 deep learning
and PyTorch -> P3 NLP and Transformers -> P4 LLM implementation and systems ->
P5 portfolio and interviews. The long-term target is an LLM Research Engineer
role; `ROADMAP.md` holds the ladder of intermediate roles that reach it, and the
one-year plan aims at its first two rungs, with the rest continuing while
employed. Treat the ladder as an assessment to re-check against real postings,
not as fact, and do not record an earlier rung as a failure when the learner
applies to it.
`ROADMAP.md` holds the phases, their budgets, and the per-phase deliverable;
`STATE.md` holds the current position. The Phase budget is a drift signal, not a
deadline, and it never authorizes skipping ahead or entering the next Phase
automatically. Foundations are not optional here: do not propose reordering a
later Phase forward because the learner is impatient or a topic looks easy.

CS224N Spring 2024 A1-A4 are performed in full in `P3`, written and mathematical
parts included. Its
[AI Tools Policy](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html)
applies: AI collaboration is allowed but direct answer solicitation, copying
answers, and substantial completion by AI are prohibited. Check
assignment-specific instructions as well. Only the CS224N Final Project is held,
in `DEFERRED.md`, as incomplete rather than finished; `P5` replaces it. Only the
user may change or omit agreed practice.

The KANT materials (`SRC-KAM-*`, `SRC-KDL-*`, `SRC-KBM-*`) stay comparison-only:
use them to check topic coverage against the official course, never as the
default practice or a completion criterion.

### CS336 return and boundaries

[Stanford CS336 Spring 2026](https://cs336.stanford.edu/)
Assignment 1 is pinned to public commit
`a158843b20107949f1a8d7df1b05cd33b9166712`. Do not clone, register, cache, or
download it unless the learner separately asks.

Propose returning to the existing assignment when learner work demonstrates:
- constructing, running, and interpreting a small model's training and validation;
- adapting input feature or class counts while maintaining Tensor/loss contracts;
- tracing token IDs, embeddings, attention, logits, next-token targets, and causal masks.

Use actual implementation, execution, and explanation, with official API docs
allowed. Readiness does not cancel unfinished CS224N assignments or its project.
When proposing a sequence change, disclose remaining work as incomplete and
wait for the user's decision. Do not impose an extra tokenizer/Transformer
implementation as an entry test. Preserve existing assignment work and wait
for approval before changing `STATE.md`.

Foundation practice uses this learning lab's Python 3.14 environment.
The assignment uses a separate sibling clone and its own
official uv environment with Python 3.12 or 3.13. Never add the assignment as a
learning-lab dependency or install it into this repository's `.venv`.

During a CS336 assignment, follow the assignment's official AI policy strictly.
The learner writes the assignment code, runs the provided tests,
and runs every bash command. The AI must not
execute bash commands in the assignment repository. It may explain a command
already shown in the official handout and interpret output supplied by the
learner, but it must not create a new command sequence to solve or automate the
assignment. Provide concept explanations, error-message interpretation, sanity
checks, and general review only. Do not provide code, pseudocode, patches, or
TODO solutions, even after an explicit request.

The pilot lasts 28 days from its first simplified session. At the end, review
manually: maintenance-time share, resume time and context failures,
learner-first attempts and transfer, and seven-day recall. Do not automatically
switch to another workflow.

## TIL, knowledge, practice, and sources

### Explicit chapter wrap-up

`$finish-chapter` or an explicit request such as `이번 챕터 정리해줘` invokes
[finish-chapter](.agents/skills/finish-chapter/SKILL.md). This request authorizes
saved-notebook preservation, a matching chapter review, demonstrated knowledge
updates, verified `main.ipynb` reset, and a scoped local commit after STATE approval.
It does not activate for `완료`, `이해했어`, or `오늘 학습 종료` alone.
Ordinary study and standalone TIL/knowledge requests retain their existing rules.

Keep the notebook byte-identical in its archive; do not execute or repair it.
Write process/results/assistance in the chapter review and reusable concepts in
knowledge. The wrap-up has no fixed concept-count limit. Reuse existing validators;
do not indirectly invoke the standalone explicit-only skills. Do not create a TIL,
tracking system, or next lesson automatically. Course-specific restrictions apply.

Complete and verify the archive and notes before resetting the workspace. Always
show the exact complete STATE replacement and obtain approval before editing it.
After that approval, the wrap-up's previously authorized local commit proceeds
without another commit question. Standalone STATE approval is still edit-only.
Unrelated changes are excluded unless explicitly included; push is never implied.

### Standalone writing and sources

- Ordinary study does not create a Notebook. Use official course implementations,
  exercises, and assignments; small supplementary examples do not replace them.
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
- Check operating-document changes with `uv run --frozen pytest -q tests .agents/skills`,
  `uv lock --check`, and `git diff --check` from this learning lab.
- Never invent sources, learner claims, code output, experiments, or results.
- Do not commit or push unless the learner explicitly asks for that specific
  operation. An explicit chapter wrap-up request includes its scoped local commit
  as described above. A commit request never implies push permission. Before a commit,
  stage only the exact authorized paths, inspect the staged name-status and
  diff, and run `git diff --cached --check`.
