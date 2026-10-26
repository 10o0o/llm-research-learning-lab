# 커리큘럼과 자료

[로드맵](ROADMAP.md)의 단계에 필요한 자료만 펼친다. 아래 확인 기준은 **우리의 학습 제안**이며
대학의 성적·공식 과제 완료 기준이 아니다. 현재 선택과 실제 수행은 [STATE](STATE.md)에만 기록한다.
한 번에 주 자료 하나를 사용하고, 수학·다른 강의는 막힌 부분의 참고로 둔다.

공식 자료 확인: 2026-10-24. 자료 열람, 수강 등록, 과제 수행, 독립 구현을 구분한다.
여기에 링크가 있다고 수강하거나 과제를 완료한 것은 아니다.

## 추천 주자료와 참고 자료

| 구분 | 자료와 역할 |
|---|---|
| 현재 추천 주자료 | AX: [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) / 모델 기반: [기존 Karpathy 학습](#1-pytorch-학습-루프)의 미완료 구간 |
| 필요한 부분을 찾는 자료 | MIT 6.036, CS224N, 수학 자료, FSDL, HF Agents 등. 현재 질문의 공백을 보완할 때 해당 부분만 참고한다. |
| 이후 전문화 자료 | CS336, smol-course, MIT 6.5940 등. 필요한 기반과 자원을 갖춘 뒤 선택한다. |

참고 자료에 등록되어 있다는 사실만으로 해당 과정을 수강하거나 과제를 수행하도록 요구하지 않는다.
새로운 자료 선택은 현재 문제와 사용자의 선택을 기준으로 한다.
추천은 선택·수강 기록이 아니며, 실제 활성 자료와 강의 위치는 STATE에만 둔다.

2026-10-26 목차 기준으로 AX의 **우리 추천 선별 경로**는 Zoomcamp `1 → 2 → 4 → 5`다.
[공식 자료](https://github.com/DataTalksClub/llm-zoomcamp)의 Agentic RAG → Vector Search →
Evaluation → Monitoring 중 현재 구현에 필요한 부분을 연결한다. 이 선별은 공식 전체 과정의
순서나 수료 기준이 아니다. 이미 직접 수행한 역량은 중복 구현을 요구하지 않는다.
오케스트레이션·추가 스택은 현재 기능에 필요하고 학습자가 선택했을 때만 추가한다.

## 0. 작은 AI 기능과 기존 경험

[문의 보조 앱](practice/ai-apps/README.md)은 입력·조회·검색·생성·표시가 연결된 기존 사례다.
이 코드를 모두 정리하는 것이 목표는 아니다. STATE에 저장된 현재 질문과 작업을 이어가며,
새 실습이나 제품의 기능은 학습자가 선택할 때 진행한다. 기존 실습은 [보관 색인](practice/README.md)에서 확인한다.

확인할 것: 입력과 출력, 자신이 바꾸는 부분, 실제 결과, 남은 문제를 직접 설명할 수 있는가.
과거 실행 기록과 도움을 받은 구현은 보존하며 이번 독립 수행으로 재분류하지 않는다.

## 1. PyTorch 학습 루프

주 자료: [Karpathy Neural Networks: Zero to Hero](https://github.com/karpathy/nn-zero-to-hero).
기존 micrograd·makemore에서 부족한 MLP/backprop 부분만 골라 본다. 완성 강의 코드를
그대로 실행하는 것과 자신의 파일에서 학습 루프를 연결하는 것을 구분한다.

실습 제안: 작은 분류기의 forward→loss→backward→update를 직접 작성한다.
입력·가중치·출력 shape, gradient와 update의 차이를 설명하고 learning rate 등 한 조건을 바꾼다.
새로운 앱 구조, 데이터 파이프라인, 예외 처리부터 만들 필요는 없다.

## 2. ML 기초와 평가

해당 개념의 참고 자료: [MIT 6.036 Introduction to Machine Learning, Fall 2020](https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/).
Python·미적분·선형대수 선행 지식을 요구한다. 표현, 지도학습, 모델 비교, 과적합/일반화를
현재 작은 모델과 연결한다. 공식 연결 학습 페이지의 URL에 1T2019가 있어도 OCW 판본과 혼동하지 않는다.
강의 원문은 복제하지 않고 링크와 자신의 설명을 남긴다.

실습 제안: train/dev/test를 구분하고 baseline과 변경 모델을 비교한다. 같은 데이터로
반복 선택한 결과를 독립 test 결과라고 하지 않는다. 점수 외에 누수 여부와 실패 예시를 확인한다.

## 3. NLP와 Transformer

해당 개념의 참고 자료: [Stanford CS224N Spring 2024, archive 1246](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/).
word vectors, backprop, attention, Transformers, pretraining, evaluation 중 필요한 강의를 선택한다.
이 페이지의 무료 공개 영상은 2023년 영상이고, 2024년 영상은 Canvas 접근이 필요하다.
2024 slides와 2023 공개 영상을 구분해 기록하며 Winter 2024 archive 1244와 섞지 않는다.

실습 제안: 작은 attention 연산에서 입력→score→mask→가중합→logits 흐름을 확인한다.
shape와 causal mask를 설명하고 조건 하나를 바꾼 실제 결과를 해석한다.
공식 과제를 선택하면 과정 AI 정책을 먼저 확인한다. 직접 답 요청·복사와 상당 부분 AI 대행은 금지된다.

## 4. 작은 LM 구현: 둘 중 하나

- 공식 경로: [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) A1.
  Python/PyTorch·수학·ML 역량을 요구하고 scaffolding이 적으므로 즉시 시작할 입문 과정은 아니다.
  선택 시 [과정별 정책](.agents/references/official-course-policies.md)의 A1 v26.0.3 고정 판본과
  정확한 handout, 환경, 자원과 AI 제한을 확인한다. 공식 답안은 별도 비공개 공간에 둔다.
- 독립 경로: 자신이 정한 작은 LM에서 토큰화·학습·생성·평가를 구현한다.
  [Karpathy 강의](https://github.com/karpathy/nn-zero-to-hero)의 GPT 부분은 연결이 부족할 때 참고한다.

확인할 것: 데이터·토큰 수·모델 설정·실제 실행 조건·held-out loss·생성 예시와 한계를 설명한다.
자체 toy run, 공식 허용 축소 경로, 공식 과제 전체 완료는 서로 다르다. 두 구현을 모두 강제하지 않는다.
모델/데이터 다운로드나 유료 GPU 실행은 이 문서만으로 승인되지 않는다.

## 5. 전문화 선택

### 후학습과 평가

주 자료: [Hugging Face smol-course](https://github.com/huggingface/smol-course).
현재 공개된 SFT와 evaluation을 우선 선택하고, baseline과 데이터가 준비되면 DPO를 검토한다.
RL·synthetic data의 예정 날짜만으로 공개 완료를 판단하지 않고 실제 자료 존재를 진입 시 확인한다.

실습 제안: 고정된 held-out 질문, 학습 전후 비교, 실패 분석을 직접 만든다.
모델 크기·라이선스·메모리·GPU 사용 가능 여부를 먼저 확인한다. 실행하지 못한 학습은 미완료다.

### 시스템 대안

주 자료: [MIT 6.5940 Fall 2024](https://hanlab.mit.edu/courses/2024-fall-65940)의 해당 단원.
작은 모델에서 profiling·메모리/FLOPs·batch·KV cache·양자화를 먼저 연결한다.
[CS336](https://cs336.stanford.edu/) A2 v26.1.3의 Triton·분산 학습은 선수 역량과 장비를 갖춘 뒤 선택한다.
CPU 기능 확인이나 단일 GPU 실험은 공식 B200/다중 GPU 검증 완료가 아니다.
후학습 경로와 동시에 의무화하지 않고, 지원하지 않는 실험을 위해 먼저 장비를 구매하지 않는다.

## 6. 독립 실험

자신의 문제에서 baseline, 바꿀 요인 하나, 고정 조건, 비교 지표를 정한다.
코드와 실제 결과를 함께 보며 학습자가 먼저 설명한다. 개선되지 않은 결과도 원인과 한계를
설명하면 학습 자료가 된다. 실행 전 예상 결과를 실제 성과처럼 적지 않는다.

## 필요할 때만 여는 수학·이론

- [MIT 18.06SC Linear Algebra, Fall 2011](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/):
  tensor 전에 행렬·벡터·rank, 회귀에서 projection/least squares, 저랭크·LoRA에서 SVD.
- [MIT 18.02SC Multivariable Calculus, Fall 2010](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/):
  backprop에서 막히면 partial derivatives, chain rule, gradient. 전 과정 선행 수료는 요구하지 않는다.
- [MIT 18.05 Probability and Statistics, Spring 2022](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/):
  확률변수·기댓값·조건부확률, 평가에서 신뢰구간·가설검정. R 공식 과제를 선택했다면 Python
  유사 실험으로 공식 완료를 대신하지 않는다.
- CS229 Summer 2020은 기존 판본의 이론 보조 후보다. 이번 원문 재확인은 완료하지 못했으며
  [기존 과정별 정책](.agents/references/official-course-policies.md)을 보존했다. MIT와 중복 의무 수강하지 않는다.
- [CS231n 개념 노트](https://cs231n.github.io/)는 최적화·신경망 공백 참고다.
  현재 연결 과제는 Spring 2026이며 과거 Spring 2024 과제와 구분한다.

## AI 도움과 기록

AI는 흐름과 변경 책임을 안내하고, 막힌 개념을 설명하고, 학습자 코드·출력·첫 해석을 검토한다.
요청 없이 핵심 구현을 대신 완성하지 않는다. 자체 실습의 명시적 구현 도움은 도움 범위를 기록하며,
CS336 등 공식 과제의 더 엄격한 제한은 [과정별 정책](.agents/references/official-course-policies.md)을 따른다.
강의 진도는 실제 보고된 위치만 기록하고, 일일 TIL·수료 점수·자동 계획표는 만들지 않는다.

## 목표 역량별 누락 방지 지도

CS336은 구현 경로의 한 예시다. 다음 영역은 목표 역량의 범위를 확인하는 지도이며,
아래 강의를 모두 수강하는 목록이나 진도 관리표가 아니다. 같은 산출물에서 여러 역량을 확인해도 된다.
CS/AI 학위 전체를 대체하는 완전한 교육과정이라고 주장하지 않는다.

### 프로그래밍과 재현성: 단계 1부터

- [Python 공식 튜토리얼](https://docs.python.org/3/tutorial/),
  [NumPy 배열·broadcasting](https://numpy.org/doc/stable/user/absolute_beginners.html),
  [PyTorch Learn Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)에서 필요한 부분만 사용한다.
- [MIT Missing Semester 2026](https://missing.csail.mit.edu/)은 debugging/profiling/packaging 공백 보완이다.
  기존 웹 개발자의 Git·셸 기초를 자동으로 다시 시키지 않는다.
- 코드·데이터·모델·설정 버전, seed와 비결정성 한계, checkpoint 저장/재개를 작은 실험에 적용한다.
  Python과 패키지 문서는 실제 설치 버전에 맞춘다. 재현성을 위해 큰 플랫폼부터 만들지 않는다.

### 딥러닝과 최적화: 단계 1–3

Karpathy 구현을 주축으로 초기화, activation, SGD/Adam, regularization, 수치 안정성을 확인한다.
[MIT 6.S191 2026](https://introtodeeplearning.com/)의 입문·sequence·RL 개요는 전체 지도를
보완할 때 선택한다. 별도 전체 부트캠프를 의무 수강하지 않는다.

### 데이터 품질과 통계적 실험: 단계 2부터 계속

출처·사용 권리·중복·오염을 확인하고 split을 지킨다. baseline과 ablation, 표본/seed에 따른
변동, 같은 예시의 전후 오류와 평가자 불일치를 검토한다. MIT 18.05는 불확실성·신뢰구간의
필요한 개념에 연결한다. 자동 judge 점수 하나를 품질이나 개선의 확정 증거로 삼지 않는다.

### 후학습의 원리: 단계 5

SFT와 평가 후 [PEFT LoRA 개념](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora)을
통해 frozen base와 trainable low-rank update를 이해한다. main 문서는 개념 참고이며 실행 시
설치된 안정 버전을 따른다. 소스 설치나 환경 변경을 자동으로 하지 않는다.

RLHF/RLVR 구현으로 가려면 [Hugging Face Deep RL Course](https://huggingface.co/learn/deep-rl-course/en/unit0/introduction)의
MDP·return, policy gradient, actor-critic, PPO 관련 단원(1·4·6·8)을 선별한다.
DPO를 전체 RL 학습과 동일시하지 않는다. RL 자체의 과제를 모두 마쳐야 SFT를 할 수 있는 것은 아니다.

### 메모리·연산·추론: 단계 4–5의 공통 기초

[MIT 6.5940 TinyML and Efficient Deep Learning Computing, Fall 2024](https://hanlab.mit.edu/courses/2024-fall-65940)의
압축·양자화·efficient LLM 단원에서 메모리, 연산, batch, prefill/decode, KV cache의 비용을 연결한다.
작은 모델의 실제 속도·메모리 관찰을 먼저 한다. 후학습 경로에서도 이 기초를 생략하지 않는다.
더 깊은 GPU kernel·분산 학습은 CS336 A2 등 선택 심화이며 공통 입문 관문이 아니다.
프로세스·메모리·동시성 설명이 막힐 때만 [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/) 관련 장을 참고한다.

### 제품과 연구의 연결: 단계 0부터, 단계 6에서 종합

[Full Stack Deep Learning 2022](https://fullstackdeeplearning.com/course/2022/)의 데이터·실험 관리·테스트·
배포·모니터링 강의를 자신의 프로젝트에 필요한 만큼 적용한다. 당시 전체 기술 스택을 그대로
설치하거나 실제 외부 배포를 자동 실행하지 않는다. 배포 설계와 실제 운영 검증은 구분한다.

논문은 주장→가정→baseline→작은 재현→ablation→한계 순으로 읽는다. 논문 개수나 요약 파일 수를
목표로 하지 않고, 자신의 질문 하나에 실제 비교 결과를 남긴다. 인터뷰 준비와 연구 역량 모두
직접 변경·설명할 수 있는 산출물이 중심이며, 세미나 시청은 구현과 실험을 대신하지 않는다.

RAG 제품에서는 검색 실패와 생성 실패를 분리하고, 작은 고정 질문·근거 문서 세트로 확인한다.
필요하면 retrieval recall@k와 답변의 근거 일치를 각각 본다. 문서·모델 출력은 신뢰 경계 밖의
입력으로 취급하고 권한·민감정보·도구 호출 제한을 확인한다. 관련 문제에서만
[HF Agents 평가 참고](https://huggingface.co/learn/agents-course/en/bonus-unit2/what-is-agent-observability-and-evaluation)와
[OWASP Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/?lang=us)를 읽는다.
별도 평가 관리 시스템 대신 기존 실습 파일/README에 설정·실제 결과·실패 예시를 남긴다.

## 국내외 커뮤니티에서 참고한 학습 방식

2026-10-24 공개 자료 기준이다. 커뮤니티 소개를 추천 품질의 보증이나 현재 참가 가능 여부로
해석하지 않는다. 가입·결제·팀 참여·외부 PR은 자동 실행하지 않는다. 아래는 추가 필수 강의가 아니다.

- [Hugging Face KREW 한국어 LLM 평가 스프린트](https://github.com/Hugging-Face-KREW/k-llm-eval-sprint):
  2026년 10~11월 운영 사례. 운영/진도 저장소와 실제 Lighteval 포크를 분리하고 평가 구현→재현→리뷰로 진행한다.
  우리 구조도 이를 참고해 허브와 구현 공간을 구분한다. 후반 한국어 평가 실험의 참고이며 신규 모집으로 안내하지 않는다.
- [가짜연구소 LLM technical report study](https://github.com/Pseudo-Lab/llm-technical-report-study):
  13기 2026-10-04 시작, 모집 종료. Transformer 이후 보고서 한 편의 구조·데이터·학습·근거를 읽는 참고다.
- [PyTorch 한국 사용자 모임의 TinyTorch 소개](https://discuss.pytorch.kr/t/tinytorch-pytorch-import/12251)와
  [TinyTorch 원문](https://mlsysbook.ai/tinytorch/): Python으로 직접 만드는 교육용 프레임워크.
  현재 Preview이며 classroom release는 Spring 2027 예정으로 API·학습 흐름이 안정화 중이다.
  주 실습 환경으로 채택하지 않고 기존 micrograd/MLP와 필요한 개념만 비교한다.
- [모두의연구소 Quant LAB](https://modulabs.co.kr/labs/816): 2026-09~12 운영, 모집 종료.
  논문 리뷰→재현→ablation→평가 순서를 후반 추론 실험에 참고하며 학회 투고를 입문 목표로 강제하지 않는다.
- [모두의연구소 AI 에이전트 LAB](https://modulabs.co.kr/labs/883): 게시상 2026-10-30까지 모집,
  11월부터 활동 예정. 개인→팀 프로젝트의 AX 피드백 참고이며 모델 학습 연구 과정의 대체가 아니다.
  실제 참여를 원할 때 일정·조건을 다시 확인한다.

### 최신성 판단

행렬·미분·확률 같은 변하지 않는 원리는 오래된 MIT 자료도 유지한다. 하지만 예전 강의의
프레임워크 버전·모델 ID·API·설치법은 그대로 따라 하지 않는다. 최신 README 수정일만으로
내부 notebook까지 최신이라고 판단하지 않고, 실행할 단위의 공식 문서·환경·라이선스를 확인한다.
새 agent/RL/추론 기법은 유행만으로 추가하지 않고 현재 질문을 해결할 때 선택한다.

### 해외 실전 커리큘럼의 선택적 활용

- [DataTalksClub LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp): 현재 self-paced 경로의
  agentic RAG·vector search·evaluation·monitoring을 단계 0의 프로젝트에 필요한 만큼 선택한다.
  [2026 과정 설명](https://github.com/DataTalksClub/docs/blob/main/courses/llm-zoomcamp/index.md)처럼
  black-box LLM 응용 과정이며 모델 학습의 대체가 아니다. Kestra/dlt 등 전체 운영 스택을 의무 설치하지 않는다.
- [Maxime Labonne LLM Course](https://github.com/mlabonne/llm-course): 분야 누락을 보는 참고 지도다.
  최근 링크 수정과 별개로 Llama 2/CodeLlama 등 오래된 예제가 남아 있으므로 notebook을 그대로 주 경로에 넣지 않는다.
  실제 도구는 공식 최신 안정 문서로 확인한다.

## Kaggle: 단계에 맞는 선택 실습

Kaggle은 알고리즘 정답을 맞히는 코딩테스트와 달리 데이터에서 모델을 만들고 평가하는 대회·실습
플랫폼이다. 학습 목표가 맞을 때 2~3번 정도 선택할 수 있으며 순위·메달·매일 제출을 목표로 하지 않는다.
다음은 확인 당시 종료 시각이 정해지지 않은 입문용 rolling 과제다. 참여 전 현 규칙을 다시 확인한다.

1. 단계 2: [Titanic](https://www.kaggle.com/competitions/titanic) 또는
   [House Prices](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/overview) 중 하나.
   CPU의 작은 baseline, 자기 split, 변경 조건 하나, held-out 지표·오류·누수 점검을 남긴다.
2. 단계 3 전후: [Digit Recognizer](https://www.kaggle.com/competitions/digit-recognizer/overview)는 선택이다.
   자기 PyTorch 학습 루프에서 MLP와 작은 CNN, train/eval 모드, 오분류 예시를 확인한다.
   같은 경험이 있으면 생략한다. MNIST는 기초 연습용 오래된 데이터이며 최신 LLM 기법으로 소개하지 않는다.
3. 단계 4–5: [LLM Classification Finetuning](https://www.kaggle.com/competitions/llm-classification-finetuning/overview/description).
   Chatbot Arena 응답 선호 예측의 log loss 과제다. 과거 LMSYS 대회와 구분하며 메달 대상이 아니다.
   작은 표본·텍스트 baseline부터 시작해 자원이 허용할 때 encoder/adapter로 확장한다.
   중복/group 분할과 응답 순서 편향을 점검한다. 이 분류 과제 자체가 DPO 학습은 아니다.

제출 여부와 무관하게 실습 코드·설정·실제 validation 결과·실패 예시로 학습을 판단한다.
외부 제출·데이터 업로드·가입·규칙 동의는 자동 수행하지 않는다.
[Notebook 자원](https://www.kaggle.com/docs/notebooks)은 계정별 한도·대기 상태를 실제 확인하며
무료 GPU 시간이나 사용 가능성을 보장하지 않는다. 비공개 회사/고객 데이터를 올리지 않는다.

최신 도구 연결에는 [Hugging Face LLM Course 개편 안내](https://huggingface.co/blog/llm-course)의
2025년 이후 tokenizer/Transformers 자료를 선택 참고한다. smol-course는 Python·ML·PyTorch·
Transformer 기반 이후에 사용하며 인증서·클라우드 job·모델 공개가 우리 학습의 필수 조건은 아니다.
[fast.ai 공식 학습 포럼](https://forums.fast.ai/c/p1v5/54)은 질문·top-down 직관 참고로 사용할 수 있지만
Part 1은 2022 과정이다. 2026년 댓글이 있다고 오래된 notebook 환경을 주 실습에 강제하지 않는다.
커뮤니티 글은 경험담이지 전체 합의가 아니며 기술 주장은 공식 문서·원 논문과 대조한다.
