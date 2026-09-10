---
title: "데이터 분할과 smoothing 선택"
updated: 2026-09-10
tags:
  - train-dev-test
  - smoothing
  - model-selection
---

# 데이터 분할과 smoothing 선택

## 핵심 요약

Train으로 모델을 만들고 dev 성능으로 설정을 선택한다. Test는 선택을 마친
모델의 평가에 사용한다. Train에서 손실이 가장 낮은 설정이 dev에서도 가장
좋지는 않을 수 있다.

## 개념 정리

### 이름 단위 분할

이름 목록을 먼저 나눈 뒤 문자 쌍을 만든다. 같은 이름의 조각이 여러 분할로
흩어지지 않도록 하는 단위 선택이다. 복사본을 seed를 고정해 shuffle하고,
80%와 90%의 경계를 각각 `train_end`, `dev_end`로 정한다.

```python
train_words = shuffled_words[:train_end]
dev_words = shuffled_words[train_end:dev_end]
test_words = shuffled_words[dev_end:]
```

슬라이스 끝은 제외되므로 다음 구간 시작에 1을 더하지 않는다. 같은 원본
순서와 seed에서 분할을 재현할 수 있다. 단순 행 분할은 원본에 같은 이름
문자열이 중복되어 있는 경우까지 자동으로 처리하는 방법은 아니다.

### 고정 모델 평가

빈도표는 train에서만 집계한다. 평가 함수는 입력받은 이름의 실제 정답 확률을
고정 확률표에서 읽어 평균 NLL을 반환한다. Dev/test로 빈도를 추가하면
평가할 데이터를 학습에 사용한 셈이다.

### Smoothing 강도

관측 빈도에 `alpha`를 더하고 다음 후보 방향으로 정규화한다. 빈도표는 유지하고
`alpha`만 바꿔 비교한다. NLL은 정답률이 아니라 벌점이므로 작을수록 좋다.

관측 빈도를 완화하면 train NLL은 커져도 dev NLL은 줄 수 있다. 반대로 너무
큰 값을 더하면 확률이 균등해져 관측 차이를 덜 활용하게 된다. Train/dev 차이가
작아도 두 손실이 모두 나쁘면 좋은 설정이라고 할 수 없다.

## 예제 또는 적용

Trigram에서 `alpha=0.01`은 train NLL이 가장 낮았지만 후보 중 dev NLL은
`alpha=0.1`이 가장 낮았다. 따라서 dev 기준으로 `0.1`을 선택했다.
분할·결과와 test 조회의 한계는 챕터 회고에 보존한다.

## 주의점

- 반복문이 끝나면 확률표 변수에는 마지막 후보가 남는다. 선택한 값으로
  확률표를 다시 만들어 최종 평가한다.
- Test로 후보를 반복 선택하면 평가의 독립성이 약해진다. 이미 조회했다면
  숨기거나 미조회 실험으로 기록하지 않는다.
- 한정된 분할과 후보에서 고른 값을 보편적 최적값으로 해석하지 않는다.

## 관련 기록

- Knowledge: [문자 n-gram](../llm/character-ngram-models.md) · [Softmax와 NLL](../deep-learning/softmax-negative-log-likelihood.md)
- Practice: [makemore E02/E03 회고](../../practice/deep-learning/makemore-bigrams.md)
- Source: [building makemore 설명란 exercises](https://www.youtube.com/watch?v=PaCmpygFfXo)
