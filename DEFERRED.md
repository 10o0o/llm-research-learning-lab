# 보류 자료

이 문서는 현재 주경로에서 뺀 범위와 다시 제안할 조건을 기록합니다. 보류는 완료나
불필요 판정이 아닙니다. 조건이 관찰되면 필요한 부분만 제안하고, 사용자가 승인한
뒤에만 `STATE.md`의 다음 범위를 바꿉니다.

## 공식 과정의 보류 범위

### CS224N Final Project

CS224N A1~A4는 **`P3`에서 정식 수행합니다.** Spring 2024의 written·수학·
programming을 모두 유지합니다. 보류 대상은 Final Project뿐이며 미완료 보류입니다.

- **왜 뺐나**: P5의 우선 산출물은 autoregressive inference의 prefill/decode,
  KV cache, batching과 성능·품질 측정입니다. Final Project를 병렬 의무화하면
  이 연구 시간을 잠식합니다.
- **복귀 조건**: embedding·reranker·encoder model을 실제 serving 범위에 넣거나,
  inference 우선 프로젝트 뒤 별도 NLP 연구 프로젝트를 하기로 결정할 때

### CS336 Assignment 3·4·5

P4는 CS336 Spring 2026 A1 Basics와 A2 Systems 전체, Lecture 10 inference를
수행합니다. A3 Scaling, A4 Data, A5 Alignment and Reasoning RL은 미완료 보류입니다.

- **왜 뺐나**: A1·A2와 P5 inference 연구가 현재 1순위 systems 경로를 채웁니다.
- **복귀 조건**: scaling 실험이면 A3, data pipeline이면 A4, post-training이면
  A5를 그 목적에 필요한 범위부터 제안

### CS231n Assignment 1·3와 Final Project

P2의 CS231n 범위는 Spring 2024 Lecture 2~6와 Assignment 2 Q1~Q5 전체입니다.
이 범위와 PyTorch 보강 뒤 Karpathy GPT·Tokenizer를 P2 끝에서 수행하며, CS231n
Assignment 1·3와 Final Project만 이 절의 보류 대상입니다.

- **왜 뺐나**: A2가 이 경로에 필요한 optimization, backprop, CNN, normalization과
  PyTorch 학습 진단을 집중적으로 다룹니다. 나머지 CV 과제는 LLM systems 주경로의
  핵심이 아닙니다.
- **복귀 조건**: multimodal의 vision encoder, detection·segmentation, generative
  vision 또는 CV 직무를 실제 목표로 추가할 때 해당 부분만 제안

## 과정·자료의 보류 범위

### CS229 최종 프로젝트·공식 시험

- **왜 뺐나**: Summer 2020 notes·PS1~PS3의 필수 written·coding과 P1 배포
  프로젝트가 이번 지정 범위입니다. 최종 프로젝트·시험까지 수행한 것으로 세지 않습니다.
- **복귀 조건**: 사용자가 해당 공식 요구사항까지 확장하기로 결정할 때

### ISLP 전권·MIT 18.01SC 전체 과정

- **왜 뺐나**: ISLP는 5·6·8·13장 본문과 Python lab만 필요하며 MIT 18.01SC는
  단변수 미분·정적분 공백을 메우는 보조 자료입니다.
- **복귀 조건**: 현재 설명이나 과제에서 빠진 개념이 실제로 드러날 때 관련 절만 보강

### fast.ai Part 1 Lesson 3 이후

- **왜 뺐나**: P0의 Lesson 1~2가 top-down workflow 역할을 맡고, 이후 modeling·
  deployment 내용은 P1·P2의 공식 과정과 프로젝트에서 더 깊게 수행합니다.
- **복귀 조건**: 특정 downstream task를 빠르게 prototype해야 하고 현재 주과정에
  해당 workflow가 없을 때 필요한 lesson만 제안

### Mathematics for Machine Learning 전권 완독

- **왜 뺐나**: P0에서는 Chapter 2~5, 7의 기초 범위를 무보조 설명·계산으로
  빠짐없이 확인하되 부족한 부분만 본문과 공식 연습문제로 보강합니다.
  전권 완독은 Karpathy·MIT 18.05·CS229 공식 작업과 중복됩니다.
- **복귀 조건**: linear algebra, vector calculus, optimization의 특정 공백이 현재
  공식 과제 수행을 막고 있을 때 해당 절만 사용

### Stat110·OpenIntro 전체 과정

- **왜 뺐나**: MIT 18.05 Spring 2022 class materials와 PS1~PS11이 P0 확률·통계
  주과정입니다. Stat110과 OpenIntro 전체를 추가하면 같은 개념을 세 과정으로
  반복합니다.
- **복귀 조건**: MIT 18.05 설명만으로 해결되지 않는 확률 또는 추론 개념에 대해
  다른 유도·예제가 필요할 때 해당 절만 보조로 사용

### CS229 2018 공개 영상 전체를 별도 과정으로 수행

- **왜 뺐나**: P1의 판본은 공개 notes와 PS1~PS3가 함께 있는 Summer 2020입니다.
  2018 영상은 같은 주제의 설명 보조이며 별도 완료 대상으로 세지 않습니다.
- **복귀 조건**: Summer 2020 notes의 특정 유도에 영상 설명이 필요할 때 해당 강의만

### Full Stack Deep Learning 전체 과정

- **왜 뺐나**: P1의 Made With ML 프로젝트와 P4·P5 systems 작업이 현재 산출물을
  직접 만듭니다. FSDL 전체 수강을 병렬 의무화하지 않습니다.
- **복귀 조건**: 실제 ML systems design 면접이나 production 설계에서 특정 공백이
  확인될 때 관련 강의만 제안

### Hugging Face LLM Course

- **왜 뺐나**: P0~P4는 내부 메커니즘과 공식 assignment를 직접 구현하는 구간입니다.
- **복귀 조건**: P5 또는 취업 준비에서 `transformers`, `tokenizers`, 실제 serving
  stack의 관례를 자기 구현과 비교해야 할 때 필요한 절만 사용

### MIT 6.S191과 기타 조망 강의

- **왜 뺐나**: 별도 완강 없이 각 Phase의 주과정이 같은 내용을 더 깊게 다룹니다.
- **복귀 조건**: 새 분야의 전체 지형을 짧게 볼 필요가 있을 때 관련 강의 하나만

### Karpathy makemore Part 5 — WaveNet

- **왜 뺐나**: convolution sequence model보다 Transformer inference가 현재
  1순위입니다.
- **복귀 조건**: convolution 기반 sequence architecture나 receptive field를 실제로
  다룰 때

## 별도 트랙과 반복 작업

### Post-training·LLM evaluation·data engineering

- **왜 뺐나**: 현재 1순위는 systems와 inference이며 병렬로 모두 수행하면 P4·P5
  연구가 분산됩니다.
- **복귀 조건**: P5 이후 전문화 순위를 다시 정하거나 실제 공고·프로젝트가 SFT,
  preference optimization, judge evaluation, data pipeline을 요구할 때

### P0·P2·P3 Kaggle competition

P1 tabular Kaggle만 필수입니다. 다른 Phase의 competition은 선택입니다.

- **왜 뺐나**: P0의 제출은 공식 학습 근거가 아니고, P2·P3의 공식 과제와 별도
  competition을 모두 의무화하면 중복 프로젝트가 됩니다.
- **복귀 조건**: P0는 예측을 만들 수 있으면 첫 제출 경험을 제안하며 이전 제출
  경험을 요구하지 않습니다. P2·P3는 핵심 학습 이후, 실제 열린 대회가 적용 능력을
  확인하고 해당 Phase 예산 안에서 수행 가능할 때 제안합니다.

### 별도 월별 논문 quota와 과제 전체 재구현

- **왜 뺐나**: 공식 지정 reading은 논문 근거에 포함하고, assignment 전체를 다시
  쓰는 대신 Phase별 대표 단위만 무보조 재구현으로 확인합니다.
- **복귀 조건**: 공식 reading이 연구 질문을 다루지 못하거나 대표 재구현에서
  실제 공백이 드러났을 때 필요한 논문 또는 구성요소만 추가

## 갱신 규칙

1. 항목을 뺄 때는 이유와 복귀 조건을 함께 적습니다.
2. 보류 항목은 완료·날짜·점수·mastery를 기록하지 않습니다.
3. 복귀 판단은 학습자의 실제 설명·계산·구현·실행·해석과 현재 외부 요구를
   근거로 합니다.
4. 조건이 생겨도 자동으로 시작하지 않고 필요한 범위를 제안한 뒤 사용자의
   `STATE.md` 교체 승인을 기다립니다.

어떤 조건도 자동으로 학습을 시작하지 않습니다.
