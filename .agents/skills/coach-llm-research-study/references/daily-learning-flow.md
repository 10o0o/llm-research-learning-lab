# Daily learning flow contract

This is the normative contract for the single ignored
`tmp/active-learning-flow.json` cursor. The cursor joins existing specialist
skills; it is not a new orchestration skill, progress database, or mastery
record. `scripts/daily_learning_flow.py` is its executable implementation.

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

## Cycle state

Each cycle records stable cycle/lesson identity, primary and optional bridge,
exact handoff path/hash, status and timestamps, confirmed concept projection,
exact learner evidence content/hash, source provenance, practice state,
knowledge state, exact learning commit records, next-target preview, and TIL
consumption receipt.

Only confirmed learner-authored evidence enters the cursor. Its exact content,
concept IDs, objective IDs, evidence kind, content hash, and capture time come
from the completed handoff. Tutor prose, delivery, partial answers,
misconceptions, and file existence are excluded.

The practice state is:

- `pending` before routing;
- `awaiting` for one exact local or external artifact;
- `completed` only after execution, interpretation, completion validation,
  exact artifact hash, and exact path-limited commit;
- `no-extra-practice` only with a justified no-practice decision.

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

- the schema-v9 lesson session is completed and captured;
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

## Safety

All paths use canonical repository-relative POSIX syntax and may not escape the
repository. Cursor writes use a same-directory temporary file, fsync, and atomic
replace. The cursor is ignored and must never be committed. Validation never
infers target satisfaction or mastery from a checker, platform pass, file, or
commit.
