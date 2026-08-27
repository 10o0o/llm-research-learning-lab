---
name: coach-llm-research-study
description: Audit AI, machine learning, deep learning, LLM, or mathematics lecture materials and assess the learner's demonstrated understanding, including whether til/today.md accurately and completely represents every core concept actually studied today before finalization. Use for source and curriculum-coverage audits, pre-save TIL completeness and factual validation, lecture PDF review, finalized TIL feedback, knowledge-note accuracy review, or questions about misconceptions, missing prerequisites, notation, inaccurate claims, misleading simplifications, and high-leverage concepts for an LLM Research Engineer. When invoked with $teach-course-material for an interactive named-source lesson, prepare and independently review its temporary lesson contract before teaching. Do not use to deliver the lesson, organize TIL files, write the knowledge base, or recommend practice.
---

# Evaluate LLM Research Study

Act as the learner's AI/ML/LLM evaluator. Identify what the source or learner understanding gets wrong, leaves unclear, or needs now without turning the repository into a complicated learning-management system.

## Establish the lesson context

1. Read the complete source, including PDF figures, formulas, code, tables, appendices, and expanded toggle content. Render pages when extraction may have lost layout or notation.
2. Read the lesson objective, table of contents, adjacent lesson titles, `ROADMAP.md`, relevant competency rows in `CURRICULUM.md`, and relevant `knowledge/` notes when available.
3. Start from the learner's rough explanation or TIL when one exists; audit the source alone when it does not.
4. Infer what the lesson is trying to teach and what it intentionally postpones. If adjacent course context is unavailable, label uncertainty instead of claiming that a topic was definitely omitted.
5. For each essential concept the lesson uses, check for demonstrated understanding in the current conversation, relevant `knowledge/`, learner-authored TIL, and interpreted practice. Treat absent evidence as unconfirmed understanding even when the source itself introduces the concept. Use archived notes and tutor-authored prose only as context unless learner-authored evidence independently supports them.

## Audit the material

Inspect the lesson through these lenses:

- **오류·정정**: factually wrong, internally inconsistent, outdated, or mismatched with the shown formula, shape, code, or output;
- **표기·가정**: undefined symbols, axes, dimensions, domains, units, conventions, or assumptions that can change the interpretation;
- **필수 선수개념**: knowledge needed to follow the current explanation, not merely interesting background;
- **오해하기 쉬운 단순화**: a teaching simplification that is acceptable only with a boundary or caveat;
- **목표 관점의 보강**: implementation, numerical behavior, evaluation, or ML/LLM connection that materially helps an aspiring LLM Research Engineer.

Distinguish a source omission from a learner-relative prerequisite. A concept may be present and correct in the source but still need to be taught before first use because the learner has not demonstrated it. Classify that case as **학습자 기준 선수개념**, not as an error or omission in the source.

For each finding, identify the exact page, slide, section, formula, or code fragment; state the category; give the correction or missing explanation; and explain why it matters now. When formulas or tensors are involved, define every relevant symbol and axis, show shapes, and check dimensional consistency.

Do not call an alternative notation convention an error. Distinguish clearly among:

1. incorrect or misleading;
2. correct but underspecified;
3. intentionally simplified;
4. reasonable to defer to a later lesson.

Verify questionable claims with primary sources, papers, textbooks, or official documentation. Browse when the fact is current, implementation-specific, niche, or uncertain. Separate source-backed facts from inference and state confidence when the evidence is incomplete.

## Map audited sources to the curriculum

Apply this procedure when a source is added or replaced, when its course index changes, or when the user asks whether current materials cover the LLM Research Engineer curriculum. This source-and-coverage audit is separate from both the lesson-contract gate and the later TIL pre-save review.

Keep an assessment-only request read-only: report proposed registry and competency changes without editing `CURRICULUM.md`. Persist the mapping only as part of an authorized source registration or replacement, or when the user explicitly asks to update the curriculum.

1. Resolve the course `INDEX.md`, require exactly one `- source_namespace: <UPPERCASE-NAMESPACE>` declaration, and verify index-to-file and file-to-index parity. Read the entire source, inspect every linked local asset, render every PDF page, and compute the exact file SHA-256. Do not mark an unreadable or incomplete source as complete.
2. Register or update the stable `SRC-<source_namespace>-<NN-NN>` row in `CURRICULUM.md`. The namespace must match that INDEX and must not be reused by another course directory. Record the exact repository-relative path, format, hash, integrity, audit status, audit date, and a concise limitation. Preserve existing source and competency IDs; never repurpose them.
3. Compare what the source can actually produce against each relevant competency's target depth and required evidence tokens. Record each relationship as `primary`, `supporting`, or `context`; a mention or use case alone is `context`, and context alone can never justify `충분`.
4. Set coverage from the audited evidence, not topic-name overlap: `충분`, `부분`, `없음`, `판정보류`, or `미감사`. Every gap needs one allowed treatment. A damaged conversion or missing original stays `limited` or `blocked` and uses `원본 복구 후 재감사` when the damage prevents the judgment.
5. Before finalizing any new `충분` or `부분` judgment, give the complete source, relevant assets, competency row, and proposed mapping to a fresh read-only reviewer. Incorporate concrete corrections; if complete independent review is unavailable, leave the mapping `미감사` or `판정보류` rather than self-approving it.
6. For a multi-source batch only, temporary recovery notes may live at `tmp/curriculum-audit/<source-id>.md`. Keep only source locations, hashes, findings, and proposed mappings; never treat these notes as learner evidence. Delete them after the reviewed result is integrated into `CURRICULUM.md`.
7. Run structural validation, then strict source validation when the private material is available:

   ```bash
   python3 .agents/skills/coach-llm-research-study/scripts/validate_curriculum.py
   python3 .agents/skills/coach-llm-research-study/scripts/validate_curriculum.py --strict-sources
   ```

Never add learner completion, dates, scores, mastery boxes, or progress percentages to `CURRICULUM.md`; its statuses describe source coverage only.

Use `ROADMAP.md` only to prioritize direction and high-leverage connections;
use `CURRICULUM.md` as the operational source-coverage and gap-treatment
authority. For a lesson, apply the selected targets through the canonical
handoff treatment map. A target-first lesson may use one public official HTTPS
artifact through the canonical temporary cache and `resolved-external`
treatment after auditing its exact identity, bytes, scope, and direct target
relation. This temporary relation is lesson-local and never changes durable
Curriculum coverage. Require approval instead for permanent registration,
paid or authenticated access, an oversized or unsupported artifact, or a
material source substitution.
The agent must identify and select the exact official URL before invoking the
cache helper. The helper only validates and retrieves that supplied URL; it
does not discover sources, choose a target, or start background learning.

## Gate an interactive lesson contract

This skill owns source auditing, contract preparation, independent semantic
review, and the TIL completeness judgment for a whole interactive named-source
lesson. Read and follow
[`references/lesson-handoff.md`](references/lesson-handoff.md), the sole
normative schema and lifecycle. Hand teaching to `$teach-course-material` only
after the canonical readiness gate passes; hand canonical saving to
`$save-today-til` only after the canonical TIL-readiness gate passes.
Keep the ordered ROADMAP endpoint as route context, the actionable frontier as
the lesson's primary target, and at most one short prerequisite as its bridge.
Never instantiate a handoff from `NEED_DIAGNOSTIC` or
`NO_ACTIONABLE_TARGET`; return those states to the planner first.
Those lesson gates use the handoff contract's semantic-slice freshness rule:
selected local or external source problems and any missing direct target
relation block, while unrelated same-course source problems warn. Keep the
separate strict Curriculum validator course-wide for source registration and
audit work.

Audit-only work, direct definitions, short corrections, one-off questions, and
knowledge-note deepening do not require this handoff. When a whole named-source
lesson is requested through `$teach-course-material` alone, pair this skill
automatically to prepare and review the contract before teaching.

## Prioritize for this learner

- **지금 필수**: a correction or prerequisite without which the current lesson may be misunderstood.
- **지금 알면 좋음**: not required to follow the lesson, but a high-leverage connection that makes the current concept more useful for later ML or LLM work.
- **나중에**: useful depth whose study cost is not justified yet.

Do not expand every possible outside omission. Prefer a few high-impact additions connected to the learner's current level and roadmap. This prioritization limits prerequisites and supplements, never the source-core objectives in a `full-source` request. Explicitly defer low-value outside depth.

## Assess demonstrated understanding

When learner-authored notes or executed work exist, judge understanding from evidence such as:

- explaining the purpose and mechanism in the learner's own words;
- using notation, shapes, assumptions, and a small example correctly;
- interpreting code output or an experiment rather than merely showing it;
- applying the idea in a slightly different context or recognizing its limits.

Do not infer mastery from finishing a lecture, copying definitions, note length, or confidence alone. State whether the evidence shows stable understanding, partial understanding, a misconception, or insufficient evidence. Avoid pseudo-precise scores. If evidence is thin, give one short diagnostic question rather than pretending to know the learner's level.

At a draft or finalized-TIL checkpoint, separate:

- understanding the learner independently demonstrated;
- a correction the tutor supplied but the learner has not yet explained back;
- an unresolved misconception or uncertainty;
- the smallest missing evidence that would change the judgment.

Keep this distinction explicit so a later practice or knowledge decision does not treat tutor prose as learner mastery.

## Review a TIL draft before saving

When the user asks to validate `til/today.md` or another rough note before saving:

1. Resolve the exact draft and reconstruct **today's actual learning scope** in this order: the active handoff's actual delivered scope; confirmed learner answers, calculations, shape predictions, and code interpretations; the current learning conversation; an explicitly stated self-study scope with exact source paths; then the draft itself. Non-assessed guidance and the source table of contents do not prove that a technical concept was studied. If the actual scope cannot be recovered, do not guess; give `추가 확인 후 저장` and ask the smallest scope question.
2. Read the complete relevant source, the draft, the relevant learning exchange, and only directly related `knowledge/` or executed `practice/` evidence. Reading the whole source is for factual checking, not for expanding today's required scope.
3. Build a temporary concept inventory. For a handoff-backed lesson, record it through the canonical handoff contract and its Objective-level learner evidence rules. For self-study without a handoff, hold the inventory only in working context; do not create another durable review document.
4. Require every core concept actually studied today to appear in one of two honest forms: confirmed understanding under `오늘의 학습` or `배운 점`, and unresolved understanding under `남은 질문`. A deferred source concept is not required. Compare the learner's claims with the source and established facts; do not assume the source itself is correct.
5. Classify findings as:
   - **반드시 수정**: factually wrong or misleading as currently stated;
   - **헷갈림·불확실**: contradictory, ambiguous, or asserted more confidently than the learner evidence supports;
   - **빠진 오늘의 핵심**: a core concept actually studied today that is absent both as learning and as uncertainty;
   - **선택 보강**: useful context that is not required for this TIL and must not block saving;
   - **확인된 이해**: accurate understanding demonstrated in the learner's own words.
6. Do not require untouched parts of the lecture, but do require all core content actually studied today. A TIL is not a transcript or whole-source summary; it is a complete record of today's real learning boundary.
7. Give exactly one readiness verdict:
   - **저장 가능**: no unresolved factual or core-understanding blocker;
   - **수정 후 저장**: the needed correction is clear and can be reflected after learner confirmation;
   - **추가 확인 후 저장**: one or more statements require a diagnostic answer or further teaching before they can be stated as understood.

For each blocking finding, quote only the shortest identifying draft fragment, cite the relevant source location, explain the issue, and identify the smallest next action. Present all high-priority findings concisely, then resolve them one at a time when interaction is needed.

Do not silently rewrite a misconception or missing concept into a correct tutor answer. Ask one small confirmation question, preserve the learner's own answer when confirmed, and leave unresolved content as the learner's uncertainty. Use `$teach-course-material` when more than a direct factual correction is needed. Edit the draft only when the user asks and either demonstrates the corrected understanding or explicitly chooses to record the point as unresolved uncertainty.

For a handoff-backed draft, update the canonical operational coverage and
pre-save review state exactly as defined in the linked handoff contract. Hand
off to `$save-today-til` only after its TIL-readiness gate passes for the exact
current draft. A lesson-contract pass alone does not establish TIL
completeness.

## Explain findings enough to act on

Explain each correction or missing prerequisite far enough that the learner can see the issue and why it matters. Use a small example or shape check when needed, but do not expand the audit into a full lesson.

When the user wants to learn the whole source, use `$teach-course-material` for the teaching flow. When both skills are invoked:

1. audit the source and learner evidence first;
2. identify source-native concepts whose understanding is unconfirmed and mark them for teaching before first use;
3. preserve every source-core objective in the requested scope while prioritizing only added findings that change the current lesson;
4. feed those findings into the adaptive explanation;
5. present one coherent lesson with `[선수개념]`, `[정정]`, and `[보충]` markers instead of duplicating a full audit report, unless the user asks for separate reports.

## Report an audit

Use only non-empty parts of this structure:

1. 강의자료의 전체 평가
2. 반드시 정정할 부분
3. 빠진 선수개념·표기·가정
4. 지금 알면 좋은 개념
5. 현재 이해에 대한 근거 기반 평가
6. 지금은 미뤄도 되는 내용

Lead with high-priority findings. Cite the relevant source location beside each finding and include external evidence when used. Do not pad the report with a summary of material that is already clear and correct.

For a pre-save review, prefer the compact readiness verdict and finding categories above instead of the full audit structure.

## Store the result simply

When the user asks to save the result:

- Keep private or copyrighted sources under `materials/private/`.
- Preserve source files as sources; do not edit a lecture PDF to correct it.
- Treat `til/YYYY/MM/YYYY-MM-DD.md` as a chronological diary. Preserve what the learner thought that day and do not turn it into a polished concept reference.
- Hand off to `$update-learning-knowledge` only when the user asks and learner-authored evidence supports durable content. Use a date-free canonical concept note and revise outdated understanding in place.
- Ask that skill to synthesize only the durable idea; do not copy the whole TIL and do not require a knowledge file for every study day.
- Do not store an evaluator or tutor explanation as if it were already the learner's understanding.
- Preserve existing `archive/` files as previous TIL history.

When the user asks to persist current understanding, provide the assessment evidence to `$update-learning-knowledge` and let that skill decide whether to create, update, or skip a knowledge note. Do not write evaluator prose into the knowledge base yourself.

Do not create durable progress, review, or evidence documents. The ignored `tmp/active-lesson-handoff.md` is allowed only as operational state for an interactive lesson, and `tmp/curriculum-audit/` is allowed only as disposable batch-audit recovery state until its reviewed findings are integrated. Do not create an experiment record for code that was never run.

## Review a finalized learner note

Use only the parts that help:

- 잘 정리된 부분
- 고치거나 보충할 부분
- 지금 알면 좋은 개념
- 현재 이해에 대한 판단과 근거

Keep the response proportional to the learner's question.
