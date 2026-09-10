---
title: "Softmax와 음의 로그우도 loss"
updated: 2026-09-10
tags:
  - softmax
  - classification
  - negative-log-likelihood
---

# Softmax와 음의 로그우도 loss

## 핵심 요약

Softmax는 후보별 logits를 양수이고 합이 1인 확률로 바꾼다. 정답 후보에 준 확률의 음의 자연로그를 loss로 삼으면 정답에 높은 확률을 주는 방향을 정할 수 있다. 확률 선택은 모델의 최대 예측이 아니라 실제 정답 인덱스를 기준으로 한다.

## 개념 정리

### Logits에서 확률로

$$
p_i=\frac{\exp(z_i)}{\sum_j\exp(z_j)}
$$

지수함수로 양수를 만든 뒤 전체 합으로 나눈다. 공식 예제의 네 점수 `[0, 3, -2, 1]`은 약 `[0.04177, 0.83902, 0.00565, 0.11355]`의 확률이 된다. 가장 높은 점수인 두 번째 후보가 가장 큰 확률을 받는다.

한 입력의 점수는 분자뿐 아니라 공통 분모에도 사용된다. 분모를 여러 출력이 공유하므로, 전체 계산 그래프에서 각 사용 경로의 기울기가 누적되어야 한다.

### 정답 후보의 음의 자연로그

$$
L=-\log(p_t)
$$

정답 인덱스가 `t`다. 예제의 정답은 네 번째 후보이므로 0부터 세는 인덱스 `3`을 사용한다. 모델이 두 번째 후보를 가장 높게 예측해도 정답 인덱스를 바꾸지 않는다.

| 정답 확률 | loss 근삿값 |
|---:|---:|
| 0.1 | 2.303 |
| 0.5 | 0.693 |
| 0.9 | 0.105 |

자연로그와 지수함수는 다르다. `-probs[3].exp()`는 별개의 함수를 계산하고 다른 기울기를 만든다. 이 목적함수에는 `-probs[3].log()`를 사용한다.

### Shape과 계산 그래프

```text
ExerciseValue: 스칼라 logits 객체 4개 → 확률 객체 4개 → loss 객체 하나
PyTorch: logits (4,) → softmax (4,) → 정답 확률 () → loss ()
```

이번 PyTorch 입력에는 batch 차원이 없다. 후보가 놓인 유일한 축 `dim=0`을 따라 softmax를 계산한다. 배치 `(B, C)`의 class 축과 혼동하지 않는다.

loss를 만들 때 Tensor/Value 연산을 유지한다. `.item()`이나 `.data`로 Python 숫자만 꺼내 loss를 만들면 원래 자동미분 연결을 유지할 수 없다. 숫자 추출은 결과를 표시할 때 사용한다.

### 연산별 구현의 연결

| 필요한 처리 | 구현 역할 |
|---|---|
| `exp()` | 지수함수 출력값을 국소 기울기로 사용 |
| `sum(counts)` | 덧셈과 숫자 0을 처리하는 `__radd__` |
| 나눗셈 | 역수와 곱셈의 기존 연산을 연결 |
| `log()` | 입력값의 역수와 전달받은 기울기를 곱함 |
| 부호 반전 | −1과의 곱셈; 역수와 구분 |

`log()`의 국소 기울기는 `out.data`가 아니라 `1 / self.data`다. 생성한 역전파 함수는 호출하지 않고 결과 객체에 저장한다.

### 배치 정답 선택과 Cross-Entropy

```text
logits: (B, C), 실수 점수
target: (B,), 정답 ID, torch.long
정답 확률 선택: (B,)
평균 NLL: ()
```

`probs[torch.arange(len(target)), target]`는 각 행의 정답 열을 짝지어 선택한다.
`probs[2]`는 후보 2가 아니라 세 번째 행이다. `(1, C)`에서 `probs[0, target]`은
한 예제의 정답 확률을 선택하지만 여러 예제에는 각 행 번호가 필요하다.

정답 class ID와 기본 옵션에서는 `F.cross_entropy(logits, target)`이
log-softmax와 정답 음의 로그확률의 평균을 계산한다. 확률을 입력하면 그것을
다시 logits로 취급하므로 의도한 손실과 달라진다. 가중치 정규화 벌점은
별도로 더하는 항이며 이 함수에 포함되지 않는다.

### 수치 안정성

큰 logits를 바로 `exp()`하면 표현 범위를 넘어 `inf`가 될 수 있다. 각 행의
모든 점수에서 같은 값을 빼도 softmax는 같으므로 최대값을 뺀 점수로 안정적으로
계산할 수 있다. `log_softmax`는 로그 확률을 직접 계산해 작은 확률이 0으로
반올림된 뒤 로그를 취하는 문제도 줄인다.

후보 세 개의 logits가 모두 `1000`이면 정답 확률은 `1/3`이다.

$$
-\ln(1/3)=\ln(3)\approx 1.0986
$$

NLL은 백분율이나 정답률이 아니다. 모델이 실제 정답에 준 확률을 벌점으로
바꾸므로 정답 확률이 높을수록 작아진다.

## 예제 또는 적용

공식 입력 `[0, 3, -2, 1]`, 정답 인덱스 `3`에서 loss는 약 2.17551536이다. 직접 구현한 `ExerciseValue`의 각 logit 기울기는 다음과 같다.

```text
[0.04177257, 0.83902451, 0.00565330, -0.88645038]
```

네 값은 공식 기대값의 절대 오차 기준 `1e-5`를 만족했다. 같은 입력의 `float64` PyTorch 계산에서도 loss와 화면에 표시된 기울기가 일치했다. PyTorch 기울기 출력은 소수 네 자리로 반올림된 표시이며, 전체 자릿수의 별도 오차 비교까지 수행한 것으로 해석하지 않는다.

정답 logit의 기울기는 음수이므로 logits를 직접 경사하강으로 조정한다면 정답 점수는 높이고 다른 점수는 낮추는 방향이다. 모델 학습에서는 이 기울기가 파라미터까지 전달된 뒤 파라미터가 업데이트된다.

Makemore 보충 실험에서 logits `[[1000, 1000, 1000]]`와 정답 `[2]`를
직접 `exp → 정규화 → log`로 계산하면 `nan`, cross-entropy로 계산하면
약 `1.0986`이었다. 일반적인 학습 logits에서는 수동 NLL과 cross-entropy가
일치했다. 실험 수치와 가중치 상태의 한계는 챕터 회고에 따로 남긴다.

## 주의점

- `requires_grad=True`와 `backward()`만으로 가중치 값이 업데이트되지는 않는다.
- 수동 softmax 뒤 음의 로그우도를 계산하는 이번 실습과, raw logits를 받는 `CrossEntropyLoss`의 사용 계약은 구분한다.
- Micrograd의 직접 구현과 달리, 후속 makemore 실습에서는 큰 logits의
  수치 안정성 차이를 확인했다. 손실 함수 구현 변경 자체가 모델 성능 향상을 뜻하지 않는다.
- 공식 기대값과 로컬 실행 비교는 대학의 공식 채점 결과가 아니다.

## 관련 기록

- Knowledge: [계산 그래프와 역전파](./computational-graph-autograd.md) · [다중분류 학습 loop와 autograd](./multiclass-training-loop.md)
- Practice: [ExerciseValue와 PyTorch 비교](../../practice/deep-learning/micrograd.ipynb)
- Practice: [makemore NLL·cross-entropy 회고](../../practice/deep-learning/makemore-bigrams.md)
- Source: [micrograd 공식 exercises](https://colab.research.google.com/drive/1FPTx1RXtBfc4MaTkf7viZZD4U2F9gtKN?usp=sharing)
- Source: [PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
