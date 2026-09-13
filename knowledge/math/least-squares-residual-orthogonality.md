---
title: "최소제곱과 잔차 직교성"
updated: 2026-09-14
tags:
  - least-squares
  - residual
  - normal-equation
---

# 최소제곱과 잔차 직교성

## 핵심 요약

`Ax = b`의 정확한 해가 없을 때 최소제곱은 잔차 제곱합을 가장 작게 만드는 `Ax`를 찾는다. 최적점의 잔차 `r = b - Ax`는 `A`의 열공간과 직교한다.

## 개념 정리

### 최소제곱의 목적

최소제곱은 다음 값을 최소화한다.

$$
\lVert A\mathbf{x}-\mathbf{b}\rVert_2^2
$$

정확한 `b`를 만들 수 없을 때도 열공간 안에서 `b`에 가장 가까운 출력 `Ax`를 선택할 수 있다.

### 잔차 직교성과 정규방정식

잔차를 `r = b - Ax`로 정의한다. 잔차에 열공간 방향의 성분이 남아 있다면 `Ax`를 그 방향으로 이동해 오차를 더 줄일 수 있다. 따라서 최적점에서는 모든 열과 잔차의 내적이 `0`이어야 한다.

$$
A^T\mathbf{r}=\mathbf{0}
$$

`r = b - Ax`를 대입하면 정규방정식을 얻는다.

$$
A^T A\mathbf{x}=A^T\mathbf{b}
$$

### NumPy 반환값

```python
coef, residuals, rank, singular_values = np.linalg.lstsq(A, b, rcond=None)
```

- `coef`: 선택된 계수
- `residuals`: 잔차 벡터가 아니라 잔차 제곱합 배열
- `rank`: `A`에서 판정된 rank
- `singular_values`: `A`의 특이값

실제 예측과 잔차 벡터는 별도로 계산한다.

```python
prediction = A @ coef
r = b - prediction
```

## 예제 또는 적용

`A = [[1], [1], [1]]`, `b = [2, 4, 9]`에서는 가장 가까운 상수 계수가 `5`다.

```text
prediction = [5, 5, 5]
r          = [-3, -1, 4]
sum(r**2)  = 26
A.T @ r    = [0]
```

잔차 성분의 합이 `0`이므로 잔차는 `A`의 열벡터 `[1, 1, 1]`과 직교한다.

## 주의점

- `lstsq`의 `residuals`와 실제 잔차 벡터 `b - A @ coef`를 구분한다.
- 열이 선형 종속이면 서로 다른 계수가 같은 예측을 만들 수 있다. 영공간 벡터 `c`에 대해 `A @ c = 0`이면 `coef`와 `coef + c`의 예측은 같다.

## 관련 기록

- Knowledge: [랭크, 영공간과 연립방정식의 해](./rank-null-space-linear-systems.md)
- TIL: [2026-08-18](../../til/2026/08/2026-08-18.md)
- Source: KANT 기초수학, 2장 3강 「연립선형방정식과 행렬 해법」
