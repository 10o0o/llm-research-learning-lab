---
name: coach-llm-research-study
description: Audit AI, ML, deep-learning, LLM, or mathematics sources and prepare or independently review the schema-v10 lesson contract. Also review mixed manual or standalone TIL material when explicitly saved or assessed. Use with teach-course-material for a whole named-source lesson. Do not teach, write knowledge, recommend practice, turn tutor prose into evidence, or re-review a pure daily-flow TIL composition.
---

# Audit Sources and Own the Lesson Contract

Read the sole normative [lesson handoff contract](references/lesson-handoff.md)
completely before preparing or reviewing `tmp/active-lesson-handoff.md`.
At a daily-flow boundary, also read the
[daily learning flow contract](references/daily-learning-flow.md).

## Source and target audit

- Resolve exact paths and registry rows. Verify hashes and relevant rendered PDF
  pages or Markdown assets.
- Distinguish errors, assumptions, required prerequisites, acceptable
  simplifications, intentional deferrals, and useful LLM Research Engineer
  additions.
- In `focused` mode, audit only the selected coherent topic, section, or example
  family, its boundary units, direct assets, and related INDEX/Curriculum/ROADMAP
  rows. Each unit has one source-anchor locator for mechanical validation; do not
  turn that anchor into a page-by-page lesson checklist. This limits review cost;
  it never shortens the teaching session.
- In `full-source` mode, preserve every source-core objective.
- Locate every finding precisely and verify unstable technical claims with
  primary sources.
- In learner-facing audit or lesson-preparation prose, place every mathematical
  symbol, shape, or relation in a standalone `$$...$$` block. Inline `$...$`
  is not reliable in this chat renderer. Keep each display block
  renderer-minimal: use bare notation such as `c_t` with one ordinary subscript
  underscore and standard ASCII LaTeX operators only. Never put Korean prose,
  API identifiers, `\text{...}`, `\_`, or a LaTex line-break command inside
  display math. Raw or escaped notation such as `c_t` or `c\_t` must not stand
  in for rendered math. Before sending, scan display blocks for `\text{`,
  `\_`, and doubled backslashes. Reserve code formatting for actual code,
  literal raw Markdown, and exact API identifiers such as `nn.Module`.

## Prepare and converge the v10 handoff

The handoff records `cycle_id`, `flow_mode`, immutable Session Profile Decision,
the full target requirement → lesson scope → practice residual partition,
prerequisite Concept IDs, source-unit boundary decisions, three to five
substantive modules, teaching steps, delivery, concept coverage, and learner
evidence. A standard session is 60–90 minutes even for a focused source slice;
vague compression wording never selects `short` or `custom`.
Those profiles require a concrete numeric duration or a recognized explicit
format constraint, not merely arbitrary non-empty text.

Each module binds one uninterrupted purpose → explanation → worked trace or
code walk → adaptive application block, uses one declared representation, and
asks at most one assessed checkpoint. Explain prerequisites before assessment.
Do not hide a learner question or assessment directive inside a
`check_policy: none` Step.
Require two distinct worked fixtures and representations, an authentic
`class Name(nn.Module):`/`def forward(...):`/concrete `nn.*(...)`/Tensor-shape
arrow walkthrough for D2 implementation or debugging scope, a limitation or
counterexample, and a normalized-content-distinct final transfer covering every
non-deferred concept and objective.

The author and first reviewer must differ. Repairable locator, wording,
objective, module, or teaching-order findings use `repair_required`; repair in
the same authorized flow and request one targeted recheck. Only source
integrity/access, irreducible factual ambiguity, or a user scope decision may
be `blocked`. Reviewer unavailability keeps review pending and is not a
semantic blocker.

The independent reviewer records separate `scope_breadth`, `teaching_order`,
`authentic_application`, `assessment_load`, and `exit_integration` verdicts.
Pass the contract's teaching-readiness gate before delivery. After every
non-deferred concept has confirmed learner evidence and the integrated exit is
complete, pass its session-capture gate. Completion means the planned session
ended, not target mastery. An uncertain concept keeps the
lesson `paused`; change the explanation and continue rather than exporting a
`남은 질문` escape hatch.

## Other reviews

For a read-only source, finalized TIL, knowledge note, or mixed/standalone TIL
review, report what is correct, what must change, and what evidence is missing.
Pure flow-generated daily TIL prose is composed only from already confirmed
cursor evidence and does not receive a redundant second factual review. Manual
or self-study material mixed into an explicit save receives one review in that
same save flow.
