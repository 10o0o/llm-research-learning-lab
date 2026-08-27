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
3. Give a fresh read-only reviewer the handoff and every manifest input. The
   reviewer must not be the contract author and must not be given an intended
   answer.
4. Add one semantic-review attempt. A `changes_required` verdict permits one
   contract correction and one new fresh review. There are at most two review
   attempts. Reviewer unavailability or a second non-pass verdict requires
   status `blocked`; do not teach.
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
   delivered. The save workflow
   may remove a completed handoff only after every confirmed evidence item is
   drafted, `--til-ready` passes, and the dated TIL commit succeeds.

Schema version 4 has no in-place migration from version 3. Rebuild an older
handoff from the current template; do not guess how old state maps to the new
Objective-level evidence and Curriculum Treatment fields.

Resume an existing handoff only when the named primary input path and hash are
unchanged. A source, curriculum, manifest, or lesson-contract change makes a
prior review stale. Never overwrite an `active`, `paused`, or `blocked` handoff
with a different lesson without an explicit close-or-replace decision.
A `completed` handoff may be replaced for a new lesson only when every
confirmed evidence item is already `drafted`. Otherwise preserve it until the
append helper recovers the pending evidence; completion alone is not permission
to discard learner content.

## Metadata

Metadata is a Markdown bullet list with exactly these keys:

- `schema_version`: currently `4`.
- `lesson_id`: stable lowercase identifier matching
  `[a-z0-9][a-z0-9-]{2,63}`.
- `title`: one non-empty line.
- `status`: `preparing`, `review_pending`, `active`, `paused`, `blocked`, or
  `completed`.
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
- Roles are `primary`, `asset`, `course-index`, `curriculum`, `knowledge`,
  `til`, or `practice`.
- Include at least one `primary` input and exactly one `curriculum` input. The
  curriculum row path is exactly `CURRICULUM.md`.
- Every primary under `materials/private/<course>/` requires that exact
  course's `materials/private/<course>/INDEX.md` as a `course-index` input.
  `--ready` and `--til-ready` apply blocking freshness checks to the lesson's
  semantic slice: each selected primary, its directly referenced local assets,
  every supporting source actually manifested for the lesson, the selected
  Curriculum targets and treatments, and the exact registry and INDEX rows for
  those sources. Missing, stale, unregistered, or mismatched inputs inside that
  slice block readiness. Unrelated source problems in the same course are
  reported as warnings and do not block the lesson gate. The standalone
  `validate_curriculum.py --strict-sources` command remains the course-wide
  parity and freshness gate.
- Keep the complete course `INDEX.md` and `CURRICULUM.md` in the manifest. Any
  byte change to either file still makes an existing handoff and its semantic
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
4. `Curriculum Treatment Map`
5. `Learner Evidence Baseline`
6. `Audited Findings`
7. `Source Coverage Index`
8. `Declared Goal Alignment`
9. `Guidance Map`
10. `Observable Objective Map`
11. `Concept Path`
12. `Prepared Teaching Steps`
13. `Deferred`

List one to three stable `CC-*` or `TR-*` curriculum IDs that actually occur in
the manifested `CURRICULUM.md` under Curriculum Targets.

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
- `defer-gap` requires `별도 자료 확보` or `원본 복구 후 재감사`. It may
  link existing `source-core` Objectives, but never added content that pretends
  to fill the missing source. External material is not source-core until the
  user separately authorizes its registration and audit.
- `defer-track` requires a `TR-*` target with `트랙 선택 시 확보` and uses
  Objective IDs `none`.

Coverage Mode contains exactly one of:

```text
- mode: full-source
- mode: focused
```

Use `full-source` when the learner requests all named sources or an entire
range. It requires every primary source's core content, including source-body
formulas, code, figures, examples, and embedded checks. Separate
`course-provided-practice/` inputs stay outside this gate unless the learner
explicitly includes them. Use `focused` only for an explicitly selected subset;
record excluded source locations and reasons rather than silently dropping
them.

Source Coverage Index has these exact columns and exactly one ordered row per
primary manifest input, in manifest order:

```text
Primary ID | Declared Goal IDs | Objective IDs | Guidance IDs | Excluded locations | Reason
```

ID cells are comma-separated or `none`. They must exactly inventory that
primary's declared goals, source-core objectives, and guidance items. A
full-source primary may be entirely guidance, but every technical source-body
core still requires an objective. Use `none` for both exclusions and reason
when nothing is excluded. Otherwise separate exact `path#location` entries
with semicolons and state why each excluded part is non-core or outside the
focused request. The index is not itself proof of completeness: the semantic
reviewer still compares it with the entire source.

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
  objective points to a primary input. Markdown and text locations must match
  an actual normalized line. PDF locations use `path.pdf#page-N` or
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

`review_attempt` equals the number of attempt blocks and is restricted to
`0`, `1`, or `2`. Attempt IDs are contiguous. Each block contains:

- `reviewer_id`: stable identity different from `author_id` and from every
  other reviewer in this handoff;
- `reviewer_mode`: exactly `fresh-subagent`;
- `reviewed_at`: RFC 3339 timestamp;
- `verdict`: `pending`, `pass`, `changes_required`, or `unavailable`;
- `reviewed_input_manifest_sha256` and `reviewed_contract_sha256`;
- a separate Blocking Findings body.

Use this exact block syntax immediately after the top-level
`- review_attempt: N` field. Replace every placeholder and use the same attempt
number in the marker and heading:

```markdown
<!-- semantic-review-attempt:1:start -->
### Review Attempt 1

- reviewer_id: replace-with-fresh-reviewer-id
- reviewer_mode: fresh-subagent
- reviewed_at: YYYY-MM-DDTHH:MM:SSZ
- verdict: pass
- reviewed_input_manifest_sha256: replace-with-current-manifest-sha256
- reviewed_contract_sha256: replace-with-current-contract-sha256

#### Blocking Findings

- none
<!-- semantic-review-attempt:1:end -->
```

For a pass, Blocking Findings must be exactly `- none`. For
`changes_required` or `unavailable`, replace it with at least one concrete
non-`none` blocking finding. A second attempt uses `2` in both marker lines and
its heading, plus a different fresh `reviewer_id`.

Only the latest attempt controls readiness. The first attempt may be followed
by another only when its verdict was `changes_required`. A pass is current only
when both reviewed hashes equal the handoff's recomputed hashes. An unavailable
reviewer ends the review flow immediately.

The reviewer checks source fidelity, facts, formulas, tensor shapes, code
claims, marker classification, curriculum alignment, lesson scope, and learner
evidence provenance. For every primary file, compare every explicit goal with
Declared Goal Alignment, then compare essential source-native formulas, code,
figures, examples, and checks with the Objective Map. Verify that guidance is
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
  `changes_required`.
- For at least one primary file with multiple explicit learning goals, match
  each goal independently to learning, guidance, or source-gap. If only a
  subset was extracted, return `changes_required` even when the file appears in
  Source Coverage Index.
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
- Audit technical body sections independently of declared goals. Reject a
  contract that covers the listed goals but omits a source-native limitation,
  decision rule, API comparison, threshold rule, worked example, or embedded
  check needed to understand the lesson. If a parent section contains both a
  basic comparison and a nested optional implementation detail, only the exact
  nested locator may be intentionally deferred.

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
requiring a current independent lesson-contract pass.

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

Codes are `SCHEMA`, `PATH`, `SOURCE_MISSING`, `SOURCE_HASH`, `SOURCE_LOCATION`,
`CONTRACT_HASH`, `CURRICULUM_FRESHNESS`, `REVIEW_STALE`, `REVIEW_NOT_PASS`, `OBJECTIVE_COVERAGE`, `EVIDENCE_STATE`,
`ASSESSMENT_ALIGNMENT`, `DRAFT_MARKER`, `DRAFT_CONTENT`, `TIL_COVERAGE`, and
`TIL_REVIEW_STALE`.
