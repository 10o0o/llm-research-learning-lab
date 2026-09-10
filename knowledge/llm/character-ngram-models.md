---
title: "문자 n-gram 언어모델"
updated: 2026-09-10
tags:
  - language-model
  - bigram
  - trigram
---

# 문자 n-gram 언어모델

## 핵심 요약

문자 언어모델은 앞 문자로 다음 문자 후보의 확률을 만든다. Bigram은 앞 문자
하나, trigram은 앞 문자 두 개를 문맥으로 사용한다. 실제 다음 문자는 학습·평가의
정답이며, 생성할 때는 모델의 분포에서 다음 문자를 선택한다.

## 개념 정리

### 입력과 정답

`stoi`는 문자를 정수 ID로, `itos`는 ID를 문자로 바꾼다. `.`을 시작·종료
경계로 사용하면 bigram의 `emma` 예제는 다음과 같다.

```text
문자:     . e m m a .
입력 ID:  0 5 13 13 1
정답 ID:  5 13 13 1 0
```

Trigram은 `..emma.`에서 `(.. → e), (.e → m), (em → m), (mm → a),
(ma → .)`를 뽑는다. 두 방식 모두 종료 문자까지 5번 예측한다.

### 빈도와 확률의 Shape

```text
어휘 크기 V=27
bigram 빈도:  (V, V)    → 현재 문자, 다음 문자
trigram 빈도: (V, V, V) → 앞 문자 1, 앞 문자 2, 다음 문자
```

`N[i, j]`, `T[i, j, k]`는 출현 횟수다. 각 문맥에서 다음 후보 축의 합으로
나누면 조건부확률이 된다. 후보는 마지막 축이므로 `dim=1`, `dim=2`로 합한다.
`keepdim=True`일 때 분모는 `(V, 1)`, `(V, V, 1)`로 나눗셈에 맞는다.
빈도 0인 후보도 양의 확률을 받도록 모든 빈도에 양수 `alpha`를 더해 정규화할 수 있다.

### 평가와 생성

평가는 고정된 확률표에서 실제 다음 문자 ID의 확률을 읽는다. 정답 확률의
음의 자연로그를 예측한 문자 수로 평균하면 NLL이다. 이름 개수로 나누지 않는다.

생성에서는 정답이 없다. 시작 문맥에서 다음 문자를 고르고 그것을 다음 문맥에
넣는다. 종료 문자를 고르면 끝난다. 평가 대상 이름으로 빈도표를 다시 학습하는
것과 고정 확률표를 조회하는 것은 구분한다.

## 예제 또는 적용

신경망 bigram은 입력 ID `(B,)`로 가중치의 행을 모아 `(B, V)` logits를
만든다. 같은 문자는 같은 행을 선택한다. 빈도 기반 확률표와 학습 가능한 logits는
다음 후보를 나타내지만, logits 자체는 확률이 아니다.

## 주의점

- 문자 ID와 빈도표 안의 횟수는 다르다. 텐서 조회에는 정수 ID를 쓴다.
- trigram용 `..`로 bigram도 집계할 때 `. → .`를 추가하지 않는다.
- 전체 데이터 NLL 감소만으로 처음 보는 이름의 성능을 결론 내리지 않는다.

## 관련 기록

- Knowledge: [데이터 분할과 smoothing](../ml/data-split-and-smoothing.md) · [Softmax와 NLL](../deep-learning/softmax-negative-log-likelihood.md) · [Sampling과 greedy](./sampling-and-greedy.md)
- Practice: [실습](../../practice/deep-learning/makemore-bigrams.ipynb) · [챕터 회고](../../practice/deep-learning/makemore-bigrams.md)
- Source: [building makemore](https://www.youtube.com/watch?v=PaCmpygFfXo)
