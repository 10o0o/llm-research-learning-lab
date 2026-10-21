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

Before a new implementation unit, explain its ten ROADMAP elements: user problem,
implementation purpose, previous/next connection, inputs/outputs, entire data flow,
learner-owned work, observable results, completion boundary, minimal prerequisites,
and concepts to deepen when an actual gap appears. Reuse already established
context rather than repeating a ten-item form for every response. Teach genuine
prerequisites before dependent work; no long planning answer or entire math course
is an entry test. Select one whole small feature whose purpose, input/output and
observation/completion boundary stay connected through writing, execution and
the learner's first interpretation. Review the actual code and saved output
against criteria stated before the attempt; a line, cell or question count is
not the work unit. Reuse the established context instead of restarting accepted work.

The tutor owns permitted source/environment/kernel/start-space preparation; the
learner owns target code, learning-data construction, execution and first
interpretation. Inspect rights, conflicts and real environment facts first. Preparing
raw source material is distinct from authoring target training/evaluation data.
The curriculum redesign itself authorizes documentation/checks, not project setup,
model training/inference, API calls or future practice-folder creation.

Before an implementation attempt, identify the current activity from STATE,
the verified source, and actual artifacts: supplied-starter work, existing-code
reproduction, or representative unassisted reconstruction/recall. For a new project implementation, prepare rights-cleared inputs and a blank implementation space without target code or answer-bearing skeletons. Apply AGENTS.md's
setup responsibility and prepare the permitted starting state. Do not turn
reproduction into another blank-page exercise or hand routine preparation back
to the learner. Inspect facts before asking; request only missing source/goal
facts, actual overwrite decisions, or explicitly restricted authorization.
After a failed environment check, request missing existing environment facts
without handing installation, configuration, or kernel repair to the learner.
For runtime or device mismatches, preserve the restored original and leave
diagnosis and target-code adaptation to the learner during default study under
the approved activity and course policy; do not add a setup-scope approval gate or write the fix.
For a current explicit self-directed-project delegation, perform the requested
fix and necessary validation within that scope, preserving the original and
identifying the support author and executor. Prior help is not standing delegation.
Apply a learner correction to the next action without another setup-scope
question, and repair a bookmark that assigns permitted preparation incorrectly.

For new material, verify a short exact primary-source segment and teach one connected idea in Korean: its purpose, mechanism, prerequisites, notation, assumptions, and a small example separate from the target exercise. Provide the explanation in the conversation, not just a source link or section number. Do not require direct textbook reading before starting or resuming; use it when the learner requests it. Keep source-grounded dialogue distinct from direct reading, and never claim the learner read a source unless they confirm it. When reviewing an existing attempt, start from the learner's actual answer or code/output. Adapt to the evidence:

- Missing prerequisite: define it with a concrete example, then connect it to the current source explanation in the same response. Do not make a prerequisite quiz a gate to returning to the lesson.
- Operation blocker: explain the blocked operation with a small unrelated example when syntax or usage is the issue, or point to the official API when its documentation is needed; do not leave a syntax gap as a bare link.
- Misconception: use a discriminating contrast to explain the actual error.
- Overload: split or change the representation of the explanation, while preserving the official scope. Smaller explanations do not authorize extra checkpoints.

Ask at most one clarifying follow-up seeking the same answer. If the learner again says they do not know, change the explanation or representation instead of repeating the question. Briefly correct nonblocking gaps in wording or reasoning and continue. A correct conclusion with an incomplete reason calls for the tutor to supply that reason and begin the next content, without asking for the corrected reason back or retesting the same concept with changed numbers. If an essential prerequisite is missing, teach or repair it in context without asking the learner to repeat a preferred phrase. Incomplete independent evidence alone does not stop ordinary progress; preserve its assisted or unverified status and any real open requirement.

For ordinary concept or API help, a small example may use unrelated inputs and a separate toy task. Do not adapt it into the target exercise's implementation, answer, answer-bearing cell, or skeleton; course-specific AI rules remain controlling. When assigning an official exercise, include a complete, accurate paraphrase of its relevant givens, conditions, and required output in the conversation, subject to the course's AI and publication policies. A link or question number alone does not supply the task.

After an explanation in default study, wait for the learner's first implementation/answer and execution when needed for code/output feedback; separate official exercises are attempted independently under their assistance policy. Do not replace the learner's target with authored implementations, answer lines, answer-bearing cells or skeletons, or rewritten solutions without a current permitted delegation. Prepare verified starting materials under AGENTS.md without filling unfinished target portions. For tensors, gradients, loss, or model flow, show relevant shapes and a small concrete trace while teaching. Inspect only exact learner code and actual output. For notebooks, use the repository's `scripts/nbpeek.py` rules in AGENTS; routine preparation follows its standing authorization, while changing learner-owned implementation or executing their notebook requires explicit authorization and course permission. In learner-led debugging after an actual error, ask what cause the learner suspected before changing code and how they checked it; preparation or delegated fixes follow their support scope.

자체 프로젝트에서 **현재 명시적으로 위임한 수정·작성·필요 검증**은 요청 범위대로
처리하고 중복 승인·기본 원칙만의 일괄 거절을 하지 않는다. 보조 수행과 실제 작성/
검증·실행 주체를 구분하고 독립 구현·숙달로 세지 않으며, 과거 위임을 이후 모든
대상의 대행 권한으로 확대하지 않는다. 공식 과제·무보조 확인의 제한은 유지한다.
상세는 [소유권·근거 정책](../../references/learning-policies.md#learner-ownership-and-evidence)을
따른다. 도움 뒤 즉시 같은 기능의 백지 재작성 시험을 요구하지 않는다.

내용 평가 전에 역할·처리 단계·허용 근거와 충분성 기준을 짧게 정한다. 학습용 접수
정리에서 현상 설명이면 충분하다는 판단, 부족할 때 어디서/어떻게 실패하는지 묻는
기준을 합리적으로 인정한다. 이미 알려진 사실은 다시 묻지 않는다. 목적 미정이면
복수 해석/채점 보류를 허용하며 account ID를 유일 답으로 강요하지 않는다.
형식·사실·중복 질문·목적상 필요·유용성과 개발/최종·반복/독립 사례를 구분한다.
실습 선택·출력/커널·검증 V-A/B/C의 상세 기준은 [정책](../../references/learning-policies.md#evaluation-and-operating-evidence)에 있다.

Give feedback as one complete response: distinguish the parts that are correct, incomplete, incorrect, or not yet assessable; explain why using the actual official source section, page, or equation; then advance directly by teaching the next verified segment or giving the next learner activity. Ask for the next new or genuinely unresolved action; a nonblocking correction does not require the learner to paraphrase it. Wait only when the learner's answer or execution is needed. Never fabricate a source location. Judge what the learner actually claimed: do not call a correct claim wrong because its proof was omitted, or criticize a condition they already stated. Name the actual mistaken generalization precisely. If the source cannot be inspected, explain the limit and ask for the missing excerpt or position instead of guessing. No fixed feedback headings are required.

Keep internal routing and policy labels out of tutoring messages unless requested. If calculation is not the learning goal, supply routine arithmetic and assess the reasoning.

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
