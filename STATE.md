# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 ROADMAP Phase: P0
- 현재 주강의: MIT 18.05 Introduction to Probability and Statistics
- 사용 판본: MIT OpenCourseWare, Spring 2022
- 현재 범위: MIT 18.05 본문과 PS1~PS11, R 요구 포함; MML의 남은 공백과 보류는 회고·DEFERRED에 보존
- 현재 강의: Unit 1 Probability, Class 1 Introduction·Counting and Sets 진입 전
- 공식 자료: [MIT 18.05 Spring 2022](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/) · [Class 자료](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/classes-reading-and-in-class-materials/)
- 연결 실습: Class 1 공식 문제의 요구 확인 후 직접 시도; 아직 미착수
- 학습 공간: main.ipynb·recall.ipynb는 빈 상태; MIT 공식 답안은 별도 비공개 공간에 저장하며 새 공간·환경은 아직 만들지 않았다
- 학습 방식: 교재를 직접 열지 않고 튜터가 제공한 설명으로 학습; 질문에 필요한 정의·표기·조건을 대화 안에 먼저 제공하고, 답 검토 후 다음 내용까지 바로 연결. 승인된 핵심 범위를 유지하며 항등식마다 추가 손계산을 붙이지 않고 미분의 개념·shape와 모델 학습의 연결을 중심으로 설명

## 관찰된 근거와 남은 범위

fast.ai Lessons 1~2는 미완료 항목을 남기고 이동했으며, 완료나 P0 종료 판정이 아니다. 새 커널 전체 재현·배포도 미검증이다. 수행·도움·미완료 요구는 [책 1장 회고](practice/deep-learning/fastai-book01-intro.md), [Lesson 1 실습 회고](practice/deep-learning/fastai-lesson1-images.md), [책 2장 회고](practice/deep-learning/fastai-book02-production.md)에 유지한다.

MML [2장 회고](practice/math/mml-ch02-linear-algebra.md)에 Exercise 2.12의 교집합 기저, 2.20(a)의 그림, §2.7.2 출력 역변환 방향과 기저 변환·상/영공간·아핀 사상의 독립 설명 공백을 유지한다.

MML [3장 회고](practice/math/mml-ch03-analytic-geometry.md)에 거리·일반 내적 조건·투영과 잔차·아핀 투영·회전 부호의 회상 공백을 유지한다. Exercise 3.8·3.10은 시도했으나 3.10 부호는 해설로 교정했고, 3.1~3.7·3.9 및 그 밖의 미확인 문제를 완료로 보지 않는다.

MML [4장 회고](practice/math/mml-ch04-matrix-decompositions.md)에 본문·선택 연습의 직접 설명과 계산, 교정·튜터 계산, 미수행을 보존했다. SVD 인자와 성분 소실, 정확한 생략과 근사, 오차에 필요한 항 수는 설명·계산했다. 고유공간·대각화 조건, 고유값 부호와 특잇값, rank와 크기의 구분은 교정 이력을 남겼다. 마지막 대각행렬의 고유값·특잇값은 맞게 답했지만 길이 배율이라는 이유는 해설로 보충했다.

Exercise 4.5는 피드백을 거쳤고 4.8은 영공간 방향 이후 튜터가 계산했다. 4.10은 제공된 인자·공식으로 직접 계산하고 rank를 설명했다. 4.11은 미수행 보류하며, 그 외 장말 문제와 4.12 증명도 미수행이다. MML의 약점 보강 범위에 따라 모든 문제를 일괄 진입 조건으로 두지 않는다. 5장 이동은 전체 문제 완료나 무보조 숙달 판정이 아니다.

MML [5장 회고](practice/math/mml-ch05-vector-calculus.md)에 편미분·연쇄법칙의 직접 계산, 야코비안 크기·조립 교정, 역행렬 미분의 부호 공백, 자동미분·Taylor의 튜터 설명과 미수행을 보존했다. 선택 Exercises 5.2·5.3의 도함수는 제공된 규칙·경로 안내 뒤 직접 구했다. 5.7(a,b)·5.8(b)는 합산·첨자·덧셈 및 과제 뜻을 설명한 뒤 수정·계산했으며 무보조 풀이로 보지 않는다. 혼합 편미분의 의미와 결합 항 제거의 인과관계는 직접 설명해 개념 초안으로 사용했다. 전체 Hessian·야코비안·Taylor 계수의 독립 구성과 장말 미수행 문제는 미완료다. 빈 작업 노트북은 보관본 생성·실행·초기화 없이 유지했다. 7장 이동은 전체 문제 완료나 전체 숙달 판정이 아니다.

MML [7장 회고](practice/math/mml-ch07-continuous-optimization.md)에 경사하강·모멘텀·SGD·제약·볼록성의 직접 설명, 튜터 유도와 미수행 공식 연습을 보존했다. Exercise 7.2는 조건과 대상 기울기를 제공받은 뒤 갱신 방법을 말로 정확히 표현했다. 전체 장 무보조 숙달이나 장말 전 문제 완료를 뜻하지 않는다. 볼록 켤레의 추가 유도·증명을 필수 관문으로 두지 않는 사용자 동의를 DEFERRED에 반영했다. 빈 main.ipynb·recall.ipynb는 실행·보관본 생성·초기화 없이 유지했다.

다음은 기존 승인 순서의 MIT 18.05 Spring 2022이다. 공식 syllabus에서 R 사용과 자기 말로 답안 작성·협력자 및 외부 출처 표기 요구를 확인했다. 강의 자료 목록에서 Class 1의 Introduction, Counting and Sets를 확인했으며 실제 본문 학습과 공식 문제 수행은 아직 시작하지 않았다. R 실행 환경·공식 온라인 문제 접근·과제별 요구는 실습 전에 확인하며 자동 설치하지 않는다. PS1~PS11의 R 포함 수행과 비공개 답안 저장 원칙을 유지한다.

CS336 Assignment 1은 기존 작업을 보존하고 진입을 보류한다. MIT 18.05 이후 승인 순서는 makemore Parts 3~4와 공식 exercises다. 이 이동은 P0 종료나 다른 미완료 범위의 생략이 아니다.

## 다음 독립 행동

MIT 18.05 Spring 2022 Class 1의 Introduction·Counting and Sets 공식 본문과 in-class 문제를 확인하고, 경우의 수와 집합을 확률에 연결하는 첫 학습 단위를 시작한다. 정의·조건을 대화에 제공하며 공식 문제는 학습자가 직접 답한다. R 사용 구간 전에 환경을 확인하고 PS1~PS11을 대체하거나 생략하지 않는다.
