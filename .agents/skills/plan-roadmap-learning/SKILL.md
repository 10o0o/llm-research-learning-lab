---
name: plan-roadmap-learning
description: Choose one actual AI, ML, deep-learning, mathematics, or LLM Curriculum target and at most one nearly satisfied bridge from this repository's ordered ROADMAP routes and learner-authored evidence, then resolve an exact source or directly related existing practice. Use when deciding what to study next or at SELECT_TARGET in the daily full learning flow. Remain read-only; do not teach, cache, register, create practice, update progress, or claim mastery.
---

# Plan the Next Learning Target

Select the target before resolving material. Read `ROADMAP.md`,
`CURRICULUM.md`, relevant `knowledge/`, finalized TILs, interpreted practice or
challenge evidence, and `tmp/active-learning-flow.json` when it exists. The
cursor is resumable operational evidence, not mastery or a progress database.

Use `scripts/inspect_target_graph.py` for the ordered endpoint routes. Keep
these meanings separate:

- `endpoint`: the long-term ROADMAP destination;
- `primary_target`: the actual competency taught in this cycle;
- `bridge_target`: at most one almost-satisfied prerequisite that can be closed
  inside the same lesson.

## Selection order

1. Honor an explicit user-named target.
2. Otherwise choose the earliest ROADMAP stage that still needs evidence.
3. On that route, make the actionable blocking frontier the primary target.
4. If the route has no blocker and the endpoint lacks required evidence, make
   the endpoint primary.
5. Use a bridge only for one nearly satisfied direct prerequisite. Two
   independent gaps require separate cycles; choose the gap with greater
   downstream impact as primary.
6. If an unknown state can change the choice, return `NEED_DIAGNOSTIC`. Return
   `NO_ACTIONABLE_TARGET` only when no executable target remains.

Source availability, chapter order, and an unrelated unfinished practice never
change target priority. A practice may be resumed only when it directly covers
the selected primary or bridge, still needs valuable execution evidence, is not
paused, and has no concept blocker. A platform pass alone never satisfies a
prerequisite.

## Resolve the exact next artifact

After target selection, rank executable inputs as:

1. a directly related existing practice that meets the reuse gate;
2. an audited registered local source;
3. an unaudited local source that needs repair;
4. an official external primary source.

Identify external material by provider, course, offering or edition, artifact,
official URL, and exact scope. The agent discovers and verifies the URL; the
cache helper only retrieves a supplied URL. Recommend registration after a
second independent lesson or when the source becomes a durable route input,
but never register automatically.

Return exactly these axes:

- `target_state`: `START_TARGET | CONTINUE_TARGET | BRIDGE_PREREQUISITE | NEED_DIAGNOSTIC | NO_ACTIONABLE_TARGET`;
- `registry_action`: `REPAIR_REQUIRED | NONE`;
- `learning_action`: `CONTINUE_EXISTING_PRACTICE | CONTINUE_LOCAL_SOURCE | USE_TEMPORARY_EXTERNAL_SOURCE | AWAIT_SOURCE_APPROVAL | NO_NEW_SOURCE_NEEDED`;
- `source_persistence`: `LOCAL_REGISTERED | EPHEMERAL | REGISTRATION_RECOMMENDED | NONE`.

Also state endpoint, primary and optional bridge, selection reason,
prerequisite states, missing evidence token, completion evidence for the actual
primary, exact artifact and bounded source scope, time/compute/access burden,
and approval status. Do not edit any file or start the lesson.

For the full output and maintenance contract, read
`references/planner-contract.md`. Use
`references/forward-test-scenarios.md` only for contract maintenance and a
fresh read-only reviewer forward test; never store a generated planner result.
