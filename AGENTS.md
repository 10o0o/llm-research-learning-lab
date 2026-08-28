# Repository Guidelines

## Purpose

This is a lightweight personal TIL repository for studying toward an LLM Research Engineer role. Keep learning notes easy to write, find, and revisit. Do not turn the repository into a learning-management system.

## Layout

- `materials/`: source files. Copyrighted or private files belong in ignored `materials/private/`.
- `til/today.md`: ignored local scratchpad for free-form study writing and confirmed learner answers; `$save-today-til` finalizes it. Root `today.md` is an ignored legacy input only when explicitly named.
- `til/`: diary-like learning records organized by date as `til/YYYY/MM/YYYY-MM-DD.md`; keep its template at `til/template.md`.
- `knowledge/`: topic-oriented, mutable notes representing the learner's current best understanding; keep its template at `knowledge/template.md`.
- `practice/`: executed notebooks, Kaggle work, model experiments, and benchmarks; keep its template at `practice/template.ipynb`.
- `ROADMAP.md`: broad learning direction, not a status tracker.
- `CURRICULUM.md`: stable competency targets and audited source coverage, not learner progress or mastery tracking.
- `USAGE.md`: concise instructions for writing TIL notes, storing practice, and using repository skills.
- `archive/`: previous TIL notes; preserve them as read-only history unless the user requests a specific change.

The normal flow is:

```text
select one primary Curriculum target and, only when needed, one bridge target
-> resolve an audited local source or one reviewed temporary official source
-> prepare and independently review one temporary lesson handoff
-> teach at the learner's level -> append only confirmed learner answers to til/today.md
-> review the draft for every core concept actually studied today
-> resolve or mark important uncertainty -> finalize a dated TIL
-> choose the practice action and modality for that target and exact TIL
-> implement, execute, diagnose, and interpret the required evidence
-> update only understanding supported by learner-authored evidence
-> recompute the next target from the new evidence
```

"No extra practice" is valid only when equivalent implementation, execution,
and interpretation evidence already covers the TIL outcomes or there is no
practice-capable outcome. "No knowledge change" remains valid. No daily streak,
promotion status, separate review log, progress table, or canonical-note gate
is required.

## Working rules

- Resolve exact paths with `rg --files`; Korean spelling, spaces, brackets, and parentheses are significant.
- Preserve unrelated working-tree changes.
- Treat review and explanation requests as read-only unless the user asks for edits.
- Use `apply_patch` for text edits.
- Use `tmp/active-lesson-handoff.md` as the only resumable interactive-lesson
  cache. It is ignored operational state, not a durable review, progress, or
  learner-evidence document. Its only normative schema and lifecycle are in
  [the coach handoff contract](./.agents/skills/coach-llm-research-study/references/lesson-handoff.md).
- Preserve the top-level invariant: the coach owns source audit, contract
  preparation, independent review, and TIL completeness; teaching and
  canonical saving may consume the handoff only after their respective
  validator gates pass.
- During a multi-source curriculum audit, `tmp/curriculum-audit/` may hold disposable per-source recovery notes. Delete them after reviewed findings are integrated into `CURRICULUM.md`; they are not learner evidence or progress records.
- Do not relocate, delete, or rewrite existing `archive/` notes in bulk.
- Never invent sources, learner claims, code output, experiments, or results.
- Verify current recommendations such as Kaggle competitions, libraries, models, and tools.
- An unregistered official HTTPS source may be cached only for one reviewed
  lesson under `tmp/active-lesson-sources/<lesson-id>/`. The handoff owns its
  exact identity, hash, scope, target relation, and cleanup. This temporary use
  never changes durable `CURRICULUM.md` coverage or silently registers a source.
- Register private course PDFs under `materials/private/<course>/` with a stable lesson-prefixed filename such as `NN-NN_title.pdf`; verify that the whole file is readable and update that course's local `INDEX.md`. Every course INDEX declares exactly one uppercase `source_namespace`, and each source ID uses `SRC-<source_namespace>-<NN-NN>`. An INDEX may additionally register bounded lesson slices in its `학습 범위` table; those rows route a reviewed lesson to exact included locators and boundary context, but do not establish coverage or mastery.
- Store instructor-provided practice under `materials/private/<course>/course-provided-practice/`; it is source material and must not be mixed with learner or agent-generated work under top-level `practice/`. Map every such file explicitly in that course `INDEX.md` with `Practice path`, `Related lesson path`, `Variant`, `Format`, and `Original`; never infer a relationship from numbering.
- When normalizing a saved Notion HTML page for long-term use, write an expanded Markdown copy with a stable lesson-prefixed name. Preserve headings, toggle children, exact code indentation, output, tables, links, formulas, captions, and content images; discard browser UI assets only after the Markdown package passes a source-to-output integrity check.
- When replacing a PDF with Markdown, preserve every page as a readable lossless page render alongside searchable extracted text. Delete the PDF only after page counts, image links, render dimensions, text extraction, and visual inspection all pass; keep the source whenever conversion is incomplete or questionable.

## Tutoring

- Use `$plan-roadmap-learning` first when the learner asks what to study next or requests a source for an unresolved target. It keeps the ordered ROADMAP endpoint as the long-term destination, chooses exactly one actual primary target, and may add one mostly satisfied inline bridge before resolving sources. A blocking prerequisite becomes the primary target, never a bridge. Source availability affects executability after selection, not target priority. The planner remains read-only. The agent selects an exact official URL when needed; the cache helper only retrieves that supplied URL and never performs discovery or background learning.
- Keep source and understanding evaluation in `$coach-llm-research-study`, adaptive teaching in `$teach-course-material`, hands-on decisions in `$suggest-learning-practice`, and durable concept writing in `$update-learning-knowledge`.
- For source registration, replacement, or `full-source` teaching, read the complete source. For a `focused` lesson, read and review the exact registered or ephemeral slice, its declared boundary context, direct assets, and relevant INDEX/Curriculum/ROADMAP rows; unrelated chapters, appendices, goals, and index entries are outside that lesson's completeness gate. In either mode, inspect relevant `knowledge/` and learner-authored evidence, reorder concepts for understanding, and teach a meaningful chunk. Check understanding only at a knowledge or skill boundary where the answer changes the next teaching move.
- Before first using an essential concept, check for demonstrated understanding in the current conversation, relevant `knowledge/`, learner-authored TIL, and interpreted practice. Treat missing evidence as unconfirmed understanding even when the source introduces the concept; archived notes and tutor-authored prose may provide context but do not establish mastery on their own.
- Teach an unconfirmed essential concept before building on it, starting from the problem it solves and a tiny example. Mark it `[선수개념]` when it appears in the source or is required to follow the source, reserve `[보충]` for useful material outside the source, and use `[정정]` for substantive source corrections.
- When deepening an existing knowledge note, treat it as the learner's starting explanation rather than as an authoritative source; follow its related source when available and verify material claims as needed.
- For reasoning tasks, start from the learner's attempt and use the smallest useful hint, then partial setup, then a full explanation when needed or requested. Fade from worked examples toward independent explanation or transfer as understanding grows. Answer direct definitions and blocking prerequisites directly.
- Start from the learner's note when they provide one.
- Say what is correct, what needs correction, and what useful idea is missing.
- When auditing lesson material, distinguish errors, missing notation or assumptions, required prerequisites, acceptable simplifications, intentional deferrals, and LLM Research Engineer-relevant additions.
- Locate each material finding by page, slide, section, formula, or code fragment. Verify uncertain or implementation-specific claims with primary sources.
- Keep high-leverage concepts worth knowing now in the lesson evaluation; explicitly defer low-value advanced detail.
- Base achievement judgments on learner explanations, correct examples or shapes, interpreted output, and transfer—not on lecture completion or note length.
- Compress ordinary programming basics unless they affect shapes, gradients, numerical behavior, or model meaning. In `full-source` mode, compress explanation depth rather than deleting a source-core objective; even an evidence-backed bridge must be stated in the lesson.
- For difficult topics, connect intuition, a small example, formulas and shapes, code, and actual ML/LLM use.
- In user-facing tutoring and audit responses, treat inline LaTeX as unsupported. Use inline code for short symbols such as `q_i`, `d_k`, and `QK^T`; put typeset formulas in standalone `$$` blocks with blank lines around them and the delimiters on lines by themselves. Never put LaTeX in a heading, table, bullet label, or ordinary sentence, and scan for single-dollar math delimiters before sending.
- Do not treat tutor-generated explanations as proof of learner knowledge. Update `knowledge/` only when explicitly requested and supported by the learner's own explanation, calculation, answer, or interpreted result.
- Before finalizing a TIL, reconstruct today's actual learning scope from the
  canonical handoff when present, learner evidence, the current conversation,
  explicitly named self-study scope, and the draft. Exclude non-assessed
  guidance and distinguish factual errors, learner uncertainty, missing studied
  concepts, optional enrichment, and tutor-supplied explanations.
- Do not require untouched parts of the lecture. Require every core concept actually studied today to appear either as confirmed learning under `오늘의 학습` or `배운 점`, or as unresolved uncertainty under `남은 질문`. Deferred source content is not a TIL omission.
- Give a pre-save verdict of `저장 가능`, `수정 후 저장`, or `추가 확인 후 저장`. Resolve one important misconception at a time with `$teach-course-material`; update the draft only after the learner demonstrates or explicitly confirms the corrected understanding. An unresolved point may instead remain clearly labeled as uncertainty.
- Treat `$save-today-til` as a formatter and filer, not a factual reviewer. In the normal daily flow, run the pre-save review first. If the current conversation still has unresolved blocking findings, do not finalize them as factual claims unless the user explicitly chooses to preserve them as uncertainty.
- After review, distinguish what the learner demonstrated from what the tutor merely corrected. Use only the former as evidence for practice and knowledge decisions.
- Keep hands-on work separate from lesson evaluation. `$suggest-learning-practice` requires one explicitly named, validated `til/YYYY/MM/YYYY-MM-DD.md`; never infer the latest note or accept `til/today.md` or the legacy root draft. Follow its exact source links and stop rather than guessing when a source-based TIL has no resolvable material.
- `$suggest-learning-practice` first returns one practice action and modality.
  Local `NOTEBOOK`, `BENCHMARK`, and `DATASET_PROJECT` modes share exactly one
  `practice/<area>/<topic>.ipynb`; external challenge or competition proposals
  require current verification and approval before account access,
  participation, or submission. `NO_EXTRA_PRACTICE` requires equivalent
  implementation, execution, and interpretation evidence or no
  practice-capable outcome.
- Invoking `$suggest-learning-practice` with an exact finalized TIL authorizes exactly one unexecuted local Notebook when its decision is `CREATE_LOCAL_PRACTICE`. Keep all coherent outcomes as exercises in that Notebook; lack of implementation evidence calls for the smallest Core practice, not more files.
- Map every major TIL outcome to `implement`, `test`, `debug`, `interpret`, or `design`. Use the one Notebook for deterministic calculations, Tensor/Shape mechanics, small training and validation flows, debugging, and local API contracts. Do not create learner `src/`, `tests/`, or a project directory unless the user explicitly asks for a reusable multi-file project outside `$suggest-learning-practice`'s default flow.
- Give every Notebook cell a stable ID and an internal role under `metadata.llm_research_lab.practice`. Keep exactly one unexecuted setup-role cell before the exercises; each exercise keeps its brief, implementation, fixture, `check_e##()`, and reflection cells adjacent.
- Treat the generated Notebook as the learner's complete task interface. Source links are provenance, not required reading: every tested threshold, precedence rule, exact token or key, dtype/device representation, axis or inclusive boundary, aggregation, and error behavior must be stated naturally before implementation. Keep source kinds, Outcome/Requirement/Target IDs, full claims and source anchors, scaffold ownership, cell roles, and assertion traces in custom metadata only; never render them as learner-facing tables, headings, IDs, or code markers. Compression or answer withholding must never hide the problem specification.
- Put folded progressive hints in the Markdown cell immediately beside each TODO, never in a global hint appendix. Read every explicitly mapped basic and advanced instructor practice first, preserve a sound starter/TODO boundary, and use its solution only for contract verification. Provide signatures, deterministic fixtures, tests, repetitive validation, return assembly, and bookkeeping; leave only the TIL-linked core algorithms, Tensor operations, training order, diagnosis, and interpretation learner-owned. Use `guided`, then `partial`, then evidence-backed `independent` scaffolding, with one primary concept and at most three learner targets per Exercise. Track every required written reflection as one of those targets; untracked reflection must be explicitly optional and not a completion condition. Do not overwrite learner work, include a complete answer, invent output, execute a new Notebook, or commit it unless separately asked.
- Before reporting generated practice as ready, validate it and obtain a pass from a fresh read-only reviewer. The reviewer first inspects only the rendered learner surface for natural standalone courseware and audit leakage, then inspects metadata and sources for fidelity and traceability. Permit one revision and one second reviewer only. If review is unavailable or the second review does not pass, do not deliver it as ready.
- When `$suggest-learning-practice` is given an exact practice path for feedback, inspect the saved code and actual traceback or test output, address one blocker at a time, and require state/output interpretation even after tests pass. Do not complete learner-owned core logic without explicit authorization.
- Use Kaggle only when data handling, validation, metrics, or error analysis is the point; use local code or benchmarks for mechanics and systems topics. Verify any current recommendation.
- Only an explicit request to proceed with the **full learning flow** authorizes
  one complete cycle in the current conversation: select the target and exact
  artifact; cache a public official source when allowed; run the reviewed
  lesson and append confirmed learner answers; after `저장 가능`, finalize and
  path-limit commit the exact dated TIL; immediately create one unexecuted local
  practice artifact without committing it; after the learner personally
  implements, executes, interprets, and passes `--completion-ready`, commit only
  that practice path as `practice: complete <artifact-stem>`; update and
  path-limit commit zero to three evidence-backed knowledge notes; preview the
  next target; then end the cycle. Coordinate the existing skills in that
  order; do not create an orchestration skill, snapshot, or progress database.
- The full-flow authorization never permits the agent to supply learner answers
  or perform learner-owned practice. It also excludes permanent source
  registration, paid or authenticated downloads, external participation or
  submission, and push. A request such as `오늘 학습 시작` or `계속` resumes the
  exact active handoff or practice only and does not grant commit authority.
- A whole interactive named-source lesson automatically pairs
  `$coach-llm-research-study` with `$teach-course-material`, even when only the
  teaching skill is invoked. The coach-owned readiness gate must pass before
  teaching starts; direct definitions, short corrections, one-off questions,
  and knowledge-note deepening remain handoff-free.
- For an explicit learning-start or full-flow request, keep repairing an
  evidence-free handoff for the same target and source within that request.
  Locator, wording, objective mapping, and teaching-order findings are
  repairable: update the contract and ask the same independent reviewer for a
  targeted recheck. Only source integrity or access failure, irreducible factual
  ambiguity, or a real user scope decision may stop the flow. A second
  repairable non-pass remains `repair_pending`; if nothing has been delivered
  and no learner evidence exists, shrink once to a micro-slice. `계속` resumes
  that state without requiring a reset phrase or a target ID.
- During that interactive lesson, append to `til/today.md` only a learner-authored answer that has been assessed as confirmed. Keep partial answers, misconceptions, simple agreement, copied tutor wording, source summaries, and tutor assessments in the temporary handoff only; a corrected explain-back is new evidence rather than a rewrite of the earlier attempt.

## TIL, knowledge, and practice

- Treat TIL files as chronological history. Preserve the learner's voice, uncertainty, and what changed that day instead of rewriting them into textbook notes.
- Use one TIL per study day under `til/YYYY/MM/`. Final notes follow `til/template.md`; natural prose is preferred inside its sections and empty optional sections may be omitted.
- When the draft clearly distinguishes them, preserve `### 라이브 수업` and `### 보충 학습` under `오늘의 학습`; do not invent that distinction when it is absent.
- For source-based study, keep an exact resolvable source link under the finalized TIL's `관련 기록`; that TIL is the required entry point for later practice. Every handoff-backed local or external lesson records exactly one `관련 역량` bullet whose backticked value is the exact primary `CC-*` or `TR-*` target, and records one `보충 선수 역량` bullet only when that exact bridge was actually delivered. A temporary external source additionally records its official URL, provider/course, offering or edition, and exact scope. These IDs are routing provenance, not mastery.
- Treat `til/today.md` as a local inbox, not a knowledge artifact. Reset it only after `$save-today-til` has written, validated, and committed the destination. Keep it ignored and untracked.
- Treat `knowledge/` as the learner's current state of knowledge. Use one date-free file per reusable concept and revise outdated understanding in place.
- Synthesize at most a few durable ideas into knowledge notes rather than copying an entire TIL. Not every TIL needs a corresponding knowledge note, and an explicit zero-change result is acceptable.
- Short code may stay in a TIL. Generated local practice uses one metadata-v3 `.ipynb` with its modality, Curriculum targets, stable source IDs, compact implementation, local checks, traces, and interpretation kept together.
- Record only observed results from code that actually ran.
- Keep datasets, model weights, credentials, and large generated files out of Git unless explicitly authorized and appropriate.
- Treat PDFs as sources, not public notes. Include toggle children, figures, code, tables, and formulas when exporting Notion pages.

## Markdown and verification

- Target GitHub Markdown in repository files.
- In repository Markdown files, use `$...$` and `$$...$$` for math. This file-writing convention does not override the no-inline-LaTeX rule for user-facing chat responses.
- Give fenced code blocks a language identifier.
- Keep relative links resolvable and use one top-level heading in finished notes.
- Run the TIL validator when applicable:

```bash
python3 .agents/skills/save-today-til/scripts/validate_til.py path/to/changed.md
```

- Run the knowledge validator when applicable:

```bash
python3 .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py path/to/changed.md
```

- Read changed files, run relevant code, and check `git diff --check` before finishing.
- For PDFs, render and visually inspect the relevant pages.

## Git

Do not commit or push unless the user explicitly asks. A request to commit does not imply permission to push. Explicitly invoking `$save-today-til` or asking to finalize a daily TIL is the narrow exception: it authorizes exactly one path-limited commit containing only the dated `til/YYYY/MM/YYYY-MM-DD.md`, after validation. An explicitly authorized full learning flow adds only the later completion-ready practice commit and evidence-backed knowledge commit defined above. It never authorizes a push, source-registration commit, external submission, unrelated path, or cleanup before the applicable validation succeeds. Stage only exact authorized paths, review the staged diff, and never rewrite history or force-push without explicit authorization.
