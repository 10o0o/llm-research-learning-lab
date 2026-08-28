---
name: teach-course-material
description: Deliver an adaptive schema-v9 reviewed lesson from an exact AI, ML, deep-learning, mathematics, or LLM source, capture confirmed learner evidence in the daily-flow cursor, and pause rather than declaring unresolved core concepts complete. Use with coach-llm-research-study for whole named-source lessons. Do not finalize TILs, perform learner-owned practice, update knowledge, or treat delivery and green checks as understanding.
---

# Teach the Reviewed Session

For a whole named-source lesson, first use the coach and require the current
[v9 handoff contract](../coach-llm-research-study/references/lesson-handoff.md)
to pass its teaching-readiness gate. Direct definitions, short corrections,
one-off questions, and knowledge-note deepening remain handoff-free.

## Deliver a meaningful session

- Default to the `standard` 60–90 minute Module Plan. A small focused review
  slice is not a reason to create a micro lesson.
- Cover motivation, concept model, at least two worked examples, a contrast or
  limitation, at least two learner applications, and an integrated transfer.
- Begin an unconfirmed prerequisite with its purpose and one tiny trace.
- Ask an intermediate question only when the answer changes the next
  explanation. Start from the learner attempt and use the smallest helpful
  hint before a fuller explanation.
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
