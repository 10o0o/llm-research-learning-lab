---
title: "벡터"
updated: 2026-09-14
tags:
  - vector
  - linear-algebra
  - numpy
---

# 벡터

## 핵심 요약

실수 좌표 벡터는 순서가 있는 여러 성분으로 이루어지며, 성분 수가 수학적 공간의 차원을 결정한다.

## 개념 정리

### 수학적 표현

$n$ 개의 성분을 가진 실수 벡터는 다음과 같이 나타낼 수 있다.

$$
\mathbf{v}=(v_1, v_2, \ldots, v_n) \in \mathbb{R}^n
$$

기하학적으로 0이 아닌 벡터는 크기와 방향을 가진 화살표로 해석할 수 있다.

### NumPy 배열과 수학적 차원

NumPy의 `ndim`은 배열을 표현하는 데 필요한 축의 개수이다. 반면 수학적 공간의 차원은 벡터의 성분 개수로 정해진다.

## 예제 또는 적용

```python
import numpy as np

v = np.array([3, 2])
```

| 관점 | 값 |
|---|---|
| `v.shape` | `(2,)` |
| `v.ndim` | `1` |
| 성분 개수 | `2` |
| 수학적 공간 | $\mathbb{R}^2$ |

## 관련 기록

- Knowledge: [벡터 L2 정규화](./vector-l2-normalization.md)
- TIL: [2026-08-13](../../til/2026/08/2026-08-13.md)
- Source: KANT 기초수학, 1장 1강 「벡터의 수학적 정의와 기하학적 해석」
