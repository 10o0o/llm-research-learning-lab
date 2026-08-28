# Active lesson handoff contract

This file is the sole normative specification for the active handoff schema,
lifecycle, hashes, review freshness, delivery state, learner evidence,
readiness gates, and cleanup conditions. Consumer skills and repository guides
link here instead of redefining those details.

Use this contract only for a named, multi-turn lesson that combines material
evaluation with adaptive teaching. The single live file is
`tmp/active-lesson-handoff.md`. It is an ignored operational cache, not a
durable note and not proof of learner understanding.

Copy `../assets/active-lesson-handoff-template.md`, replace every placeholder,
and validate it before teaching:

```bash
python3 .agents/skills/coach-llm-research-study/scripts/validate_lesson_handoff.py \
  tmp/active-lesson-handoff.md
python3 .agents/skills/coach-llm-research-study/scripts/validate_lesson_handoff.py \
  --ready tmp/active-lesson-handoff.md
python3 .agents/skills/coach-llm-research-study/scripts/validate_lesson_handoff.py \
  --til-ready tmp/active-lesson-handoff.md
```

`--json` emits the same result as JSON, including computed hashes. The
validator never edits the handoff.

## Lifecycle

1. Build the manifest and lesson contract with status `preparing`.
2. Record the computed manifest and contract hashes, change the status to
   `review_pending`, and run structural validation.
3. Give a fresh read-only reviewer the handoff, the exact selected source slice,
   its boundary context, directly used assets, and the relevant INDEX,
   Curriculum, and ROADMAP rows. The reviewer must not be the contract author
   and must not be given an intended answer. A focused review must not expand
   into a new whole-source audit.
4. Record the current semantic decision. A `repair_required` verdict uses status
   `repair_pending`; the author corrects only the named findings and the same
   reviewer performs one `targeted-recheck`. Locator, wording, objective mapping,
   and teaching-order findings are repairable and never become a semantic block.
   A second repairable non-pass remains resumable and, when nothing has been
   taught or captured, permits one automatic reduction to a smaller slice.
   `blocked` is reserved for source integrity or access failure, irreducible
   factual ambiguity, or a material user scope decision.
5. A current `pass` permits status `active`. Run `--ready` before the first
   teaching chunk and again after resuming a paused lesson.
6. Update Current Position, Objective Delivery, learner evidence, and Daily
   Learning Coverage without rewriting the reviewed contract. These changes do
   not invalidate a current lesson-contract review. Delivery records that a
   teaching move actually occurred; it never proves learner understanding.
7. Before saving, inventory what was actually taught. Every confirmed concept
   must be represented as learning, every unresolved taught concept as a
   remaining question, and untouched content as deferred. Record the coach's
   verdict and the exact draft hash, then run `--til-ready`.
8. Set status `completed` only after every non-deferred objective has been
   delivered. The save workflow may remove a completed local-only handoff only
   after every confirmed evidence item is drafted, `--til-ready` passes, and
   the dated TIL commit succeeds. When a practice artifact still needs an
   external source receipt, preserve the handoff and exact lesson cache through
   strict practice provenance validation; delete only that lesson cache
   directory afterward. Preserve both on interruption or validation failure.

Schema version 7 has no in-place migration from version 6 or earlier. Rebuild
an older handoff from the current template. When the same target and source are
unchanged and no Objective has been delivered and no learner evidence exists,
an explicit lesson-start or full-flow request already authorizes that mechanical
rebuild; never ask the learner to repeat a reset phrase.

Resume an existing handoff only when the named primary input path and hash are
unchanged. A source, curriculum, manifest, or lesson-contract change makes a
prior review stale. Never overwrite an `active` or `paused` handoff, or any
handoff with delivery or learner evidence, with a different lesson without an
explicit close-or-replace decision. `review_pending` and `repair_pending`
handoffs without delivery or evidence may be repaired or narrowed automatically
for the same target/source.
A `completed` handoff may be replaced for a new lesson only when every
confirmed evidence item is already `drafted`. Otherwise preserve it until the
append helper recovers the pending evidence; completion alone is not permission
to discard learner content.

## Metadata

Metadata is a Markdown bullet list with exactly these keys:

- `schema_version`: currently `7`.
- `lesson_id`: stable lowercase identifier matching
  `[a-z0-9][a-z0-9-]{2,63}`.
- `title`: one non-empty line.
- `status`: `preparing`, `review_pending`, `repair_pending`, `active`, `paused`,
  `blocked`, or `completed`.
- `study_date`: `YYYY-MM-DD`.
- `created_at`, `updated_at`: RFC 3339 timestamps with `Z` or an explicit UTC
  offset.
- `author_id`: stable identity for the contract-writing agent.
- `draft_path`: exactly `til/today.md`.
- `input_manifest_sha256`, `contract_sha256`: lowercase SHA-256 values.

## Input manifest and hashes

The Input Manifest table has these exact columns:

```text
ID | Role | Path | SHA-256
```

- IDs are contiguous `I001`, `I002`, and so on.
- Roles are `primary`, `external-primary`, `external-asset`, `asset`,
  `course-index`, `curriculum`, `roadmap`, `knowledge`, `til`, or `practice`.
- Include at least one local `primary` or `external-primary`, exactly one
  `curriculum`, and exactly one `roadmap`. Their paths are exactly
  `CURRICULUM.md` and `ROADMAP.md`.
- External rows live only under
  `tmp/active-lesson-sources/<lesson-id>/`. Create them with
  `cache_external_source.py` after the agent has selected and audited one exact
  official URL. The helper does not search for a source or start work in the
  background. Every redirect remains HTTPS, credentials and
  cookies are not stored, local or non-public network destinations are rejected,
  and unsupported, authenticated, paid, archive,
  dataset, weight, or over-100-MiB access returns `AWAIT_SOURCE_APPROVAL`.
  Cache content and receipts are content-addressed and atomic. Every
  `external-asset` keeps its generated receipt; readiness verifies its lesson,
  kind, HTTPS URLs, path, byte count, and hash as well as the manifested bytes.
- Every primary under `materials/private/<course>/` requires that exact
  course's `materials/private/<course>/INDEX.md` as a `course-index` input.
  `--ready` and `--til-ready` apply blocking freshness checks to the lesson's
  semantic slice: each selected primary, its directly referenced local assets,
  every supporting source actually manifested for the lesson, the selected
  Curriculum targets and treatments, every local source-core primary's direct
  `primary` or `supporting` relation to its target, every temporary external
  relation, and the exact
  registry and INDEX rows for those sources. A `context` relation is not direct
  support. Missing, stale, unregistered, duplicated, or mismatched inputs inside
  that slice block readiness. Unrelated source problems in the same course are
  reported as warnings and do not block the lesson gate. The standalone
  `validate_curriculum.py --strict-sources` command remains the course-wide
  parity and freshness gate.
- Keep the complete course `INDEX.md`, `CURRICULUM.md`, and `ROADMAP.md` in the
  manifest. Any byte change to one still makes an existing handoff and its semantic
  review stale, so rebuild and review the handoff once. After rebuilding,
  unrelated same-course source problems remain warnings under the semantic
  slice rule above.
- Include every local figure or asset referenced by the source. A PDF is one
  input hashed as file bytes.
- Never include `draft_path` (`til/today.md`) in the manifest. The draft,
  Current Position, Objective Delivery, Daily Learning Coverage, and Learner
  Evidence are mutable operational state outside the reviewed input and
  contract hashes. The `til`
  role is only for a prior, finalized dated TIL used as baseline evidence.
- Paths are POSIX, repository-relative paths. Absolute paths, backslashes,
  `.` or `..` components, duplicate paths, non-files, and symlinks that resolve
  outside the repository are invalid.
- Each row hash is SHA-256 over the exact file bytes.

The manifest aggregate is SHA-256 over UTF-8 bytes of the following canonical
text. Sort rows by `(role, path, sha256)`, omit IDs, and retain the final LF:

```text
<role>\t<path>\t<sha256>\n
```

The contract hash is SHA-256 over the exact text inside the
`lesson-contract:start` and `lesson-contract:end` marker lines after converting
CRLF or CR newlines to LF. The LF immediately following the start marker and
the LF immediately preceding the end marker delimit the markers and are not
part of the hashed body. All other whitespace is significant.

## Lesson Contract

Keep the contract between its marker lines and retain these headings in order:

1. `Objective`
2. `Coverage Mode`
3. `Curriculum Targets`
4. `Target Decision`
5. `Curriculum Treatment Map`
6. `External Source Identity`
7. `External Target Relation`
8. `Learner Evidence Baseline`
9. `Audited Findings`
10. `Source Coverage Index`
11. `Declared Goal Alignment`
12. `Guidance Map`
13. `Observable Objective Map`
14. `Concept Path`
15. `Prepared Teaching Steps`
16. `Deferred`

List one or two stable `CC-*` or `TR-*` curriculum IDs that actually occur in
the manifested `CURRICULUM.md` under Curriculum Targets.

Target Decision contains exactly these ordered bullet fields:

```text
selection_mode
target_state
primary_target
bridge_target
evidence_gap
completion_evidence
endpoint
why_now
```

Selection mode is `planner`, `user-named-target`, or `user-named-source`.
Handoffs accept only actionable planner states: `START_TARGET`,
`CONTINUE_TARGET`, or `BRIDGE_PREREQUISITE`. Resolve `NEED_DIAGNOSTIC` before
building a lesson and never build one for `NO_ACTIONABLE_TARGET`.

`endpoint` is the long-term ordered ROADMAP destination while `primary_target`
is the target whose evidence this lesson advances. A blocking prerequisite is
therefore the primary, not the bridge. In planner mode, endpoint is an exact
ROADMAP endpoint and primary belongs to its prerequisite closure or is that
endpoint itself. A user-named target or source may use an exact containing
endpoint or `user-directed`; planner mode may not use that sentinel.

Curriculum Targets is exactly the primary target followed by its optional
prerequisite bridge. The bridge is one mostly satisfied prerequisite closed
inline and exists only with `BRIDGE_PREREQUISITE`. Evidence gap is `none` or
unique required-evidence tokens from the primary Curriculum row. Source
convenience, chapter order, or this handoff never changes that target decision.

Curriculum Treatment Map has these exact columns and exactly one ordered row
per selected target:

```text
Target ID | Coverage | Gap action | Lesson treatment | Objective IDs | Note
```

`Coverage` and `Gap action` must exactly match that target's current Curriculum
row. `Objective IDs` are comma-separated or `none`.

- `source-only` requires `충분` / `그대로 사용` and links one or more
  `source-core` objectives only.
- `supplement-now` requires `수업 내 보충` and links at least one
  `required-added` Objective. The supplement is taught now and must be backed
  by an Audited Finding and a manifested exact source location.
- `resolved-external` links one or more `source-core` Objectives from an
  `external-primary`. It is valid only inside this reviewed lesson contract and
  never changes durable Curriculum coverage.
- `defer-gap` requires `별도 자료 확보` or `원본 복구 후 재감사`. It may
  link existing `source-core` Objectives, but never added content that pretends
  to fill the missing source.
- `defer-track` requires a `TR-*` target with `트랙 선택 시 확보` and uses
  Objective IDs `none`.

External Source Identity has one ordered row per `external-primary` and these
columns:

```text
Primary ID | Provider | Course | Offering/Edition | Artifact | Official URL | Final URL | Retrieved at | Media type | Scope | Receipt path
```

Local-only lessons use one all-`none` row. URLs are public HTTPS without
credentials. The cache receipt must exactly match both URLs, retrieval time,
media type, lesson ID, primary kind, content and receipt paths, byte count, and
SHA-256. `Receipt path` is exactly
`tmp/active-lesson-sources/<lesson-id>/<primary-sha256>.receipt.json`.

External Target Relation has these columns:

```text
Target ID | Primary ID | Relation | Objective IDs | Audit basis
```

Each relation is `primary` or `supporting`, never `context`, and identifies the
exact external source-core Objectives audited for that target. Every external
primary linked by a target treatment needs its own row. For mixed lessons,
every linked local and external primary must independently satisfy its direct
relation; one matching source cannot hide an unrelated source.

Before `--til-ready` can pass for any handoff-backed local or external lesson,
the reviewed draft's `## 관련 기록` section contains exactly this line, with a
`CC-*` or `TR-*` value:

```markdown
- 관련 역량: `<primary_target>`
```

When the selected bridge has at least one delivered Objective, add exactly
this line; omit it when that bridge was not delivered:

```markdown
- 보충 선수 역량: `<bridge_target>`
```

These lines record routing provenance only and do not establish mastery or
durable Curriculum coverage.

A temporary external lesson additionally preserves each external primary's
exact Official URL, Offering/Edition, and Scope. External identity validation
does not redefine which target provenance lines are required.

Coverage Mode contains exactly one of:

```text
- mode: full-source
- mode: focused
```

Use `full-source` when the learner requests all named sources or an entire
range. It requires every primary source's core content, including source-body
formulas, code, figures, examples, and embedded checks. Separate
`course-provided-practice/` inputs stay outside this gate unless the learner
explicitly includes them. Use `focused` for one bounded subset. Content outside
that subset is not part of the lesson contract, is not a deferred Objective,
and cannot block readiness.

A course INDEX may preserve a reusable logical slice without duplicating the
source bytes. Its optional `학습 범위` table has these exact columns:

```text
Scope ID | Source ID | Title | Included locations | Boundary context | Note
```

`Scope ID` is `SCOPE-<Source ID without SRC->-<NN>`. Every included and boundary
locator points to that source, exists, and is unique; PDF pages must be within
the parsed page count. Boundary context is review-only and cannot become an
Objective, Goal, Guidance item, or Finding. An unregistered one-lesson slice is
allowed in the handoff and does not change durable Curriculum coverage.

Source Scope Map has these exact columns and one ordered row per primary:

```text
Primary ID | Scope kind | Scope ID | Included locations | Boundary context | Outside-scope disposition
```

Scope kind is `entire-source`, `registered-slice`, or `ephemeral-slice`.
`full-source` requires `entire-source`, Scope ID `none`, Included locations
`entire-source`, and no boundary or outside disposition. `focused` requires a
registered or ephemeral slice, one or more included locators, and one coarse
outside-scope disposition. A registered row must exactly match the manifested
course INDEX; an ephemeral row uses Scope ID `none`.

Source Coverage Index has these exact columns and exactly one ordered row per
primary manifest input, in manifest order:

```text
Primary ID | Declared Goal IDs | Objective IDs | Guidance IDs
```

ID cells are comma-separated or `none`. They must exactly inventory that
primary's declared goals, source-core objectives, and guidance items inside the
selected scope. A
full-source primary may be entirely guidance, but every technical source-body
core still requires an objective. In focused mode the reviewer compares only
the included locations and uses boundary context solely to verify that the cut
does not hide a definition, limitation, or continuation needed by that slice.

Declared Goal Alignment has these exact columns:

```text
Goal ID | Primary ID | Goal location | Disposition | Linked IDs | Body support | Reason
```

- IDs are contiguous `D001`, `D002`, and so on. If no primary has an explicit
  goal, use one `none | none | none | none | none | none | reason` row.
- `Goal location` is the exact source line containing the declared goal.
- `learning` links one or more source-core Objective IDs and requires exact
  semicolon-separated body locations that actually explain the goal. The goal
  wording itself is never body support; use Reason `none`. Every substantive
  clause must be supported: when definitions, task contracts, and model choice
  occur in different sections, list all of those locations rather than the one
  most convenient heading.
- `guidance` links exactly one same-primary Guidance ID and explains why the
  item is not knowledge or skill to assess.
- `source-gap` means a substantive declared learning goal has no supporting
  body explanation. Use Body support `none` and state the gap. In full-source,
  link it to a `required-added` Objective marked `correction` or `supplement`,
  unless the current Curriculum Treatment explicitly defers the missing
  material with `defer-gap` or `defer-track`. Never relabel an unsupported
  mechanism as `source-core` or invent the absent explanation.

Guidance Map has these exact columns:

```text
Guidance ID | Kind | Source location | Summary | Trigger
```

IDs are contiguous `G001`, `G002`, and so on; use one all-`none` row when
there is no guidance. `Kind` is `orientation`, `diagnostic`, or `reference`.
`Trigger` states the concrete learner request or path decision that makes the
item useful. Guidance is preserved for on-demand navigation, but it must never
appear in a Teaching Step, Objective Delivery, an understanding question,
Learner Evidence, or Daily Learning Coverage.

Audited Findings has these exact columns:

```text
Finding ID | Type | Source location | Linked IDs | Note
```

IDs are contiguous `F001`, `F002`, and so on. `Type` is `correction`,
`underspecification`, `prerequisite`, `supplement`, or
`intentional-deferral`. Each finding links at least one declared Goal,
Guidance, or Objective ID. Each marked or deferred Objective and each
source-gap Goal needs the matching finding. Use one
`none | none | none | none | No audited findings.` row when there are none.

Observable Objective Map has these exact columns:

```text
Objective ID | Requirement | Marker | Source location | Observable outcome | Concept ID | Treatment | Teaching move | Baseline evidence
```

- IDs are contiguous `O001`, `O002`, and so on with no upper limit.
- `Requirement` is `source-core`, `required-added`, or `optional-added`.
- `Marker` is `none`, `prerequisite`, `correction`, or `supplement`, rendered
  during teaching as no marker, `[선수개념]`, `[정정]`, or `[보충]`.
- `Source location` is an exact manifested `path#location`. A `source-core`
  objective points to a local or external primary input. Markdown and local
  text locations match an actual normalized line. Cached HTML uses
  `path.html#text: <normalized exact excerpt>` while preserving raw bytes.
  PDF locations use `path.pdf#page-N` or
  `path.pdf#page-N: short locator`; `N` must be within the parsed page count.
- `Observable outcome` says what the learner should be able to explain,
  calculate, trace, predict, or distinguish. Topic names alone are invalid.
- Keep only assessable technical knowledge and skill here. Orientation,
  self-diagnosis, roadmap navigation, final-artifact descriptions, and study
  advice belong in Guidance Map.
- `Treatment` is `full`, `bridge`, or `deferred`. A `full-source`
  `source-core` or any `required-added` objective cannot be deferred.
- Every non-deferred objective has a concrete `Teaching move`; a deferred row
  uses `none` and must appear in Deferred.
- A `bridge` still requires an actual short explanation in the conversation.
  Its baseline is either `learner-evidence:E001` or an exact manifested
  `knowledge`, finalized `til`, or interpreted `practice` location. Separate
  multiple references with semicolons. Other treatments use `none`.

Concept Path contains three to seven contiguous conceptual groups using:

```text
1. C01 | [선수개념] | 개념 이름 | source: path#exact-location
```

The three-to-seven range limits navigation groups, not objectives, source
coverage, or teaching steps. The marker is `none`, `[선수개념]`, `[정정]`, or
`[보충]`. Every source location must identify a page, section, formula, code
fragment, or other exact location, and the path before `#` must be present in
the Input Manifest.

Prepared Teaching Steps use contiguous `#### T001`, `#### T002`, and so on,
with no count limit. Each has these ordered, non-empty fields:

```text
concept_id
objective_ids
delivery_outline
tiny_example
check_policy
check_basis
check_question
```

Every non-deferred objective appears exactly once under its Concept ID. Step
order is the actual teaching order and may differ from stable Objective audit
order. The outline and objective-level Teaching moves must make the explanation
observable; mentioning a filename, topic, or `lesson_scope` is not coverage.

`check_policy` is `adaptive` only when the learner's answer changes the next
explanation. Its `check_basis` uses the explicit form
`if <answer condition> -> <next move>; else -> <different move>`, and its
question checks only the Step's objectives. It must not ask the learner to
explain course design, learning method, source organization, or guidance. A
focused lesson whose explicit technical subject is that meta-topic is the only
exception. Use `none` when no instructional branch depends on an answer;
explain why in `check_basis` and write `check_question: none`. Do not create a
question merely to end every explanation with a quiz. Keep full-length
teaching prose out of the contract.

Deferred is a table with `Objective ID | Source location | Reason`. List every
deferred objective once in objective order. If none are deferred, use one
`none | none | No objectives are deferred.` row.

## Semantic Review

The handoff stores the current semantic decision, not an accumulating review
log. It contains these bullets in order:

```markdown
- initial_reviewer_id: replace-with-independent-reviewer-id
- reviewer_id: replace-with-the-same-reviewer-id
- review_iteration: 1
- review_phase: independent-slice
- recheck_of: none
- reviewed_at: YYYY-MM-DDTHH:MM:SSZ
- verdict: pass
- reviewed_input_manifest_sha256: replace-with-current-manifest-sha256
- reviewed_contract_sha256: replace-with-current-contract-sha256
```

`review_iteration` is `0`, `1`, or `2`. Iteration 0 uses `none`, `pending`, and
empty finding rows exactly as the template shows. Iteration 1 uses
`independent-slice`; its reviewer differs from `author_id`. Iteration 2 uses
`targeted-recheck`, keeps that same reviewer, and lists the repaired `R###` IDs
under `recheck_of`.

Verdict is `pending`, `pass`, `repair_required`, or `blocked`. Repair Findings
uses:

```text
Finding ID | Location | Detail
```

Blocking Findings uses:

```text
Finding ID | Kind | Location | Detail
```

Repair IDs are unique `R###`. Blocker IDs are unique `B###`, and Kind is exactly
`source-integrity`, `source-access`, `irreducible-factual-ambiguity`, or
`user-scope-decision`. A pass has no current findings. `repair_required` has
only Repair Findings and requires status `repair_pending`; `blocked` has only
true Blocking Findings and requires status `blocked`. Reviewer unavailability
is not a semantic verdict: try one replacement reviewer and otherwise preserve
`review_pending` without manufacturing a blocker.

A pass is current only when both reviewed hashes equal the recomputed hashes.
The validator's JSON `workflow_action` is one of `PREPARE_CONTRACT`,
`REQUEST_INDEPENDENT_REVIEW`, `REPAIR_CONTRACT`, `REQUEST_TARGETED_RECHECK`,
`ACTIVATE_LESSON`, `TEACH_OR_RESUME`, `SHRINK_TO_MICRO_SLICE`,
`RESOLVE_TRUE_BLOCKER`, or `COMPLETE`. Follow it without asking the learner for
a reset phrase.

The reviewer checks source fidelity, facts, formulas, tensor shapes, code
claims, marker classification, curriculum alignment, lesson scope, and learner
evidence provenance. In `full-source`, compare the entire primary. In `focused`,
compare only Included locations and use Boundary context only to verify the
cut. Within that review scope, compare every explicit goal with Declared Goal
Alignment and compare essential source-native formulas, code, figures,
examples, and checks with the Objective Map. Verify that guidance is
preserved without becoming an assessment target and that each Objective has an
aligned Teaching Step. A path, goal sentence, or topic name alone is never body
support or teaching coverage. Also verify that corrections use authoritative
primary references and that supplements directly support a selected curriculum
target. Tutor explanations and source summaries are never learner evidence.

Before a `pass`, apply these semantic regression probes rather than trusting
topic-name overlap:

- If a multiclass lesson names its source, logits shape, and
  `CrossEntropyLoss` but never assigns a teaching move for Softmax's operation,
  class axis, normalized output meaning, and per-sample sum of one, return
  `repair_required`.
- For each explicit learning goal inside the review scope, match it independently
  to learning, guidance, or source-gap. Goals outside a focused slice are not
  contract inputs and must not be requested as exclusions or mappings.
- Reject a `learning` goal whose Body support is merely its own goal wording,
  a source-gap represented as source-core, or any mechanism invented to fill
  absent body prose. Reject guidance promoted into an Objective, Teaching Step,
  question, delivery record, learner evidence, or daily learning coverage.
- For every adaptive Step, state what correct and incorrect answers change in
  the immediately following explanation. If both answers lead to the same
  teaching, use `check_policy: none`. Compare the question with manifested
  baseline and Learner Evidence; reject an identical claim or numeric fixture
  whose answer already fixes the branch. Reject questions about learning plans,
  lesson roles, or source organization unless that meta-topic is the explicit
  subject of a focused lesson. In particular, a 01-00 Step must fail if it asks
  “flatten 같은 개념에서 이론·복습·실습은 각각 무엇을 확인하게 해 주나요?”
  rather than checking a technical Objective.
- Audit included technical body independently of declared goals. Reject a
  contract that covers the listed goals but omits a source-native limitation,
  decision rule, API comparison, threshold rule, worked example, or embedded
  check needed to understand that slice. Do not inspect unrelated chapters,
  appendices, references, indexes, or book-wide goals during a focused review.

## Current Position

Keep exactly these fields and update them after each meaningful checkpoint:

- `last_completed_step`
- `current_step`
- `next_action`
- `target_objectives`
- `basis`
- `resume_note`

They may change without semantic re-review. Step IDs follow Prepared Teaching
Step order. `next_action` is `teach`, `await-answer`, `remediate`, or
`complete`. For `teach`, target exactly the pending Objectives in the current
Step and use Basis `none`. `await-answer` is valid only after every Objective
in an adaptive current Step has been delivered; target that Step's Objectives
and use Basis `none`. `remediate` targets Objectives in the current Step and
uses `basis: learner-evidence:E###` for a partial, misconception, or
unconfirmed answer in the same concept. A completed lesson has its final Step
as `last_completed_step`, uses `current_step`, `target_objectives`, and `basis`
`none`, and sets `next_action: complete`. `resume_note` preserves only the
concrete next teaching move, not a forced next question.

`last_completed_step` tracks the contiguous completed prefix of the reviewed
teaching sequence. Recovery may retain genuinely delivered technical
Objectives in later Steps when an earlier contract had taught out of order;
those records do not skip the earliest incomplete Step or make intervening
Steps completed.

## Objective Delivery

This mutable operational table has exactly one ordered row per Observable
Objective:

```text
Objective ID | State | Mode | Basis/Note
```

- `State` is `pending` or `delivered`.
- Pending rows use `Mode` `none`; delivered rows use `full` or `bridge`.
- A planned `full` objective must be delivered in full mode. A planned bridge
  may be expanded to full, but it cannot be marked delivered until the short
  connection was actually stated.
- Deferred objectives remain pending until a reviewed contract change.
- `Basis/Note` records the concrete teaching checkpoint, not a mastery claim.
- `completed` is invalid while any non-deferred objective remains pending.

Objective Delivery answers only "was this covered in teaching?" Daily Learning
Coverage and Learner Evidence separately answer "what did the learner
demonstrate today?" Never turn delivery into `confirmed` evidence.

## Daily Learning Coverage

This section records today's taught scope, not the source's whole syllabus and
not durable progress. It contains exactly these pre-save fields:

- `pre_save_verdict`: `pending`, `저장 가능`, `수정 후 저장`, or
  `추가 확인 후 저장`;
- `reviewed_at`: `pending` or an RFC 3339 timestamp;
- `reviewed_draft_sha256`: `pending` or SHA-256 of the exact current
  `til/today.md` bytes.

Follow them with exactly one ordered row per Concept Path concept:

```markdown
| Concept ID | Today state | Evidence IDs | TIL representation | Note |
| --- | --- | --- | --- | --- |
| C01 | confirmed | E001 | learning | The learner explanation is in today's learning. |
| C02 | uncertain | E002 | remaining-question | draft-anchor: 왜 오른쪽 축부터 비교하는가? |
| C03 | deferred | none | not-required | This concept was not taught today. |
```

`Today state` is `confirmed`, `uncertain`, or `deferred`.
`TIL representation` is `learning`, `remaining-question`, `missing`, or
`not-required`. A confirmed row needs confirmed learner evidence whose
`objective_ids` collectively cover every Objective in that Concept that was
delivered today; a subset leaves the Concept `uncertain`. It uses `learning`
only after all cited confirmed evidence is drafted. During an active lesson,
an uncertain row may use `missing`; it may cite partial, misconception, or
narrowly confirmed evidence while broader objectives remain unestablished.
The confirmed subset is still drafted verbatim, while the unconfirmed portion
is linked to `남은 질문`. Before `--til-ready`, change it to
`remaining-question` and make
its Note `draft-anchor: <exact excerpt>`, where the non-empty excerpt occurs
verbatim under the reviewed draft's `## 남은 질문` section. This gives
`--til-ready` a mechanical representation check without pretending to judge the
question's semantics. A deferred row has `none` evidence and `not-required`.
Do not classify an untouched source concept as missing.

If any objective in a concept is delivered, that concept cannot remain
`deferred`; use `uncertain` until matching learner evidence supports
`confirmed`. The coach compares Concept Path, Current Position, learner evidence, the
actual learning conversation, explicitly named self-study scope, and the draft.
Tutor prose does not satisfy a confirmed row. After corrections, set the exact
review timestamp, hash the current draft bytes, and record `저장 가능` only
when every non-deferred concept is represented. Any later draft edit makes the
review stale. `--til-ready` verifies this operational contract in addition to
requiring a current independent lesson-contract pass and, for temporary
external sources, the exact `관련 기록` provenance described above.

## Learner Evidence

Each evidence block has a contiguous ID such as `E001` and these fields:

- `concept`: a contract concept ID such as `C01`;
- `objective_ids`: one or more comma-separated Objective IDs from that same
  Concept. Every referenced Objective must already be `delivered`;
- `kind`: `explain_back`, `calculation`, `shape_prediction`,
  `code_interpretation`, `transfer`, or `limit`;
- `provenance`: exactly `learner`;
- `verdict`: `confirmed`, `partial`, `misconception`, or `unconfirmed`;
- `append_state`: `pending`, `drafted`, or `not_eligible`;
- `captured_at`: RFC 3339 timestamp;
- `content_sha256`: SHA-256 of the LF-normalized Learner Content marker body,
  using the same boundary-newline rule as the contract.

Preserve the complete learner answer between the Learner Content markers.
Place evaluation separately under Tutor Assessment. A core error makes the
answer `partial` or `misconception`; never silently repair it. A corrected
explain-back is a new evidence item.

Use this exact block syntax under `## Learner Evidence`, with contiguous IDs.
Replace the content hash with the LF-normalized Learner Content body hash:

```markdown
<!-- learner-evidence:E001:start -->
### E001

- concept: C01
- objective_ids: O001
- kind: explain_back
- provenance: learner
- verdict: confirmed
- append_state: pending
- captured_at: YYYY-MM-DDTHH:MM:SSZ
- content_sha256: replace-with-learner-content-sha256

#### Learner Content

<!-- learner-content:start -->
Preserve the learner's exact answer here.
<!-- learner-content:end -->

#### Tutor Assessment

State why this answer is confirmed, partial, a misconception, or unconfirmed.
<!-- learner-evidence:E001:end -->
```

Only `provenance: learner` plus `verdict: confirmed` may use `pending` or
`drafted`. Every other verdict uses `not_eligible`. Append eligible evidence
with:

```bash
python3 .agents/skills/teach-course-material/scripts/append_lesson_evidence.py \
  tmp/active-lesson-handoff.md --evidence E001
```

The helper writes this idempotency envelope to `til/today.md`:

```html
<!-- lesson-evidence:<lesson_id>:E001:<content_sha256> -->
<exact learner content>
<!-- /lesson-evidence:<lesson_id>:E001 -->
```

It writes the draft atomically before marking the evidence `drafted`. If a
process stops between those writes, rerunning the helper finds and verifies the
existing envelope, then repairs the handoff state without duplicating content.
The save workflow removes only the envelope comments and preserves their body
verbatim.

## Save preflight

`$save-today-til` obtains its parsing input through the read-only preflight:

```bash
python3 .agents/skills/save-today-til/scripts/prepare_til_input.py <draft-path>
```

- Canonical `til/today.md` plus `tmp/active-lesson-handoff.md` always requires
  this handoff's `--til-ready` result, whether or not a marker is present.
- After that gate passes, the preflight prints input with only validated
  evidence envelope comments removed and learner content preserved.
- Canonical input with a marker but no active handoff is invalid.
- An explicitly named non-canonical draft is standalone. It may be printed
  unchanged only when it has no lesson-evidence marker, and it never changes or
  deletes the active handoff.
- Every failure leaves both draft and handoff byte-for-byte unchanged.

## Validator results

Exit status `0` means success. Status `1` reports path, source, hash, review,
evidence, or draft-state errors. Status `2` reports CLI, schema, or unexpected
internal errors. A warning-only result keeps status `0`; human-readable
warnings and errors use:

```text
WARNING path:line [CODE] message
ERROR path:line [CODE] message
```

JSON output always contains separate `warnings` and `errors` arrays. A warning
never changes the report's `ok` value; only an error does.

Codes include `SCHEMA`, `PATH`, `SOURCE_MISSING`, `SOURCE_HASH`, `SOURCE_LOCATION`,
`CONTRACT_HASH`, `CURRICULUM_FRESHNESS`, `CURRICULUM_SOURCE_RELATION`,
`TARGET_DECISION`, `EXTERNAL_IDENTITY`, `EXTERNAL_CACHE_MISSING`,
`EXTERNAL_CACHE_IDENTITY`, `EXTERNAL_SOURCE_RELATION`, `REVIEW_STALE`,
`REVIEW_NOT_PASS`, `OBJECTIVE_COVERAGE`, `EVIDENCE_STATE`,
`ASSESSMENT_ALIGNMENT`, `DRAFT_MARKER`, `DRAFT_CONTENT`, `TIL_COVERAGE`, and
`TIL_REVIEW_STALE`.
