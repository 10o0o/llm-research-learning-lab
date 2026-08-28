---
name: update-learning-knowledge
description: Create or update zero to three durable concept notes from confirmed learner-authored lesson evidence plus completed and interpreted practice, without requiring a TIL, then commit only validated knowledge paths. Use at UPDATE_KNOWLEDGE in an authorized daily full flow or when the learner explicitly asks to save demonstrated understanding. Do not teach, format TILs, copy tutor prose, infer mastery, or write before practice is terminal.
---

# Update Demonstrated Knowledge

Maintain `knowledge/` as the learner's current reusable understanding, not a
lecture summary, transcript, or progress log. Read `knowledge/template.md`,
`knowledge/README.md`, related existing notes, and only the exact evidence
input.

In the daily full flow, prepare the TIL-independent input with:

```bash
python3 .agents/skills/update-learning-knowledge/scripts/prepare_session_knowledge_input.py
```

It requires the exact captured session and a terminal practice decision. A
completed local or external practice must have its path/hash/commit and learner
interpretation verified; otherwise return `PRACTICE_INCOMPLETE`. A justified
`NO_EXTRA_PRACTICE` may proceed from session evidence alone. For manual use,
an exact finalized TIL, current learner answer, calculation, or interpreted
artifact remains a valid named input.

Select zero to three concepts with durable reuse value. Update an existing
date-free concept note in place or create the narrowest
`knowledge/<area>/<concept>.md`. Include only the demonstrated range: concise
definition, mechanism, conditions, useful example, and stable cautions. Do not
claim experiments that did not run or complete a partial account from tutor or
source prose. `NO_CHANGE` is the correct result when evidence is insufficient
or the current note already says the same thing.

Validate every changed path:

```bash
python3 .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py \
  knowledge/<area>/<concept>.md
git diff --check -- knowledge/<area>/<concept>.md
```

For a nonzero update, commit only the one to three changed knowledge paths with
`knowledge: YYYY-MM-DD 학습 내용 반영`. Record that exact commit in the daily
cursor before moving to `PLAN_NEXT`. For `NO_CHANGE`, record the terminal
result without creating a placeholder commit. Never push.
