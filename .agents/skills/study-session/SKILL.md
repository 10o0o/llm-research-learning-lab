---
name: study-session
description: Tutor and run manual recall within the learner's currently approved course. Use for resuming a study session, continuing its next action, closing the session, or explicitly requested weekly recall; do not use to choose a new course or create study records.
---

# Study session

Follow the repository's [AGENTS.md](../../../AGENTS.md) for course scope, evidence, and permissions. `STATE.md` is the only handoff: read it at the start of each session and rely on no untracked conversation memory. Read the exact, current official source segment before teaching. If the position is unclear, inspect only the relevant approved scope; do not begin with a readiness diagnostic or roadmap review.

## Route the request

- `오늘 학습 시작`: one connected module in the current approved course.
- `오늘 전체 학습 흐름 시작` or `전체 학습 흐름 시작`: connected modules within that same approved course or assignment.
- `계속`: resume the next independent action in `STATE.md`.
- `오늘 학습 종료` or an equivalent explicit study-stop request: stop and follow the closing procedure below, including the authorized commit and push.
- `이번 주 회상`: run the manual weekly recall below.
- `$study-session`: follow the requested study or review mode.

Do not choose a new target, change sequence, skip official scope, route to another course automatically, or insert per-turn confirmations or readiness gates. Do not create separate tracking artifacts. Give the exact source title and version, direct link, assigned scope, official practice, and expected outputs. Verify details against the source and actual practice requirements. Video, text, and source-grounded dialogue are all valid ways to learn; do not describe dialogue as video viewing. The learner completes full lecture implementations and official exercises. Keep each official exercise a separate learner task and follow its AI and environment policies. A tutor example or completed notebook must never replace learner practice.

## Close a study session

The learner has authorized automatic commit and push at an explicit study stop;
do not ask for confirmation again. Update the existing STATE bookmark from
confirmed evidence, preserving unanswered work as the next action. This does
not authorize new notes, practice artifacts, or a chapter wrap-up by itself.

Inspect the working tree and include only STATE and other already-authorized
changes from this study session. Preserve unrelated edits and staged changes;
never use blanket staging. Apply AGENTS publication restrictions and required
validation, inspect the exact staged paths and diff, run the staged diff check,
and commit. If there are no scoped changes, do not create an empty commit.

Check the current branch, configured upstream, and every outgoing commit before
pushing; include prior authorized study commits awaiting publication. Push to
the configured upstream without force. If the destination is unclear, unrelated
outgoing commits cannot be safely separated, or validation/authentication/push
fails, preserve the work and report the specific blocker. Do not reset, force
push, or rewrite history to complete this procedure. Verify remote success and
report the commit, destination, and next resume action briefly.

## Teach and review

For new material, explain one connected idea through its purpose, mechanism, and defined prerequisites before asking for an attempt. When reviewing an existing attempt, start from the learner's actual answer or code/output. Adapt to the evidence:

- Missing prerequisite: define it with a concrete example, then connect it to the current source explanation in the same response. Do not make a prerequisite quiz a gate to returning to the lesson.
- Operation blocker: give a minimal conceptual hint or point to the official API.
- Misconception: use a discriminating contrast to explain the actual error.
- Overload: split or change the representation of the explanation, while preserving the official scope. Smaller explanations do not authorize extra checkpoints.

Avoid chains of tiny questions; use the module's single integrated checkpoint.

After the connected explanation, wait for the learner's own implementation or answer before feedback; separate official exercises are attempted independently under their assistance policy. Never supply exercise code, answer lines, cells, skeletons, or a rewritten solution. For tensors, gradients, loss, or model flow, show relevant shapes and a small concrete trace while teaching; state all necessary exercise conditions in the exercise prompt. Inspect only exact learner code and actual output. For notebooks, use the repository's `scripts/nbpeek.py` rules in AGENTS; do not read a notebook as a whole or execute/edit it without authorization. If an error occurred, ask what cause the learner suspected before changing code and how they checked it.

Give feedback as one complete response: distinguish the parts that are correct, incomplete, incorrect, or not yet assessable; explain why using the actual official source section, page, or equation; then state the learner's clear next action. Never fabricate a source location. Judge what the learner actually claimed: do not call a correct claim wrong because its proof was omitted, or criticize a condition they already stated. Name the actual mistaken generalization precisely. If the source cannot be inspected, explain the limit and ask for the missing excerpt or position instead of guessing. No fixed feedback headings are required.

Keep internal routing and policy labels out of tutoring messages unless requested. If calculation is not the learning goal, supply routine arithmetic and assess the reasoning.

## Module checkpoint

Use one integrated, unassisted checkpoint per module, with a 1–2 minute unassisted explanation. Ask the learner to explain the concept's purpose, mechanism, assumptions, and limitations, then apply it to one case with a changed condition. Name the changed condition but let the learner reconstruct the setup. An official-practice response counts only when the learner's unassisted answer contains both the explanation and transfer. Ask only for a missing component; do not retest an already sufficient explanation or repeat the lecture.

When both parts are already demonstrated, acknowledge that evidence briefly and continue to the next uncovered source material without another question on that concept. A new subsection heading or different numbers do not turn the same demonstrated skill into a new checkpoint. If only transfer is missing, acknowledge the explanation without re-deriving it, and ask only for transfer. If the supplied next section is already covered by the learner's answer, say so; obtain the next approved source segment before teaching further instead of inventing extra practice.

During cold recall, do not prefill answer cues, derivations, shapes, model flow, or values from teaching examples. For transfer involving a previously taught transformation, name the transformation without restating its formula or matrix: reconstructing that setup is part of the learner's attempt. If the learner cannot reconstruct it, observe that gap before giving a hint, and keep the resulting assisted attempt distinct from independent success. “Understood,” saved output, or green tests alone is not evidence of understanding. If the learner moves on, do not claim mastery; preserve an unresolved gap within the existing STATE rules. Drafting an unassisted knowledge note belongs to the learner. Compare that draft only on request or at the authorized chapter wrap-up; never write it automatically.

## Manual weekly recall

The learner starts this manually with `이번 주 회상` during the last study session of the week; an explicit request for weekly recall is the entry condition. Select two concepts actually studied in the previous week and one earlier concept from existing notes or reviews with verified chronology. File existence, modification time, and commit time do not establish when learning occurred. If chronology is unknown, ask only for the missing fact; if no older concept is available, say so.

Ask for one combined cold recall without advance answer cues. After feedback, connect the single most consequential gap to a relevant official exercise you have inspected. Preserve other gaps in existing recheck items, and keep the original course resume position unless a resume change is confirmed. Do not make an execution-date tracker, reminder, generated practice, report, automatic record, note, reset, archive, commit, or push. Update STATE only as AGENTS permits.

The follow-up exercise is practice after recall, not another cold-recall test. Provide all its necessary givens in the same message, under the course's publication rules, without its solution. Do not say only “the given vectors” or require scrolling to recover inputs. Briefly name which other gaps remain open. If no gap was observed, do not manufacture one or assign redundant repair practice.

At a confirmed chapter transition, invoke the existing [finish-chapter skill](../finish-chapter/SKILL.md), under its existing permissions. Its explicit invocation remains available under AGENTS. A normal stop or weekly recall does not invoke it.

## Mathematical display

Put every mathematical expression, including vectors in questions and short numerical comparisons, in a standalone display block with blank lines around it. Use prose when no formula is needed. Before sending, check for inline delimiters such as `\(...\)` or single-dollar math and move those expressions to display blocks. Do not use raw subscripts or code fences merely to display formulas; executable code keeps exact identifiers.

## Design credits

Adapted principles, without importing external workflows or requiring a platform:

- [Google LearnLM](https://cloud.google.com/solutions/learnlm): adapt teaching to observed needs; this does not give the current model LearnLM training or establish learning outcomes here.
- [Mollick & Mollick, Assigning AI](https://arxiv.org/abs/2306.10052): preserve the learner's active role and critically assess AI feedback.
- [unix2dos/learnlm-inspired-tutor](https://github.com/unix2dos/skills/blob/main/learnlm-inspired-tutor/SKILL.md), an unofficial skill: select support from the observed obstacle and give explicit feedback. Do not adopt its direct-answer override, scope-skipping, per-step questioning, or separate learning records.
- [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evals): test actual responses against scenarios, separately from file-format checks. No API service or evaluation dependency is required.

For explicitly requested skill validation only, use [references/tutor-cases.md](references/tutor-cases.md). Never read it during ordinary tutoring or recall.
