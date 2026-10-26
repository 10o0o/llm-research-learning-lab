---
name: study-session
description: >-
  Resume a selected course from the learning hub, connect its exact material and
  task to the learner's external practice repository, answer in-scope questions,
  review supplied work, and save verified progress. Use for starting, continuing,
  pausing or ending study in this hub and for reporting external practice progress.
  Do not use for curriculum redesign, repository cleanup or general implementation.
---

# Study session

공통 행동 규칙은 [AGENTS](../../../AGENTS.md), 현재 위치는 [STATE](../../../STATE.md)를 따른다.
이 스킬에 강의 목록·공통 정책을 중복 작성하지 않는다.

## 1. 요청에 맞춰 현재 위치를 확인한다

- 시작·계속: STATE의 실제 선택·구간·실습 위치·다음 행동을 읽는다.
  자료가 미선택이면 [CURRICULUM](../../../CURRICULUM.md)의 추천 하나와 시작 위치를
  제시하고 선택을 짧게 확인한다. 자체 과제나 준비도 시험부터 시작하지 않는다.
- 개념 질문: 바로 충분히 설명하고 현재 자료와 연결한다.
  설명만 요청한 상황에 과제·시험·별도 수학 과정을 붙이지 않는다.
- 코드·결과 리뷰: 제시된 코드·출력·학습자 해석부터 검토한다.
  전체 과정을 다시 시작하거나 핵심 코드를 대신 완성하지 않는다.
- 외부 진행 보고: 보고된 강의 위치·실습 경로·결과·도움을 확인한다.
  직접 확인한 산출물과 학습자 보고를 구분한다.
- 종료·중단: 새 활동을 시작하지 않고 아직 저장하지 않은 진행과 미완료를 정리한다.

## 2. 선택한 자료와 외부 실습을 연결한다

현재 자료의 직접 링크, 이번 범위, 직접 수행할 부분, 실제 실습 위치를 짧게 안내한다.
선택한 공식 순서·과제를 기본으로 사용한다. 주제를 넓히는 자료는 현재 필요와 선택을 확인한다.

실습 공간이 미연결이거나 도움 규칙을 전달해야 하면
[외부 실습 안내](../../../docs/external-practice.md)를 사용한다.
존재하지 않는 레포·파일을 만든 것으로 기록하거나 허브 안에 새 실습을 생성하지 않는다.
외부 공간의 기존 지침과 공식 과제 정책도 확인한다. 공식 과제일 때만
[과정별 정책](../../references/official-course-policies.md)을 추가로 읽는다.

학습자가 작성·실행할 차례에는 기다린다. 막히면 설명·오류 해석·작은 확인 방법을 제공한다.
이미 제공된 결과가 있으면 학습자의 해석을 바탕으로 피드백한다.

## 3. 재개 위치를 저장한다

의미 있는 진행·막힘·다음 행동 변경과 종료·중단에는 AGENTS의 자동 저장 절차를 따른다.
미완료·도움 범위를 보존하고 다음 행동 하나를 남긴다. 새 근거가 없으면 변경하지 않는다.

허브에 접근할 수 있으면 최신 STATE를 확인한 뒤 갱신하고 다시 읽어 검증한다.
접근할 수 없으면 수행·남은 문제·다음 행동과 코드 위치를 짧게 반환한다.
이 전달문을 STATE 저장 완료라고 보고하지 않는다. 다른 저장소에 진도 원본을 추가하지 않는다.

로컬 저장·커밋·원격 반영은 각각 실제 확인한 단계만 알린다.
관리 문서 변경과 수강·실습 수행을 구분한다.
