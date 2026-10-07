# 보류 자료

이 문서는 현재 주경로에서 뺀 범위와 다시 제안할 조건을 기록합니다. 보류는 완료나
불필요 판정이 아닙니다. 조건이 관찰되면 필요한 부분만 제안하고, 사용자가 승인한
뒤에만 `STATE.md`의 다음 범위를 바꿉니다.

## 공식 과정의 보류 범위

### MIT 18.05 전체 과정의 일괄 이수

Spring 2022 전체 reading·in-class·온라인 문제·PS1~PS11·R 튜토리얼을 일괄
필수 조건에서 제외한다. 미선택 활동은 **미완료 보류**이며 MIT 전체 완료를 뜻하지
않는다. 이미 확인한 실행·설명과 미검증 완료 보고는 STATE의 근거 구분을 유지한다.

- **왜 뺐나**: P0의 핵심 확률 개념은 기존 MLP의 손실·샘플링·평가에 연결하고,
  P0~P1의 likelihood·MLE·통계적 불확실성은 승인된 CS229·ISLP 작업에 연결한다.
  전체 MIT 과정과 R 문법 실습을 마쳐야 모델 학습을 진행하는 의존성을 없앤다.
- **복귀 조건**: 승인된 공식 과제나 읽는 논문에서 현재 경로로 해결되지 않는
  구체적인 확률·추론 공백이 확인될 때 해당 활동만 제안한다. 현재 승인된 핵심
  개념에 대한 MIT 해당 절의 설명은 기존 범위의 보강이며, 미선택 공식 과제의
  추가나 전체 이수 의무 복귀는 별도 승인 없이 진행하지 않는다. 선택한 활동이
  R을 요구하면 R로 수행하며 Python 모델 실습을 공식 완료로 대신하지 않는다.

### 연속 사전분포·켤레 사전분포의 상세 계산

- **왜 뺐나**: likelihood·prior·posterior·MAP의 기본 구분과 모델 손실 연결은
  유지하되, 모든 사전분포의 갱신 계산·유도를 P0의 필수 관문으로 두지 않는다.
  상세 계산은 **미완료 보류**이며 Bayes 개념을 이해했다는 완료 기록이 아니다.
- **복귀 조건**: 승인된 공식 과제나 읽는 논문이 해당 사전분포의 선택·사후분포
  계산·유도를 실제로 요구할 때 필요한 범위만 보강한다.

### CS224N 미선택 written·programming·Final Project

Spring 2024, archive 1246의 A3 Q1(i) attention 비교와 A4 Q1~Q2 written만
P2/P3에서 사용한다. 기존 A1~A4 전체 의무를 이번 승인 재설계로 줄였으며
나머지 written·programming·Final Project는 **미완료 보류**다.

- **왜 뺐나**: 작은 autoregressive LM을 CS336 A1에서 독립 구현하는 경로와
  전체 NLP 과정을 중복 의무화하지 않기 위해서다. 선택 written 수행은 A1~A4
  전체 완료나 대학 채점 통과가 아니다.
- **복귀 조건**: word-vector·dependency parsing·RNN/LSTM·seq2seq·encoder 모델의
  실제 공백 또는 연구/직무 요구가 확인될 때 해당 요구만 제안한다. Winter 2024,
  archive 1244의 과제 번호·환경으로 교체하지 않는다.

### CS336 Assignment 2의 미선택·외부 hardware 검증

A1은 P3의 공식 독립 구현 기준이며 v26.0.3의 공식 저자원 경로와 임의 축소
실험을 구분한다. A2 v26.1.3 전체는 현재 의무가 아니다. P4에서 training
profiling·memory/FLOPs·mixed precision·activation checkpointing·kernel·parallelism을
선택하고 별도 inference/운영 workload를 설계한다.

- **왜 뺐나**: B200 benchmark와 2/4/6 GPU all-reduce, 2 GPU DDP/FSDP 측정을
  단일 8GB 장치로 모두 검증했다고 할 수 없다. 로컬/축소 결과는 해당 범위의
  근거이며 공식 A2 전체 완료가 아니다. Triton backward는 OPTIONAL로 유지한다.
- **복귀 조건**: 질문이나 직무가 해당 GPU benchmark·distributed scaling을 실제로
  요구하고, VRAM·연산시간·장치 수·공식 지정 hardware·비용·한도를 확인한 뒤
  외부 자원 사용을 별도 승인했을 때 필요한 검증부터 수행한다. 그 전에도
  가능한 로컬 학습·측정은 진행한다.

### CS336 Assignment 3·4·5

A3 Scaling, A4 Data, A5 Alignment and Reasoning RL의 전체 과제는 미완료 보류다.

- **왜 뺐나**: 작은 LM·한 전문화·한 독립 연구 cycle에 집중하고 대규모 과제
  전체를 병렬 의무화하지 않기 위해서다. split·leakage·dedup·contamination·
  uncertainty·error analysis는 공통 핵심이므로 함께 보류하지 않는다.
- **복귀 조건**: scaling 질문이면 A3, data pipeline 질문이면 A4, Eval /
  Post-training 분기에서 선수가 확인된 SFT/RL 질문이면 A5의 필요한 범위부터
  제안한다. Transformer 이후의 작은 SFT/eval 노출은 이미 ROADMAP 범위이며
  P5까지 기다리는 별도 복귀 승인을 요구하지 않는다.

### CS231n A2 Q4·Q5, Assignment 1·3와 Final Project

Spring 2024 Lecture 2~6 필요한 설명과 A2 Q1~Q3를 선택한다. 기존 Q1~Q5
전체 의무에서 빠진 Q4 CNN·Q5 CIFAR-10도 미완료 보류이며 수행 완료가 아니다.

- **왜 뺐나**: FC/backprop·optimizer·normalization·dropout이 현재 LM 경로의
  직접 선수다. 전체 CV 과제와 별도 GPT 구현을 함께 요구하지 않는다.
- **복귀 조건**: multimodal vision encoder·CNN·CV 연구 또는 실제 직무 공백이
  확인될 때 해당 부분만 제안한다.

### Karpathy GPT·Tokenizer의 별도 전체 구현

- **왜 뺐나**: CS336 A1에서 BPE·Transformer LM을 독립 구현한다. 동일한 모델을
  세 과정으로 반복하는 별도 전체 구현은 현재 의무가 아니다. GPT 설명 bridge는
  A1 전에 막힌 개념만 사용하고 공식 A1 중에는 다른 구현을 참고하지 않는다.
- **복귀 조건**: A1 진입 전 개념 연결이 막힌 경우의 필요한 구간, 또는 별도
  tokenizer 연구를 선택하고 공식 과제 정책과 중복 범위를 검토한 경우다.

## 과정·자료의 보류 범위

### CS229 최종 프로젝트·공식 시험

- **왜 뺐나**: Summer 2020 notes·PS1~PS3 필수 written·coding과 같은 P1 실험의
  작은 배포·검증이 지정 범위입니다. 최종 프로젝트·시험까지 수행한 것으로 세지 않습니다.
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

### MML §7.3.3 볼록 켤레의 추가 유도·증명

- **왜 뺐나**: 현재 기초 보강에서는 지지 직선·하한·쌍대 표현의 용도를 이해하는 깊이로 제한합니다. Examples 7.7~7.9의 일반 행렬·합성함수 유도와 Exercises 7.9~7.11의 켤레 계산·증명은 추가 필수 관문으로 두지 않습니다. 이미 제공한 튜터 계산은 학습자의 독립 수행으로 보지 않습니다.
- **복귀 조건**: 승인된 공식 과제나 읽는 논문의 최적화 방법에서 볼록 켤레·쌍대 유도가 실제로 필요할 때 해당 부분만 보강합니다.

### Mathematics for Machine Learning 전권 완독

- **왜 뺐나**: P0에서는 Chapter 2~5, 7의 기초 범위를 무보조 설명·계산으로
  빠짐없이 확인하되 부족한 부분만 본문과 공식 연습문제로 보강합니다.
  전권 완독은 Karpathy·CS229 공식 작업과 필요한 MIT 설명에서 다루는 범위와 중복됩니다.
- **복귀 조건**: linear algebra, vector calculus, optimization의 특정 공백이 현재
  공식 과제 수행을 막고 있을 때 해당 절만 사용

### Stat110·OpenIntro 전체 과정

- **왜 뺐나**: 확률·통계 핵심은 기존 모델 실습과 승인된 CS229·ISLP 작업에
  연결하고 필요한 MIT 18.05 Spring 2022 구간으로 보강합니다. Stat110과
  OpenIntro 전체를 추가하면 같은 개념을 별도 전체 과정으로 반복합니다.
- **복귀 조건**: 현재 경로의 설명만으로 해결되지 않는 확률 또는 추론 개념에 대해
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
- **복귀 조건**: Transformer 기초 이후의 작은 SFT/eval 비교 또는 실제 serving에서
  `transformers`, `tokenizers` 관례를 자기 구현과 비교해야 할 때 필요한 절만 사용.
  smol-course 선택 절은 ROADMAP에 포함되어 있으며 전체 과정과 구분한다.

### MIT 6.S191과 기타 조망 강의

- **왜 뺐나**: 별도 완강 없이 각 Phase의 주과정이 같은 내용을 더 깊게 다룹니다.
- **복귀 조건**: 새 분야의 전체 지형을 짧게 볼 필요가 있을 때 관련 강의 하나만

### Karpathy makemore Part 5 — WaveNet

- **왜 뺐나**: convolution sequence model보다 Transformer inference가 현재
  1순위입니다.
- **복귀 조건**: convolution 기반 sequence architecture나 receptive field를 실제로
  다룰 때

## 별도 트랙과 반복 작업

### GP·ICA 추가 심화·넓은 RL 과정

- **왜 뺐나**: P1은 회귀/분류·likelihood·최적화·규제와 실험에 집중한다.
  **CS229 Summer 2020 PS3 Q1 RL·Q6 ICA는 기존 필수 범위로 유지**하며 해당
  선수 notes를 먼저 읽는다. 보류는 이 문제들을 조용히 삭제한다는 뜻이 아니다.
- **복귀 조건**: 공식 필수 문제를 넘어 특정 논문·연구 질문에서 GP·ICA 또는
  policy gradient·reward·RL 평가를 실제로 필요로 할 때 해당 개념만 보강한다.

### Post-training 전문화의 전체 심화·data engineering 전체 과정

- **왜 뺐나**: 현재 주전문화는 잠정 Systems / Inference다. 전 트랙 병렬 의무는
  연구 시간을 분산한다. 평가 공통 핵심과 Transformer 이후의 작은 SFT/eval
  비교는 보류하지 않으며 loss 감소를 held-out 품질로 대체하지 않는다.
- **복귀 조건**: 작은 SFT/eval 비교·독립 품질·실제 공고로 전문화를 재검토하고
  Eval / Post-training을 선택하면 held-out eval → SFT/LoRA → 독립 평가 →
  하나의 DPO/RLVR 질문을 준비한다. data engineering 전체는 실제 data 질문이
  있을 때만 제안한다. 학교 노출만으로 연구-level 독립 수행을 인정하지 않는다.

### P0·P2·P3 Kaggle competition

P1 tabular Kaggle만 필수입니다. 다른 Phase의 competition은 선택입니다.

- **왜 뺐나**: P0의 제출은 공식 학습 근거가 아니고, P2·P3의 공식 과제와 별도
  competition을 모두 의무화하면 중복 프로젝트가 됩니다.
- **복귀 조건**: P0는 예측을 만들 수 있으면 첫 제출 경험을 제안하며 이전 제출
  경험을 요구하지 않습니다. P2·P3는 핵심 학습 이후, 실제 열린 대회가 적용 능력을
  확인하고 실제 확보한 개인 학습 시간 안에서 수행 가능할 때 제안합니다.

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
4. 조건이 생겨도 자동으로 시작하지 않고 필요한 범위를 제안한 뒤 실질적인
   과정·트랙 확장 결정을 확인합니다. 이미 승인된 ROADMAP 범위나 확인된
   북마크 수정에 반복 승인을 요구하지 않습니다.

어떤 조건도 자동으로 학습을 시작하지 않습니다.
