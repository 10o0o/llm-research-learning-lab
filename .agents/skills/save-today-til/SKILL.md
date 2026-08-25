---
name: save-today-til
description: Parse the canonical ignored draft til/today.md, or an explicitly named repository Markdown draft, into the Korean TIL template, enforce the current coach completeness gate for a handoff-backed draft, save or merge it at til/YYYY/MM/YYYY-MM-DD.md, commit only that dated TIL, and clean up the canonical draft after success. Use only when the user explicitly invokes $save-today-til or asks to finalize, file, or save a named rough note as a daily TIL. Do not use for tutoring feedback, factual or completeness auditing, knowledge-base synthesis, practice recommendations, or generic Markdown editing.
---

# Save Today TIL

Turn one rough study memo into this repository's dated TIL without replacing the learner's thinking with a textbook summary.

Explicit invocation of this skill authorizes exactly one path-limited commit containing the resulting dated TIL. It does not authorize committing any other path or pushing.

## Respect the review boundary

This skill formats and files a draft; it does not establish conceptual correctness.

The handoff schema, lifecycle, readiness gates, evidence rules, and cleanup
conditions are defined only in
[`../coach-llm-research-study/references/lesson-handoff.md`](../coach-llm-research-study/references/lesson-handoff.md).
This skill consumes that contract through the read-only preflight; do not
redefine or bypass it here.

- In the normal daily workflow, use `$coach-llm-research-study` to review the draft against its studied source before invoking this skill.
- Do not perform a source audit merely because no prior review is visible; a standalone save request remains valid, and a TIL may intentionally preserve uncertainty.
- For the canonical draft, always run the read-only preflight below. An active
  handoff requires its current TIL-readiness gate even when the draft contains
  no evidence marker. A separately named draft remains standalone and must not
  alter or remove the active handoff.
- If the current conversation contains a pre-save verdict with unresolved `반드시 수정` or `추가 확인` findings, do not finalize those statements as established facts. Continue only after the learner resolves them, asks to express them explicitly as uncertainty, or knowingly asks to preserve the unverified draft.
- Never treat a `저장 가능` verdict as evidence for `knowledge/`; it only means the draft is suitable as a chronological TIL.

## Resolve the input

1. Work from the repository root.
2. Use the file named by the user. If none is named, use `til/today.md`. Never fall back automatically to root `today.md`; accept it only when the user explicitly names that legacy input.
3. Require a Markdown file inside this repository. Do not read from or write to `archive/` for this workflow.
4. If the default `til/today.md` does not exist, create it with only the reset comment below, report that there is nothing to save, and stop. Treat any other missing input as an error without creating it.
5. Read the entire draft and `til/template.md` before editing anything.
6. Treat an empty file or the reset comment alone as having nothing to save. Report that and make no other changes.
7. Prepare the parsing input without mutating either file:

   ```bash
   python3 .agents/skills/save-today-til/scripts/prepare_til_input.py <draft-path>
   ```

   Omit `<draft-path>` only for canonical `til/today.md`. Stop on any preflight
   error. Parse the printed output, not an independently stripped or re-read
   marker body.

## Choose the date and destination

Use the first applicable date source:

1. an exact date explicitly supplied by the user;
2. one unambiguous `YYYY-MM-DD` study date written in the draft;
3. the current date in `Asia/Seoul`.

Do not use file modification time as the study date. If multiple dates could change the destination and the intended date is unclear, ask before writing.

Save to:

```text
til/YYYY/MM/YYYY-MM-DD.md
```

Use one file per study date, even when the draft contains several topics. Create missing year and month directories. Never derive a topic-based filename.

## Parse into the template

Follow the headings and order in `til/template.md`.

- Put the session narrative, studied material, calculations, and actions under `오늘의 학습`.
- Put conclusions, changed understanding, and personally meaningful takeaways under `배운 점`.
- Put explicit uncertainty, questions, and unresolved contradictions under `남은 질문`.
- Put only next actions the learner actually wrote under `다음에 할 것`.
- Put only real source, knowledge, or practice links under `관련 기록`.
- For a source-based session, preserve each explicitly named source link. When the exact repository source is known from the draft or the reviewed learning context and exists, add or rewrite its link under `관련 기록` relative to the dated TIL.
- Before finalizing a source-based session, require at least one resolvable source link, normally under `materials/`. If the exact source cannot be determined, ask instead of guessing. This requirement does not apply to source-free study such as an independent coding reflection.
- Keep `오늘의 학습`. Omit any other section when the draft contains no supporting content.
- When classification is uncertain, keep the content under `오늘의 학습` instead of inventing structure.
- For multiple topics, use `###` subheadings only when they materially improve scanning.
- When the learner explicitly distinguishes the live lecture from later GPT-assisted study, preserve that provenance with `### 라이브 수업` and `### 보충 학습` under `오늘의 학습`. Do not infer the distinction from writing style alone, and do not add empty provenance headings.

Preserve the learner's first-person voice, uncertainty, examples, equations, code, observed results, and reasoning. Fix mechanical spelling, spacing, paragraph breaks, obvious repetition, and Markdown. Do not silently correct concepts, answer questions, add facts, fabricate links or results, or compress the note into a generic concept summary.

Keep pre-save factual evaluation in `$coach-llm-research-study`, reusable concept synthesis in `$update-learning-knowledge`, and optional activities in `$suggest-learning-practice` unless the user separately requests those tasks.

## Write safely

- If the destination does not exist, create it from the template with all placeholders removed.
- If the destination exists, read it fully and merge new material into the matching sections. Preserve existing content and remove only clear duplication. Never overwrite the file wholesale.
- Resolve relative links from the source location and rewrite them relative to the destination. Do not create a link unless its target is known and exists.
- Use only the preflight output prepared during input resolution. Do not
  reproduce internal envelope comments in the destination, and allow no
  `lesson-evidence` marker in the finalized TIL.
- Use `apply_patch` for the note and other text changes.
- Do not reset the source until the destination passes validation and its dated TIL commit succeeds.
- After those steps succeed, replace the canonical `til/today.md`, or explicitly named legacy root `today.md`, with only:

```markdown
<!-- 형식 없이 자유롭게 작성하세요. 저장할 때 $save-today-til을 사용합니다. -->
```

- Leave every other explicitly named source unchanged, including another directory's file whose basename happens to be `today.md`, unless the user explicitly asks to reset it.
- Do not update `knowledge/`, create a practice file, or push as part of this skill unless the user explicitly requests that separate action.

## Validate, commit, and report

Run from the repository root:

```bash
python3 .agents/skills/save-today-til/scripts/validate_til.py til/YYYY/MM/YYYY-MM-DD.md
git diff --check -- til/YYYY/MM/YYYY-MM-DD.md
```

Read the final file once more, then commit only the exact dated TIL. The final validator already rejects remaining HTML comments, including internal evidence markers.

1. Run `git status --short` and preserve all unrelated worktree and staged changes.
2. Stage only `til/YYYY/MM/YYYY-MM-DD.md`. Do not unstage, discard, or otherwise alter unrelated staged work.
3. Inspect `git diff --cached --name-status -- til/YYYY/MM/YYYY-MM-DD.md` and run `git diff --cached --check -- til/YYYY/MM/YYYY-MM-DD.md`.
4. Commit with `git commit --only -m "til: YYYY-MM-DD 학습 기록" -- til/YYYY/MM/YYYY-MM-DD.md` so unrelated staged changes cannot enter the commit.
5. If the dated TIL has no change to commit, do not create an empty commit. Leave the source unchanged and report that no new commit was created, except for the interrupted-cleanup recovery below.
6. Do not push.

After the commit succeeds:

1. inspect the created commit and require its changed-path set to equal the one dated TIL path;
2. reset the canonical or explicitly named legacy inbox as described above;
3. apply the canonical handoff cleanup condition from the linked contract;
   otherwise preserve `tmp/active-lesson-handoff.md`;
4. read the reset source and report the saved path, whether an existing daily note was merged, the commit hash, the exact committed path, draft and handoff cleanup, and any check that could not be completed.

If validation, staging checks, a commit hook, or the commit fails, do not reset the draft or delete the handoff. Do not create an empty commit and never push.

If a previous invocation already reported an exact successful commit hash but stopped before cleanup, a rerun may finish only the cleanup even though the dated TIL now has no diff. First require that the recorded commit is reachable from the current `HEAD`, its changed-path set is exactly the intended dated TIL, the destination worktree file still matches that commit, and the completed handoff still corresponds to this canonical draft with every confirmed evidence item drafted. If the exact prior commit hash is unavailable or any check differs, preserve the draft and handoff instead of guessing.
