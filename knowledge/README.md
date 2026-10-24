# Knowledge

다시 사용할 개념을 모은 지식 베이스다. 날짜별 학습 일기는 만들지 않는다.
파일과 화면에 쓰는 frontmatter·본문 형식은 [템플릿](template.md)을 유지한다.
기존 개념 문서를 먼저 찾고, 새 노트는 학습자가 요청한 자신의 설명을 교정할 때만 추가한다.
AI가 먼저 완성한 설명, 파일 존재, 녹색 테스트는 학습자의 이해를 입증하지 않는다.

한 문서는 정의·원리·조건·필요한 예제와 한계를 담고, 다른 개념과 직접 연결될 때 링크한다.
비공개 원문·내부 경로·공식 과제 답안은 공개하지 않는다. 출처는 공개 URL 또는 자료명·판본으로 식별한다.
과거 TIL을 인용하던 링크는 복구 가능한 고정 Git 이력으로 연결했다. 이는 새 TIL 작성을 요구하지 않는다.

문법 검사는 `.agents/skills/update-learning-knowledge/scripts/validate_knowledge.py`를 사용한다.
검사 통과는 문서 의미나 학습자의 숙달을 보장하지 않는다. 학습 후 자동 갱신·회고·초기화는 없다.
공통 행동과 Git 권한은 [AGENTS](../AGENTS.md)를 따른다.

## Micrograd에서 연결한 개념

MLP에서 다시 연결한 초기화·수동 SGD는
[E02 회고](../practice/deep-learning/makemore-mlp-e02-initialization-training.md)와
[보관본](../practice/deep-learning/makemore-mlp-e02-initialization-training.ipynb)에 있습니다.
[MLP 초기화와 경사하강](./deep-learning/mlp-and-gradient-descent.md),
[backward와 실제 갱신](./deep-learning/multiclass-training-loop.md)을 함께 참고합니다.

다시 읽을 때는 아래 순서로 연결할 수 있습니다. 구현과 실행 출력은
[micrograd 실습 보관본](../practice/deep-learning/micrograd.ipynb)에 있습니다.

| 개념 | 다시 확인할 내용 |
|---|---|
| [도함수와 수치 미분](./math/derivatives-and-finite-differences.md) | 부호·크기, 편미분, 미분 규칙, 전진·중앙 차분 |
| [계산 그래프와 역전파](./deep-learning/computational-graph-autograd.md) | Value, 클로저, 위상 순서, 누적, 객체와 숫자 구분 |
| [MLP 구성과 경사하강 학습](./deep-learning/mlp-and-gradient-descent.md) | 뉴런·층·파라미터 수, loss, 초기화·역전파·업데이트 |
| [Softmax와 음의 로그우도 손실](./deep-learning/softmax-negative-log-likelihood.md) | 정답 확률, 연산 구현, PyTorch 비교 |

배치 학습·검증으로 연결할 때는 기존
[다중분류 학습 반복과 autograd](./deep-learning/multiclass-training-loop.md)를 참고합니다.

## Makemore bigram에서 연결한 개념

[챕터 회고](../practice/deep-learning/makemore-bigrams.md)에서 질문·수정·
도움·실험 한계를, [실습 보관본](../practice/deep-learning/makemore-bigrams.ipynb)에서
당시 코드와 출력을 확인할 수 있습니다.

| 개념 | 다시 확인할 내용 |
|---|---|
| [문자 n-gram 언어 모델](./llm/character-ngram-models.md) | 현재/다음 문자 ID, 빈도표, 문맥별 확률 |
| [데이터 분할과 평활화 계수 선택](./ml/data-split-and-smoothing.md) | 이름 단위 분할, train 집계, dev 선택, test 한계 |
| [행렬곱과 one-hot 행 선택](./math/matrix-multiplication-linear-layer.md) | ID 목록으로 여러 가중치 행 가져오기 |
| [Softmax와 NLL](./deep-learning/softmax-negative-log-likelihood.md) | 정답 확률, 배치 인덱싱, 안정적인 cross-entropy |
| [샘플링과 탐욕적 생성](./llm/sampling-and-greedy.md) | 확률 추출과 최대 선택, seed, 이름별 초기화 |

## Makemore MLP에서 연결한 개념

[E01·E03 회고](../practice/deep-learning/makemore-mlp-e01-e03.md)와
[학습·평가 재구현 회고](../practice/deep-learning/makemore-mlp-training-recall.md)에
실행 조건, 결과, 도움의 범위와 독립 설명이 남은 부분을 구분했습니다.

| 개념 | 다시 확인할 내용 |
|---|---|
| [MLP와 경사하강](./deep-learning/mlp-and-gradient-descent.md) | 학습률, 임베딩 조회, 은닉층과 직접 연결 |
| [학습 반복과 autograd](./deep-learning/multiclass-training-loop.md) | 같은 행 번호로 배치 추출, gradient 초기화, 학습 후 평가 |
| [모델 비교 실험](./ml/controlled-model-comparison.md) | 조건 통제, 추가 학습의 혼동, 작은 개선의 해석 |

## Makemore Part 3에서 연결한 개념

[챕터 회고](../practice/deep-learning/makemore-part3.md)에 제공 코드·학습자 구현,
실제 저장 출력·대화 해석과 튜터 도움을 구분했다. 공식 연습 구현과 저장 출력은
비공개 영역에 보존했다.

- [초기화 크기와 tanh 포화](./deep-learning/initialization-and-tanh-saturation.md):
  학습자의 기억 기반 초안을 교정한 범위다. 작은 값과 포화의 원인 구분 및
  출력층 초기화의 목적은 보충했으며, 여러 환경의 재현이나 지연 회상 통과를 뜻하지 않는다.
- [계산 그래프와 역전파](./deep-learning/computational-graph-autograd.md)와
  [MLP와 경사하강](./deep-learning/mlp-and-gradient-descent.md)은 기존 참고 노트다.
  파일 존재를 이번 챕터의 독립 설명 증거로 바꾸지 않는다.

## fast.ai Lesson 1에서 연결한 개념

[이미지 실습 회고](../practice/deep-learning/fastai-lesson1-images.md)와
[책 1장 회고](../practice/deep-learning/fastai-book01-intro.md)에 독립 설명과
해설로 보완한 부분을 구분했습니다. 아래 노트는 대화의 학습자 초안에서
확인한 범위를 정리한 것이며 챕터 전체의 무보조 회상 통과를 뜻하지 않습니다.

- [모델 비교와 평가](./ml/controlled-model-comparison.md): 작은 평가 표본의 한계
- [파라미터와 하이퍼파라미터](./ml/parameters-and-hyperparameters.md): 가중치와 학습 제어 설정
- [분류와 회귀](./ml/classification-and-regression.md): 예측 목적과 대응하는 정답
- [예측의 피드백 루프](./ml/prediction-feedback-loops.md): 추천 노출과 클릭의 관계
- [입력 해상도](./deep-learning/image-input-resolution.md): 계산량과 세부 정보
- [사전학습과 계산 자원](./deep-learning/pretraining-and-compute.md): 미세조정과 처음부터 학습의 차이

## fast.ai Lesson 2에서 연결한 개념

[책 2장 회고](../practice/deep-learning/fastai-book02-production.md)에 도움과 미완료를
구분했다. 아래 노트는 학습자의 대화 초안을 교정한 범위이며 전체 독립 회상 통과가 아니다.

- [입력과 정답 대응](./ml/input-label-matching.md): 폴더 라벨과 CSV 매칭
- [모델 저장과 추론](./deep-learning/model-export-inference.md): 구조·가중치와 입력 처리
- [이미지 크기와 crop](./deep-learning/image-input-resolution.md): 잘린 특징과 정답 타당성
- [모델 비교와 평가](./ml/controlled-model-comparison.md): 실제 환경과 어려운 사진의 보존
- [예측과 행동의 피드백](./ml/prediction-feedback-loops.md): 추천 후 구매와 추가 효과

## MML 2장에서 연결한 개념

[2장 회고](../practice/math/mml-ch02-linear-algebra.md)에 직접 시도와 교정,
미완료를 구분했다. 다음 문서는 학습자의 대화 초안을 교정한 참고 노트다.

- [벡터 부분공간](./math/vector-subspaces.md): 영벡터와 덧셈·실수배 닫힘
- [선형독립과 생성 공간](./math/linear-independence-and-span.md): 피벗 판별과 조합 벡터 추가
- [아핀 공간과 아핀 사상](./math/affine-spaces-and-mappings.md): 평행이동과 선형성의 구별

## MML 3장에서 연결한 개념

[3장 회고](../practice/math/mml-ch03-analytic-geometry.md)에 직접 설명·계산,
해설로 교정한 부분, 장말 무보조 회상에서 복원되지 않은 내용을 구분했다.

- [회전행렬과 Givens 회전](./math/rotation-matrices.md): 기저벡터의 상, 능동 회전과 기저 좌표, 보존 성질, 고차원 평면 회전
- [벡터 내적과 코사인 유사도](./math/dot-product-cosine-similarity.md): 유클리드 점곱과 방향 관계
- [벡터 L2 정규화](./math/vector-l2-normalization.md): 노름과 단위벡터
- [최소제곱과 잔차 직교성](./math/least-squares-residual-orthogonality.md): 투영과 직교 잔차의 기존 연결

일반 내적의 조건과 비정규직교 기저·아핀 부분공간 투영은 장말에 무보조로
복원되지 않아 새 지식 노트로 대신 작성하지 않았다.

## MML 4장에서 연결한 개념

[4장 회고](../practice/math/mml-ch04-matrix-decompositions.md)에 학습자 설명을
초안으로 사용한 범위와 피드백·튜터 계산·미수행 증명을 구분했다.

- [SVD의 입력·출력 기저와 특잇값](./math/singular-value-decomposition.md): 인자 크기, 길이 배율과 방향, 성분 소실
- [SVD 저랭크 근사와 오차](./math/svd-low-rank-approximation.md): 영인 기여 생략, 양의 기여를 버리는 근사, 최대 단위 입력 오차
- [전치행렬 곱과 양의 준정부호](./math/gram-matrix-positive-semidefinite.md): 변환 결과의 길이 제곱과 대칭성의 구분

고유공간·대각화·Cholesky 조건과 최적성 증명의 독립 설명 공백은 회고에
남겼으며, 기존 노트가 있다는 사실만으로 현재 숙달을 판단하지 않는다.

## MML 5장에서 연결한 개념

[5장 회고](../practice/math/mml-ch05-vector-calculus.md)에 직접 계산·설명과
표기 교정·튜터 조립·미수행 공식 연습을 구분했다.

- [혼합 편미분과 Hessian 비대각원소](./math/mixed-partials-hessian.md): 다른 입력이 해당 기울기에 미치는 영향과 결합 항 제거의 의미

위 노트는 학습자의 비대각원소 설명과 조건 변경 이유를 초안으로 사용한
범위다. 야코비안 조립·역행렬 미분·Taylor 계수의 독립 설명 공백은 회고에
남겼다. 기존 도함수·자동미분 노트의 존재를 새 무보조 회상의 증거로 보지 않는다.

## MML 7장에서 연결한 개념

[7장 회고](../practice/math/mml-ch07-continuous-optimization.md)에 학습자 초안·튜터 교정과 미수행을 구분했다. 다음 노트는 확인된 대화 초안을 교정한 범위이며 장 전체 숙달을 뜻하지 않는다.

- [미니배치 기울기와 SGD](./deep-learning/mini-batch-gradient.md)
- [모멘텀과 이동 방향의 누적](./deep-learning/momentum-directions.md)
- [볼록함수의 합과 최적해의 유일성](./math/convex-function-combinations.md)
- [제약 최적화와 최솟값의 상한·하한](./math/constrained-optimum-bounds.md)
