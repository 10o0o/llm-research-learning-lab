# Planner forward-test scenarios

Use these scenarios only after changing planner policy. Give a fresh read-only
reviewer each prompt plus the referenced raw repository files. Do not give the
reviewer the expected invariants, and do not save its generated answer.

## F01 Existing practice outranks a new course

- Prompt: "현재 상태에서 다음에 무엇을 공부하면 좋을까?"
- Fixture facts: the KDL registry is fresh and the existing deep-learning
  Notebook has unfinished learner-owned work; CS336 is not a registered local
  source.
- Expected invariants: continue the exact existing practice or its audited KDL
  source before proposing CS336; do not treat green checks as mastery.

## F02 Registered Stat110 artifact

- Prompt: "CC-PROB-01을 채울 다음 자료를 추천해줘."
- Fixture facts: `SRC-HARV-STAT110-2E-00-01` is registered, fresh, and directly
  related to `CC-PROB-01` at
  `materials/private/harvard-stat110-probability/00-01_introduction_to_probability_2e.pdf`.
- Expected invariants: return `registry_action: NONE` and
  `learning_action: CONTINUE_LOCAL_SOURCE`; preserve Harvard Stat110, Second
  Edition, the registered complete textbook PDF, its exact source ID and path,
  and Chapters 1–4; do not propose the same artifact as a new external source.

## F03 Challenge pass is not prerequisite evidence

- Prompt: "플랫폼 문제를 통과했으니 이 선수개념은 충족됐다고 봐도 돼?"
- Fixture facts: only a platform pass is available; no linked learner
  explanation, calculation, implementation interpretation, or target mapping
  exists.
- Expected invariants: do not classify the prerequisite as `satisfied`; use
  `unknown` unless other learner-authored evidence supports a stronger state.

## F04 Registered Stat110 freshness and exclusion

- Prompt: "이제 CC-PROB-01은 어떤 자료로 이어가면 돼?"
- Fixture variants: test the exact Stat110 source as registered and fresh,
  registered but stale, and explicitly declined in the current conversation
  with an instruction not to propose an alternative source.
- Expected invariants: fresh registration uses the normal local-source ranking;
  stale registration returns `REPAIR_REQUIRED`; a current-conversation decline
  excludes that source without resurrecting the retired external-source pilot,
  inventing a replacement, or persisting candidate state.
