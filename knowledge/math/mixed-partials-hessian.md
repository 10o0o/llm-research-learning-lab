---
title: "혼합 편미분과 Hessian 비대각원소"
updated: 2026-09-30
tags:
  - calculus
  - gradient
  - hessian
---

# 혼합 편미분과 Hessian 비대각원소

## 핵심 요약

혼합 편미분은 한 입력에 대한 기울기가 다른 입력의 변화에 따라 얼마나
달라지는지 나타낸다. Hessian의 비대각원소에 이 정보가 담긴다.
두 입력의 결합 항을 제거하여 각각 따로 의존하는 함수의 합이 되면,
다른 입력이 해당 기울기에 미치는 영향도 사라진다.

## 개념 정리

### 기울기의 변화율

두 실수 입력을 갖는 스칼라 함수의 첫 입력에 대한 편미분은 다른 입력을
고정하고 구한다. 그 편미분을 다시 둘째 입력으로 미분하면, 첫 입력의
기울기가 둘째 입력에 얼마나 민감한지 알 수 있다. 아래 미분들이 존재하는
범위에서 Hessian의 해당 비대각원소는 다음과 같다.

$$
H_{12}=\frac{\partial}{\partial v}\left(\frac{\partial g}{\partial u}\right)
$$

같은 입력으로 다시 미분하는 대각원소와 구분해서, 비대각원소는 서로
다른 입력 사이의 기울기 변화를 다룬다.

### 결합 항을 제거한 경우

다음은 고정된 실수 계수와 이차 미분 가능한 단변수 함수 두 개를 갖는
보충 예다.

$$
g(u,v)=p(u)+q(v)+cuv
$$

첫 입력에 대한 기울기는 다음과 같다.

$$
\frac{\partial g}{\partial u}=p'(u)+cv
$$

이 기울기에 둘째 입력이 들어 있으므로, 둘째 입력을 바꾸면 고정 계수만큼
첫 입력의 기울기도 변한다.

$$
H_{12}=\frac{\partial}{\partial v}\bigl(p'(u)+cv\bigr)=c
$$

결합 항을 제거하면 첫 입력의 기울기는 첫 입력에만 의존한다. 따라서
둘째 입력을 바꿔도 그 기울기는 변하지 않아 해당 혼합 편미분은 영이 된다.
둘째 입력의 기울기를 첫 입력으로 미분하는 경우도 같은 원리다.

## 관련 기록

- Knowledge: [도함수와 수치 미분](./derivatives-and-finite-differences.md)
- Practice: [MML 5장 회고](../../practice/math/mml-ch05-vector-calculus.md)
- Source: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning*, Cambridge University Press (2020), Draft 2024-01-15, §5.7. [공식 PDF](https://mml-book.github.io/book/mml-book.pdf#page=170)
