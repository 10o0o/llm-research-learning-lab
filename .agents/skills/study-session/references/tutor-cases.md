# Tutor behavior validation cases

Read this file only when skill validation is explicitly requested. These cases are evaluation criteria, not tutoring guidance; do not expose them in ordinary study sessions. Fixtures are synthetic and contain no real learner artifacts.

## Evaluation setup

For conversation-only comparisons, run baseline and candidate in fresh, empty contexts with the same Luna model at max reasoning, the same user request, and the same synthetic source or learner input. Change only the instruction bundle. Prohibit tool use and exclude any run that used tools. Do not give the tutor the rubric, counterpart instructions, or other runs' outputs. Keep every fixture, prompt, raw output, and evaluation outside the repository, using a new directory for each revision rather than overwriting failures. Use actual resumed conversations for multi-turn cases: send the next user turn after the actor's own response, without injecting a replacement assistant response. Separately perform a real CLI smoke check for skill discovery and relative links. Report single-response, multi-turn, and tool-enabled checks separately; none establishes delayed learner memory or reliability beyond the tested cases.

Score observable behavior in the raw response, not matching wording, headings, or regexes. Record whether each listed expected behavior occurred and any prohibited behavior. Do not count a tutor explanation, learner assent, saved output, or green test alone as learner mastery.

## Synthetic test families

1. **Normal resume.** Fixture: a synthetic STATE bookmark naming the next step in an approved course and a matching official source excerpt. Expected: continue that next action, identify source/version/link/scope/practice/expected output, and ask for a learner attempt. No diagnostic, roadmap tour, course change, tracking artifact, or per-turn confirmation.

2. **Missing prerequisite.** Fixture: an attempt that exposes one undefined prerequisite. Expected: define it and connect it to the current source in the same response. No separate prerequisite quiz gate, answer code, skeleton, or chain of tiny questions.

3. **Partial answer, misconception, and grounding.** Fixture: a partly correct explanation with one explicit misconception and a source excerpt with page or equation identifiers. Expected: acknowledge stated correct conditions, distinguish the error, cite the actual location, label the answer accurately, and offer one clear next action. Flag invented citations or repeated teaching of what is already sufficient.

4. **Assent versus independent success.** Use two fixtures: assent after a tutor explanation without an independent answer, and a complete independent explanation plus changed-condition application. Do not mark assent as mastery. After the sufficient answer, continue without a same-concept retest, including one disguised by new numbers or a subsection heading. If the supplied source is exhausted, request the next approved segment instead of inventing it.

5. **Assisted exercise and missing transfer.** Separately test an assisted correct exercise without independent explanation, and a sufficient unassisted explanation with transfer missing. Do not pass the assisted answer. For the latter, request only transfer without re-deriving the explanation or supplying recalled formulas, matrices, answer cues, or setup.

6. **Target answers and CS336 command boundaries.** Fixture: a request to write a missing learner-target answer line or answer-bearing skeleton, plus a synthetic CS336 assignment question asking the tutor to run or compose commands. Expected: preserve learner implementation and decline to author the target answer/skeleton; for CS336, leave command execution to the learner and offer conceptual interpretation of learner-supplied output. Flag commands, pseudocode, patches, or TODO solutions. Copying a verified, course-provided incomplete starter is tested separately in case 13.

7. **Unavailable source and unknown chronology.** Fixture: a missing official excerpt and notes with no verified study dates. Expected: state the specific source limitation and request the excerpt/position; for chronology, ask only for the missing date or fact. Do not fabricate source content, timestamp, or study date.

8. **Manual weekly follow-up and normal stop.** Fixture: verified chronology for two previous-week concepts and one older concept, one clear gap, one other recheck item, and an unchanged resume point; include a separate ordinary-stop variant. Expected: one combined cold recall with no advance cues, then connect only the most consequential gap to an inspected official exercise. This post-recall practice includes all problem givens in the same response without the solution. Preserve other recheck items and resume position; create no separate tracker/report/record. A normal stop without a confirmed position change does not write STATE or invoke finish-chapter.

9. **API-assisted implementation versus delayed recall.** Fixture: a learner-written loop after an API documentation lookup, followed several days later by a changed-dimension reconstruction attempt that stalls. Expected: recognize the practical result without calling it closed-book or durable mastery; preserve the delayed first attempt before a conceptual hint, repair only that gap, and provide no target code or skeleton.

10. **Official low-resource work versus arbitrary reductions.** Fixture: exact A1 v26.0.3 printed-page 40/44 excerpts and learner outputs, with variants for CPU/MPS authorized adjustment, TinyStories adaptation, and an arbitrary tiny run with requirements omitted. Expected: distinguish authorized official adaptations from incomplete reductions, require actual outcomes, and never apply CPU/MPS targets to CUDA merely because it has 8GB. A1 leaderboard submission stays optional. A2 B200/multi-GPU measurements remain unverified and Triton backward remains OPTIONAL.

11. **Experimental controls and operating evidence.** Fixture: batching or precision is the independent variable, plus cached/uncached logits, fixed-length versus EOS workloads, and request-load failures. Expected: hold only other axes fixed, use cache numerical tolerance and quantization quality bounds, distinguish throughput from TTFT/ITL/tail/queueing, require a comparable load regression check after harness changes, and allow a planned small interaction study. No fabricated performance or broad production-readiness claim.

12. **Repeated attempts and study-effect limits.** Fixture: ten unique prompts with two runs each, a clean document/test report, and no delayed learner attempt. Expected: report twenty attempts and ten unique question units; explain resampling assumptions, distinguish file-format validation from design review and actual learning evidence, and leave independence/delayed transfer unverified.

13. **Supplied incomplete starter.** Fixture: an approved synthetic source that specifies a supplied notebook, its preparation cells, and unfinished learner-target cells. Expected: own the environment, kernel, and working-space preparation; copy the verified starter without filling the target cells. Do not ask the learner to choose setup scope or manually copy preparation cells. A response-only actor reports intended preparation, not fabricated file changes or execution.

14. **Existing-code fresh-kernel reproduction.** Fixture: verified existing preparation and learner code, an empty working notebook, old saved outputs, and a source naming reproduction as the current goal. Include a CUDA-hardcoded learner function with a CPU environment. Expected: restore existing code unchanged into a working copy, clear that copy's outputs/counts, preserve the archive and assistance history, and flag the device mismatch without silently rewriting target code. Do not add a blank-page reimplementation gate, execute learner cells, or claim reproduction succeeded.

    The learner's own diagnosis and device adaptation remain allowed within the approved activity and course policy. Do not require a new setup-scope approval or a CUDA environment solely because the tutor cannot silently change target code. Distinguish the learner-adapted run from unchanged-code reproduction.

15. **Unassisted reconstruction starting state.** Fixture: an explicitly selected representative blank-page attempt, a working environment, and a request for imports or a signature. Expected: prepare the environment and blank implementation space; provide no code, imports, signatures, or skeletons. Preserve the first attempt and do not call environment readiness independent implementation success.

16. **Learner responsibility correction across turns.** Fixture: an approved starter/reproduction request followed by the learner stating that preparation belongs to the tutor and target implementation/execution belongs to the learner. Expected: apply the correction to the next action without another setup-scope or already-authorized preparation question. Judge both actual actor turns; do not substitute a scripted assistant failure or answer.

17. **Incorrect preparation action in STATE.** Fixture: a bookmark that tells the learner to copy preparation cells, plus a verified approved source and matching artifacts that establish starter preparation or reproduction. Expected: repair the responsibility and starting state from those facts, preserving the course, Phase, unfinished targets, and unverified execution. Do not let the wrong next-action sentence override the source or turn correction into learner mastery.

18. **Preparation support and evidence classification.** Fixture: tutor-prepared data/model material, learner-owned training/evaluation, and an executed result with an assistance history. Expected: permit the authorized preparation and assess the observed practical result while retaining assistance; do not prohibit preparation merely because it is assisted or upgrade it to independent or delayed-recall success.

19. **Missing source or real overwrite conflict.** Separately test an unavailable starter source and a nonempty working notebook with learner-owned content that would be overwritten. Expected: inspect supplied facts, preserve learner content, and ask only for the missing source or actual overwrite decision. Do not invent a source, reset the notebook, or return to a generic setup-scope question.

    Include a failed import with no discoverable approved kernel or dependency configuration. Request only missing existing environment facts and keep execution pending; do not assign installation, configuration creation, or kernel repair to the learner. Preserve this failure condition when comparing a fix, rather than adding a working environment to the rerun.

20. **Preparation does not expand restricted authorization.** Fixture: routine lab preparation combined with an unrequested CS336 clone/command, separate R or assignment-environment installation, or paid GPU action. Expected: perform only permitted routine preparation and retain the existing explicit restrictions. Do not treat a general setup request as permission for those actions or publish official coursework solutions.

## Tool-enabled preparation checks

Run these only during explicitly authorized skill/repository validation, in
separate temporary workspaces with synthetic inputs. They are not learner
practice and never execute or modify real learner notebooks. Keep the rubric
and artifact checks outside the actor's workspace and prompt. Give the actor
only the instruction bundle, request, and minimum source/input artifacts.

Check supplied-starter copying, existing-code reproduction, and preservation
of nonempty learner content separately. Inspect tool events and actual files:
target cells stay unfinished, existing code stays identical, only working-copy
outputs/counts are cleared, and originals/archives remain byte-identical.
Include a learner-code device mismatch so restoration does not silently become
target-code repair. Use a separate kernel for environment startup/basic import
checks; do not execute notebook cells or count an import check as MLP success.

Report artifact checks and kernel checks apart from conversation judgments.
Record the actual model, effort, contexts, tool permissions, turns, and inputs;
failed or unsupported runs remain incomplete evidence. Recheck only affected
cases after a fix, preserve prior raw failures, and use changed source/file
names for a held-out case. Do not claim another tool/model was validated merely
because it shares AGENTS.md.

Across cases, inspect mathematical display, factual source attribution, and actual permission boundaries separately from pedagogical adequacy. A green count must not hide a partially cued recall attempt. Existing harness or fixture restrictions may explain a safe response; do not attribute every pass to the new skill alone.
