---
name: teach-course-material
description: Deliver an adaptive schema-v10 reviewed lesson from an exact AI, ML, deep-learning, mathematics, or LLM source, capture confirmed learner evidence in the daily-flow cursor, and pause rather than declaring unresolved core concepts complete. Use with coach-llm-research-study for whole named-source lessons. Do not finalize TILs, perform learner-owned practice, update knowledge, or treat delivery and green checks as understanding.
---

# Teach the Reviewed Session

For a whole named-source lesson, first use the coach and require the current
[v10 handoff contract](../coach-llm-research-study/references/lesson-handoff.md)
to pass its teaching-readiness gate. Direct definitions, short corrections,
one-off questions, and knowledge-note deepening remain handoff-free.

## Deliver a meaningful session

- Default to the `standard` 60–90 minute Module Plan. “압축”, “빠르게”, and
  “따라잡기” remain standard without an explicit learner time or format
  constraint. A focused source unit,
  even when its validation anchor is a short page range, is not a reason to
  create a micro lesson.
- Deliver each reviewed module as its bound purpose → explanation → worked
  trace/code walk → learner application block. Keep at most one assessed
  checkpoint in that module.
- Cover motivation, concept model, at least two worked examples in distinct
  representations, a contrast or limitation, and the novel integrated exit.
- Begin an unconfirmed prerequisite with its purpose and one tiny trace, and
  explain it before asking a dependent question.
- Treat `check_policy: none` literally: do not turn its outline or tiny example
  into a hidden learner question or assessment directive.
- Ask an intermediate question only when the answer changes the next
  explanation. Start from the learner attempt and use the smallest helpful
  hint before a fuller explanation.
- For D2 implementation/debugging scope, actually walk the reviewed
  `class Name(nn.Module):`, `def forward(...):`, concrete `nn.*(...)` call, and
  multi-stage Tensor/shape arrow flow. A vocabulary list is not a code walk.
  The walkthrough is teaching, not learner-owned implementation evidence.
- Use only standalone `$$...$$` blocks for learner-facing mathematical
  notation, including short symbols, Tensor shapes, and full relations; inline
  `$...$` is not reliable in this chat renderer. Keep every display block
  renderer-minimal: bare notation such as `h_n` uses one ordinary subscript
  underscore, and only standard ASCII LaTeX operators may appear. Never put
  Korean prose, an API identifier, `\text{...}`, `\_`, or a LaTex line-break
  command inside display math. Do not replace mathematics with raw or escaped
  source text such as `h_t` or `h\_t`, and do not use code blocks merely to
  display a formula. Keep exact identifiers such as `h_n` in literal code only,
  and use surrounding Korean prose for their role. Before sending, scan display
  blocks for `\text{`, `\_`, and doubled backslashes. Code blocks remain for
  executable code, pseudocode, or raw Markdown that the learner explicitly
  requests.
- Preserve the learner's exact answer and put tutor assessment separately.

Delivery is not evidence. Record partial, misconception, and unconfirmed
answers honestly, then change representation and continue. Do not end a normal
session by filing an essential uncertainty under `남은 질문`. If time or the
learner stops, keep the handoff and day-flow cursor `paused` so `계속` resumes
the exact step.

Only confirmed learner-authored answers enter the ignored cursor. Capture them
idempotently with:

```bash
python3 .agents/skills/teach-course-material/scripts/append_lesson_evidence.py \
  tmp/active-lesson-handoff.md --evidence E001
```

This does not write `til/today.md`; that file remains the learner's manual
scratchpad. Complete the handoff only after all non-deferred concepts and the
integrated exit have confirmed, captured evidence. Then the daily flow captures
the session and moves to `DECIDE_PRACTICE`. A single-lesson request stops there;
an authorized full-day flow continues to the practice skill. Never call the
TIL skill automatically at lesson end.
