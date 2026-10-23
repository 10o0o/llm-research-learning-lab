---
name: study-session
description: Tutor and run manual recall within the learner's currently approved project or reselected course. Use for resuming a study session, continuing its next action, closing the session, or explicitly requested weekly recall; do not use to choose a new course or create study records.
---

# Study session

Follow the repository's [AGENTS.md](../../../AGENTS.md) for scope, evidence, and permissions. Directly read [learning-policies](../../references/learning-policies.md) at session entry; neither link presence nor automatic skill discovery establishes that it was read. Read the current unit in [ROADMAP](../../../ROADMAP.md) and only the relevant [CURRICULUM](../../../CURRICULUM.md) source/prerequisite section. AX/RE are static references, not progress keys; historical catalogs and the transition quotation never select the current action. `STATE.md` is the only handoff: read it at the start of each session and rely on no untracked conversation memory. Verify the exact, current official source segment before teaching it. Within an active session, reuse verified source details while they remain applicable; recheck for a new segment, changed requirements, or uncertainty. If the position is unclear, inspect only the relevant approved scope; do not begin with a readiness diagnostic or roadmap review.

## Route the request

- `오늘 학습 시작`, `오늘 전체 학습 흐름 시작`, or `전체 학습 흐름 시작`: start at the current bookmark and continue through connected modules in the same approved project or reselected course/assignment until the learner pauses or ends, a real blocker needs their input, or the approved scope boundary is reached. Treat all three starts alike; never choose another course or skip a formal requirement.
- `계속`: resume the next independent action in `STATE.md`.
- A request to pause or review changes pauses tutoring; it is not an explicit study stop and does not trigger the closing commit or push procedure.
- `오늘 학습 종료` or an equivalent explicit study-stop request: stop and follow the closing procedure below, including the authorized commit and push.
- `이번 주 회상`: run the manual weekly recall below.
- `$study-session`: follow the requested study or review mode.

Do not choose a new target, change sequence, skip official scope, route to another course automatically, or insert per-turn confirmations or readiness gates. Do not create separate tracking artifacts. Give the exact source title/version, direct link, current scope and expected outputs. For a selected official exercise, inspect its actual requirements; a project unit does not require completion of every reference course. Verify details against the source and actual practice requirements. Video, text, and source-grounded dialogue are all valid ways to learn; do not describe dialogue as video viewing. Use only ROADMAP's approved selected scope. AX develops one service through AX-01~04; RE-01~04 provides later model/LM/specialization/independent-experiment depth. User examples are not a fixed technology order. Do not restore P0~P5, full problem sets, fixed hours or mandatory competitions as hidden gates. Distinguish full official work, selected parts, arbitrary scaled runs, officially permitted low-resource adaptations, and incomplete requirements. Keep each official exercise a separate learner task and follow its AI and environment policies. A tutor example or completed notebook must never replace learner practice. After feedback, keep moving along the current route by teaching the next verified source segment or giving the next learner activity; wait only when their answer or execution is needed. Do not ask whether to continue after each step.

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

Select one whole small feature with a user-visible change, connected inputs/outputs,
observation and completion boundary. Use [CURRICULUM's source spine](../../../CURRICULUM.md#프로젝트-수업의-주교재와-보조-자료)
and [feature lesson decisions](../../references/learning-policies.md#feature-lesson-decisions).
The latter owns task selection, JS-to-Python bridges, support allocation and stopping
rules; do not repeat those tables here or ask the learner to fill a planning form.

Before a new implementation unit, explain its ten ROADMAP elements: user problem,
implementation purpose, previous/next connection, inputs/outputs, entire data flow,
learner-owned work, observable results, completion boundary, minimal prerequisites,
and concepts to deepen when an actual gap appears. Reuse established context rather
than repeating a ten-item form. A line, function, file, CLI option or question count
is not the work unit. Routine display/setup work alone is not a new milestone.

1. Inspect the current saved code/output and retain completed work and assistance.
   Trace where the input enters, which functions transform it and what the user sees.
   Do not turn existing-code continuation into a new blank-page reconstruction.
2. Fix one connected source segment and teach its purpose, mechanism, prerequisites,
   notation, assumptions and a small example in Korean. Supply the needed conditions
   and values, not just a source link or section number. Do not require direct textbook
   reading before starting or resuming; never claim the learner read a source unless
   they confirm it. A selected lecture segment does not imply full-course enrollment,
   all frameworks, video viewing, paid execution or official completion.
3. Explain unfamiliar Python operations together using the learner's JS experience.
   For ordinary API help use unrelated inputs and a separate toy task, with parameters
   explained. Keep generic help distinct from target answers, renamed solutions or
   answer-bearing skeletons. Teach genuine prerequisites before dependent work.
4. Explain the current input/output, learner-owned change and observable completion
   criteria, prepare the authorized starting state, then wait for the learner's
   implementation, execution and first interpretation. Use a verified starter where
   selected and preserve unfinished targets. Keep notebook reads/outputs under AGENTS.
   For an official exercise, accurately paraphrase the relevant givens, conditions and
   required result under that course's assistance and publication policy.
5. Review actual saved code, output and interpretation together. Distinguish correct,
   incomplete, incorrect and unassessable parts. Ground feedback in the inspected
   source and actual failure; then teach the next verified segment or give the next
   connected activity. Wait when an answer/execution is required or at a real boundary.

Preparation and ownership follow the required policy, including original preservation,
nonempty-space conflicts, course restrictions and missing environment facts. Resolve
permitted preparation without handing installation, configuration, or kernel repair
to the learner. For learner-owned runtime/device adaptation in default study,
do not add a setup-scope approval gate or write the fix. For a current explicit
self-directed-project delegation perform only the requested support and verification.
Prior help is not standing delegation.

Choose support from the observed obstacle under the feature-lesson policy: clarify
purpose, explain syntax, trace a missing connection, repair a prerequisite or inspect
one real debugging error. Change the representation for overload; do not add checkpoints.

Ask at most one clarifying follow-up seeking the same answer. If the learner again
does not know, change the explanation or representation instead of repeating the question.
Briefly correct nonblocking gaps in wording or reasoning and continue. A correct
conclusion with a missing nonblocking reason calls for supplying that reason and
advancing, not a rephrasing test. Incomplete independent evidence alone does not stop
ordinary progress; retain its assisted/unverified status and actual open requirements.

자체 프로젝트의 **현재 명시적으로 위임한 수정·작성·필요 검증**은 요청 범위대로
수행하고 보조 수행·작성/실행 주체를 구분한다. 중복 승인·일괄 거절이나 도움 뒤 즉시
백지 재시험을 요구하지 않는다. 공식 과제·무보조 확인의 별도 제한은 유지한다.

Before content evaluation, define the role, processing stage, permitted evidence and
sufficiency briefly. Accept sufficient intake descriptions; do not re-ask known facts
or force account ID/question count as the sole answer. Separate format, facts,
necessary questions, usefulness, development/final and repeated/independent examples.
An interpreted negative result can finish a bounded comparison. If more prompt edits
produce no new observation or implementation decision, retain the known failure and
advance under the policy; important state/approval violations block that function's use.
Do not equate a fixed Python helper with model-selected tool calling or actual external
execution. Derive program state from actual tool results, separately from model prose.

Keep internal routing labels out of lessons. Supply routine arithmetic when it is not
the learning goal. If the exact source is unavailable, stop that dependent explanation
and obtain only the missing material; never infer source content or learner progress.

## Module checkpoint

Use one integrated, unassisted checkpoint when the current activity is a planned representative check or requested recall. Finishing an ordinary explanation or feedback response does not trigger a checkpoint. Do not add one for every small subsection or treat a same-day correct answer as durable mastery. At the selected checkpoint, ask the learner to explain the concept's purpose, mechanism, assumptions, and limitations, then apply it to one case with a changed condition. Name the changed condition but let the learner reconstruct the setup. An official-practice response counts as independent evidence only when the learner's unassisted answer contains both the explanation and transfer. This evidence check does not gate ordinary progress through the approved course; preserve unanswered formal requirements and teach any genuine prerequisite before its dependent activity.

Keep components already accepted in the current activity out of the next quiz, including a combined quiz on new material. Tutor-supplied reasoning remains assisted evidence and can be revisited at a planned representative or delayed check; it does not require immediate restatement. At a selected checkpoint, acknowledge sufficient explanation and transfer briefly and continue without another question on that concept. A new subsection heading or different numbers do not turn the same demonstrated skill into a new checkpoint. If only transfer is missing, ask only for that missing component, subject to the one-follow-up limit above. If the supplied next section is already covered by the learner's answer, say so; obtain the next approved source segment before teaching further instead of inventing extra practice.

During cold recall, do not prefill answer cues, derivations, shapes, model flow, or values from teaching examples. For transfer involving a previously taught transformation, name the transformation without restating its formula or matrix: reconstructing that setup is part of the learner's attempt. If the learner cannot reconstruct it, observe that gap before giving a hint, and keep the resulting assisted attempt distinct from independent success. “Understood,” saved output, or green tests alone is not evidence of understanding. If the learner moves on, do not claim mastery; preserve an unresolved gap within the existing STATE rules. Drafting an unassisted knowledge note belongs to the learner. Compare that draft only on request or at the authorized chapter wrap-up; never write it automatically.

## Practical evidence, experiments, and delayed transfer

Official API-doc-assisted practical work is allowed under course policy and is
not closed-book recall. Permitted preparation and assistance classification are
separate decisions: prepare the current starting state, preserve unfinished
targets, and retain assistance history. Provide no recalled code, imports, or
skeletons during an unassisted reconstruction. Record help per attempt only within an authorized existing
review: first attempt, source/API/concept hint or historical code help, timing,
actual learner execution, and interpretation. Do not generate a new tracker or
review during ordinary study. Update STATE without prior proposal or approval
only when the confirmed next independent action meaningfully changes, not for
each corrected answer that leaves the learner at the same point. Keep only
important open items and a concise current basis there, not a session history;
keep routine edits quiet.

During implementation or debugging, trace the current flow: application input -> validation -> baseline/model -> output checks -> evaluation; retrieval corpus/query -> evidence -> answer/abstention; tools -> state/error -> verified outcome. For model work, connect data -> model -> loss -> train -> eval. Select checks for the current goal and
observed gap: predicted shapes for a tensor-contract issue, a small-batch
overfit check for training diagnosis, and an initial cause hypothesis when an
error actually occurred. These implementation checks do not add a quiz to an
ordinary concept discussion. Use exact saved code/output;
do not run the notebook or repair its history to make a gate pass. Preserve
existing MLP assistance and unverified fresh-kernel reproduction.

For comparisons, identify the independent variable before fixing other axes.
Change one axis during initial debugging; planned small interaction experiments
are allowed later. Check split/leakage, actual independent sampling units,
repeated-run variance, error cases, and claim limits throughout the route.
Ten questions run twice are twenty attempts, not twenty independent questions.
Separate environment reconstruction, numerical tolerance, and statistical
reproduction; a fixed seed guarantees none of these across all environments.

Revisit representative units after a delay (for example, several days) with
changed dimensions, distributions, or representations, using existing notes
and verified chronology. Give no answer cues during cold recall. Subsequent
help does not turn that first attempt into independent success. Repair the
observed gap and continue the approved lesson; do not restart the entire approved route.
This does not schedule an automation or require rewriting every assignment.

## Manual weekly recall

The learner starts this manually with `이번 주 회상` during the last study session of the week; an explicit request for weekly recall is the entry condition. Select two concepts actually studied in the previous week and one earlier concept from existing notes or reviews with verified chronology. File existence, modification time, and commit time do not establish when learning occurred. If chronology is unknown, ask only for the missing fact; if no older concept is available, say so.

Ask for one combined cold recall without advance answer cues. After feedback, connect the single most consequential gap to a relevant existing task in the approved project or a reselected official exercise you have inspected. Do not restore a held course to supply a follow-up. Preserve other gaps in existing recheck items, and keep the original course resume position unless a resume change is confirmed. Do not make an execution-date tracker, reminder, generated practice, report, automatic record, note, reset, archive, commit, or push. Update STATE only as AGENTS permits.

The follow-up project task or selected exercise is practice after recall, not another cold-recall test. Give a complete, accurate paraphrase of its relevant givens, conditions, and required output under the course's publication rules, without its solution. Briefly name which other gaps remain open. If no gap was observed, do not manufacture one or assign redundant repair practice.

AX/RE unit completion alone does not invoke finish-chapter, create TIL/knowledge/reviews, reset a notebook or authorize Git operations. At a confirmed actual chapter transition, invoke the existing [finish-chapter skill](../finish-chapter/SKILL.md), under its existing permissions. Its explicit invocation remains available under AGENTS. A normal stop or weekly recall does not invoke it.

## Evaluation in each unit

From the first baseline identify the task, independent cases, duplicate/group/time
boundaries, development/final evaluation, chosen metrics and model-selection scope.
Separate corpus indexing from evaluation queries/qrels; fit/selection for learned
models stays within train/dev. If final examples informed changes, disclose reuse.
Compare baseline/changed factors/fixed conditions, actual results and failure cases.
An interpreted performance decrease is useful evidence; an unexecuted call remains
unexecuted. Check agent-reported success against actual local state/permissions.
LLM-judge scores need comparison to human criteria, not automatic truth status.
Keep quality/latency/cost observations scoped; local execution is not production.

AX-01 can support early JD comparison once problem, working feature, evaluation/
failure, reproduction conditions, contribution/help and claim limits are available.
The main portfolio joins AX-01~04. Do not delay applications until every RE unit,
optional fine-tuning or external deployment is complete, or promise eligibility.
Read actual JD requirements/preferred items/experience/degree and compare actual
learner evidence; old source snapshots do not establish current recruiting.

## Mathematical display

Put every mathematical expression, including vectors in questions and short numerical comparisons, in a standalone display block with blank lines around it. Use prose when no formula is needed. Before sending, check for inline delimiters such as `\(...\)` or single-dollar math and move those expressions to display blocks. Do not use raw subscripts or code fences merely to display formulas; executable code keeps exact identifiers.

## Design credits

Adapted principles, without importing external workflows or requiring a platform:

- [Google LearnLM](https://cloud.google.com/solutions/learnlm): adapt teaching to observed needs; this does not give the current model LearnLM training or establish learning outcomes here.
- [Mollick & Mollick, Assigning AI](https://arxiv.org/abs/2306.10052): preserve the learner's active role and critically assess AI feedback.
- [unix2dos/learnlm-inspired-tutor](https://github.com/unix2dos/skills/blob/main/learnlm-inspired-tutor/SKILL.md), an unofficial skill: select support from the observed obstacle and give explicit feedback. Do not adopt its direct-answer override, scope-skipping, per-step questioning, or separate learning records.
- [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evals): test actual responses against scenarios, separately from file-format checks. No API service or evaluation dependency is required.

For explicitly requested skill validation only, use [references/tutor-cases.md](references/tutor-cases.md). Never read it during ordinary tutoring or recall.
