---
name: save-today-til
description: Compose a natural Korean TIL from a completed v8 lesson handoff's classified learner evidence, review only mixed manual or standalone material, merge it into til/YYYY/MM/YYYY-MM-DD.md, commit only that dated TIL, and preserve resumable state on failure. Use automatically at the end of an ordinary reviewed lesson with auto-commit, when the learner asks to save or finalize a TIL, or at the TIL stage of a full learning flow. Do not treat tutor prose as learner evidence, update knowledge, create practice, or push.
---

# Save Today TIL

Create one honest chronological note from learner-authored evidence. A reviewed
lesson normally reaches this skill automatically; the learner does not need a
separate draft-review and save conversation.

The handoff schema, evidence classifications, workflow actions, and cleanup
conditions are defined only in
[`../coach-llm-research-study/references/lesson-handoff.md`](../coach-llm-research-study/references/lesson-handoff.md).
Consume that contract rather than restating or bypassing it.

## Authority boundary

`오늘 학습 시작`, `다음 목표로 수업 시작`, and `계속` authorize the current
reviewed lesson through its default dated-TIL-only auto-commit. An exact
handoff field may instead preserve `explicit-request`, selected by a request
such as `저장과 커밋은 요청할 때만`; then compose the draft but wait for a save
request before committing. Explicit `$save-today-til` or a request to finalize
a standalone daily note also authorizes exactly one dated-TIL-only commit.

None of these permissions authorizes push, source registration, practice or
knowledge commits, or unrelated cleanup. Only `전체 학습 흐름 시작` continues
past the TIL into practice and knowledge stages.

## Finish a handoff-generated lesson

1. Read the whole active handoff and its exact draft. Require current schema v8,
   a current lesson-contract pass, completed or honestly paused delivery, and
   the canonical workflow action. Never replace a completed handoff whose TIL
   is not committed.
2. Build a small structured item list from the evidence table:
   - use confirmed learner evidence for technical `learning` claims;
   - use a corrected partial or misconception together with later confirmed
     evidence for `changed-understanding`;
   - use unresolved or partial evidence for `remaining-question`;
   - never add tutor explanations, source summaries, delivery state, checker
     success, or unobserved results as learner claims.
3. Compose atomically:

   ```bash
   python3 .agents/skills/save-today-til/scripts/compose_lesson_til.py \
     tmp/active-lesson-handoff.md --spec <structured-items.json>
   ```

   The helper writes natural Markdown, exact source and target provenance,
   evidence-linked internal markers, the draft hash, and the destination path.
   Pure handoff output uses `handoff-generated` and `review: not-required`.
4. If the inbox also contains manual notes or named self-study material, use
   `mixed`, bind its exact manual-text hash, and have
   `$coach-llm-research-study` review the final composition once in this same
   save flow. Repair clear wording or classification findings without asking
   for a new save request. Stop only when a real factual uncertainty needs the
   learner's choice; otherwise record unresolved material under `남은 질문`.
5. Run the final preflight only after composition:

   ```bash
   python3 .agents/skills/save-today-til/scripts/prepare_til_input.py
   ```

   The second command removes only validated internal markers. Its output is
   final input: do not revise meaning or sentences after it.
6. Under `auto-commit`, or after explicit approval for `explicit-request`, run:

   ```bash
   python3 .agents/skills/save-today-til/scripts/finalize_lesson_til.py \
     tmp/active-lesson-handoff.md
   ```

   Add `--allow-explicit-request` only when the current request supplies that
   approval. The helper merges another same-day session into canonical section
   order, deduplicates exact provenance, validates the result, and commits only
   `til/YYYY/MM/YYYY-MM-DD.md` with `til: YYYY-MM-DD 학습 기록`.
7. Inspect the commit and require its changed-path set to equal the dated TIL.
   Then reset canonical `til/today.md` to its one-line reset comment and clean
   the completed handoff. Preserve an external lesson cache when the explicitly
   authorized full flow still needs it for strict practice provenance;
   otherwise delete only that lesson's exact cache directory after successful
   TIL finalization.

If composition, validation, a hook, or commit fails, keep the draft and handoff.
Do not ask the learner to repeat the lesson or a reset phrase; `계속` resumes at
`COMPOSE_TIL`, `REVIEW_MIXED_DRAFT`, `FINALIZE_TIL`, or `AWAIT_TIL_SAVE`.

## Save a standalone or manual draft

Use the exact file named by the learner, or canonical `til/today.md` when none
is named. Never infer root `today.md`. If canonical input is missing, create
only the reset comment and report that there is nothing to save. Keep every
explicitly named non-canonical input unchanged after saving.

Because standalone text was not generated from a reviewed handoff, invoke
`$coach-llm-research-study` once inside this same save request to check its
actual named study scope, facts, uncertainty, and source links. Apply clear
mechanical corrections that preserve the learner's voice. Do not silently turn
a misconception into a learned claim; keep it as uncertainty or ask the one
learner decision that changes the record. A separate prior “검토해줘” exchange
is not required.

Use the first unambiguous date among an explicit learner date, one date written
in the draft, and the current date in Asia/Seoul. If competing dates change the
destination, ask rather than guess. Save under `til/YYYY/MM/YYYY-MM-DD.md`.

## TIL content rules

Follow [`../../../til/template.md`](../../../til/template.md) section order:

- `오늘의 학습`: session narrative, studied material, calculations, and
  actions;
- `배운 점`: conclusions and changed understanding;
- `남은 질문`: explicit uncertainty and unresolved contradictions;
- `다음에 할 것`: only next actions the learner actually stated;
- `관련 기록`: only exact real source, target, knowledge, or practice links.

Keep `오늘의 학습`; omit empty optional sections. Preserve the learner's
first-person reasoning and observed results. Fix mechanical Korean and
Markdown, but do not create facts, output, or understanding. A handoff-backed
TIL keeps exactly one primary target provenance line, an actually delivered
bridge only, and exact local or temporary-external source identity. These IDs
are routing provenance, not mastery.

For multiple sessions on one date, merge into the existing daily file before
committing each session. Preserve earlier prose and deduplicate identical
source and target lines. Never overwrite a valid daily note wholesale.

## Verify and clean up

For every destination run:

```bash
python3 .agents/skills/save-today-til/scripts/validate_til.py \
  til/YYYY/MM/YYYY-MM-DD.md
git diff --check -- til/YYYY/MM/YYYY-MM-DD.md
git diff --cached --check -- til/YYYY/MM/YYYY-MM-DD.md
```

Read the final file and inspect the exact commit paths. Do not reset the inbox
or delete operational state before the dated TIL commit succeeds. If the
destination has no new change, do not create an empty commit unless the exact
path-only prior commit is being verified to finish interrupted cleanup.

After success, report the dated path, whether a same-day note was merged, the
commit SHA and only changed path, inbox/handoff/cache cleanup, and any check
that could not be completed. Do not update `knowledge/`, create practice, or
push from this skill.
