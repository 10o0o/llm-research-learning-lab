# Recordkeeping policies

기록 작성·챕터 마무리·보관·초기화를 다룰 때 직접 읽는 권한과 근거 정책이다. 절차는 해당 스킬을 따른다. 일반 수업의 필독이나 자동 기록 지시가 아니다. 현재 재개는 [STATE](../../STATE.md), 공통 소유권·Git은 [공통 정책](learning-policies.md)을 따른다.

## Default chapter-transition wrap-up

AX/RE 단위 완료는 실제 챕터 전환이 아니다. 단위 완료만으로 finish-chapter·기록 생성·초기화·로컬 커밋 권한이 생기지 않는다.

At a confirmed chapter transition, invoke
[finish-chapter](../skills/finish-chapter/SKILL.md) before starting the next
chapter, without a separate wrap-up request. The learner has authorized this as
the default: preserve saved chapter notebooks, write matching reviews, update
demonstrated knowledge, and reset only verified chapter workspaces after the
evidence prerequisites below. It also authorizes a scoped local commit after validation. `$finish-chapter` and `이번 챕터 정리해줘` also invoke it directly.
Confirm the chapter boundary from the approved course and actual work; an ordinary
cell, subsection, or session ending is not a chapter transition. Report incomplete
requirements instead of silently marking a chapter complete. A wrap-up does not
authorize changing courses; use the already approved next step or ask about scope.
It does not activate for `완료`, `이해했어`, or `오늘 학습 종료` alone.
Ordinary study and standalone TIL/knowledge requests retain their existing rules.

Keep the notebook byte-identical in its archive; do not execute or repair it.
Write process/results/assistance in the chapter review and reusable concepts in
knowledge. The wrap-up has no fixed concept-count limit. Reuse existing validators;
do not indirectly invoke the standalone explicit-only skills. Do not create a TIL,
tracking system, or next lesson automatically. Course-specific restrictions apply.
Confirm the learner's unassisted concept drafts before knowledge edits or workspace
reset. If a needed draft is missing, ask for it instead of writing it for them.
Learner-authored conceptual answers already in the conversation can serve as
drafts; do not require a duplicate formal note. Use their actual explanation and
interpreted artifacts, not the tutor's prose or an "understood" response, and
preserve any assistance boundary. Concepts without learner evidence stay in the
review as open questions, not as established knowledge.

Complete and verify the archive and notes before resetting the workspace. The
archive/reset/validator sequence is defined only in [finish-chapter](../skills/finish-chapter/SKILL.md).
The wrap-up's previously authorized local commit proceeds without another commit
question. Standalone STATE updates are still edit-only except at an explicit
study stop. Unrelated changes are excluded unless explicitly included; a chapter
wrap-up alone does not authorize push, while the study-stop procedure does.

## Standalone writing and sources

- Ordinary study may prepare a necessary starting notebook or script for the
  current approved activity under the [common setup policy](learning-policies.md#learning-setup-and-starting-materials). Do not invent
  supplementary exercises or replace official implementations, exercises, or
  assignments with them.
- Other `practice/` artifacts require an explicit learner request or the
  authorized chapter-transition wrap-up's archive and review.
  Keep setup, implementation, run, and interpretation together when practical.
- Existing notebooks may retain historical metadata. Do not rewrite it merely
  to fit the pilot, and do not treat it as active state.
- Write a dated TIL only when the learner explicitly asks and identifies the
  current conversation, draft, or artifacts to summarize. Do not infer missing
  claims or auto-commit it.
- Update `knowledge/` on an explicit request or during the authorized chapter
  transition, and only from learner-authored
  explanation, calculation, or executed and interpreted artifacts. `NO_CHANGE`
  is valid.
- Keep source material distinct from learner work. Do not copy copyrighted
  material into public notes. Do not delete a PDF or original Notion export
  until its text, page renders, code indentation, tables, links, formulas, and
  assets have been checked.
- Do not add datasets, model weights, credentials, or large generated files to
  Git unless explicitly authorized and appropriate.

개별 작성의 입력·형식·검사 절차는 [save-today-til](../skills/save-today-til/SKILL.md)과 [update-learning-knowledge](../skills/update-learning-knowledge/SKILL.md)에 둔다. 두 스킬은 명시 요청 때만 사용하며 별도 커밋·푸시 권한이 없다.
