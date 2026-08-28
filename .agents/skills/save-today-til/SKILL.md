---
name: save-today-til
description: On the explicit request "오늘 TIL 저장해줘", compose a concept-first Korean daily TIL from completed unconsumed daily-flow cycles, exact practice and knowledge commits, and source/target provenance; review mixed manual material once; then commit only the dated TIL. Also finalize an explicitly named standalone manual draft. Do not run automatically after a lesson, include unfinished cycles, update knowledge, create practice, infer Git history, or push.
---

# Save an Explicit Daily TIL

This skill is not a lesson-end hook. Use it only when the learner explicitly
asks to save today's TIL or names a standalone draft. `til/today.md` is a manual
scratchpad and is never the reviewed-lesson evidence store.

## Daily-flow input

Load `tmp/active-learning-flow.json`. Select completed, unconsumed cycles by
their `completed_on` date; exclude active and paused cycles. For every cursor
recorded learning commit, verify the commit exists and that its committer date,
subject, exact changed-path set, and current artifact match. Do not scan or
summarize unrelated `git log` entries.

Merge only those unconsumed cycles into the exact current dated note. Preserve
already-saved concept history and related provenance without asking the spec to
repeat consumed cycles. During the first v9 save of a legacy dated note,
preserve its visible confirmed content while removing obsolete `남은 질문`,
next-step instructions, and internal markers. Use this order for each new
concept:

1. concept and core definition;
2. validity conditions, mechanism, and limitation;
3. examples and learner applications used to confirm it;
4. observed and interpreted practice result;
5. exact source, practice, knowledge, primary-target, and delivered-bridge
   provenance.

Tutor prose, delivery, file existence, and checker success are not learner
claims. Flow-generated notes must not contain `남은 질문`, “내 말로”
instructions, assessment language, TODOs, or internal markers. Unfinished
learning remains in the cursor instead. If manual scratch or self-study content
is mixed in, ask the coach for one same-flow review and use `mode: mixed` only
after pass.

Use a structured JSON spec and run:

```bash
python3 .agents/skills/save-today-til/scripts/finalize_daily_til.py \
  --spec <daily-til-spec.json>
```

The helper merges `til/YYYY/MM/YYYY-MM-DD.md`, verifies the latest cursor-saved
file hash when one exists, validates the complete result, commits only that path
with `til: YYYY-MM-DD 학습 기록`, then atomically records the new full-file
hash, commit SHA, and consumed cycle IDs in the cursor. It never pushes.
If validation or commit fails, leave the dated file and unconsumed cursor state
for a plain `계속` retry.

For an explicitly named standalone manual draft, preserve genuine uncertainty
after the coach review and use the normal TIL validator and same path-limited
commit rule. Never silently merge unreviewed manual prose into a flow-generated
note.
