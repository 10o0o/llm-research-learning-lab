# Daily learning flow contract

This is the normative contract for the single ignored
`tmp/active-learning-flow.json` cursor. The cursor joins existing specialist
skills; it is not a new orchestration skill, progress database, or mastery
record. `scripts/daily_learning_flow.py` is its executable implementation.
The current cursor schema is `2`.

## Entry points and authorization

- `오늘 전체 학습 흐름 시작` and `전체 학습 흐름 시작` activate
  `full-day` authorization for the current Asia/Seoul calendar date.
- `오늘 학습 시작` activates `lesson-only` authorization.
- `계속` resumes the exact stored phase while same-day authorization is active.
  A new full-day request reactivates preserved paused work after expiry.
- `오늘 학습 종료` writes `PAUSED`, preserves `resume_phase`, and clears
  authorization without creating a TIL.
- `오늘 TIL 저장해줘` does not activate learning. It consumes completed,
  unrecorded cycles through the save skill's exact dated-file commit.

Authorization expires when the Asia/Seoul date changes. Expiry never deletes an
unfinished cycle or an unconsumed completed cycle. Commit rights do not carry
to the next date.

## Phases

The only phases are:

1. `SELECT_TARGET`
2. `PREPARE_LESSON`
3. `TEACH`
4. `DECIDE_PRACTICE`
5. `AWAIT_PRACTICE`
6. `UPDATE_KNOWLEDGE`
7. `PLAN_NEXT`
8. `PAUSED`

The forward path follows this order. `DECIDE_PRACTICE` may move directly to
`UPDATE_KNOWLEDGE` only for a justified `NO_EXTRA_PRACTICE`.
`DEFER_TO_MILESTONE` instead releases the captured cycle as
`milestone-pending` and moves directly back to `SELECT_TARGET`.
`PLAN_NEXT` completes the current cycle and returns to `SELECT_TARGET`.
`PAUSED` records exactly one non-paused resume phase.

Retries are idempotent. Repeating the same evidence, practice decision, or Git
commit is a no-op only when its complete identity is equal. The helper refuses
silent replacement of a different decision or different bytes.

## Top-level state

The cursor records:

- schema version, timezone, flow date, authorization and its date;
- current phase and optional resume phase;
- exact active cycle, handoff, and practice path;
- ordered cycles;
- aggregate learner-evidence hash;
- ordered exact learning commit SHAs;
- dated TIL save receipts;
- creation and update times.

There is at most one unfinished active or paused cycle. Completed cycles remain
until their TIL is explicitly saved; consumption marks them rather than
deleting them.

Schema v2 also permits two non-completed released states. `superseded` preserves
an explicitly restarted attempt and its exact archive/practice receipts;
`milestone-pending` preserves a captured session routed by
`DEFER_TO_MILESTONE`. Neither state is eligible for TIL, knowledge, completion,
or mastery claims, and either releases the cursor to begin a new cycle. A later
module assignment or capstone may name that immutable captured session in its
v5 `learning_inputs`; the released cycle remains an honest historical deferral
record rather than being rewritten as completed or consumed.

## Cycle state

Each cycle records stable cycle/lesson identity, primary and optional bridge,
exact handoff path/hash, status and timestamps, confirmed concept projection,
exact learner evidence content/hash, source provenance, practice state,
knowledge state, exact learning commit records, next-target preview, and TIL
consumption receipt.

After `CAPTURE_SESSION`, `captured_session` is the immutable authoritative
projection. Its exact keys are `schema_version`, `cycle_id`, `lesson_id`,
`primary_target`, `bridge_target`, `handoff_sha256`, `concepts`,
`learner_evidence`, `learner_evidence_sha256`, `source_provenance`, and
`projection_sha256`. The projection hash is SHA-256 over canonical UTF-8 JSON
of all those fields except the hash itself. Downstream practice binds
`captured_session_sha256` to this value and never reinterprets a live handoff or
mutable top-level fields. A new capture requires a schema-v10 handoff. A
v1→v2 migration may preserve an already captured v9 projection as read-only
legacy provenance, but it cannot recapture or promote it.

Only confirmed learner-authored evidence enters the cursor. Its exact content,
concept IDs, objective IDs, evidence kind, content hash, and capture time come
from the completed handoff. Tutor prose, delivery, partial answers,
misconceptions, and file existence are excluded.

The practice state is:

- `pending` before routing;
- `awaiting` for one exact local or external artifact. A created or continued
  local assignment may carry the exact `MA-*` or `PC-*` milestone ID that its
  metadata-v5 Notebook must also bind;
- `completed` only after execution, interpretation, completion validation,
  exact artifact hash, and exact path-limited commit;
- `no-extra-practice` only with a justified no-practice decision.
- `milestone-pending` only for `DEFER_TO_MILESTONE` with one exact `MA-*` or
  `PC-*` ID and an eligible current schema-v10 captured session; migrated
  schema-v9 provenance can never be deferred or upgraded this way. It is not
  equivalent to completed practice. This branch returns directly to target
  selection and does not run implementation, knowledge, or TIL completion for
  the released cycle.

Local Notebook, benchmark, dataset project, and competition execution paths
live under `practice/` and use `.ipynb`. Short external challenge work lives
under `challenges/`. Recommendation, account access, participation, and
submission remain separate approval boundaries.

Knowledge is `pending`, `committed`, or `no-change`. A commit records one to
three exact `knowledge/` paths. `no-change` has no placeholder file or commit.

## Exact Git evidence

Every practice or knowledge commit is recorded by full SHA, committer date,
subject, and sorted exact changed-path set. The cursor accepts it only after
reading Git. Practice and knowledge terminal states must reference one of those
records.

Later TIL composition re-reads each exact SHA and compares all stored metadata.
It additionally verifies the current practice artifact hash and current
knowledge blobs. It never scans unrelated commits by date.

## Cycle completion and TIL consumption

A cycle is completed only when:

- the schema-v10 lesson session is completed and captured;
- confirmed concepts and learner evidence are non-empty;
- practice is `completed` or `no-extra-practice`;
- knowledge is `committed` or `no-change`;
- the planner has stored a next-target preview.

`completed_on` is the Asia/Seoul completion date. That date determines the TIL
path even if the explicit save request happens later.

A TIL save selects completed, unconsumed cycles for one completion date,
recomposes all completed cycles already belonging to that dated file, commits
only the exact dated path, then atomically stores full file hash, commit SHA,
and newly consumed cycle IDs. Failed validation or commit leaves cycles
unconsumed and retryable.

## Migration and explicit restart

`migrate_daily_learning_flow_v1_to_v2.py` is deterministic and idempotent. It
adds v2 fields without rewriting any existing learner evidence, hashes,
practice state, or commit receipts. An already captured v1 session becomes an
immutable schema-v9 legacy projection.

`supersede_learning_cycle.py` requires a concrete reason, a distinct
replacement cycle ID, and one preserved handoff file directly under
`tmp/lesson-attempts/<cycle-id>/`. The archive's bytes and receipt SHA-256 must
equal the selected old cycle's `handoff_sha256`. Its practice receipt must name
an existing `practice/*.ipynb` whose actual metadata is schema v5,
`PRE_LAB / I1_MECHANISM / preserved_attempt`, has both milestone fields null,
and contains exactly one captured-cycle input matching the selected old
cycle's immutable projection. Receipt claims cannot override Notebook
metadata. Validation reopens and rehashes both artifacts. Supersession changes
only cycle lifecycle/supersession fields, preserves learner evidence and its
hashes, releases the active slot, and is idempotent for the same receipt.

## Safety

All paths use canonical repository-relative POSIX syntax and may not escape the
repository. Cursor writes use a same-directory temporary file, fsync, and atomic
replace. The cursor is ignored and must never be committed. Validation never
infers target satisfaction or mastery from a checker, platform pass, file, or
commit.
