---
name: finish-chapter
description: Finish a learning chapter when explicitly requested with $finish-chapter or a phrase such as 이번 챕터 정리해줘. Preserve the saved notebook, write a chapter review, update demonstrated knowledge, reset the workspace after verification, propose STATE, and commit locally after STATE approval. Do not activate for 완료, 이해했어, or 오늘 학습 종료 alone.
---

# Finish a Chapter

This is a repository-local wrap-up, not a course selector or completion database.
Invocation authorizes the chapter's archive, review, knowledge edits, verified
workspace reset, and local commit. It does not authorize push, assignment-code
repair/execution, automatic next-course teaching, or a dated TIL. Explicit narrower
instructions (for example, no reset or no commit) override these defaults.
Course-specific restrictions still apply: never run commands or this helper in
a CS336 assignment checkout or copy that checkout through this workflow.

## Establish the chapter

Read `AGENTS.md`, `STATE.md`, `ROADMAP.md`, the current conversation and saved
`main.ipynb` (or an explicitly named artifact). Read relevant existing knowledge
and index files. Do not mine ignored state, old sessions, or Git history for
learning evidence. Use Git status/diffs only to preserve changes and bound commits.
If the chapter is ambiguous, ask for its scope before mutating anything. A stale
STATE is not evidence that the current conversation did not happen; report its
discrepancy and propose a replacement at the end, without silently editing it.

Identify official implementation/exercises and supplementary work from the actual
requirements. Inspect all relevant cells, saved outputs, and learner explanations.
Separate current saved evidence, results observed earlier in this conversation,
and unverified work. Execution numbers alone neither prove nor disprove execution.
Record assistance accurately; tutor explanations and a passing check alone are
not learner understanding. Do not invent mastery, video viewing, or official grading.
Review public-safe contents without printing secrets or copying private source text.
If sensitive content prevents a public archive, preserve the source and resolve
that specific obstacle before archiving or resetting; do not silently redact history.

## Preserve, explain, and reset

1. Choose `practice/<area>/<chapter>.ipynb` and matching `<chapter>.md`; use a
   stable, descriptive slug. Inspect an existing destination before reuse. Different
   existing contents are a conflict, not permission to overwrite or invent versions.
2. Read source bytes and calculate SHA-256. Keep that exact digest through this
   operation; do not silently recalculate it after a concurrent edit. Archive with:

   ```bash
   uv run python .agents/skills/finish-chapter/scripts/archive_notebook.py --source main.ipynb --archive practice/<area>/<chapter>.ipynb --expected-sha256 <inspected-digest>
   ```

   This preserves bytes, outputs and metadata; it does not run cells. Syntax errors,
   stale outputs, and repeated-training state belong in the review. Do not turn the
   archive into a cleaned solution or claim a fresh-kernel run. An empty workspace
   is not a new chapter; use existing authorized artifacts to resume an interrupted
   wrap-up, or report no new material without generating duplicate records.
3. Write/merge the review using [the review template](references/chapter-review.md).
   Keep confirmed existing content. Cite saved cell numbers (1-based) and distinguish
   conversational observations from content still present in the archived file.
   Do not reproduce the chat transcript or mark unresolved requirements complete.
4. Update reusable concepts using `knowledge/template.md` and existing notes first.
   Cover the chapter's demonstrated range without a fixed concept-count cap. Keep
   process and detailed results in the review, mechanisms and small examples in
   knowledge. `NO_CHANGE` is valid. Do not invoke the standalone TIL/knowledge
   skills indirectly; their separate explicit-only contracts remain unchanged.
   Link the review, notebook and relevant concepts from the existing practice and
   knowledge indexes. Do not create a new catalog, scorecard, or progress manifest.
5. Validate notes and links before reset. Then repeat the archive command with the
   same paths/digest and `--reset`. It requires an already matching archive and
   leaves notebook-level metadata with one blank code cell. Verify the result and
   that the archive remains byte-identical. Never retry a mismatch by accepting a
   new digest without re-inspecting the changed work. Reset covers the saved file,
   not an editor's unsaved buffer or live kernel; avoid editing/saving concurrently.

## STATE approval and commit

Prepare all authorized artifacts and checks first. Show the exact full STATE
replacement as a public resume bookmark, with one next independent action inside
the approved route. Do not include metrics, hashes, transcripts or private paths.
Show changed paths and verification, then request its explicit approval under
AGENTS.md. This is the only routine final approval; it is not a second commit request.
If STATE is already accurate, no replacement approval is needed.

After approval, apply the exact replacement, rerun affected checks and finish the
already authorized local commit. Standalone `STATE 반영해` does not independently
authorize a commit: here that authorization came from the wrap-up invocation.
If approval is declined, preserve the completed artifacts and do not commit the
pending bundle unless the learner explicitly chooses a commit without STATE.

Inspect `git status --short`, diffs and any existing staged changes. Stage only
authorized chapter paths/hunks; never `git add .`. Existing work is excluded unless
explicitly included. Preserve unrelated staged changes too: do not make a normal
commit while they are in the index. Use an isolated temporary Git index populated
from HEAD for the authorized commit if needed, and reconcile only the committed
paths afterward, preserving unrelated index entries and worktree bytes. Mixed
authorized/unrelated changes within one file require hunk-level selection and review.

Check staged name-status, the full staged diff (notebook JSON may be reviewed as
cell/source/output summaries plus byte verification), and `git diff --cached --check`.
Commit as `study: finish <chapter-slug>`; a first skill implementation can use a
descriptive `feat:` message. Verify committed paths and remaining changes. Report
commit ID, archive/review/knowledge links, checks and limitations. Never amend or
push automatically. On validation/commit failure, preserve artifacts and explain
the failure rather than resetting work or claiming completion.

## Validation

Validate changed concept files with the existing validator and check new/changed
relative links in reviews and operating docs. Preserve external source URLs;
report access limitations rather than inventing successful verification.

```bash
uv run python .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py knowledge/<area>/<concept>.md
uv run --frozen pytest -q tests .agents/skills
uv lock --check
git diff --check
git diff --cached --check
```

Tests check archive safety and operating boundaries, not mastery. Do not execute
the learner's notebooks during wrap-up. A schema-valid notebook or successful
commit does not establish that its cells reproduce in order.
