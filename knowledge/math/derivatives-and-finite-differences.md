---
title: "도함수와 수치 미분"
updated: 2026-09-09
tags:
  - calculus
  - gradient
  - finite-difference
---

# 도함수와 수치 미분

## 핵심 요약

도함수는 현재 입력 근처에서 입력 변화에 대한 출력의 변화율이다. 여러 입력을 가진 함수의 편미분은 다른 입력을 고정하고 하나만 바꿔 구한다. 미분식으로 구한 값은 함수의 출력 변화만 사용하는 수치 미분과 비교할 수 있다.

## 개념 정리

### 변화율의 부호와 크기

$$
f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}
$$

작은 입력 변화에 대한 출력 변화는 다음처럼 근사한다.

$$
\Delta f\approx f'(x)\Delta x
$$

- 양의 기울기: 입력을 조금 늘리면 출력이 증가한다.
- 음의 기울기: 입력을 조금 늘리면 출력이 감소한다.
- 기울기의 절댓값: 같은 작은 입력 변화에 대한 출력 변화의 민감도다.
- 기울기 0: 그 지점의 일차 변화가 0이라는 뜻이며, 함수 전체가 상수라는 뜻은 아니다.

입력 3에서 함수와 기울기는 다음과 같다.

$$
f(x)=3x^2-4x+5,\qquad f(3)=20,\qquad f'(3)=14
$$

입력을 0.001 늘리면 출력은 약 0.014 증가한다. 기울기 14는 출력값도, 입력을 실제로 1만큼 움직인 결과도 아니다.

### 편미분과 국소 기울기

$$
d=ab+c
$$

$$
\frac{\partial d}{\partial a}=b,\qquad
\frac{\partial d}{\partial b}=a,\qquad
\frac{\partial d}{\partial c}=1
$$

입력이 음수인지와 기울기가 음수인지는 별개다. 입력이 어떤 연산을 거쳐 출력에 영향을 주는지 봐야 한다. 각 입력에 대한 편미분을 모으면 gradient가 된다.

### 구현에 사용한 미분 규칙

아래는 모두 스칼라 입력·출력에 대한 국소 기울기다. 거듭제곱의 지수는 고정된 숫자이며, 식이 정의되고 미분 가능한 입력에서 사용한다.

$$
\frac{d(x^p)}{dx}=p x^{p-1},\qquad
\frac{d\exp(x)}{dx}=\exp(x)
$$

$$
\frac{d\log(x)}{dx}=\frac1x\quad(x>0),\qquad
\frac{d\tanh(x)}{dx}=1-\tanh^2(x)
$$

$$
\frac{d\sin(3x)}{dx}=3\cos(3x)
$$

`exp`에서는 미분값이 출력값과 같아 `out.data`를 재사용한다. 제곱에서는 입력값의 두 배, 로그에서는 입력값의 역수를 써야 한다. 출력과 미분값을 일반적으로 같은 것으로 취급하지 않는다.

### 전진 차분과 중앙 차분

다른 입력을 고정하고 첫 입력을 바꾸는 경우:

$$
g_a^{\mathrm{forward}}=
\frac{f(a+h,b,c)-f(a,b,c)}{h}
$$

$$
g_a^{\mathrm{central}}=
\frac{f(a+h,b,c)-f(a-h,b,c)}{2h}
$$

중앙 차분은 앞뒤 두 위치를 사용하므로 분모가 두 위치 사이 거리인 두 배의 변화량이다. 매끄러운 함수에서는 대칭 계산으로 주요 근사 오차가 상쇄된다. 방식 간 비교에는 같은 변화량을 사용한다.

## 예제 또는 적용

다음 함수의 입력 세 개와 출력은 모두 스칼라다.

$$
f(a,b,c)=-a^3+\sin(3b)-\frac1c+b^{2.5}-a^{0.5}
$$

$$
\frac{\partial f}{\partial a}=-3a^2-0.5a^{-0.5}
$$

$$
\frac{\partial f}{\partial b}=3\cos(3b)+2.5b^{1.5},\qquad
\frac{\partial f}{\partial c}=\frac1{c^2}
$$

入力 `(2, 3, 4)`에서 해석적 기울기는 약 `[-12.35355339, 10.25699027, 0.0625]`다. 변화량 `1e-6`으로 계산한 전진 차분은 각 항의 절대 오차가 `1e-5`보다 작았고, 중앙 차분은 세 항 모두 더 작은 오차를 보였다. 정확한 코드와 출력은 연결된 실습에 둔다.

## 주의점

- `a**1/2`는 `(a**1)/2`다. 분수 지수는 `a**(1/2)`처럼 괄호로 묶는다.
- 음의 제곱근을 미분할 때 음수를 유지하고 지수에서 1을 뺀다.
- 사인 안쪽의 계산은 연쇄법칙으로 곱한다. 사인 항을 추가로 남기지 않는다.
- 수치 미분은 근사이며, 작은 변화량과 부동소수점 반올림 때문에 미분식의 결과와 끝자리가 다를 수 있다.

## 관련 기록

- Knowledge: [계산 그래프와 역전파](../deep-learning/computational-graph-autograd.md)
- Practice: [micrograd 구현과 공식 exercises](../../practice/deep-learning/micrograd.ipynb)
- Source: [micrograd 공식 exercises](https://colab.research.google.com/drive/1FPTx1RXtBfc4MaTkf7viZZD4U2F9gtKN?usp=sharing)
