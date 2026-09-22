# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 ROADMAP Phase: P0
- 현재 주강의: Mathematics for Machine Learning, Cambridge University Press (2020)
- 사용 판본: 공식 사이트 배포 PDF, Draft 2024-01-15
- 현재 범위: Chapter 2~5·7 수학 보강; 기존 설명·계산을 보존하고 부족한 부분을 본문·공식 연습문제로 연결
- 현재 강의: Chapter 2, §2.4.3 Vector Subspaces, 인쇄 쪽 39~40
- 공식 자료: https://mml-book.github.io/
- 공식 PDF: https://mml-book.github.io/book/mml-book.pdf
- 연결 실습: Exercise 2.9, 인쇄 쪽 66; 아직 미시도
- 학습 공간: main.ipynb·recall.ipynb는 빈 상태; 이번 단위는 손으로 설명·계산
- 이전 챕터: [fast.ai 책 2장 회고](practice/deep-learning/fastai-book02-production.md)
- CS336 Assignment 1: 기존 작업 보존, 진입 보류

## 관찰된 근거와 남은 범위

사용자의 명시적 결정으로 fast.ai Lessons 1~2의 미완료 항목을 남기고
로드맵의 다음 P0 수학 보강으로 이동했다. fast.ai 전체 완료나 P0 종료가 아니다.
책 2장의 학습·검증·저장·불러오기·추론 저장 출력을 확인하고 노트북을 보존했다.
라벨 연결, crop의 한계, 실제 환경 평가와 추론의 갱신 여부를 학습자가 설명했다.
전체 학습 흐름과 Drivetrain 순서의 독립 설명은 막혀 해설로 보완했다.

위젯 업로드·버튼 동작, 웹 공개 배포, 데이터 정리 후 재학습 비교,
Questionnaire 전체 독립 답변과 Further Research는 미완료로 남겼다.
Lesson 1의 IMDb 중단과 기타 미완료는 이전 회고에 유지한다.
책 원문과 저장 출력은 비공개 보관하고, 공개 노트에는 학습자 초안을 교정한 개념만 반영했다.

기존 선형변환·기저·랭크·영공간·최소제곱·고유기저 노트가 있다.
그 존재만으로 MML 2~5·7장 전체 이해나 공식 연습문제 완료를 추정하지 않는다.
이미 설명한 내용을 다시 완독시키는 대신 현재 단위의 연결에 필요한 부분을 보강한다.

## 재확인할 항목

- 새 커널 전체 재현과 배포 환경 동작은 미검증이다.
- 튜터 해설 후 동의는 독립 회상 완료가 아니다.
- 실습 전에 CPU/GPU 요구와 환경·비용을 먼저 확인한다.
- MML 다음은 승인된 MIT 18.05 Spring 2022와 makemore Parts 3~4다.
  현재 전환은 그 범위의 생략·자동 설치를 허용하지 않는다.
- 남은 수학 범위는 MML 2~5·7장이며 부분공간 단위가 전체 범위를 대체하지 않는다.

## 다음 독립 행동

사용자의 요청으로 부분공간 설명부터 아직 시작하지 않은 상태로 재개한다.
다음은 MML §2.4.3 Vector Subspaces의 목적과 조건을 처음부터 설명하는 것이다.
본문 읽기·독립 설명·Exercise 2.9 시도는 미완료다.
설명 후 같은 절의 공식 Exercise 2.9(a)로 연결하고 이후 (b)~(d)를 다룬다.
코드 실행·환경 설치·GPU 대여는 필요 없다.
