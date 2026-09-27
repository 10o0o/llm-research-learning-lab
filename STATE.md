# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 ROADMAP Phase: P0
- 현재 주강의: Mathematics for Machine Learning, Cambridge University Press (2020)
- 사용 판본: 공식 사이트 배포 PDF, Draft 2024-01-15
- 현재 범위: Chapter 2~5·7 수학 보강; 설명·계산한 내용은 보존하고 부족한 부분을 본문·공식 연습문제로 연결
- 현재 강의: Chapter 4, §4.2 Eigenvalues and Eigenvectors, 인쇄 쪽 108의 Graphical Intuition in Two Dimensions부터
- 공식 자료: [MML](https://mml-book.github.io/) · [PDF](https://mml-book.github.io/book/mml-book.pdf)
- 연결 실습: 행렬식·고유값·고유방향으로 2차원 변환의 늘림·전단·회전·차원 붕괴 해석
- 학습 공간: `main.ipynb`·`recall.ipynb`는 빈 상태; 이번 단위는 손으로 설명·계산

## 관찰된 근거와 남은 범위

fast.ai Lessons 1~2는 미완료 항목을 남기고 이동했으며, 완료나 P0 종료 판정이 아니다. 새 커널 전체 재현·배포도 미검증이다. 수행·도움·미완료 요구는 [책 1장 회고](practice/deep-learning/fastai-book01-intro.md), [Lesson 1 실습 회고](practice/deep-learning/fastai-lesson1-images.md), [책 2장 회고](practice/deep-learning/fastai-book02-production.md)에 유지한다.

MML [2장 회고](practice/math/mml-ch02-linear-algebra.md)에 Exercise 2.12의 교집합 기저, 2.20(a)의 그림, §2.7.2 출력 역변환 방향과 기저 변환·상/영공간·아핀 사상의 독립 설명 공백을 유지한다.

MML [3장 회고](practice/math/mml-ch03-analytic-geometry.md)에 거리·일반 내적 조건·투영과 잔차·아핀 투영·회전 부호의 회상 공백을 유지한다. Exercise 3.8·3.10은 시도했으나 3.10 부호는 해설로 교정했고, 3.1~3.7·3.9 및 그 밖의 미확인 문제를 완료로 보지 않는다.

MML [4장 진행 중 기록](practice/math/mml-ch04-matrix-decompositions.md)은 기존 §4.1~4.2 관찰과 재확인 항목을 옮긴 기록이며, 새 학습이나 장 완료를 뜻하지 않는다.
핵심 재확인: §4.1 대각합의 순환 불변성은 무보조 재확인 전이고, §4.2 고유공간과 `B - λI`·`span` 표기는 교정 후 상태다. 해설 후 동의는 독립 회상이 아니다.

CS336 Assignment 1은 기존 작업을 보존하고 진입을 보류한다. MML 이후 승인 순서는 MIT 18.05 Spring 2022 PS1~PS11(R 포함), makemore Parts 3~4와 공식 exercises다. 범위 생략·자동 설치는 승인되지 않았으며 실습 전 CPU/GPU 요구·환경·비용을 확인한다. 자세한 범위는 [ROADMAP](ROADMAP.md)을 따른다.

## 다음 독립 행동

Chapter 4 §4.2 인쇄 쪽 108의 Graphical Intuition in Two Dimensions부터 Figure 4.4의 늘림·전단·회전·차원 붕괴를 행렬식, 고유값, 고유방향으로 연결한다. 기존 대각화 설명은 반복하지 않고, 실수 고유방향이 없는 회전과 고유값 0인 방향의 붕괴를 대비한다.

코드 실행·환경 설치·GPU 대여는 필요 없다.
