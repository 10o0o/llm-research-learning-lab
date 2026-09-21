# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 진도 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 ROADMAP Phase: P0
- 현재 주강의: fast.ai — Practical Deep Learning for Coders (2022 Part 1)
- 현재 강의: Lesson 1 — Getting started (진입 전)
- 현재 범위: 로드맵의 Lessons 1~2, 현재는 Lesson 1의 영상·공식 실습·책 1장
- 공식 강의: https://course.fast.ai/Lessons/lesson1.html
- 공식 실습: https://www.kaggle.com/code/jhoward/is-it-a-bird-creating-a-model-from-your-own-data
- 책 1장: https://github.com/fastai/fastbook/blob/master/01_intro.ipynb
- 작업 공간: main.ipynb, recall.ipynb는 이전 챕터 보관 후 빈 셀로 초기화
- 이전 챕터: practice/deep-learning/makemore-mlp-e01-e03.md
- 재구현 회고: practice/deep-learning/makemore-mlp-training-recall.md
- CS336 Assignment 1: 기존 작업 보존, 새 구현 진도 보류

## 관찰된 근거

- Makemore Part 2의 E01 검증 손실 목표와 E03 직접 연결의 구현·실행·해석을
  확인했다. E02는 별도 보관본에 있다. 학습률·조건 통제·학습 반복 개념을
  학습자의 설명과 실행·해석 근거에서 knowledge에 연결했다.
- recall에서 학습자가 학습·평가 함수를 작성하고 train/dev 개선을 해석했다.
  입력과 정답을 다른 행 번호로 추출하면 대응이 깨진다고 설명했다.
- 기준 모델 재구성 및 recall의 데이터·모델 준비는 요청에 따라 AI가 제공했다.
  구현 중 도움도 있었으므로 완전 무보조 재구현 성공으로 취급하지 않는다.
- 학습자의 챕터 정리·초기화 요청으로 보관과 지식 정리를 진행했다.
  fast.ai의 영상 시청·실습 실행·책 읽기는 아직 확인된 바 없다.

## 재확인할 항목

- 논문 읽기와 설명 후 이해 응답을 독립 설명의 근거로 확대하지 않는다.
  논문 전체 회상의 혼동과 실험 출력의 경계는 이전 챕터 회고에 남겼다.
- 이번 전환은 P0 종료가 아니다. fast.ai는 Lessons 1~2 범위를 유지한다.
- fast.ai 실행 환경은 아직 준비하지 않았다. 기존 lab 환경에 자동 설치하지 않는다.
- 파일 초기화는 실행 중인 노트북 커널의 변수·가중치를 지우지 않는다.

## 다음 독립 행동

fast.ai Lesson 1 공식 페이지에서 첫 실습 “Is it a bird?”를 열고,
강의의 시작 구간과 함께 데이터 수집부터 분류 모델 학습·예측까지의 흐름을 따라간다.
영상·실습·책 1장과 자기 주제의 이미지 분류기 구현이 Lesson 1 범위이며,
자료 접근이나 실행 환경에서 막히면 그 지점부터 확인한다.
