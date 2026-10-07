# Repository Guidelines

## Purpose

This is a lightweight personal learning repository centered on becoming an LLM
Research Engineer and building evidence for employment. The tutor owns the
approved learning design, adapts teaching to actual evidence, and connects math,
implementation, experiments, and research. KANT is supporting context, not the
calendar or curriculum authority. Keep learning easy to start, continue, and revisit.
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
- `ROADMAP.md`: approved long-term scope and a provisional personal activity
  allocation, not current study state or fixed Phase hours.
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

The tutor verifies each official source segment and teaches it in Korean by
default, including the concepts, notation, assumptions, and a useful example.
Do not require direct textbook reading before starting or resuming; use it when
the learner requests it. Keep source-grounded dialogue distinct from direct
reading. During one active session, reuse verified source details and
instructions while they still apply; recheck when the segment or requirements
change, or when uncertainty arises. Preserve official practice and
learner-owned work.

- `오늘 학습 시작`, `오늘 전체 학습 흐름 시작`, or `전체 학습 흐름 시작`:
  start from the current position and continue through connected modules in the
  same approved course or assignment until the learner pauses or ends, a real
  blocker needs their input, or the approved course boundary is reached. Treat
  these starts alike; never choose another course or skip a formal requirement.
- `계속`: resume the next independent action in `STATE.md`.
- A request to pause or review changes pauses the tutoring flow; it is not an
  explicit study stop and does not trigger the closing commit or push procedure.
- `오늘 학습 종료` (or an equivalent explicit study-stop request): stop, update
  the bookmark from confirmed evidence, then validate, commit, and push the
  session's authorized changes using the study-session closing procedure.
- `이번 주 회상`: run the manual weekly recall defined by the skill.

Do not route these requests through ignored files under `tmp/`, select new
targets automatically, or generate tracking files, new exercises, TIL, knowledge,
or next-lesson preparation during ordinary study. Preparing the starting space
for the current approved activity follows the setup responsibility below.
A normal stop or weekly
review does not trigger `finish-chapter`. The confirmed chapter-transition
wrap-up below remains the standing exception for its authorized work.

If `STATE.md` is missing or conflicts with a tracked artifact, report the facts
and repair the bookmark from confirmed evidence without prior approval. If the
correct position is unclear, ask only for missing facts; never infer it from
old notebook metadata or ignored files.

Follow the approved course sequence in `ROADMAP.md`; `STATE.md` identifies the
current lecture, segment, related practice, and next action. Do not begin with
a new readiness diagnostic or roadmap review. Verify the exact official source
segment before teaching. If unavailable, pause that source-dependent lesson,
state the limitation, and request the relevant excerpt or viewing position.
Do not replace the missing segment with a lesson inferred from its title or
general recollection. Never invent source content, timestamps,
or learner viewing progress. After feedback, continue along the approved route:
teach the next verified segment or give the next learner activity, then wait
when their answer or execution is needed. Do not ask whether to continue after
each step. If assigning an exercise, give its complete relevant givens,
conditions, and required output in the conversation; a source link or question
number alone is insufficient. Source details available only to the tutor are
not learner-visible givens: include the actual values and shapes needed to
start the task. In unassisted recall, supply task givens while withholding
formulas and derived shapes whose reconstruction is the learning target.
Use official course implementations, exercises,
and assignments as primary practice, and inspect actual requirements before
assigning them. KANT is supporting context; supplementary examples and completed
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
- The same learner-first boundary applies to every tutor and coding assistant.
  Never silently complete the learner-owned target implementation, exercise
  execution, interpretation, or recall. Every tutor also owns the permitted
  preparation below. Historical AI-provided setup/code stays assisted
  evidence; it is not rewritten as independent work.
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
- Update `STATE.md` without prior proposal or approval when the confirmed next
  independent action meaningfully changes. Do not edit it for
  each corrected answer when the resume action stays the same. Keep its basis
  concise and current, not a session history. Use learner explanations and
  inspected artifacts; distinguish completed work, planned work, and
  unverified claims. Do not infer understanding from tutor explanations or
  successful execution alone. Keep routine edits quiet; report one when the
  user asks for status, at an explicit study stop, or when a real blocker or
  conflict needs explanation.
- If the bookmark incorrectly assigns permitted preparation to the learner,
  repair that responsibility from the verified source and actual artifacts.
  Do not turn this correction into a new exercise, course transition, or claim
  of learner understanding or execution.
- Keep the bookmark current at `오늘 학습 종료`, an explicit chapter wrap-up,
  module completion, and a Phase transition when these change the confirmed
  resume action.
  At a Phase transition, run the `ROADMAP.md` check first and record its result.
  This edit permission does not authorize a new course, a sequence change,
  skipped requirements, or unverified Phase completion.
- Updating `STATE.md`, automatically or on request, authorizes only the file edit.
  An explicit study-stop request is the standing exception: the learner has
  authorized a scoped commit and push without another confirmation.
- Never synchronize `STATE.md` with old notebook metadata or ignored temporary
  state.

## Learning setup and starting materials

The tutor owns permitted environment setup and starting materials for the
current approved activity. A study-start or resume request includes this
routine preparation; do not ask the learner to choose its scope or manually
copy preparation cells. Determine the starting state from the current goal,
the verified course requirements, and the actual artifacts before applying
implementation restrictions.

| Current activity | Starting state prepared by the tutor |
|---|---|
| Work using a supplied starter | Copy the verified starter; preserve its unfinished learner-target portions |
| Fresh-kernel reproduction of existing code | Restore verified existing code unchanged into a working copy; remove that copy's old outputs and execution counts |
| Representative unassisted reconstruction or cold recall | Prepare the environment and a blank implementation space; provide no code, imports, signatures, or skeletons |

Permitted preparation includes creating or restoring the necessary current
working notebook or script, synchronizing the approved lab environment, and
registering or checking its kernel. Copying verified code is not permission
to author missing target implementations or silently repair existing learner
code. Preserve original starters, archives, and existing learner-owned cells;
do not overwrite a nonempty working space without authorization.
The tutor's restoration and edit limits do not make learner-owned diagnosis
or adaptation a new approval gate. Report runtime or device mismatches and
leave target-code changes to the learner within the approved activity and
course policy. Restore the original first, and distinguish any learner-adapted
run from unchanged-code reproduction.

Inspect discoverable facts first. Ask only for missing source or goal facts,
an actual overwrite conflict, or authorization required by an existing explicit
restriction; do not ask again about already-authorized routine preparation.
Keep failed environment checks and missing dependency or kernel configuration
within tutor-owned preparation. If the existing configuration, interpreter path,
or approved requirements cannot be discovered, ask only for those missing facts.
Do not assign package installation, configuration creation, or kernel repair
to the learner as their next action; keep target execution pending until the
permitted preparation is resolved.
If the learner corrects the responsibility split, apply it to the next action
and repair a conflicting bookmark rather than repeating the scope question.

Course-specific AI, command-execution, acquisition, separate-environment,
paid-resource, and publication restrictions still apply. Official assignment
starters and solutions stay in their permitted private workspaces. Preparing
the current activity does not authorize a new exercise, future lesson, or
course. Keep historical assistance visible; its evidence classification does
not by itself prohibit permitted preparation.

## Learner ownership and evidence

Do not supply learner-owned target exercise implementations, answer lines,
answer-bearing cells or skeletons, or rewritten solutions, even when asked.
Apply this restriction to the learning target, not to the notebook cell format
or permitted starting materials above. Explain concepts and official APIs, and
review the learner's code and actual output. For ordinary concept or API help,
use a small example of the requested operation with unrelated inputs and a
separate toy task. Explain the relevant parameters and their values; generic
API signatures and calls are allowed in this learning mode. An explicit request
to fill an exercise answer is not ordinary API help: keep that response
conceptual or review the learner's own attempt. A template for that target with
placeholders or the same solution under renamed variables is still a target answer.
Never adapt that example into the target exercise's
code, answer, or scaffold, including spelling out the target's exact API call,
inputs, and chosen arguments in prose. Course-specific AI policies may impose stricter
limits. Preserve learner-owned implementation unless an edit is explicitly
requested and permitted.
Tutor explanations, assent, file existence, successful execution, and green
tests alone do not establish understanding.
Separate API-doc-assisted practical implementation from closed-book recall.
Keep first attempt, assistance type/timing, actual execution, and interpretation
distinct in existing reviews; do not create an evidence dashboard. Same-day
success does not establish delayed recall or transfer. Check representative
units after a delay with changed dimensions, distributions, or representations,
and repair only the observed gap rather than restarting an entire Phase.
For debugging, inspect the exact current file and actual output, and address
one blocker at a time. If an error occurred, ask for the learner's first cause
hypothesis formed before changing the code and how they checked it; do not
require an error when none occurred.
Never read a notebook as a whole file. List and read only relevant cells and
saved outputs with the required `scripts/nbpeek.py`; read raw JSON only when
structure or metadata is the subject. For root `main.ipynb`, inspect saved
cells before feedback. If output is missing or stale, ask for those cells to
be run and saved. Routine preparation is authorized as described above;
changing learner-owned implementation or executing a learner's notebook needs
explicit authorization and must obey course policy. Check the environment
with a separate kernel or standalone commands, not by running learner cells.

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
  Supplementary Deep-ML and timed attempts repair observed gaps in these
  representative units within ROADMAP's personal implementation/recall allocation.
  Separate job-preparation algorithm practice belongs to the excluded time intent;
  do not count it twice or add another mandatory track. A reimplementation that
  did not finish unaided is not recorded as passed.

Do not infer durable knowledge from fluency alone. Use the learner's actual
attempt and artifact as evidence, under the boundaries in this file and the
study-session skill.

## Course-specific scope and assistance

The learner-approved spine is P0 executable math/statistics and a PyTorch loop ->
P1 ML experiment evidence -> P2 neural-network diagnosis and attention -> P3 one
small Transformer LM with CS336 A1 as the formal independent implementation ->
P4 one provisional Systems / Inference specialization -> P5 one independent
research/replication cycle and evidence-matched applications. Evaluation is core
throughout; it does not wait until P5. Foundations are not optional here, and
later research depends on demonstrated prerequisites rather than course counts.
Do not propose reordering a later Phase forward solely to match a school calendar.

Follow the exact selected editions and requirements in `ROADMAP.md`. This
approved redesign replaces the former full MIT/CS231n/CS224N/Karpathy/CS336 sequence;
removed requirements are incomplete holds in `DEFERRED.md`, not accomplishments.
Do not restore them as hidden gates or infer whole-course completion. Use
`STATE.md` for the current activity and preserve the observed MIT evidence.
The existing MLP's fresh-kernel data -> train ->
eval reproduction is the next practical gate in P0, not a reason to restart study
or to wait until all probability work ends. User-written train/eval code with
AI-provided data/model/API support remains assisted and not yet fresh-kernel verified.

Personal study intent is 60+ hours/week excluding KANT's 40 hours/week, roughly
two hours/day of algorithms, and job preparation. Preserve that distinction;
do not certify the combined calendar as feasible. ROADMAP's 18/27/9/6 allocation
is a provisional example, not an optimal/mandatory schedule. Check actual time
and independent outcomes during the first 1-2 weeks, then adjust the calendar
without lowering the goal. Do not carry forward 2,880 hours as a fixed forecast.

P0 retains conditional probability, independence, random variables and distributions,
expectation and variance, and the meaning and assumptions of LLN/CLT. Connect
these to the existing MLP's loss, sampling, and evaluation. MIT 18.05 Spring 2022
is a source for the relevant verified segments. Full MIT course completion is
not required: all readings, in-class work, online questions, PS1-PS11, and R
tutorials are no longer blanket requirements. Unselected work remains incomplete
and deferred; it must not return as a hidden prerequisite.

Across P0-P1, connect likelihood/MLE to model losses using CS229 Summer 2020
notes, and sampling units, leakage, confidence intervals, testing/power,
bootstrap, and multiple comparisons to actual evaluation using the selected
ISLP chapters/labs and relevant MIT explanations. Keep basic likelihood, prior,
posterior, and MAP distinctions where the selected CS229 work needs them;
detailed continuous-prior and conjugate-prior calculations are deferred until
an approved assignment or paper requires them. Repair core prerequisites in
context before their dependent activity, rather than adding a full probability course.

R is required only when a selected official activity requires it. Python/PyTorch
model work does not establish official MIT activity completion. MML chapters
2-5 and 7 repair actual gaps. Already demonstrated work does not require repeat
lectures. After the existing MLP reproduction, continue makemore Parts 3-4 and
official exercises without waiting for MIT completion; preserve fast.ai Lesson
1-2 and MML incomplete work in the existing reviews.

P1 retains CS229 Summer 2020 PS1-PS3 in full, required written and coding work,
and ISLP chapters 5, 6, 8, 13 with Python labs. NumPy reimplementations cannot
replace official problem sets. PS3 Q1 RL and Q6 ICA stay required: defer GP,
extra ICA depth, and broad RL courses, not those problem-set questions. Repair
their MDP/Bellman, probability/likelihood, and matrix-calculus prerequisites
before the relevant question. The current CS229 homepage is not interchangeable
with the Summer 2020 problem sets; 2018 videos are supporting explanations.

P2 uses targeted CS231n Spring 2024 Lecture 2-6 explanations and A2 Q1-Q3
(FC/backprop/optimizers, normalization, dropout). Q4-Q5 and full CV assignments
are held. CS224N is Spring 2024, archive 1246: A3 Q1(i) and A4 Q1-Q2 written
attention/position exploration are selected; remaining written, programming,
and Final Project requirements are held. Never mix Winter 2024 archive 1244.
Its [AI Tools Policy](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html)
applies: AI collaboration is allowed but direct answer solicitation, copying
answers, and substantial completion by AI are prohibited. Check assignment-specific
requirements. Karpathy GPT is an optional conceptual bridge before A1, not a
second full LM implementation. Do not consult other implementations during A1.

P3 centers on tokenization, embeddings, attention, causal masks, Transformer
blocks, next-token targets/CE, sampling, and checkpoint/resume in the same LM.
Distinguish educational core implementation, arbitrary scaled experiments,
and formal A1 requirements under the default or officially permitted low-resource
path. A1 v26.0.3 is pinned in ROADMAP. Its printed pages 40 and 44 permit specific
CPU/MPS and TinyStories adaptations; do not misclassify authorized adaptations
as missing work, apply CPU/MPS targets to CUDA without authority, or call an
arbitrary toy run full official completion. Preserve the existing private clone.

P4 uses A2 v26.1.3 for selected training profiling, memory/FLOPs, mixed precision,
activation checkpointing, FlashAttention-2, and parallelism. A2 is not a serving
assignment. Single-device/scaled results do not complete B200/multi-GPU benchmarks.
Triton backward remains OPTIONAL; the PyTorch/torch.compile backward is separate.
Use CMU as a gap reference, not another mandatory course. Design separate
prefill/decode, KV cache, batching, quality, and operational-load measurements.
Hold all non-independent-variable axes fixed; distinguish cache numerical
tolerance, quantization quality tolerance, fixed-length and EOS request tests.
Early one-variable debugging does not prohibit planned interaction experiments.

After Transformer/PyTorch basics, one bounded SFT/eval comparison can inform
specialization or align with school work. Do not defer split/leakage, uncertainty,
error analysis, dedup/contamination, or held-out evaluation until P5. Independent
DPO/RLVR research needs its own objective, data/reward, optimization and evaluation
prerequisites. Systems / Inference stays provisional; do not require both branches.
P5 combines one question, baseline, controls, ablation, reproduction/variation,
failed cases, paper-vs-local differences and claim limits in one report.

Treat the job-role comparisons as an assessment to re-check against real postings,
without promising employability at any Phase or date; an earlier rung is not a failure.
From P1, compare real required experience and learner-owned work and apply when
they fit. Do not treat other-language backend experience as verified Python/FastAPI
experience, or previous RAG/model comparisons as independent research.

This repository is public and part of it is published as a site, so official
coursework solutions must not land in it. MIT 18.05 problem-set answers and
CS229, CS231n, CS224N, and CS336 assignment solutions belong in separate private
workspaces; preserve existing private clones. This includes written answers,
code, notebooks, and saved outputs, even when self-studying without grades. What may
be published is the learner's own concept notes, reimplementations written from
an empty file, competition work, and research report — never assignment code,
official problem statements, or copyrighted course material. Review publication
rights before staging. Never copy private KANT outlines/content, customer data,
personal profile/education details, internal links, or secrets into public notes.

The KANT materials (`SRC-KAM-*`, `SRC-KDL-*`, `SRC-KBM-*`) are supporting context.
Reuse a matching assignment only when independent quality, assistance and rights
are verified; it cannot replace an explicitly required official problem set.

### CS336 return and boundaries

[Stanford CS336 Spring 2026](https://cs336.stanford.edu/) Assignment 1 remains
pinned to public commit `a158843b20107949f1a8d7df1b05cd33b9166712` (handout v26.0.3).
Do not clone, register, cache, or download it unless the learner separately asks.

Return to the existing assignment when learner work demonstrates:
- constructing, running, and interpreting a small model's training and validation;
- adapting feature or class counts while maintaining Tensor/loss contracts;
- tracing token IDs, embeddings, attention, logits, next-token targets, and masks.

Official API docs are allowed under course policy. Do not impose a second full
tokenizer/Transformer implementation as an entry test. Entry does not cancel
unfinished work or authorize claiming full CS224N/CS231n completion. Apply the
already approved selected route without asking again about removed requirements.

Foundation practice uses this learning lab's Python 3.14 environment.
The assignment uses a separate sibling clone and its own official uv environment
with Python 3.12 or 3.13. Never add it as a lab dependency or install it into this
repository's `.venv`. Check required R and older assignment environments before
entry; do not install them automatically. External GPU consideration includes
VRAM, runtime, device count and official hardware requirements. Paid GPU purchase,
registration or execution needs separate authorization; continue feasible local
work and keep unavailable hardware benchmarks incomplete.

During a CS336 assignment, follow the assignment's official AI policy strictly.
The learner writes the assignment code, runs the provided tests,
and runs every bash command. The AI must not
execute bash commands in the assignment repository. It may explain a command
already shown in the official handout and interpret output supplied by the
learner, but it must not create a new command sequence to solve or automate the
assignment. Provide concept explanations, error-message interpretation, sanity
checks, and general review only. Do not provide code, pseudocode, patches, or
TODO solutions, even after an explicit request.

Review the first 1-2 weeks of the redesign manually for real time, resume
failures, learner-first attempts, execution, transfer and delayed recall.
Documentation checks are not proof of learning; do not automatically switch workflows.

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
question. Standalone STATE updates are still edit-only except at an explicit
study stop. Unrelated changes are excluded unless explicitly included; a chapter
wrap-up alone does not authorize push, while the study-stop procedure does.

### Standalone writing and sources

- Ordinary study may prepare a necessary starting notebook or script for the
  current approved activity under the setup responsibility above. Do not invent
  supplementary exercises or replace official implementations, exercises, or
  assignments with them.
- Other `practice/` artifacts require an explicit learner request or the
  authorized chapter-transition wrap-up's archive and review.
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
  operation or invokes the authorized study-stop procedure (scoped commit and push).
  An explicit or default chapter-transition wrap-up includes its scoped local commit
  as described above. A commit request never implies push permission. Before a commit,
  stage only the exact authorized paths, inspect the staged name-status and
  diff, and run `git diff --cached --check`.
