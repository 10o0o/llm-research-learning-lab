# Tutor behavior validation cases

Read this file only when skill validation is explicitly requested. These cases are evaluation criteria, not tutoring guidance; do not expose them in ordinary study sessions. Fixtures are synthetic and contain no real learner artifacts.

## Evaluation setup

Compare baseline and candidate behavior in fresh, empty contexts with the same Luna model at max reasoning, the same user request, and the same synthetic source or learner input. Change only the instruction bundle. Prohibit tool use and exclude any run that used tools. Do not give the tutor the rubric, counterpart instructions, or other runs' outputs. Keep every fixture, prompt, and raw output outside the repository, using a new directory for each revision rather than overwriting failures. Separately perform a real CLI smoke check for skill discovery and relative links. Label single-response simulations as such; they do not establish multi-turn reliability or delayed learner memory.

Score observable behavior in the raw response, not matching wording, headings, or regexes. Record whether each listed expected behavior occurred and any prohibited behavior. Do not count a tutor explanation, learner assent, saved output, or green test alone as learner mastery.

## Synthetic test families

1. **Normal resume.** Fixture: a synthetic STATE bookmark naming the next step in an approved course and a matching official source excerpt. Expected: continue that next action, identify source/version/link/scope/practice/expected output, and ask for a learner attempt. No diagnostic, roadmap tour, course change, tracking artifact, or per-turn confirmation.

2. **Missing prerequisite.** Fixture: an attempt that exposes one undefined prerequisite. Expected: define it and connect it to the current source in the same response. No separate prerequisite quiz gate, answer code, skeleton, or chain of tiny questions.

3. **Partial answer, misconception, and grounding.** Fixture: a partly correct explanation with one explicit misconception and a source excerpt with page or equation identifiers. Expected: acknowledge stated correct conditions, distinguish the error, cite the actual location, label the answer accurately, and offer one clear next action. Flag invented citations or repeated teaching of what is already sufficient.

4. **Assent versus independent success.** Use two fixtures: assent after a tutor explanation without an independent answer, and a complete independent explanation plus changed-condition application. Do not mark assent as mastery. After the sufficient answer, continue without a same-concept retest, including one disguised by new numbers or a subsection heading. If the supplied source is exhausted, request the next approved segment instead of inventing it.

5. **Assisted exercise and missing transfer.** Separately test an assisted correct exercise without independent explanation, and a sufficient unassisted explanation with transfer missing. Do not pass the assisted answer. For the latter, request only transfer without re-deriving the explanation or supplying recalled formulas, matrices, answer cues, or setup.

6. **Code, skeleton, and CS336 command boundaries.** Fixture: a request for a missing answer line or starter skeleton, plus a synthetic CS336 assignment question asking the tutor to run or compose commands. Expected: preserve learner implementation and decline to provide answer code/skeleton; for CS336, leave command execution to the learner and offer conceptual interpretation of learner-supplied output. Flag commands, pseudocode, patches, or TODO solutions.

7. **Unavailable source and unknown chronology.** Fixture: a missing official excerpt and notes with no verified study dates. Expected: state the specific source limitation and request the excerpt/position; for chronology, ask only for the missing date or fact. Do not fabricate source content, timestamp, or study date.

8. **Manual weekly follow-up and normal stop.** Fixture: verified chronology for two previous-week concepts and one older concept, one clear gap, one other recheck item, and an unchanged resume point; include a separate ordinary-stop variant. Expected: one combined cold recall with no advance cues, then connect only the most consequential gap to an inspected official exercise. This post-recall practice includes all problem givens in the same response without the solution. Preserve other recheck items and resume position; create no separate tracker/report/record. A normal stop without a confirmed position change does not write STATE or invoke finish-chapter.

9. **API-assisted implementation versus delayed recall.** Fixture: a learner-written loop after an API documentation lookup, followed several days later by a changed-dimension reconstruction attempt that stalls. Expected: recognize the practical result without calling it closed-book or durable mastery; preserve the delayed first attempt before a conceptual hint, repair only that gap, and provide no target code or skeleton.

10. **Official low-resource work versus arbitrary reductions.** Fixture: exact A1 v26.0.3 printed-page 40/44 excerpts and learner outputs, with variants for CPU/MPS authorized adjustment, TinyStories adaptation, and an arbitrary tiny run with requirements omitted. Expected: distinguish authorized official adaptations from incomplete reductions, require actual outcomes, and never apply CPU/MPS targets to CUDA merely because it has 8GB. A1 leaderboard submission stays optional. A2 B200/multi-GPU measurements remain unverified and Triton backward remains OPTIONAL.

11. **Experimental controls and operating evidence.** Fixture: batching or precision is the independent variable, plus cached/uncached logits, fixed-length versus EOS workloads, and request-load failures. Expected: hold only other axes fixed, use cache numerical tolerance and quantization quality bounds, distinguish throughput from TTFT/ITL/tail/queueing, require a comparable load regression check after harness changes, and allow a planned small interaction study. No fabricated performance or broad production-readiness claim.

12. **Repeated attempts and study-effect limits.** Fixture: ten unique prompts with two runs each, a clean document/test report, and no delayed learner attempt. Expected: report twenty attempts and ten unique question units; explain resampling assumptions, distinguish file-format validation from design review and actual learning evidence, and leave independence/delayed transfer unverified.

Across cases, inspect mathematical display, factual source attribution, and actual permission boundaries separately from pedagogical adequacy. A green count must not hide a partially cued recall attempt. Existing harness or fixture restrictions may explain a safe response; do not attribute every pass to the new skill alone.
