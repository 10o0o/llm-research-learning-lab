---
title: "행렬곱과 완전연결층"
updated: 2026-09-10
tags:
  - matrix-multiplication
  - linear-layer
  - tensor-shape
---

# 행렬곱과 완전연결층

## 핵심 요약

행렬곱은 앞 행렬의 각 행과 뒤 행렬의 각 열 사이의 내적을 한 번에 계산한다. 완전연결층은 이 구조를 `X @ W + b`로 사용하며, 입력의 마지막 차원을 출력 차원으로 바꾼다.

## 개념 정리

### 행렬곱과 Shape

다음 두 행렬을 곱하려면 안쪽 차원 `k`가 같아야 한다.

```text
A:      (m, k)
B:      (k, n)
A @ B:  (m, n)
```

결과의 `(i, j)` 원소는 `A`의 `i`번째 행과 `B`의 `j`번째 열을 내적한 값이다. 따라서 행렬곱은 여러 내적을 묶어 계산하는 연산으로 볼 수 있다.

### 완전연결층

배치 데이터에 완전연결층을 적용할 때 Shape은 다음과 같이 흐른다.

```text
X:  (batch, in_features)
W:  (in_features, out_features)
b:  (out_features,)
Y:  (batch, out_features)
```

```python
Y = X @ W + b
```

`b`는 broadcasting을 통해 배치의 모든 행에 똑같이 더해진다. 입력에 배치 외의 선행 차원이 더 있어도 마지막 특성 차원만 바뀐다.

```text
입력:  (*, in_features)
출력:  (*, out_features)
```

### PyTorch의 저장 방향

`nn.Linear(in_features, out_features)`는 수식에서 사용하는 `W`와 반대 방향으로 가중치를 저장한다.

```text
수식의 W:             (in_features, out_features)
layer.weight:         (out_features, in_features)
layer.bias:           (out_features,)
```

따라서 PyTorch의 실제 계산은 다음과 같이 대응한다.

```python
Y = X @ layer.weight.T + layer.bias
```

### One-hot 행렬곱은 행 선택이다

입력 ID가 `i`인 one-hot 벡터는 i번째 성분만 1이고 나머지는 0이다.
그 벡터와 `W`를 곱하면 `W`의 i번째 행만 남는다.

```text
one-hot: [0, 1, 0]
W: [[10, 11], [20, 21], [30, 31]]
결과: [20, 21]
```

입력 ID 텐서 `ids`가 `(B,)`, 가중치가 `(V, C)`이면 `W[ids]`는 `(B, C)`다.
입력 `[0, 5, 13, 13, 1]`은 0·5·13·13·1번 행을 순서대로 가져온다.
같은 ID가 반복되면 같은 행을 여러 번 가져온다. 입력 ID는 정답이나 확률이 아니다.

따라서 one-hot을 명시적으로 만드는 대신 행 인덱싱을 사용할 수 있다.
이는 일반 실수 특성 벡터의 행렬곱까지 행 선택으로 바꿀 수 있다는 뜻은 아니다.

## 예제 또는 적용

```text
X:     (2, 3)
W:     (3, 2)
b:     (2,)
Y:     (2, 2)
```

첫 번째 출력 하나를 행과 열의 내적으로 계산한 값과 전체 배치 행렬곱의 같은 위치 값이 일치한다. 같은 숫자를 넣은 `nn.Linear(3, 2)`의 출력도 명시적으로 계산한 `X @ W + b`와 일치한다.

Makemore에서 `W_all[all_xs]`와 `all_xenc @ W_all`의 결과 shape이
`(228146, 27)`이고 비교가 `True`인 것을 확인했다. 행 인덱싱으로 바꾼
학습 셀에서도 역전파와 가중치 업데이트를 실행했다.

## 주의점

- 행렬곱에서는 앞 행렬의 열 수와 뒤 행렬의 행 수를 먼저 확인한다.
- 수식의 `W`와 `layer.weight`의 Shape을 혼동하지 않는다. 같은 값을 옮길 때는 저장 방향 때문에 전치가 필요하다.
- `b.shape == (out_features,)`가 출력 전체와 같은 Shape이라는 뜻은 아니다. broadcasting으로 출력의 선행 차원에 반복된다.

## 관련 기록

- Knowledge: [벡터 내적과 코사인 유사도](./dot-product-cosine-similarity.md) · [NumPy axis, keepdims와 broadcasting](./numpy-axis-broadcasting.md)
- TIL: [2026-08-18](../../til/2026/08/2026-08-18.md)
- Practice: [makemore one-hot 제거 회고](../../practice/deep-learning/makemore-bigrams.md)
- Source: [building makemore](https://www.youtube.com/watch?v=PaCmpygFfXo)
- Source: [1장 3강: 행렬 연산과 딥러닝 레이어](../../materials/private/kant-basic-math/01-03_행렬_연산과_딥러닝_레이어.md)
