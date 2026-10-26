---
name: study-session
description: >-
  Resume a selected study activity, explain its concepts, review the learner's
  own work, and save verified progress. Use for starting or continuing study,
  questions or code review within the active learning activity, and ending or
  pausing study in this repository. Do not use for curriculum redesign,
  repository maintenance, or general implementation requests.
---

# Study session

공통 행동 규칙은 [AGENTS.md](../../../AGENTS.md)를 따른다.
현재 위치의 원본은 [STATE.md](../../../STATE.md)다.
이 스킬에 공통 정책이나 강의 목록을 중복 작성하지 않는다.

## 1. 현재 요청에 맞춰 진입한다

- 시작·계속:
  STATE와 연결된 현재 코드·출력을 확인하고 저장된 다음 행동으로 돌아간다.
  현재 목표와 이어갈 지점을 짧게 안내한다.

- 개념 질문:
  질문에 직접 답하고 현재 학습과 연결한다.
  설명만 필요한 요청에 새 구현 과제나 확인 시험을 자동으로 붙이지 않는다.

- 코드·결과 리뷰:
  사용자가 제시한 코드·출력·해석부터 검토한다.
  해당 작업을 처음부터 다시 설명하거나 핵심 구현을 대신 고치지 않는다.

- 종료·중단:
  새 학습 활동을 시작하지 않는다.
  아직 저장되지 않은 확인 사항과 다음 행동을 AGENTS의 절차로 저장한다.

## 2. 필요한 학습 활동만 수행한다

구현 전 설명이 필요하면 현재 질문, 입출력, 전체 흐름, 직접 작성할 부분,
결과 확인 방법을 안내한다.

학습자가 작성·실행할 차례에는 기다린다.
막히면 현재 문제를 해결하는 데 필요한 설명과 도움을 제공한다.

실제 결과가 있으면 학습자의 첫 해석을 바탕으로 피드백한다.
조건 변경은 학습에 도움이 될 때만 제안하며 매번 강제하지 않는다.

새 강의·프로젝트·공식 과제를 선택하는 요청이 있을 때만
[CURRICULUM](../../../CURRICULUM.md)의 해당 구간과 필요한 과정별 정책을 확인한다.

## 3. 재개 위치를 유지한다

의미 있는 진행·막힘·다음 행동 변경과 종료·중단 시
AGENTS의 자동 저장 절차를 따른다. 새 근거가 없으면 변경하지 않는다.

미완료와 도움 범위를 보존하고 다음 행동 하나를 남긴다.
저장 후 파일을 다시 확인하며, 저장 실패는 미저장으로 알린다.

별도 TIL, 지식 서재, 점수판, 진도 데이터베이스를 만들지 않는다.
지침을 읽거나 검사를 통과한 것과 실제 학습 개선은 다르다.
