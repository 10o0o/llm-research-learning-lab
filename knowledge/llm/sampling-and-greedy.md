---
title: "Sampling과 greedy 생성"
updated: 2026-09-10
tags:
  - sampling
  - greedy
  - generation
---

# Sampling과 greedy 생성

## 핵심 요약

Sampling은 확률에 따라 후보를 뽑고, greedy는 최대 확률 후보를 고른다.
같은 모델과 시작 문맥에서도 sampling은 다른 경로를 갈 수 있다. 고정된 모델의
greedy는 난수를 사용하지 않아 sampling용 seed의 영향을 받지 않는다.

## 개념 정리

### 다음 문자 선택

확률이 `a=0.5, b=0.3, .=0.2`라면 greedy는 `a`를 고른다. Sampling은
각각 50%, 30%, 20% 확률로 뽑는다. `num_samples=1`은 최대 후보 하나가
아니라 한 번 추출한다는 뜻이다.

```python
# probs: (1, V), 각 후보 확률. g: 반복문 밖에서 만든 Generator
sampled_id = torch.multinomial(probs, num_samples=1, generator=g).item()
greedy_id = probs.argmax(dim=1).item()
```

선택 텐서 shape은 각각 `(1, 1)`, `(1,)`이다. 원소 하나를 `.item()`으로
꺼내 다음 입력 문자 ID로 사용한다. 정답을 받아 손실을 계산하는 연산과 다르다.

### 이름 하나와 여러 이름

바깥 반복은 이름 개수, 안쪽 반복은 한 이름의 문자 선택이다. 이름마다 시작 ID,
문자 목록, 종료 여부를 초기화한다. 선택 ID가 `0`이면 종료하고, 아니면 문자로
추가한 뒤 다음 입력으로 사용한다. 최대 선택 횟수로 멈춘 경우는 종료 문자를
만나 끝난 경우와 구분한다.

### Seed

Generator는 여러 이름을 뽑는 반복문 밖에서 한 번 초기화한다. 이름마다 같은
seed로 다시 만들면 같은 선택 순서를 반복할 수 있다. Greedy는 Generator를
쓰지 않는다. 단, seed로 모델 초기화까지 바꾸면 모델 자체가 달라지므로,
고정 모델에서 선택 seed만 바꾸는 실험과는 구분한다.

## 예제 또는 적용

같은 bigram 가중치와 시작 문자에서 sampling은 다섯 다른 이름을 만들었고,
greedy는 `. → a → .` 경로로 `a`를 다섯 번 만들었다. 모두 종료 문자에
도달했다. 모델 재학습이 아닌 선택 방식의 차이를 비교했다.

## 주의점

- Sampling도 같은 이름을 여러 번 뽑을 수 있다.
- 각 단계의 최대 선택이 전체 문자열 확률의 전역 최적을 보장하지는 않는다.
- 후보 ID와 확률을 혼동하지 않는다. 생성 목록에는 ID를 문자로 바꿔 넣는다.

## 관련 기록

- Knowledge: [문자 n-gram](./character-ngram-models.md)
- Practice: [sampling/greedy 비교 회고](../../practice/deep-learning/makemore-bigrams.md)
- Source: [building makemore](https://www.youtube.com/watch?v=PaCmpygFfXo)
