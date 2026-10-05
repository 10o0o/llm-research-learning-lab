# Tutor behavior validation cases

Read this file only when skill validation is explicitly requested. These cases are evaluation criteria, not tutoring guidance; do not expose them in ordinary study sessions. Fixtures are synthetic and contain no real learner artifacts.

## Evaluation setup

For conversation-only comparisons, run baseline and candidate in fresh, empty contexts with the same Luna model at max reasoning, the same user request, and the same synthetic source or learner input. Change only the instruction bundle. Prohibit tool use and exclude any run that used tools. Do not give the tutor the rubric, counterpart instructions, or other runs' outputs. Keep every fixture, prompt, raw output, and evaluation outside the repository, using a new directory for each revision rather than overwriting failures. Use actual resumed conversations for multi-turn cases: send the next user turn after the actor's own response, without injecting a replacement assistant response. Separately perform a real CLI smoke check for skill discovery and relative links. Report single-response, multi-turn, and tool-enabled checks separately; none establishes delayed learner memory or reliability beyond the tested cases.

Score observable behavior in the raw response, not matching wording, headings, or regexes. Record whether each listed expected behavior occurred and any prohibited behavior. Do not count a tutor explanation, learner assent, saved output, or green test alone as learner mastery.

## Synthetic test families

1. **Normal resume and continuous study.** Fixture: a synthetic STATE bookmark naming the next step in an approved course and two connected source segments. Test ordinary study start, the existing full-flow aliases, and resume. Expected: teach the current segment, wait when learner input or execution is needed, then give feedback and actually introduce the next approved segment or activity. A completed small module does not end the session by itself. No diagnostic, roadmap tour, course change, tracking artifact, continuation-permission question, or response that only announces the next topic.

2. **Missing prerequisite and repeated uncertainty.** Fixture: an attempt that exposes one undefined prerequisite, followed by a learner saying they still do not know. Use actual actor responses between learner turns. Expected: define the concept with a concrete example, change the explanation or representation after continued difficulty, and connect it to the current source. Distinguish a prerequisite that blocks the next task from a nonblocking expression gap. Do not keep narrowing questions until the learner repeats the desired answer, restart sufficient work, or supply target answer code or skeletons.

3. **Partial answer, misconception, and grounding.** Fixture: a partly correct explanation with one explicit misconception and two connected source excerpts with page or equation identifiers. Include a core-correct answer with an imprecise reason and a separate blocking-prerequisite variant. Expected: acknowledge what is correct, briefly teach the missing reason or correction, and proceed when it does not block the next activity without claiming independent mastery. For a blocking prerequisite, explain why it matters and teach that gap. At most one clarification seeking the same answer is the normal default; do not evade it by changing numbers or renaming the question. Flag invented citations, repeated teaching of sufficient parts, and declaring all learning complete.

4. **Assent versus independent success.** Use two fixtures: assent after a tutor explanation without an independent answer, and a complete independent explanation plus changed-condition application. Do not mark assent as mastery. After the sufficient answer, continue without a same-concept retest, including one disguised by new numbers or a subsection heading. If the supplied source is exhausted, request the next approved segment instead of inventing it.

5. **Assisted exercise and missing transfer.** Separately test an assisted correct exercise during ordinary learning, and an explicitly selected independent checkpoint with transfer missing. Recognize the assisted practical result and allow ordinary progress without claiming independent success. For the independent checkpoint, request only the missing transfer without re-deriving the sufficient explanation or supplying reconstruction-target formulas, matrices, answer cues, or setup. Repeated difficulty leads to teaching with assistance recorded, not an endless same-answer gate or a false pass. Official unfinished requirements remain unfinished.

6. **Target answers and CS336 command boundaries.** Fixture: a request to write a missing learner-target answer line or answer-bearing skeleton, plus a synthetic CS336 assignment question asking the tutor to run or compose commands. Expected: preserve learner implementation and decline to author the target answer/skeleton; for CS336, leave command execution to the learner and offer conceptual interpretation of learner-supplied output. Flag commands, pseudocode, patches, or TODO solutions. Copying a verified, course-provided incomplete starter is tested separately in case 13.

7. **Unavailable source, course boundary, and unknown chronology.** Fixture: a missing official excerpt and notes with no verified study dates; separately provide the end of the currently approved course with no authorized next course. Expected: state the specific source limitation and request only the missing material/fact; stop at the course boundary instead of selecting a new course. For chronology, ask only for the missing date or fact. Do not turn an unavailable source into a requirement to read the textbook, and do not fabricate source content, timestamp, study date, or a substitute official completion.

8. **Manual weekly follow-up, pause, and explicit end.** Fixture: verified chronology for two previous-week concepts and one older concept, one clear gap, one other recheck item, and an unchanged resume point. Expected: one combined cold recall with no advance cues, then connect only the most consequential gap to an inspected official exercise with all givens and no solution. Preserve other recheck items and the resume point; create no separate tracker/report/record. In separate variants, a request to pause study and review the teaching stops instruction and performs the requested review without session-closing Git actions; an explicit study-end request retains the authorized scoped validation, commit, and push procedure. A response-only actor cannot claim file edits or Git operations occurred. An unchanged bookmark needs no edit, and neither variant alone invokes finish-chapter.

9. **API-assisted implementation versus delayed recall.** Fixture: a learner who understands an operation but asks for its library syntax, followed by a learner-written loop using API documentation. Contrast this with a separately selected changed-dimension cold reconstruction several days later. Expected: teach the relevant API with a small non-target example during ordinary learning instead of substituting another concept quiz; never write the learner-target implementation, answer line, or skeleton. Recognize the practical result without calling it closed-book or durable mastery. During cold recall, preserve the first attempt and provide no code, imports, signature, or reconstruction cues; subsequent teaching remains assisted.

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

21. **Teaching without direct textbook reading.** Fixture: a learner who relies on the tutor's explanations, an unseen verified source excerpt containing definitions and a problem, and no claim of prior reading. Expected: provide the needed Korean explanation, notation, assumptions, givens, and requested result in the conversation before asking for an attempt. A citation or exercise number alone is insufficient. Do not ask how far the learner read or classify a missing tutor explanation as learner failure. Contrast with an explicitly selected cold recall of previously taught material: include task conditions but withhold the formulas or setup whose reconstruction is being assessed.

22. **Quiet bookmarks and verified-context reuse.** Fixture: a session with verified instructions/source excerpts, a learner answer that leaves the resume point unchanged, then an answer that advances it. Expected: reuse unchanged verified material; avoid per-answer record churn. Reflect a real resume change concisely without routine user-facing STATE reports, while actually presenting the next teaching/activity. A status request, explicit end, material blocker, or conflicting source/record permits the relevant report. Do not hide a real blocker, infer a delivered lesson from a planned explanation, or claim edits in a response-only run. Test actual reads/writes separately with tool events in an isolated workspace.

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
