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

For ordinary study and manual review, directly open and read
[study-session](.agents/skills/study-session/SKILL.md) at the start of the task. Do not assume
the current tool discovers or automatically loads repository skills. `$study-session`
is also an explicit entry point. The skill defines the tutoring and review
procedure; this file remains authoritative for course scope, evidence,
permissions, and other repository boundaries.

- `오늘 학습 시작`: one connected module in the current approved course.
- `오늘 전체 학습 흐름 시작` or `전체 학습 흐름 시작`: connected modules
  within the same approved course or assignment; never enter another course automatically.
- `계속`: resume the next independent action in `STATE.md`.
- `오늘 학습 종료`: stop and update the bookmark only from confirmed evidence.
- `이번 주 회상`: run the manual weekly recall defined by the skill.

Do not route these requests through ignored files under `tmp/`, select new
targets automatically, or generate tracking files, practice, TIL, knowledge,
or next-lesson preparation during ordinary study. A normal stop or weekly
review does not trigger `finish-chapter`. The confirmed chapter-transition
wrap-up below remains the standing exception for its authorized work.

If `STATE.md` is missing or conflicts with a tracked artifact, report the facts
and repair the bookmark from confirmed evidence without prior approval. If the
correct position is unclear, ask only for missing facts; never infer it from
old notebook metadata or ignored files.

Follow the approved course sequence in `ROADMAP.md`; `STATE.md` identifies the
current lecture, segment, related practice, and next action. Do not begin with
a new readiness diagnostic or roadmap review. Verify the exact official source
segment before teaching. If unavailable, state the limitation and request the
relevant excerpt or viewing position. Never invent source content, timestamps,
or learner viewing progress. Use official course implementations, exercises,
and assignments as primary practice, and inspect actual requirements before
assigning them. KANT is comparison-only; supplementary examples and completed
instructor notebooks do not replace official practice. Report access or runtime
limits as incomplete; do not invent substitute completion. Preserve
Optional/Bonus labels, and do not describe dialogue as video viewing or local
checks as official university grading.

## More than one assistant

The learner uses more than one AI tool. These rules live in files, not in any
one tool's settings, so every tool gets them: `AGENTS.md` is the source and
`CLAUDE.md` is a symlink to it. Keep both working by never writing
tool-specific commands into these documents.

- `STATE.md` is the only handoff. Conversation history, per-tool memory, and
  settings do not cross over. Read `STATE.md` at the start of every session and
  never rely on something "we discussed" that is not in a tracked file.
- One session at a time. Two assistants editing against the same `STATE.md`
  produce a conflict the bookmark cannot resolve. If the tracked files disagree
  with `STATE.md`, report the facts and repair it from confirmed evidence.
  Ask about unresolved facts rather than silently merging conflicting claims.
- A second assistant is not a second chance to be handed an answer. The rules
  on exercise code, blank-page reimplementation, and unassisted recall apply
  identically whichever tool is running; asking elsewhere for the code defeats
  the checks, not the rule.
- Cross-checking explanations between tools is useful and encouraged. When they
  disagree, the official source settles it, not the more confident assistant.
- Do not start a per-turn agent swarm. One tutor owns any `STATE.md` change;
  request a read-only source or feedback cross-check only when the user asks or
  when it can resolve a substantive explanation conflict.

## State changes and authorization

- `STATE.md` contains only public technical information: pilot dates, the
  current `ROADMAP.md` Phase ID, current source and scope, concise observed
  basis, items to recheck, and one next independent action.
- The Phase ID is a static pointer into `ROADMAP.md` (`P0`-`P5`), nothing more.
  Never add a percentage, a score, a readiness judgement, an hour tally, a
  checklist of finished items, or a computed next target beside it. Those are
  the progress machinery this repository removed, and a Phase ID is not an
  opening to bring them back.
- Never put learner answer transcripts, private paths, internal IDs, hashes,
  readiness scores, session history, or metrics in `STATE.md`. A public source
  commit pin is allowed.
- Update `STATE.md` without prior proposal or approval when the confirmed
  resume point changes. Use learner explanations and inspected artifacts;
  distinguish completed work, planned work, and unverified claims. Do not infer
  understanding from tutor explanations or successful execution alone.
- Keep the bookmark current at `오늘 학습 종료`, an explicit chapter wrap-up,
  module completion, and a Phase transition; briefly report what changed.
  At a Phase transition, run the `ROADMAP.md` check first and record its result.
  This edit permission does not authorize a new course, a sequence change,
  skipped requirements, or unverified Phase completion.
- Updating `STATE.md`, automatically or on request, authorizes only the file edit.
  It does not authorize a commit or push.
- Never synchronize `STATE.md` with old notebook metadata or ignored temporary
  state.

## Learner ownership and evidence

Do not write exercise code, answer lines, cells, skeletons, or rewritten
solutions, even when asked. Explain concepts and official APIs, and review the
learner's code and actual output. Preserve learner-owned implementation unless
an edit is explicitly requested and permitted; course policies may impose
stricter limits. Explain the missing concept or operation, point to official
APIs, and review learner work without providing code or a rewritten solution.
Tutor explanations, assent, file existence, successful execution, and green
tests alone do not establish understanding.
For debugging, inspect the exact current file and actual output, and address
one blocker at a time. If an error occurred, ask for the learner's first cause
hypothesis formed before changing the code and how they checked it; do not
require an error when none occurred.
Never read a notebook as a whole file. List and read only relevant cells and
saved outputs with the required `scripts/nbpeek.py`; read raw JSON only when
structure or metadata is the subject. For root `main.ipynb`, inspect saved
cells before feedback. If output is missing or stale, ask for those cells to
be run and saved. Do not execute or edit a learner's notebook without explicit
authorization.

The study-session skill defines tutoring procedure and mathematical display
formatting. Repository-wide course and assistance limits remain authoritative.

## Evidence and long-term review

The study-session skill defines ordinary module checkpoints and user-requested
weekly recall. They are learner evidence, not added exams or progress tracking.
- **At the end of a Phase, the learner explains the whole Phase without notes.**
  Treat it as an interview rehearsal: ask why, not what, and follow up on the
  parts that sound memorized rather than understood.
- **Run the phase-transition check before closing a Phase.** `ROADMAP.md` lists
  the items, including the job check. If any is empty, say which and do not
  close the Phase. Never state that a company is hiring, what a posting
  requires, what it pays, or that a posting exists, without having read it;
  propose what kind of posting to look for and what to compare, and let the
  learner open them. When a real posting contradicts the ladder in
  `ROADMAP.md`, the posting is right and the ladder needs fixing. A rejected
  application is information about scope, not a learning failure, and is never
  recorded as one.
- **Competitions and papers are proposed, never invented.** Follow the required
  and optional scope in `ROADMAP.md`. Kaggle is required only in P1; P0, P2,
  and P3 participation is optional after the relevant core learning. P0 needs
  the ability to produce predictions, not a previous submission: the first
  submission is the proposed experience. Do not name a specific Kaggle competition
  without checking
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
- **Code is rebuilt from an empty file at representative implementation units.**
  Use P0 scalar autodiff and MLP training; P1 linear/logistic regression, PCA,
  k-means, and cross-validation; P2 a PyTorch training loop and attention;
  P3 a Transformer block and causal mask; P4 KV cache and inference measurement.
  Do not require rewriting every module's full implementation or entire
  assignments. The learner closes the lecture, notebook, and notes for these
  representative attempts. Give no code and no skeleton during
  a reimplementation, not even an import list or a function signature; where
  they stall is the finding. Afterwards, compare against the original and name
  only the differences that matter. Official assignment work and unassisted
  reconstruction are separate evidence; assisted code is not unassisted success.
  `ROADMAP.md` bounds supplementary Deep-ML, timed, and algorithm-test practice
  within the same activity budget. A reimplementation that did not finish
  unaided is not recorded as passed.

Do not infer durable knowledge from fluency alone. Use the learner's actual
attempt and artifact as evidence, under the boundaries in this file and the
study-session skill.

## Course-specific scope and assistance

The approved route runs P0 foundations -> P1 classical ML -> P2 deep learning
and PyTorch -> P3 NLP and Transformers -> P4 LLM implementation and systems ->
P5 independent experiments and interviews. Build ML Engineer application
evidence, then LLM Systems / Inference expertise toward the long-term LLM
Research Engineer target. `ROADMAP.md` holds the possible intermediate roles,
without promising employability at any Phase or date. Treat the ladder as an
assessment to re-check against real postings. From P1 onward, compare actual
postings with the learner's work and apply when they fit; an earlier rung is
not a failure.
`ROADMAP.md` holds the phases, their budgets, and the per-phase deliverable;
`STATE.md` holds the current position. The Phase budget is a drift signal, not a
deadline, and it never authorizes skipping ahead or entering the next Phase
automatically. Foundations are not optional here: do not propose reordering a
later Phase forward because the learner is impatient or a topic looks easy.
Use 52 calendar weeks with 48 effective study weeks at 60 hours (2,880 hours)
and four calendar slack weeks as an initial allocation hypothesis. Extend the
schedule before cutting core assignments or oral explanation. Account for each
activity in the Phase where it happens; do not borrow another Phase's hours.

Follow the exact editions and scope in `ROADMAP.md`: P0 keeps the currently
approved makemore Part 2 E01-E03, then fast.ai lessons 1-2, foundation repair,
and makemore Parts 3-4. MML chapters 2-5 and 7 define the math coverage;
already demonstrated explanation and calculation do not require repeat
lectures. Repair gaps with the relevant text and official exercises, using
MIT 18.01SC only for missing single-variable calculus. MIT 18.05 Spring 2022
and Problem Sets 1-11 are the probability/statistics core, including required R
work. Stat110 and OpenIntro remain supplementary references.

P1 uses CS229 Summer 2020 PS1-PS3 in full, including required written and coding
work; NumPy reimplementations cannot replace official problem sets. The 2018
videos support matching topics. ISLP chapters 5, 6, 8, and 13 and their Python
labs connect theory with experiments. P2 uses CS231n Spring 2024 Lectures 2-6
and Assignment 2 Q1-Q5 in full, with notes/slides as the default accessible
medium. CS231n A1, A3, and the final project are outside this route. Do not call
either selected scope whole-course completion. Check each course's assistance
and environment requirements before entry; required R and older assignment
environments must not be installed into the learning lab automatically.

CS336 A1-A2 and related lectures remain in P4. A2 covers training performance
and distributed training, not completed inference serving. Connect 2026
Lecture 10 on inference at the end of P4. P5 combines inference optimization
and paper reproduction around one research question, with a fixed workload,
baseline, controlled comparison, quality/memory/performance results, and
limitations. Do not add a second reproduction project. Paid GPU use is planned
for later work; verify service, cost, limits, and assignment compatibility before
entry, without inventing access or replacing an unavailable official task.

CS224N Spring 2024 A1-A4 are performed in full in `P3`, written and mathematical
parts included. Its
[AI Tools Policy](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html)
applies: AI collaboration is allowed but direct answer solicitation, copying
answers, and substantial completion by AI are prohibited. Check
assignment-specific instructions as well. Only the CS224N Final Project is held,
in `DEFERRED.md`, as incomplete rather than finished; `P5` replaces it. Only the
user may change or omit agreed practice.

This repository is public and part of it is published as a site, so official
coursework solutions must not land in it. MIT 18.05 problem-set answers and
CS229, CS231n, CS224N, and CS336 assignment solutions belong in separate private
workspaces; preserve existing private clones. This includes written answers,
code, notebooks, and saved outputs, even when self-studying without grades. What may
be published is the learner's own concept notes, the reimplementations they
wrote from an empty file, competition work, and the reproduction report — never
assignment code, official problem statements, or copyrighted course material.
Before any commit that touches coursework, check which side of that line it
falls on; if it is unclear, leave it out and say so.

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
implementation as an entry test. Preserve existing assignment work. Once the
learner decides on a sequence change, update `STATE.md` without a second approval.

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

### Default chapter-transition wrap-up

At a confirmed chapter transition, invoke
[finish-chapter](.agents/skills/finish-chapter/SKILL.md) before starting the next
chapter, without a separate wrap-up request. The learner has authorized this as
the default: preserve saved chapter notebooks, write matching reviews, update
demonstrated knowledge, reset the verified chapter workspaces (including a
chapter-specific recall notebook), update STATE, and make a scoped local commit
after validation. `$finish-chapter` and `이번 챕터 정리해줘` also invoke it directly.
Confirm the chapter boundary from the approved course and actual work; an ordinary
cell, subsection, or session ending is not a chapter transition. Report incomplete
requirements instead of silently marking a chapter complete. A wrap-up does not
authorize changing courses; use the already approved next step or ask about scope.
It does not activate for `완료`, `이해했어`, or `오늘 학습 종료` alone.
Ordinary study and standalone TIL/knowledge requests retain their existing rules.

Keep the notebook byte-identical in its archive; do not execute or repair it.
Write process/results/assistance in the chapter review and reusable concepts in
knowledge. The wrap-up has no fixed concept-count limit. Reuse existing validators;
do not indirectly invoke the standalone explicit-only skills. Do not create a TIL,
tracking system, or next lesson automatically. Course-specific restrictions apply.
Confirm the learner's unassisted concept drafts before knowledge edits or workspace
reset. If a needed draft is missing, ask for it instead of writing it for them.
Learner-authored conceptual answers already in the conversation can serve as
drafts; do not require a duplicate formal note. Use their actual explanation and
interpreted artifacts, not the tutor's prose or an "understood" response, and
preserve any assistance boundary. Concepts without learner evidence stay in the
review as open questions, not as established knowledge.

Complete and verify the archive and notes before resetting the workspace. Update
STATE from confirmed evidence without prior approval, then run affected checks.
The wrap-up's previously authorized local commit proceeds without another commit
question. Standalone STATE updates are still edit-only.
Unrelated changes are excluded unless explicitly included; push is never implied.

### Standalone writing and sources

- Ordinary study does not create a Notebook. Use official course implementations,
  exercises, and assignments; small supplementary examples do not replace them.
- Create or edit a `practice/` artifact only when the learner explicitly asks
  or the authorized chapter-transition wrap-up requires an archive and review.
  Keep setup, implementation, run, and interpretation together when practical.
- Existing notebooks may retain historical metadata. Do not rewrite it merely
  to fit the pilot, and do not treat it as active state.
- Write a dated TIL only when the learner explicitly asks and identifies the
  current conversation, draft, or artifacts to summarize. Do not infer missing
  claims or auto-commit it.
- Update `knowledge/` on an explicit request or during the authorized chapter
  transition, and only from learner-authored
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

- Resolve exact paths by searching the tracked file list (`rg --files`,
  `git ls-files`, or the equivalent in whatever tool is running); Korean
  spelling, spaces, brackets, and parentheses are significant.
- Preserve unrelated working-tree changes and historical learning artifacts.
- Use whatever patch or edit mechanism the running tool provides. Read changed
  files and run checks relevant to the actual change.
- Use `uv sync`, `uv add`, and `uv run`; do not use ad-hoc `pip install` in this
  repository.
- Check operating-document changes with `uv run --frozen pytest -q tests .agents/skills`,
  `uv lock --check`, and `git diff --check` from this learning lab.
- Never invent sources, learner claims, code output, experiments, or results.
- Do not commit or push unless the learner explicitly asks for that specific
  operation. An explicit or default chapter-transition wrap-up includes its scoped local commit
  as described above. A commit request never implies push permission. Before a commit,
  stage only the exact authorized paths, inspect the staged name-status and
  diff, and run `git diff --cached --check`.
