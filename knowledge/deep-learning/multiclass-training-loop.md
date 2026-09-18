---
title: "다중분류 학습 반복과 autograd"
updated: 2026-09-18
tags:
  - deep-learning
  - pytorch
  - multiclass-classification
  - autograd
---

# 다중분류 학습 반복과 autograd

## 핵심 요약

다중분류 모델은 입력을 class별 raw logits로 바꾸고 `CrossEntropyLoss`로 학습한다. 파라미터 update는 `zero_grad → forward → loss → backward → step` 순서이며, 검증에서는 `model.eval()`과 `torch.no_grad()`를 함께 사용한다.

## 개념 정리

### Tensor 역할과 Shape

입력 feature 수가 `F`, class 수가 `C`, batch 크기가 `B`라면:

```text
X:              (B, F)
layer.weight:   (C, F)
layer.bias:     (C,)
logits:         (B, C)
target:         (B,)
loss:           scalar
```

`nn.Linear(F, C)`의 저장된 weight는 `(C, F)`이고, 입력의 마지막 차원 `F`를 출력 차원 `C`로 바꾼다. 개념적으로는 다음과 같은 흐름이다.

```python
logits = X @ layer.weight.T + layer.bias
```

행렬곱은 `(B, F) @ (F, C)`를 `(B, C)`로 만든다. bias `(C,)`는 오른쪽 차원부터 맞춰져 `(1, C)`처럼 해석되고 batch의 각 행에 broadcasting된다.

### Cross-Entropy 계약

```text
input logits:  (B, C), floating-point dtype
target:        (B,), torch.long
target value:  0 <= target < C
```

target은 one-hot 벡터가 아니라 각 샘플의 정답 class index다. `CrossEntropyLoss`가 logits 내부에서 log-softmax와 negative log-likelihood 계산을 처리하므로, loss에 전달하기 전에 softmax를 직접 적용하지 않는다. 예측 class는 `logits.argmax(dim=1)`로 얻으며 shape은 `(B,)`이다.

### 학습과 검증의 분리

한 번의 parameter update는 다음 순서를 따른다.

```text
optimizer.zero_grad()
→ logits = model(train_X)
→ loss = criterion(logits, train_y)
→ loss.backward()
→ optimizer.step()
```

gradient는 기본적으로 누적되므로 다음 update 전에 `zero_grad()`가 필요하다. parameter는 forward에서 바뀌지 않고 `optimizer.step()`에서 바뀐다.

검증에서는 다음을 사용한다.

```text
model.eval()
torch.no_grad() 안에서 validation logits와 loss 계산
argmax(dim=1)로 예측
label과 비교해 accuracy 계산
```

baseline은 학습하지 않는 단순한 기준이다. 예를 들어 train label에서 가장 많이 등장한 class를 validation 전체에 예측해 model accuracy와 비교할 수 있다.

### Autograd 상태

`requires_grad`는 Tensor를 계산 그래프에 기록해 gradient를 계산할지 결정한다.

- model parameter: 보통 `requires_grad=True`
- 입력 feature: 보통 `requires_grad=False`
- class label: `requires_grad=False`

입력 feature가 gradient를 요구하지 않아도 parameter가 gradient를 요구하면 parameter까지의 연산이 graph에 기록된다. `loss.backward()` 후 gradient는 loss 자체가 아니라 leaf parameter에 저장된다.

```python
model.fc.weight.grad
model.fc.bias.grad
```

`no_grad()`는 블록 안에서 수행하는 연산 전체의 계산 graph 생성을 막으므로 검증 forward의 graph 생성 비용도 줄인다. `detach()`는 이미 만들어진 특정 Tensor를 현재 graph에서 분리하지만, 그 Tensor를 만들기까지 든 forward 계산과 graph 생성 비용을 없애지는 않는다. `model.eval()`은 dropout이나 batch normalization 등의 평가 동작을 전환하는 별도의 기능이다.

## 예제 또는 적용

### backward와 실제 갱신

`loss.backward()`는 파라미터를 바꾸지 않고 각 leaf 파라미터의 `.grad`에
기울기를 누적한다. `optimizer.step()`이 실제 파라미터를 변경한다.
학습률 0.1, momentum과 weight decay가 없는 SGD의 갱신은
`torch.no_grad()` 안에서 모든 파라미터에 `p -= 0.1 * p.grad`를 적용하는
것과 대응한다. Adam 등 다른 optimizer의 규칙까지 같다는 뜻은 아니다.

예를 들어 파라미터 원소가 0.5이고 gradient가 0.2라면, backward 직후
파라미터는 여전히 0.5다. 갱신에서 0.1 × 0.2를 빼면 0.48이 된다.
파라미터 Tensor와 gradient는 같은 shape이며 원소별로 갱신한다.

### 갱신 후 손실과 반복문의 범위

손실 Tensor는 그 순간의 forward 결과다. `.item()`은 저장된 숫자를
꺼내며, 가중치가 바뀌었다고 이전 손실을 다시 계산하지 않는다.
마지막 갱신의 결과를 평가하려면 전체 학습 반복문 밖에서 forward와
손실을 다시 계산한다. 평가만 할 때는 `torch.no_grad()`를 사용한다.

바깥 학습 반복문은 학습 횟수를, 안쪽 파라미터 반복문은 갱신할 Tensor를
정한다. 안쪽 반복문이 끝난 뒤 남은 `p` 하나만 갱신하면 마지막 파라미터만
변경된다. 각 파라미터 갱신마다 평가하면 중간 상태도 계산하게 되므로,
최종 결과만 필요할 때는 모든 갱신을 마친 뒤 한 번 평가한다.

샘플 9개와 feature 2개인 작은 분류 예제에서 train/validation으로 나누고 `nn.Linear(2, 3)`을 사용하면 logits는 `(batch, 3)`이다. 세 번째 feature를 추가해 입력을 `(N, 3)`으로 바꾸고 `nn.Linear(3, 3)`을 사용하면 weight는 `(3, 3)`, logits는 여전히 `(batch, 3)`이다.

결과를 해석할 때는 train loss 감소와 validation accuracy의 단순 baseline 대비 값을 함께 본다.

## 주의점

- logits에 softmax를 직접 적용한 뒤 `CrossEntropyLoss`에 넣지 않는다.
- target은 실수 확률 벡터가 아니라 `torch.long` class index다.
- `requires_grad=True`는 gradient 계산 여부이고, optimizer에 전달하는 것은 실제 update 대상 여부다.
- `no_grad()`가 `optimizer.step()` 자체를 호출하지 못하게 하는 것은 아니다. 평가 경로에서 graph와 gradient를 만들지 않도록 하는 기능이다.
- 하나의 작은 synthetic dataset에서 loss나 accuracy가 좋아진 사실만으로 일반적인 모델 성능을 결론 내리지 않는다.

## 관련 기록

- Knowledge: [계산 그래프와 역전파](./computational-graph-autograd.md) · [MLP 구성과 경사하강 학습](./mlp-and-gradient-descent.md) · [Softmax와 음의 로그우도 손실](./softmax-negative-log-likelihood.md)
- TIL: [2026-09-02](../../til/2026/09/2026-09-02.md)
- Practice: 당시 실습 파일 `main.py`는 현재 작업 트리에 없다. 학습 내용은 위 TIL에 남아 있다.
- Practice: [MLP 초기화와 수동 SGD 회고](../../practice/deep-learning/makemore-mlp-e02-initialization-training.md)
- Source: [Stanford CS336 Spring 2026](https://cs336.stanford.edu/)
