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
- 공식 course assignment가 있으면 그 과제가 주 practice입니다.
- 정확한 파일을 만들거나 수정해 달라는 요청이 있을 때만 작업합니다.
- 핵심 구현, 실행, 첫 debugging 가설, 결과 해석은 학습자가 담당합니다.
- 함수나 Tensor를 수정한 뒤에는 영향을 받는 셀 또는 script를 다시
  실행하고 최신 결과를 확인합니다.
- 성공한 테스트만이 아니라 상태, shape, gradient, loss, metric이 왜 그런
  결과를 냈는지 설명합니다.
- 실행하지 않은 출력이나 실험 결과를 기록하지 않습니다.

작은 실습은 다음 흐름이면 충분합니다.

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

## CS336 예외

CS336 assignment에서는 공식 AI 지침이 우선합니다. 학습자가 코드와 test를
작성하고 명령을 실행해야 하므로 Agent는 코드, pseudocode, patch, TODO
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
