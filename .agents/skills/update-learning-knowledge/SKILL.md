---
name: update-learning-knowledge
description: Create or update this repository's concise, concept-oriented knowledge notes from understanding the learner has demonstrated in their own TIL, answers, calculations, or interpreted experiment results, then commit only the validated knowledge changes. Use when the user explicitly invokes $update-learning-knowledge, asks to reflect or save verified learning into knowledge/, or an explicitly authorized full learning flow has reached its evidence-backed knowledge stage. Create or update zero to three concept notes, revise existing notes in place, and return no knowledge change when evidence is insufficient or nothing durable changed. Do not use for teaching, source auditing, TIL formatting, or copying tutor prose into the knowledge base.
---

# Update Learning Knowledge

Maintain `knowledge/` as the learner's current demonstrated understanding, not as a transcript of what a lecture or tutor said.

## Resolve the requested scope

1. Work from the repository root and read `knowledge/template.md` and `knowledge/README.md`.
2. Use the TIL, lesson, concepts, or date named by the user. If no source is named, use the current learning conversation and the most recently finalized relevant TIL; do not scan unrelated history.
3. Read only related existing `knowledge/` notes and executed `practice/` artifacts. Search by concepts and relationships before deciding that no note exists.
4. Use source material and `$coach-llm-research-study` findings to check accuracy, but never treat source text or tutor feedback as evidence that the learner understands it.
5. In a full learning flow, run only after the learner has supplied the required
   answer or interpreted practice evidence. The full-flow request supplies the
   update and path-limited commit authorization, but never supplies evidence.

## Separate evidence from instruction

Accept learner-authored evidence such as:

- an explanation of purpose and mechanism in the learner's own words;
- a correct calculation, notation or Tensor-shape account;
- an answer that applies the idea in a slightly changed situation;
- an interpretation of code output, an experiment, an error, or a limitation;
- an explicit correction the learner can now explain, rather than a correction supplied only by the tutor.

Do not count copied definitions, lecture completion, tutor-generated summaries, unexecuted code, confidence, or note length as understanding. Treat a correction from the evaluator as a guardrail, not as learner evidence.

If one short diagnostic answer would materially determine whether a concept is ready, ask only that question and wait before writing. Otherwise defer the concept. Do not manufacture a complete note from partial evidence.

## Choose what belongs in the knowledge base

Select zero to three concepts with the highest reuse value. A concept belongs when it is durable, relevant to the roadmap or future lessons, and supported by the learner's own evidence.

Choose file boundaries by concept, not by study date or source. Split concepts when each can be searched, explained, reused, and extended independently, even if they were learned together. Keep one concept's definition, mechanism, formula, example, and cautions together; do not fragment trivial subparts into separate files.

Return zero changes when:

- no new or corrected understanding was demonstrated;
- the material is a one-day observation rather than reusable knowledge;
- the only accurate explanation came from the tutor;
- an unresolved misconception affects the core idea;
- an existing note already represents the demonstrated understanding.

Do not create one knowledge file per TIL, a progress record, an evidence log, a review file, or an index merely to record that learning happened.

## Locate or create the canonical concept note

1. Search `knowledge/` for an existing note covering the same concept or relationship.
2. Update that note in place when it exists. Merge aliases into one note instead of creating duplicates.
3. Otherwise choose the narrowest useful area such as `math`, `ml`, `deep-learning`, `llm`, or `systems`, and create `knowledge/<area>/<concept>.md` from `knowledge/template.md`.
4. Use a stable, date-free, lowercase kebab-case filename when English terminology is natural. Do not encode course name, lesson number, or study date in the filename.
5. Set `updated` to the current date in `Asia/Seoul`. Keep a few useful tags, not an exhaustive taxonomy.

## Write only the demonstrated range

Use the template headings in order. Require only `핵심 요약` and `개념 정리`; omit every optional section that has no durable content:

- `핵심 요약`: the shortest accurate definition or purpose the learner can support;
- `개념 정리`: a concise reference explanation of the definition, mechanism, formula, Tensor Shape, or distinctions that belong to this concept;
- `예제 또는 적용`: an optional minimal example, shape, interpreted result, or application that helps reconstruct the concept without duplicating a practice artifact;
- `주의점`: optional stable assumptions, failure conditions, or limits that prevent misuse; do not use it for transient confusion, next-study tasks, or a list of experiments not yet attempted;
- `관련 기록`: only resolvable links to directly related knowledge notes, TILs, practice artifacts, or sources worth revisiting; omit when empty.

Use learner-authored evidence to decide what may enter the note, not as content that must be displayed in an evidence section. Keep detailed code, output, and experiment history in `practice/`; retain only the smallest example or observed result needed to make the reusable concept clear.

Present admitted knowledge as a compact reference rather than a diary entry. Use neutral, direct language and organize `개념 정리` with useful `###` subheadings such as `정의`, `원리`, `수식과 Shape`, or `다른 개념과의 차이`. Prefer compact paragraphs, bullets, tables, formulas, and Shape traces according to the concept. Avoid chronological phrases such as “이번 실습에서는”, first-person learning reflections, and prose that exists only to document how the concept was learned.

Preserve the learner's demonstrated scope and conceptual meaning, not their raw wording or narrative order. If part of their account is wrong, include only the verified portion. Defer the update when unresolved uncertainty affects the core explanation; keep ordinary open questions in the chronological TIL or related practice artifact instead of turning the knowledge note into a progress log. Do not paste whole TIL passages, lecture text, evaluator reports, or long tutor explanations.

Revise outdated knowledge in place so the file represents the current best understanding. Keep the chronological record in TIL unchanged. Do not claim calculations, code output, experiments, or transfer that did not occur.

## Write and validate safely

- Use `apply_patch` and preserve unrelated content and links.
- Never edit `archive/`, the source PDF, the finalized TIL, or a practice result as part of this skill.
- Do not create a practice task or push as part of this skill.
- Validate every changed knowledge note from the repository root:

```bash
python3 .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py path/to/knowledge-note.md
git diff --check -- path/to/knowledge-note.md
```

## Commit the knowledge update

After every nonzero knowledge change, commit only the knowledge notes created or updated by the current run:

1. Read every final note once more and ensure that all validators and `git diff --check` pass.
2. Run `git status --short` and preserve all unrelated worktree and staged changes.
3. Stage only the exact changed `knowledge/` paths from the current run.
4. Inspect `git diff --cached --name-status -- <knowledge-paths>` and run `git diff --cached --check -- <knowledge-paths>`.
5. Commit only those paths with the message `knowledge: YYYY-MM-DD 학습 내용 반영`, using the current date in `Asia/Seoul`. Use a path-limited commit so unrelated staged changes cannot enter the commit.
6. If there is no justified knowledge change or the selected notes have no change to commit, do not create an empty commit.
7. Do not push.

Report which notes were created, updated, or deliberately skipped, the learner-authored evidence used, the commit hash and committed paths. If there was no justified change, say so plainly without creating a placeholder or commit.
