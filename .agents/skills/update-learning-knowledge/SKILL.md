---
name: update-learning-knowledge
description: Explicit standalone update of zero to three durable knowledge notes from learner-authored explanations, calculations, or exact executed and interpreted artifacts. Use only when the learner explicitly invokes $update-learning-knowledge. Do not activate from an ordinary knowledge request or after study, read ignored state, infer mastery, commit, or push.
---

# Update Demonstrated Knowledge

Maintain `knowledge/` as the learner's current reusable understanding, not a
lecture summary, transcript, or progress record. Read `knowledge/template.md`,
`knowledge/README.md`, relevant existing notes, and only the exact learner
evidence named in the current request.

Valid inputs are the learner's own explanation or calculation in the current
conversation, or an exact artifact that the learner executed and interpreted.
`STATE.md`, tutor prose, source text, file existence, and green tests alone are
not evidence. Never read ignored state or infer missing mastery.

Select zero to three concepts with durable reuse value. Update an existing
date-free concept note in place or create the narrowest
`knowledge/<area>/<concept>.md`. Include only the demonstrated range: concise
definition, mechanism, conditions, useful example, and stable cautions.
`NO_CHANGE` is correct when evidence is insufficient or existing notes already
say the same thing.

Validate every changed path:

```bash
python3 .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py \
  knowledge/<area>/<concept>.md
git diff --check -- knowledge/<area>/<concept>.md
```

Show the exact changed paths and validation result. Knowledge authorization
permits only the requested file edits. Commit and push each require a separate
explicit request.
