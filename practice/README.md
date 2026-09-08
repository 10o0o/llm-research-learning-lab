# Practice

학습자가 직접 구현하고 실행한 뒤 결과를 해석한 산출물을 둡니다.

```text
practice/<area>/<topic>.py
practice/<area>/<topic>.ipynb
```

Notebook, Python script, benchmark, 작은 dataset experiment 중 목적에 가장
단순한 형태를 선택합니다. 재사용 가능한 여러 모듈과 테스트 구조 자체가
학습 목표일 때만 다중 파일 프로젝트를 만듭니다.

## 기본 원칙

- 일반 학습 요청만으로 새 practice 파일을 자동 생성하지 않습니다.
- 공식 구현·exercises·assignments가 기본 실습입니다.
- KANT는 진도·주제 대조용이며 기본 실습이나 완료 기준으로 사용하지 않습니다.
- 정확한 파일을 만들거나 수정해 달라는 요청이 있을 때만 작업합니다.
- 핵심 구현, 실행, 첫 debugging 가설, 결과 해석은 학습자가 담당합니다.
- 함수나 Tensor를 수정한 뒤에는 영향을 받는 셀 또는 script를 다시
  실행하고 최신 결과를 확인합니다.
- 성공한 테스트만이 아니라 상태, shape, gradient, loss, metric이 왜 그런
  결과를 냈는지 설명합니다.
- 실행하지 않은 출력이나 실험 결과를 기록하지 않습니다.

## 공식 실습의 수행과 확인

| 자료 | 수행 방식 |
|---|---|
| 강의 속 구현 | 설명을 따라 전체 구현을 작성·실행하고 해석 |
| 별도 exercises·assignments | 요구사항을 읽고 직접 시도하며 과목별 도움 정책 준수 |
| 강사의 완성 노트북 | 설명·비교용 참고 자료 |
| AI 보충 예제 | 공식 실습을 이해하기 위한 보충 |

완성 노트북 실행이나 AI 보충 예제로 공식 실습을 대체하지 않습니다.
영상·문서·공식 자료 기반 대화를 허용하며 설명 매체가 달라도 공식 내용과
실습은 유지합니다. 실습을 배치할 때 본문을 읽고 Optional·Bonus는 선택
항목으로 표시합니다. 접근·실행 제약은 알리고 해당 항목을 미완료로 남깁니다.
매 구간마다 새 시험·보고서를 만들지 않고 공식 요구사항에 대한 답·코드·
실행·해석을 확인합니다. 대화형 학습을 영상 시청으로, 로컬 검사 통과를
대학의 공식 채점 통과로 표현하지 않습니다.

실습은 다음 흐름으로 진행합니다.

```text
목적과 입력 조건
→ learner-owned 구현
→ deterministic fixture 또는 sanity check
→ 실제 실행과 오류 확인
→ 결과 의미와 한계 해석
```

기존 Notebook의 provenance나 metadata는 당시 산출물의 일부로 보존합니다.
현재 resume state로 읽거나 새 형식으로 자동 migration하지 않습니다. 예전
validator가 없어도 Notebook 코드와 출력은 그대로 열고 실행할 수 있습니다.

## 피드백 요청

새 대화에서는 exact 경로와 현재 오류 또는 질문을 함께 적습니다.

```text
practice/deep-learning/example.ipynb의 현재 코드와 실제 traceback을 보고
첫 번째 원인을 설명해줘.
```

Agent는 현재 파일과 실제 출력부터 확인합니다. 별도 허가 없이 learner-owned
구현을 덮어쓰지 않으며, 코드 수정 요청을 받았을 때만 course 정책 범위에서
편집합니다.

## 과목별 도움 범위

[CS224N Spring 2024](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html)는
AI 협업을 허용하지만 직접 답 요구·복사와 AI의 실질적 과제 대행을 금지합니다.
기본 수행 범위는 A1~A4의 written·수학·프로그래밍과 공식 BERT Final Project
하나입니다. 변경·생략은 사용자 결정으로만 하며, CS336 복귀 준비도가
남은 공식 과제를 자동 취소하지 않습니다.

CS336 assignment에서는 공식 AI 지침이 우선합니다. 학습자가 과제 코드를
작성하고 제공된 테스트와 모든 명령을 실행해야 하므로 Agent는 코드, pseudocode, patch, TODO
해답, 실행 명령을 제공하지 않습니다. 개념 설명, 오류 메시지 해석, sanity
check, 일반적인 리뷰만 제공합니다.

## 강의 제공 실습과 외부 제출

강의 제공 원본은 다음 위치에 보존합니다.

```text
materials/private/<course>/course-provided-practice/
```

학습자 산출물과 섞지 않으며, 원본의 starter나 해답을 학습자 결과로
간주하지 않습니다. Kaggle처럼 data handling, validation, metric, error
analysis가 핵심인 외부 활동은 현재 공식 정보를 확인하고 계정 접근·참여·
제출 전에 별도 승인을 받습니다. 짧은 외부 제출 코드는 `challenges/`에
둡니다.

Dataset, model weight, credential, 큰 출력은 명시적 승인과 적절한 ignore
없이는 Git에 추가하지 않습니다.
