---
name: save-today-til
description: Explicit standalone TIL writing from learner-authored content and exact named artifacts. Use only when the learner explicitly invokes $save-today-til. Do not activate from an ordinary TIL request or after study, read ignored state, infer evidence, update knowledge, commit, or push.
---

# Save a Standalone TIL

Use only the inputs named in the current request: learner-authored explanations
or calculations in the current conversation, an exact draft, and exact
executed artifacts with the learner's interpretation. `STATE.md` is a resume
bookmark, not evidence. Do not read ignored files, reconstruct old sessions,
or scan Git history for material to include.

Write or merge one dated file under `til/YYYY/MM/YYYY-MM-DD.md`. Preserve any
existing confirmed content. Organize new material concept-first:

1. concept and core definition;
2. mechanism, validity conditions, and limitation;
3. the learner's own example, calculation, or application;
4. an observed and interpreted result when one actually ran;
5. useful source, practice, and knowledge links.

Tutor prose, lesson delivery, file existence, and green tests are not learner
claims. Never invent an explanation, output, experiment, or result. A manual or
standalone note may preserve uncertainty the learner actually expressed.

Use `til/template.md` when creating a new file and validate the finished note:

```bash
python3 .agents/skills/save-today-til/scripts/validate_til.py \
  til/YYYY/MM/YYYY-MM-DD.md
git diff --check -- til/YYYY/MM/YYYY-MM-DD.md
```

Show the exact changed path and validation result. TIL authorization permits
only the requested file edit. Commit and push each require a separate explicit
request.
