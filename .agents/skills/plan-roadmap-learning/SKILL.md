---
name: plan-roadmap-learning
description: Recommend the next one to three AI, ML, deep-learning, or LLM study targets from this repository's ROADMAP, curriculum coverage, source freshness, and learner-authored evidence. Use when the learner asks what course, lecture, topic, or source to study next or asks for a source for a named curriculum target. Keep the result read-only; do not use this skill to teach, register or download sources, edit the curriculum, create practice, or claim mastery.
---

# Plan Roadmap Learning

Turn the repository's current direction, source state, and demonstrated learner evidence into a small, executable next-learning recommendation without creating another progress tracker.

Read and follow [`references/planner-contract.md`](references/planner-contract.md) whenever this skill is used.

## Preserve responsibility boundaries

- This skill reads and recommends only. It may run read-only validators, but it must not edit files, download or register material, create a lesson handoff, teach, generate practice, or update TIL/knowledge.
- Leave source fidelity and curriculum-coverage judgments to `$coach-llm-research-study`. Report an existing registry problem; do not repair or reinterpret it here.
- Leave adaptive delivery to `$teach-course-material` and hands-on generation or attempt feedback to `$suggest-learning-practice`.
- Require explicit user approval before any later workflow writes, downloads, registers, or replaces a source.

## Produce a bounded recommendation

1. Read `ROADMAP.md`, the relevant `CURRICULUM.md` rows, and the exact source registry or course INDEX needed to verify freshness.
2. Inspect only evidence relevant to the candidate targets: current learner-authored answers, current `knowledge/`, finalized TIL, executed/interpreted practice, and explicitly linked challenge work.
3. Classify prerequisites and select one to three targets using the contract. Prefer an unfinished or directly reusable local artifact over adding new material.
4. If no audited local source can cover the chosen gap, propose one exact official external artifact. Do not download or register it.
5. Return the two action axes and the observable next step required by the contract. State uncertainty instead of inferring progress from file presence or completion signals.

Do not persist a planner snapshot, daily status, mastery checkbox, score, or completion percentage.
