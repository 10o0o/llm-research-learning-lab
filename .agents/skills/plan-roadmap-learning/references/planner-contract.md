# Learning planner contract

Use this contract to recommend the next learning move. It is a read-only decision aid, not learner progress state.

## Inputs and evidence boundaries

Read the smallest relevant subset in this order:

1. `ROADMAP.md` for broad specialization priority;
2. the target and prerequisite rows in `CURRICULUM.md` for operational gaps and source relations;
3. the related registry rows, course `INDEX.md`, and read-only freshness result;
4. learner-authored evidence in the current conversation, `knowledge/`, finalized dated TIL, and executed practice;
5. challenge evidence only when an exact target or TIL link, actual verification result, and learner explanation all exist.

Treat practice implementation plus executed output and learner interpretation as the strongest local evidence. Treat `knowledge/` as the current explanation but verify its cited provenance. Treat TIL as dated historical evidence. Tutor prose, source summaries, lecture completion, green checks alone, and platform passes alone do not establish mastery.

Do not scan unrelated history merely to fill the response. If evidence is absent or contradictory, classify it as `unknown`.

## Freshness and prerequisite classification

Run the relevant structural or scoped source validator when needed. Keep registry health separate from the learning recommendation:

- `registry_action: REPAIR_REQUIRED` when a selected or candidate local source has missing registration, stale bytes, incomplete audit, or INDEX parity failure;
- `registry_action: NONE` when the relevant source slice is current or the recommendation does not rely on a local source.

Classify every prerequisite that can change the recommendation:

- `satisfied`: learner-authored explanation or implemented, executed, and interpreted evidence supports reuse;
- `bridgeable`: enough prior evidence exists for a short explicit bridge before the target;
- `blocking`: the target cannot be understood or practiced safely without first learning the prerequisite;
- `unknown`: current evidence cannot support one of the other judgments.

Never hardcode a universal course order. A blocking prerequisite outranks specialization preference; otherwise use ROADMAP priority to break ties.

## Candidate selection

Rank candidates by:

1. unresolved work in an existing linked practice artifact;
2. an audited local source that addresses the highest-priority current gap;
3. an unaudited local source, clearly paired with registry repair before learning;
4. one official primary external artifact when no suitable local source exists.

Return at most three targets. Prefer one precise next artifact and range over a broad syllabus. An optional bridge may precede the primary target, but it is not a reason to add unrelated study.

External identity is the tuple `provider + course + offering or edition + artifact`. Do not combine slides, videos, assignments, or readings from different offerings as if they were one audited source. Include the official URL and exact chapter, lecture, or assignment range. Mark every download or registration as awaiting user approval.

For this repository's current `CC-PROB-01` gap, preserve the already selected
candidate identity while its bytes are pending: provider `Harvard University`,
course `Stat 110: Introduction to Probability`, edition `Second Edition`, and
artifact `official complete textbook PDF` intended for
`materials/private/harvard-stat110-probability/00-01_introduction_to_probability_2e.pdf`
as `SRC-HARV-STAT110-2E-00-01`. Recommend only Chapters 1–4 as the first
learning range. Until the user supplies the official PDF and the coach audits
and registers it, use `registry_action: NONE`,
`learning_action: PROPOSE_EXTERNAL_SOURCE`, and an explicit approval state of
waiting for the user-provided PDF. Report its URL or access location as pending
the supplied artifact rather than searching for, downloading, substituting, or
blending another probability course. Once that exact artifact is registered
and fresh, it becomes a local-source candidate under the normal ranking rule.

## Output contract

Always return these two independent axes first:

- `registry_action`: `REPAIR_REQUIRED` or `NONE`;
- `learning_action`: `CONTINUE_EXISTING_PRACTICE`, `CONTINUE_LOCAL_SOURCE`, `PROPOSE_EXTERNAL_SOURCE`, or `NO_NEW_SOURCE_NEEDED`.

Then state:

- one to three target competency IDs and why they rank now;
- the evidence used and its limitations;
- prerequisite states and any smallest bridge;
- the exact next artifact and range;
- explicit excluded scope;
- expected time, compute, data, and access burden using honest qualitative bounds;
- observable completion evidence, such as an explanation, hand calculation, shape trace, implementation, executed check, or interpreted output;
- approval state for any future write, download, registration, or replacement.

When `registry_action` is `REPAIR_REQUIRED`, say whether learning can safely continue from an already verified artifact or must wait for the source repair. Do not turn the repair into proof of learner understanding.
