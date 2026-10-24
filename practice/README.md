# Practice

학습자의 구현·실행·해석과 도움 범위를 구별해 보관합니다.

## 현재 실습

[문의 보조 Python 실습](./ai-apps/README.md)에 현재 코드의 파일 역할과 CLI가 있습니다.
실제 재개 위치·다음 독립 행동은 [STATE](../STATE.md)만 정합니다. Python 본체 하나를
기준으로 필요한 모듈을 분리하고, 탐색·시각화에는 선택적으로 notebook을 사용합니다.
다중 파일 구조는 재사용 경계가 필요할 때 늘리며 먼저 큰 패키지를 만들지 않습니다.

## 보관한 실습

- [makemore Part 3 회고](./deep-learning/makemore-part3.md): 초기화 비교·첫 backward
  관찰·저자 진단 사본·평가용 변환의 실행과 도움을 구분했다. 공식 구현과 출력이
  포함된 노트북 네 개는 비공개 영역에 바이트 그대로 보관했다.

- [MML 7장 회고](./math/mml-ch07-continuous-optimization.md): 최적화의 직접 설명과 튜터 유도, 공식 연습의 수행·보류를 구분했다. 빈 노트북은 그대로 유지했다.

- [MML 5장 회고](./math/mml-ch05-vector-calculus.md): 편미분·야코비안·자동미분·Hessian·Taylor 설명과 선택 공식 연습의 도움·미수행을 구분했다. 빈 작업 노트북은 새 보관본을 만들지 않았다.

- [MML 4장 회고](./math/mml-ch04-matrix-decompositions.md): 본문·선택 연습의 직접 설명과 계산, 튜터 계산, 보류 증명을 구분했다. 빈 작업 노트북은 새 보관본을 만들지 않았다.

- [MML 2장 회고](./math/mml-ch02-linear-algebra.md): 대화 계산·설명과 교정,
  미완료 연습을 구분했다. 빈 작업 노트북은 새 보관본을 만들지 않았다.

- [fast.ai 책 2장 회고](./deep-learning/fastai-book02-production.md): 곰 분류기 학습과
  저장·추론, 데이터 검토와 공식 복습. 위젯·공개 배포 등 미완료를 남겼다.
  책 원문이 포함된 노트북은 비공개 영역에 바이트 그대로 보존했다.

- [fast.ai Lesson 1 이미지 실습 회고](./deep-learning/fastai-lesson1-images.md) ·
  [책 1장 회고와 미완료 범위](./deep-learning/fastai-book01-intro.md):
  분류·분할 실행, 개념 복습, 중단된 IMDb와 미수행 예시를 구분했습니다.
  원문·사진이 포함된 노트북 두 개는 비공개 영역에 바이트 동일하게 보존했습니다.

- [MLP E02 초기화·수동 SGD 보관본](./deep-learning/makemore-mlp-e02-initialization-training.ipynb) ·
  [회고와 다음 학습 준비](./deep-learning/makemore-mlp-e02-initialization-training.md):
  초기 손실, backward와 갱신의 분리, 같은 배치 10회 학습. 당시 미완료였던
  E01·E03의 후속 실험은 아래 보관본에 있습니다.
- [MLP E01·E03 실험 보관본](./deep-learning/makemore-mlp-e01-e03.ipynb) ·
  [회고](./deep-learning/makemore-mlp-e01-e03.md): 학습률 비교, 논문 읽기,
  직접 연결 비교와 단일 seed의 해석 한계.
- [MLP 학습·평가 재구현 보관본](./deep-learning/makemore-mlp-training-recall.ipynb) ·
  [회고](./deep-learning/makemore-mlp-training-recall.md): 준비 코드 제공과 API 보조를
  구분한 학습자 구현, 실행 결과와 입력·정답 대응 설명.

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

## 새 실습과 보존

새 실험은 질문 하나에 필요한 작은 코드로 시작한다. 지속 제품은 필요할 때 별도 저장소에서
학습자가 직접 구성한다. 기존 코드·notebook·저장 출력은 재실행·초기화하지 않고 보존한다.
현재 실제 진도는 [STATE](../STATE.md), 진행 방법은 [AGENTS](../AGENTS.md)를 따른다.

KANT 원자료와 개인 사본은 기존 비공개 경로에 유지한다. 공식 과제 답안과 출력은 공개하지 않는다.
공식 과제를 다시 선택할 때만 [과정별 정책](../.agents/references/official-course-policies.md)을 읽는다.
완성 강의 코드 실행과 독립 구현, 저장 출력과 이번 실행을 구분한다.
