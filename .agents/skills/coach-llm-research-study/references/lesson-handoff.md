# Lesson handoff contract

This document is the sole normative specification for
`tmp/active-lesson-handoff.md`. The schema is currently `9`.
`assets/active-lesson-handoff-template.md` is the canonical surface template,
and `scripts/validate_lesson_handoff.py` is the executable contract.

The handoff is ignored operational state. It binds one reviewed source slice to
one teaching session and preserves exact delivery and learner evidence. It is
not a TIL, mastery record, progress database, or permission record. Same-day
authorization and multi-cycle resumption live only in
`tmp/active-learning-flow.json`.

## Lifecycle

1. The planner chooses one actual primary target and at most one nearly
   satisfied bridge.
2. The daily cursor enters `PREPARE_LESSON` and names the cycle and handoff.
3. The coach resolves the exact source, builds this contract, and obtains a
   fresh independent review.
4. Repairable findings are fixed in the same flow and receive a targeted
   recheck. True blockers alone stop preparation.
5. A passed handoff becomes `active`; teaching updates only mutable delivery,
   current-position, coverage, and evidence fields.
6. Confirmed learner-authored evidence is copied atomically into the daily
   cursor. Partial, mistaken, or unconfirmed attempts remain in the handoff.
7. If a non-deferred concept is uncertain, preserve the lesson as `paused`
   and resume it with `계속`. Do not close it as a TIL question.
8. When every non-deferred concept and the integrated exit are confirmed and
   captured, mark the session `completed`. The next action is
   `CAPTURE_SESSION`, then `DECIDE_PRACTICE`.

A completed handoff may be replaced only after all confirmed evidence has been
captured, or after an explicit learner decision to discard it. Schema v8 and
earlier files must be rebuilt from the current template. The sole migration
helper is the evidence-preserving v8-to-v9 paused-session migration.

## Metadata and hashes

Metadata contains exactly:

- `schema_version: 9`
- stable `cycle_id` and `lesson_id`
- title and `status`
- `session_profile: standard | short | custom`
- `flow_mode: day-full | single-lesson`
- Asia/Seoul `study_date`, RFC 3339 creation/update times, and author ID
- SHA-256 of the canonical input manifest and immutable contract

Allowed status values are `preparing`, `review_pending`,
`repair_pending`, `active`, `paused`, `blocked`, and `completed`.
`short` is allowed only after an explicit short-session request or an
evidence-preserving legacy recovery. The normal default is `standard`.

The input manifest includes every contract input with its exact current hash:
all local or cached external primaries and direct assets, course INDEX,
`CURRICULUM.md`, and `ROADMAP.md`, plus any knowledge, finalized TIL, or
practice used only as baseline evidence. Roles are `primary`,
`external-primary`, `external-asset`, `asset`, `course-index`,
`curriculum`, `roadmap`, `knowledge`, `til`, and `practice`.

The immutable contract is exactly the text enclosed by
`lesson-contract:start` and `lesson-contract:end`. Semantic review hashes
both the manifest and this contract. Any change makes the review stale.

## Target, source, and scope

`Target Decision` records selection mode, target state, exact primary and
optional bridge, evidence gap, completion evidence, endpoint, and reason.
Only `START_TARGET`, `CONTINUE_TARGET`, and `BRIDGE_PREREQUISITE` are
teachable. Diagnostic and no-action planner states cannot enter a handoff.

For planner selection, endpoint must be an exact ordered ROADMAP endpoint and
primary must be in its prerequisite closure or the endpoint itself. A bridge
is legal only in `BRIDGE_PREREQUISITE`, must be in the primary prerequisite
closure, and must be suitable for one inline repair. Explicit work outside a
ROADMAP route uses `endpoint: user-directed` and cannot claim planner mode.

Every primary has one `Source Scope Map` row:

- `entire-source`: only with `full-source`;
- `registered-slice`: a valid scope declared in the course INDEX;
- `ephemeral-slice`: an exact lesson-local scope for a cached official source.

`focused` requires a registered or ephemeral slice. Objective, goal,
guidance, and source finding locators must be inside included locations.
Boundary context is review-only and cannot carry an objective. Outside-scope
goals, examples, appendices, and index material are neither deferred
objectives nor readiness blockers. The whole source hash remains in the
manifest so byte drift still invalidates review.

Review cost and teaching depth are independent. A three-page slice may support
a 60–90 minute session if its concepts are developed through multiple modules,
examples, applications, limits, and transfer. Shrinking a semantic review
slice never silently changes the Module Plan.

Local primaries must map through the course INDEX and Curriculum treatment.
Every source-core primary referenced by a treatment needs its own direct
`primary` or `supporting` target relation; a relation for only one of
several primaries is insufficient. `context` is not a teaching relation.

An external primary additionally records provider, course, exact offering or
edition, artifact, official and final HTTPS URLs, retrieval time, media type,
scope, and receipt path. It also needs a target relation and audited objective
basis. Cache bytes and receipt identity must match. Temporary use never changes
durable Curriculum coverage.

## Audited teaching contract

Use the canonical template headings and table columns exactly. The immutable
contract contains:

- one observable lesson objective;
- coverage mode, Curriculum targets, target decision, and treatment map;
- external identity and relation tables where applicable;
- learner-evidence baseline and precisely located audit findings;
- source scope, source coverage, declared-goal, and guidance maps;
- observable objectives and an ordered Concept Path;
- Module Plan, Session Plan, Example Map, and Prepared Teaching Steps;
- explicit deferred objectives, if any.

Each objective states requirement, marker, source locator, observable outcome,
concept, treatment, teaching move, and exact baseline evidence. Source-core
objectives may not be silently dropped. `bridge` treatment needs confirmed
learner baseline evidence; otherwise the prerequisite is taught in full or is
selected as the primary target.

### Standard depth

A standard session lasts 60–90 expected minutes and has three to five
substantively different connected modules. Renaming the same micro-concept does
not satisfy depth. Modules must record source locators, a learner application
step, and expected time.

The complete arc contains motivation, concept model, worked example,
contrast/limit, and synthesis/transfer roles; at least two genuinely distinct
worked fixtures; at least two learner application steps; an explicit
counterexample or limitation; and a final task combining at least two
concepts. Every non-deferred core concept must be represented in the modules
and exit design.

`short` and `custom` still require an explicit coherent objective, reviewed
scope, honest evidence, and an exit. They do not waive target/source identity
or semantic review.

## Review convergence

`Semantic Review` holds one current record:

- iteration `0 | 1 | 2`;
- phase `none | independent-slice | targeted-recheck`;
- initial and current reviewer IDs, `recheck_of`, review timestamp, verdict,
  and exact reviewed hashes;
- `R###` repair findings and `B###` blocking findings.

The first reviewer differs from the author. A targeted recheck normally uses
the same reviewer and points to the repaired iteration. Locator errors, wording,
objective mapping, module depth, example choice, and teaching order are
`repair_required`. Only `source-integrity`, `source-access`,
`irreducible-factual-ambiguity`, and `user-scope-decision` may be blocked.
Reviewer unavailability preserves pending review and may try one replacement;
it is not a semantic block.

A second repairable non-pass remains `repair_pending`. With no delivery or
learner evidence, the author may rebuild one smaller semantic slice while
preserving standard session depth. Once delivery or evidence exists, preserve
the handoff and resume repair; never demand a special reset phrase.

## Mutable teaching state

`Current Position` names the last completed step, current step, next action,
target objectives, evidence basis, and exact resume note. Its next action is
`teach`, `await-answer`, `remediate`, or `complete`.

`Objective Delivery` records pending/delivered plus none/full/bridge mode.
`Teaching Step Delivery` records pending/delivered/completed. Neither table
is learner evidence.

Each learner-evidence block is added only after an answer and contains:

- contiguous evidence ID;
- provenance `learner`;
- one or more concept IDs and objective IDs;
- kind `explain_back | calculation | shape_prediction | code_interpretation |
  transfer | limit`;
- verdict `confirmed | partial | misconception | unconfirmed`;
- captured state `pending | captured | not_eligible`, capture time, and exact
  lowercase content SHA-256;
- exact learner content followed by a separate coach assessment.

Never rewrite an earlier attempt. A corrected explain-back is a new evidence
item. Only confirmed learner evidence can be captured in the daily cursor.

`Session Concept Coverage` gives every concept one state:
`confirmed`, `uncertain`, or `deferred`, with exact evidence IDs.
Confirmed state requires confirmed evidence covering all delivered objectives
for that concept. A completed session requires all non-deferred concepts
confirmed, every confirmed item captured, all non-deferred objectives
delivered, and confirmed evidence matching the configured integrated exit.
This means the planned session ended; it does not assert Curriculum mastery.

## Validation and workflow action

Basic validation checks structure, target/source relations, locators, module
depth, review-state consistency, delivery, evidence, and content hashes.

`--ready` additionally requires current source/index/Curriculum/ROADMAP
freshness, external receipts where used, active or paused status, and a fresh
passing review. Same-course source problems outside the selected semantic
slice remain warnings; selected-slice problems are errors.

`--capture-ready` additionally requires completed status, a fresh pass,
complete confirmed/captured concept evidence, and the integrated exit.

JSON output returns errors, warnings, computed hashes, and one workflow action:
`PREPARE_CONTRACT`, `REQUEST_INDEPENDENT_REVIEW`, `REPAIR_CONTRACT`,
`REQUEST_TARGETED_RECHECK`, `ACTIVATE_LESSON`, `TEACH_OR_RESUME`,
`SHRINK_TO_MICRO_SLICE`, `RESOLVE_TRUE_BLOCKER`, `CAPTURE_SESSION`, or
`DECIDE_PRACTICE`. Warning-only reports exit successfully.

After session capture, preserve the handoff and any external cache until
practice provenance has been validated. Delete only the exact lesson cache
directory after successful downstream capture. On interruption, drift, or
validation failure, keep both handoff and cache for `계속`.
