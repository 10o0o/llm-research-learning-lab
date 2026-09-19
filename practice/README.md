# Practice

학습자가 직접 구현하고 실행한 뒤 결과를 해석한 산출물을 둡니다.

## 보관한 실습

- [MLP E02 초기화·수동 SGD 보관본](./deep-learning/makemore-mlp-e02-initialization-training.ipynb) ·
  [회고와 다음 학습 준비](./deep-learning/makemore-mlp-e02-initialization-training.md):
  초기 손실, backward와 갱신의 분리, 같은 배치 10회 학습. E01·E03은 미완료입니다.

- [micrograd 구현과 공식 exercises](./deep-learning/micrograd.ipynb):
  `Value` 자동미분, 뉴런·MLP 학습, 미분 검산, `ExerciseValue`의 softmax·로그 loss,
  PyTorch 비교를 담은 코드·출력 보관본입니다. 강의 따라 구현한 부분과 공식
  exercises의 직접 시도·피드백 수정, 보충 예제가 함께 들어 있습니다.
  관련 개념은 [knowledge 안내](../knowledge/README.md)에 연결했습니다.
- 루트의 `main.ipynb`는 다음 학습을 위한 작업 공간입니다. 과거 실습을
  확인할 때는 위 보관본을 사용합니다.
- [makemore bigram 보관본](./deep-learning/makemore-bigrams.ipynb) ·
  [챕터 회고](./deep-learning/makemore-bigrams.md): counting bigram/trigram,
  분할·smoothing, 인덱싱·cross-entropy, sampling/greedy 실험입니다.
  원본은 수정·재실행하지 않았으며, 문법 오류와 저장 출력의 한계는 회고에 명시했습니다.

## 챕터 마무리

`$finish-chapter` 또는 `이번 챕터 정리해줘`는
[마무리 스킬](../.agents/skills/finish-chapter/SKILL.md)을 호출합니다.
`practice/<area>/<chapter>.ipynb`에 원본 바이트를 보존하고, 같은 이름의
`.md`에 과정·결과·도움·한계를 정리합니다. 개념은 knowledge와 연결합니다.
보관본 일치와 문서 검증 후 `main.ipynb`를 빈 코드 셀로 초기화하고,
STATE 전체 교체안 승인 후 해당 범위의 로컬 커밋까지 진행합니다.

보관본은 학습 흔적이지 재실행을 검증한 완성본이 아닙니다. 과거 오류를
지우거나 노트북을 실행해 결과를 새로 만들지 않습니다. 기존 보관본이 다른
내용이면 덮어쓰지 않으며, 빈 노트북의 재호출로 과거 실습을 교체하지 않습니다.
일반 `완료` 응답에는 적용하지 않고, TIL과 push는 별도 요청입니다.

## 저장 위치

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
- KANT 자료는 `P1`·`P2`의 정식 주자료이며 자체 실습을 포함하지만, 다른 과정의
  공식 실습을 대체하거나 완료 기준이 되지 않습니다.
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

연습 코드는 학습자가 직접 씁니다. Agent는 원리와 필요한 연산·shape를 설명하고
공식 API를 가리키며 작성한 코드를 리뷰하지만, 해당 줄이나 셀을 대신 써 주지
않습니다. 다섯 줄짜리 갱신 루프도 그 자체가 연습의 목적인 경우가 많습니다.
Notebook을 확인할 때는 파일을 통째로 읽지 않고 `scripts/nbpeek.py`를 씁니다.

## 과목별 도움 범위

[CS224N Spring 2024](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html)
A1~A4는 `P3`에서 전부 수행합니다. 공식 AI 정책은 AI 협업을 허용하지만 직접 답
요구·복사와 AI의 실질적 과제 대행을 금지합니다. 파이널 프로젝트만 보류이며
복귀 조건은 [`DEFERRED.md`](../DEFERRED.md)에 있습니다.

Phase별 주자료와 산출물은 [`ROADMAP.md`](../ROADMAP.md)의 Phase 표를 따릅니다.
`P1`·`P2`에서는 보유한 KANT 자료가 정식 주자료입니다.

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
