# Target-first learning planner contract

Use this contract to choose one primary curriculum target and, only when needed, one bridge prerequisite. This is a read-only decision aid, not learner progress state.

## Inputs and evidence boundaries

Read the smallest relevant subset:

1. `ROADMAP.md` for static endpoint priority;
2. `CURRICULUM.md` through `scripts/inspect_target_graph.py` for `depth`, prerequisite closure, required evidence, source relations, coverage, and gap action;
3. the selected target's registry rows, course `INDEX.md`, and read-only freshness result;
4. learner-authored evidence in the current conversation, `knowledge/`, finalized dated TIL, and executed practice;
5. challenge evidence only when an exact target or TIL link, actual verification result, and learner explanation all exist.

Do not persist a planner snapshot, target status, mastery flag, score, or completion percentage. Source availability never changes target priority. Resolve source feasibility only after choosing the target.

Implementation plus executed output and learner interpretation is the strongest local evidence. `knowledge/` is the current explanation but its cited provenance still matters. TIL is dated historical evidence. Tutor prose, source summaries, lecture completion, green checks alone, and platform passes alone do not establish mastery.

## Prerequisite and evidence classification

Classify every prerequisite that can change the decision:

- `satisfied`: learner-authored explanation or implemented, executed, and interpreted evidence supports reuse;
- `bridgeable`: a short explicit bridge can close a narrow gap before the primary target;
- `blocking`: the target cannot be learned or practiced safely before this target is addressed;
- `unknown`: available evidence cannot support another classification.

For the chosen target, subtract demonstrated evidence from `required_evidence` and report the remaining evidence tokens. Do not infer a token from file presence. When a prerequisite is `unknown` and that uncertainty changes the route, return a diagnostic instead of guessing.
An evidence token remains missing until learner-authored evidence covers the
materially distinct behaviors named by that target row; one narrow green check
does not satisfy `debug`, `implement`, or `interpret` across the whole target.

## Target selection

Choose exactly one primary target and at most one bridge target in this order:

1. an exact target named by the user;
2. a blocking prerequisite on the path to the earliest still-needed ROADMAP stage;
3. the active target when it still lacks required learner evidence;
4. the current frontier target that unlocks the greatest number of downstream targets;
5. only for a tie, expected time, compute, access cost, and explicit user constraints.

`endpoint` is the ordered ROADMAP destination, never a synonym for the current
lesson target. Before step 2, classify its prerequisite closure. Use the graph
inspector's route edges, downstream counts, endpoint membership, and optional
state-derived frontier candidates as deterministic facts; learner evidence
still determines each state.

A frontier target is one whose own prerequisites are `satisfied` or can be
closed by one short inline `bridgeable` treatment. An actionable `blocking`
frontier becomes `primary_target`. It is not a bridge. Among multiple blockers,
choose the one with the largest route-local downstream count; only then use
time, compute, access cost, explicit user constraints, and finally Curriculum
row order as a reproducible last tie-breaker. When no blocker remains but the
endpoint still lacks required evidence, the endpoint itself becomes
`primary_target`.

`bridge_target` is reserved for exactly one mostly satisfied prerequisite of
the selected primary target that can be closed inside that lesson. When two or
more prerequisite gaps need materially distinct assessed treatment, promote
the highest-impact gap to `primary_target` and use no bridge instead of hiding
several lessons behind one target. If an `unknown` state could change the
primary choice, return `NEED_DIAGNOSTIC` before source resolution.

A chapter number, source order, local source availability, or unfinished
artifact cannot independently select a target.

After selecting the target, reuse an existing practice only when all are true:

- its metadata directly names the primary target or bridge target;
- at least one still-required execution evidence token remains;
- completing it is valuable relative to its time and compute cost;
- it is not paused or explicitly deferred;
- no unresolved conceptual blocker makes practice premature.

Unrelated, low-value, paused, legacy-without-target-metadata, or merely unfinished practice does not outrank the target. A directly related useful unfinished practice may determine the next artifact, never the target priority.

## Source resolution after target selection

Keep registry health separate from the learning move:

- `registry_action: REPAIR_REQUIRED` when a selected local source is missing, stale, incompletely audited, or inconsistent with its INDEX;
- `registry_action: NONE` when the selected slice is current or no local source is used.

Prefer a current registered local source when it directly supports the selected target. Otherwise identify one exact official external primary source as `provider + course + offering/edition + artifact + scope`. After choosing the artifact, resolve the smallest registered or ephemeral slice that can close the actual `primary_target` evidence gap. A route or chapter range may describe where later lessons will come from; it does not authorize one lesson to audit or teach the whole range.

Use `learning_action: USE_TEMPORARY_EXTERNAL_SOURCE` when a public official HTTPS artifact can be safely cached and audited for this lesson. Use `AWAIT_SOURCE_APPROVAL` for login, payment, more than 100 MiB, an archive, dataset, model weight, non-HTTPS access, permanent registration, or a user decision that materially changes scope. Never combine artifacts from different offerings or editions as one source.

Use `source_persistence: EPHEMERAL` for the first temporary lesson. Change the recommendation to `REGISTRATION_RECOMMENDED` when the same exact source is needed for a second independent lesson or is becoming a central long-term route. Do not register it automatically. Registered sources use `LOCAL_REGISTERED`; no source need uses `NONE`.

The registered Harvard Stat110 source is normal local material. Resolve its exact Second Edition PDF only when `CC-PROB-01` is the selected target; its mere availability never changes target selection. Chapters 1–4 are the broader target route, not one lesson scope. Each lesson must use an exact registered or ephemeral slice such as the currently relevant pages and boundary context.

## Output contract

Return these four fields first:

- `target_state`: `START_TARGET`, `CONTINUE_TARGET`, `BRIDGE_PREREQUISITE`, `NEED_DIAGNOSTIC`, or `NO_ACTIONABLE_TARGET`;
- `registry_action`: `REPAIR_REQUIRED` or `NONE`;
- `learning_action`: `CONTINUE_EXISTING_PRACTICE`, `CONTINUE_LOCAL_SOURCE`, `USE_TEMPORARY_EXTERNAL_SOURCE`, `AWAIT_SOURCE_APPROVAL`, or `NO_NEW_SOURCE_NEEDED`;
- `source_persistence`: `LOCAL_REGISTERED`, `EPHEMERAL`, `REGISTRATION_RECOMMENDED`, or `NONE`.

Then report:

- exactly one `primary_target`, or `none` only with `NO_ACTIONABLE_TARGET`;
- optional `bridge_target` and each relevant prerequisite state;
- the exact ordered ROADMAP `endpoint` it advances, or `user-directed` for an
  explicitly named target outside every endpoint route;
- the target-first selection reason, keeping endpoint and current target distinct;
- evidence consulted, its limitations, and exact missing evidence tokens;
- observable target completion evidence;
- the exact next artifact and range, plus explicit excluded scope;
- honest qualitative time, compute, data, and access burden;
- approval state for temporary retrieval, persistent registration, paid/authenticated access, or external participation.

`bridge_target` is non-`none` if and only if `target_state` is
`BRIDGE_PREREQUISITE`. `NEED_DIAGNOSTIC` retains the tentative
`primary_target` but uses `bridge_target: none` until the missing evidence makes
the route decidable. `NO_ACTIONABLE_TARGET` alone uses `primary_target: none`.
`START_TARGET` and `CONTINUE_TARGET` use no bridge. A lesson handoff may consume
only the three actionable states; diagnostic and no-action results must return
to the planner before source audit or teaching.

When registry repair is required, state whether learning can continue from already verified bytes or must wait. Repair and source completion are never learner evidence.

For `NEED_DIAGNOSTIC`, use `registry_action: NONE`,
`learning_action: NO_NEW_SOURCE_NEEDED`, and `source_persistence: NONE` unless
the diagnostic itself has already revealed a source integrity problem. Name the
exact evidence needed to decide; these values mean “diagnose before source
resolution,” not that the target is complete or needs no future source.
