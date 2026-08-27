---
name: plan-roadmap-learning
description: Choose one primary AI, ML, deep-learning, or LLM curriculum target and at most one bridge prerequisite from this repository's static ROADMAP endpoints, target graph, and learner-authored evidence, then resolve the exact next source or directly related existing practice. Use when the learner asks what target, course, lecture, topic, source, or practice to pursue next. Keep the result read-only; do not teach, cache or register sources, edit files, create practice, or claim mastery.
---

# Plan Roadmap Learning

Turn the repository's static endpoints, target graph, and demonstrated learner evidence into one executable target decision without creating another progress tracker.

Read and follow [`references/planner-contract.md`](references/planner-contract.md) whenever this skill is used.

## Preserve responsibility boundaries

- This skill reads and recommends only. It may run `scripts/inspect_target_graph.py` and read-only validators, but it must not edit files, cache or register material, create a lesson handoff, teach, generate practice, or update TIL/knowledge.
- Leave source fidelity and curriculum-coverage judgments to `$coach-llm-research-study`. Report an existing registry problem; do not repair or reinterpret it here.
- Leave adaptive delivery to `$teach-course-material` and hands-on generation or attempt feedback to `$suggest-learning-practice`.
- Temporary retrieval of a public official HTTPS source may be proposed for the lesson flow. Require approval for permanent registration, paid or authenticated access, large or unsupported artifacts, and external participation.

## Produce a bounded recommendation

1. Run `scripts/inspect_target_graph.py` for the relevant endpoint or user-named target, then inspect only the evidence needed to classify its prerequisites and missing evidence.
2. Inspect only evidence relevant to the candidate targets: current learner-authored answers, current `knowledge/`, finalized TIL, executed/interpreted practice, and explicitly linked challenge work.
3. Select exactly one primary target and at most one bridge using the contract. Do not use source availability or chapter order to choose the target.
4. When several prerequisites are missing, choose an actionable frontier
   blocker by graph impact before looking at practice. A narrow bridgeable gap
   may be taught inline; it must not hide a deeper blocking prerequisite.
5. After target selection, reuse only a directly linked, valuable practice with required execution evidence and no blocker. Otherwise resolve a current local source or one exact official external artifact.
6. Return all four decision axes and the observable completion evidence required by the contract. State uncertainty instead of inferring progress from file presence or completion signals.

Do not persist a planner snapshot, daily status, mastery checkbox, score, or completion percentage.

## Maintain this skill

After changing ranking, evidence, prerequisite, or source-state behavior, read
[`references/forward-test-scenarios.md`](references/forward-test-scenarios.md)
and run its prompts through a fresh read-only reviewer. Give the reviewer this
skill, the planner contract, and raw repository evidence, but do not expose the
scenario file or its expected invariants. Compare the result afterward and do
not save generated answers as repository state.
