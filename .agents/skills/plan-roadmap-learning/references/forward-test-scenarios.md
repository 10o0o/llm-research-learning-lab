# Planner forward-test scenarios

Use these scenarios only after changing planner policy. Give a fresh read-only reviewer each prompt, this skill, the planner contract, and the referenced raw repository evidence. Do not give the reviewer the expected invariants, and do not save its generated answer.

## F01 Higher-priority target is source-independent

- Prompt: "현재 상태에서 다음 목표를 정해줘. 1순위 목표에는 로컬 자료가 없고, 2순위 목표에는 감사된 자료가 있어."
- Fixture facts: no learner evidence changes the prerequisite route; the higher-priority endpoint has no local source while a lower-priority frontier has a fresh local source.
- Expected invariants: choose from the higher-priority endpoint route before source resolution; do not choose the lower-priority target because its source is convenient; resolve the selected gap afterward with a temporary official source or approval state.

## F02 Chapter order does not select a target

- Prompt: "KDL 다음 장이 남았으니 그걸 바로 공부하면 될까?"
- Fixture facts: the next KDL chapter is not directly related to the selected endpoint or its blocking prerequisite.
- Expected invariants: do not select it because it is the next chapter; choose one primary target from the graph first and use the chapter only if it directly supports that target.

## F03 Existing practice is conditionally reusable

- Prompt: "미완료 실습이 몇 개 있는데 무조건 먼저 끝내야 해?"
- Fixture variants: unrelated, low-value, paused, and legacy-without-target-metadata artifacts; then one unfinished artifact directly linked to the selected target with needed execution evidence and no conceptual blocker.
- Expected invariants: reject automatic priority for the first group; reuse only the directly linked valuable artifact in the second variant and keep the same target decision.

## F04 Blocking frontier and unknown prerequisites

- Prompt: "최우선 endpoint를 향해 지금 무엇을 해야 해?"
- Fixture variants: several prerequisite branches are incomplete, including a nearly completed bridgeable branch with an unfinished practice and one actionable blocking frontier; in the other, evidence is insufficient to distinguish blocking from satisfied.
- Expected invariants: keep the endpoint as `primary_target` and return the actionable blocker, not the convenient bridgeable practice, as `bridge_target` with `BRIDGE_PREREQUISITE`; for the unknown variant use `NEED_DIAGNOSTIC`, `NO_NEW_SOURCE_NEEDED`, and `source_persistence: NONE` without guessing.

## F05 Challenge pass is not prerequisite evidence

- Prompt: "플랫폼 문제를 통과했으니 이 선수개념은 충족됐다고 봐도 돼?"
- Fixture facts: only a platform pass is available; no linked learner explanation, calculation, implementation interpretation, or target mapping exists.
- Expected invariants: do not classify the prerequisite as `satisfied`; use `unknown` unless other learner-authored evidence supports a stronger state.

## F06 Stat110 resolves only a selected probability target

- Prompt: Test both "CC-PROB-01을 다음 목표로 공부할 자료를 정해줘." and "Systems endpoint로 갈 다음 목표를 정해줘."
- Fixture facts: `SRC-HARV-STAT110-2E-00-01` is registered and fresh at `materials/private/harvard-stat110-probability/00-01_introduction_to_probability_2e.pdf`.
- Expected invariants: only the `CC-PROB-01` variant uses Harvard Stat110, Second Edition, the exact source ID/path, and Chapters 1–4 with `CONTINUE_LOCAL_SOURCE`; the Systems variant does not choose probability because Stat110 is available.
