---
title: "파라미터와 하이퍼파라미터"
updated: 2026-09-22
tags:
  - neural-network
  - model-selection
---

# 파라미터와 하이퍼파라미터

## 핵심 요약

모델 가중치는 학습되는 파라미터다. 학습률과 배치 크기는 학습 방식을
제어하는 하이퍼파라미터다. 자동으로 값이 변하는지만으로 둘을 구분하지 않는다.

## 개념 정리

파라미터는 모델이 입력으로 예측을 계산할 때 사용하는 학습 대상 값이다.
하이퍼파라미터는 학습이나 모델 구성을 정하는 설정이다.
학습률을 정해진 일정에 따라 줄여도 모델의 가중치로 바뀌는 것은 아니다.

## 예제 또는 적용

학습률 0.01과 배치 크기 32를 정하고 가중치를 학습한다면 앞의 두 값은
하이퍼파라미터, 갱신되는 모델 가중치는 파라미터다. 학습률을 이후 0.001로
자동 변경하는 일정도 학습을 제어하는 설정이라는 역할은 같다.

## 관련 기록

- Knowledge: [모델 비교 실험](./controlled-model-comparison.md)
- Practice: [fast.ai 책 1장 회고](../../practice/deep-learning/fastai-book01-intro.md)
- Source: [fastbook 1장](https://github.com/fastai/fastbook/blob/master/01_intro.ipynb)
