---
title: "예측과 행동의 피드백 루프"
updated: 2026-09-22
tags:
  - machine-learning
  - experiment
---

# 예측과 행동의 피드백 루프

## 핵심 요약

추천 모델은 사용자가 접하는 항목에 영향을 준다. 따라서 클릭 기록은 사용자
선호만 반영한 독립적인 관측이 아니며, 클릭 증가만으로 선호 증가를 단정할 수 없다.

## 개념 정리

모델의 추천이 노출을 바꾸고, 노출이 클릭에 영향을 준다.
그 클릭 기록을 다음 학습에 사용하면 모델의 이전 선택이 다음 추천에
다시 영향을 줄 수 있다. 예측 시스템은 관찰할 데이터의 생성 과정에도 참여한다.

## 예제 또는 적용

액션 영화를 이전보다 자주 보여준 뒤 총 클릭 수가 늘었다고 하자.
사용자가 더 좋아하게 된 것일 수도 있지만, 단순히 더 많이 보게 되어
클릭 기회가 늘어난 결과일 수도 있다. 노출 조건을 고려하지 않고 총 클릭 수만
비교해서 선호 변화라고 판단하지 않는다.

### 추천 후 구매와 추천의 효과

추천하지 않아도 살 상품이라면 추천 후 발생한 구매를 전부 추천의 효과로
볼 수 없다. 추천의 목적이 추가 구매라면 추천하지 않았을 경우와 비교해야 한다.
원래 구매 가능성이 높다는 이유만으로 증가 폭이 작다고 확정할 수도 없다.

## 관련 기록

- Knowledge: [모델 비교 실험](./controlled-model-comparison.md)
- Practice: [fast.ai 책 1장 회고](../../practice/deep-learning/fastai-book01-intro.md)
- Source: [fastbook 1장, Limitations Inherent To Machine Learning](https://github.com/fastai/fastbook/blob/master/01_intro.ipynb)

- Practice: [fast.ai 책 2장 회고](../../practice/deep-learning/fastai-book02-production.md)
