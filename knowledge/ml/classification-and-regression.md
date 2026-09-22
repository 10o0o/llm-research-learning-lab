---
title: "분류와 회귀의 정답"
updated: 2026-09-22
tags:
  - classification
  - regression
---

# 분류와 회귀의 정답

## 핵심 요약

분류는 범주를, 회귀는 수치적인 양을 예측한다. 같은 사진을 입력하더라도
예측 목적에 따라 필요한 정답이 달라진다.

## 개념 정리

고양이와 개를 구분하는 문제에는 각 사진의 종류가 정답이다.
동물의 체중을 예측하는 문제에는 그 사진에 대응하는 실제 체중이 정답이다.
입력 형식만으로 분류인지 회귀인지 결정하지 않는다.

## 예제 또는 적용

한 사진의 라벨이 고양이라면 동물 종류 분류에 쓸 수 있다.
같은 사진으로 체중을 예측하려면 예를 들어 4.2kg 같은 별도의 실제 측정값이
필요하다. 고양이라는 라벨만으로 그 개체의 체중 정답을 대신할 수 없다.
4.2kg는 설명용 값이며 실습 측정값이 아니다.

## 관련 기록

- Practice: [fast.ai 책 1장 회고](../../practice/deep-learning/fastai-book01-intro.md)
- Source: [fastbook 1장](https://github.com/fastai/fastbook/blob/master/01_intro.ipynb)
