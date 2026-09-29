# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 ROADMAP Phase: P0
- 현재 주강의: Mathematics for Machine Learning, Cambridge University Press (2020)
- 사용 판본: 공식 사이트 배포 PDF, Draft 2024-01-15
- 현재 범위: Chapter 2~5·7 수학 보강; 설명·계산한 내용은 보존하고 부족한 부분을 본문·공식 연습문제로 연결
- 현재 강의: Chapter 5 Vector Calculus, §5.1 Differentiation of Univariate Functions, 인쇄 쪽 141부터
- 공식 자료: [MML](https://mml-book.github.io/) · [PDF](https://mml-book.github.io/book/mml-book.pdf)
- 연결 실습: 기존 미분 노트를 연결해 차분몫과 도함수의 국소 변화율 해석
- 학습 공간: `main.ipynb`·`recall.ipynb`는 빈 상태; 이번 단위는 손으로 설명·계산

## 관찰된 근거와 남은 범위

fast.ai Lessons 1~2는 미완료 항목을 남기고 이동했으며, 완료나 P0 종료 판정이 아니다. 새 커널 전체 재현·배포도 미검증이다. 수행·도움·미완료 요구는 [책 1장 회고](practice/deep-learning/fastai-book01-intro.md), [Lesson 1 실습 회고](practice/deep-learning/fastai-lesson1-images.md), [책 2장 회고](practice/deep-learning/fastai-book02-production.md)에 유지한다.

MML [2장 회고](practice/math/mml-ch02-linear-algebra.md)에 Exercise 2.12의 교집합 기저, 2.20(a)의 그림, §2.7.2 출력 역변환 방향과 기저 변환·상/영공간·아핀 사상의 독립 설명 공백을 유지한다.

MML [3장 회고](practice/math/mml-ch03-analytic-geometry.md)에 거리·일반 내적 조건·투영과 잔차·아핀 투영·회전 부호의 회상 공백을 유지한다. Exercise 3.8·3.10은 시도했으나 3.10 부호는 해설로 교정했고, 3.1~3.7·3.9 및 그 밖의 미확인 문제를 완료로 보지 않는다.

MML [4장 회고](practice/math/mml-ch04-matrix-decompositions.md)에 본문·선택 연습의 직접 설명과 계산, 교정·튜터 계산, 미수행을 보존했다. SVD 인자와 성분 소실, 정확한 생략과 근사, 오차에 필요한 항 수는 설명·계산했다. 고유공간·대각화 조건, 고유값 부호와 특잇값, rank와 크기의 구분은 교정 이력을 남겼다. 마지막 대각행렬의 고유값·특잇값은 맞게 답했지만 길이 배율이라는 이유는 해설로 보충했다.

Exercise 4.5는 피드백을 거쳤고 4.8은 영공간 방향 이후 튜터가 계산했다. 4.10은 제공된 인자·공식으로 직접 계산하고 rank를 설명했다. 4.11은 미수행 보류하며, 그 외 장말 문제와 4.12 증명도 미수행이다. MML의 약점 보강 범위에 따라 모든 문제를 일괄 진입 조건으로 두지 않는다. 5장 이동은 전체 문제 완료나 무보조 숙달 판정이 아니다.

CS336 Assignment 1은 기존 작업을 보존하고 진입을 보류한다. MML 이후 승인 순서는 MIT 18.05 Spring 2022 PS1~PS11(R 포함), makemore Parts 3~4와 공식 exercises다. 범위 생략·자동 설치는 승인되지 않았으며 실습 전 CPU/GPU 요구·환경·비용을 확인한다. 자세한 범위는 [ROADMAP](ROADMAP.md)을 따른다.

## 다음 독립 행동

Chapter 5 §5.1 인쇄 쪽 141~142에서 차분몫과 도함수 정의를 기존 [도함수와 수치 미분](knowledge/math/derivatives-and-finite-differences.md)에 연결한다. 입력 변화로 나눈 출력 변화와 그 극한의 의미를 설명하고, 같은 함수에서 평균 변화율과 순간 변화율을 구분한다. 코드를 실행하거나 새 실습 파일을 만들 필요는 없다.
