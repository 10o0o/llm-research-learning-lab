# 따라갈 강의와 참고 자료

주요 공식 자료와 목차 확인: **2026-10-26**.
여기는 추천 자료 목록이다. 실제 선택·시청 위치·외부 실습 레포는 [STATE](STATE.md)에만 기록한다.
한 번에 주자료 하나를 따라가고, 보충 자료는 현재 막힌 부분에 필요할 때만 연다.

## 먼저 고를 주자료

| 목적 | 추천 자료 | 시작 위치와 사용 방법 |
|---|---|---|
| AX/LLM 애플리케이션 | [LLM Zoomcamp 2026](https://github.com/DataTalksClub/llm-zoomcamp) | Module 1의 공식 안내부터. 실습 코드는 자신의 외부 레포에 작성한다. |
| 신경망·언어모델 기반 | [Karpathy Zero to Hero](https://karpathy.ai/zero-to-hero.html) | 처음이면 micrograd, 이어서 공부한다면 확인된 강의 구간부터. 영상과 공식 연습을 따른다. |
| 모델 기반의 책 대안 | [Build a Large Language Model (From Scratch)](https://github.com/rasbt/LLMs-from-scratch) | 책의 장 순서를 기준으로 공부한다. 공식 코드는 참고하고, 학습 대상은 자기 파일에 구현한다. |

공식 자료 저장소와 자신의 실습 저장소를 구분한다. 과제 starter가 제공되면 그 구조를 사용하고,
직접 만들어가는 강의라면 작은 파일부터 작성한다. 자세한 연결 방법은 [외부 실습 안내](docs/external-practice.md)에 있다.

## AX: LLM Zoomcamp

[공식 목차](https://github.com/DataTalksClub/llm-zoomcamp#syllabus) ·
[공식 영상 목록](https://www.youtube.com/playlist?list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv) ·
[프로젝트 안내](https://datatalks.club/docs/courses/llm-zoomcamp/project/)

### 첫 진입: Module 1의 작은 흐름부터

[Module 1 안내](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/01-agentic-rag)의 공식 순서를 따른다.
자료·설치·RAG 개념을 확인한 뒤 검색→프롬프트→모델 응답을 연결하고, 이후 재사용과 agent로 확장한다.

| 공식 구간 | 바로가기 | 여기서 익히는 것 |
|---|---|---|
| 1–4: 소개·환경·RAG·데이터 | [첫 안내](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/01-intro.md) | 무엇을 만들고 어떤 데이터와 환경을 쓰는지 |
| 5–7: Search → Prompt → LLM | [검색](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/05-search.md) · [프롬프트](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/06-building-prompt.md) · [연결](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/07-llm.md) | 검색한 근거를 모델 입력과 응답에 연결하기 |
| 8–10: 재사용·저장·정리 | [RAG Helper](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/08-rag-helper.md) | 앞에서 만든 흐름을 재사용하는 구조 |
| 11–16: Agent와 도구 사용 | [Agent 소개](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/11-agents-intro.md) · [Function Calling](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/13-function-calling.md) · [Agent Loop](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/14-agentic-loop.md) | 도구 호출과 반복을 이해한 뒤 framework 비교 |

이 표는 공식 단원을 찾는 안내다. 새로운 자체 과제나 모든 코드를 미리 채운 템플릿을 추가하지 않는다.
Module 1의 12번 복습 강의와 추가 검색 심화는 공식 자료에서도 선택 항목이다.

### 이후 공식 모듈

| 모듈 | 자료 | 연결되는 역량 |
|---|---|---|
| 2 | [Vector Search](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/02-vector-search) | embedding과 검색 |
| 3 | [Orchestration](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/03-orchestration) | 작업 흐름 실행·관리 |
| 4 | [Evaluation](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/04-evaluation) | 검색과 답변 품질 비교 |
| 5 | [Monitoring](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/05-monitoring) | 실제 사용과 피드백 관찰 |
| 6–7 | [Best Practices](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/06-best-practices) · [Project Example](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/07-project-example) | 검색 개선과 프로젝트 구성 참고 |

기본은 공식 순서다. 기존 추천이었던 `1 → 2 → 4 → 5`는 선별 수강을 명시적으로 선택한 경우의
후보이며 공식 전체 과정이나 수료 기준이 아니다. 현재 목적에 필요 없는 운영 스택을 추가할지는
해당 단원에서 결정한다. 실제 과제·프로젝트 기준과 환경은 선택한 판본의 원문을 확인한다.

## 모델 기반: Karpathy

[공식 목차와 영상](https://karpathy.ai/zero-to-hero.html) ·
[공식 노트북·연습 안내](https://github.com/karpathy/nn-zero-to-hero)

| 흐름 | 공식 자료 | 핵심 |
|---|---|---|
| micrograd | [영상](https://www.youtube.com/watch?v=VMj-3S1tku0) | 자동미분과 학습의 연결 |
| makemore bigram → MLP | [bigram](https://www.youtube.com/watch?v=PaCmpygFfXo) · [MLP](https://youtu.be/TCH_1BHY58I) | tensor, loss, 분할, 학습·생성 |
| Activations/Gradients → 수동 backprop | [Part 3](https://youtu.be/P6sfmUTpUmc) · [Part 4](https://youtu.be/q8SA3rM6ckI) | 초기화·BatchNorm·gradient 흐름 |
| WaveNet → GPT → Tokenizer | [WaveNet](https://youtu.be/t3YJ5hKiMQ0) · [GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) · [Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) | 모델 구조 확장과 토큰화 |

이전 micrograd·makemore 기록은 [보관 색인](archive/README.md)에서 확인한다. 과거 기록을 다시 선택할 때
실제 완료·미완료·도움 범위를 확인하고 이어간다. 이 자료 목록만 보고 기초부터 다시 시작하지 않는다.
영상 설명의 연습문제와 제공된 starter를 사용하고, 이해한 자기 코드는 이후 실습에서 재사용한다.

## 이후 전문화: 필요한 경로 하나

| 경로 | 자료와 진입 위치 | 선택할 때 확인할 것 |
|---|---|---|
| 모델 구현 심화 | [CS336 Spring 2026](https://cs336.stanford.edu/) · [A1 공식 과제](https://github.com/stanford-cs336/assignment1-basics) | Python/PyTorch·ML·수학 기반, handout, 실행 자원, AI 정책 |
| 평가·후학습 | [Hugging Face smol-course](https://github.com/huggingface/smol-course) · [현재 단원](https://github.com/huggingface/smol-course/tree/main/units/en) | SFT·평가부터, 이후 필요하면 preference alignment. 모델·데이터·메모리 조건 확인 |
| 추론·시스템 | [MIT 6.5940 Fall 2024](https://hanlab.mit.edu/courses/2024-fall-65940) | quantization, efficient LLM deployment, long context 등 현재 실험에 필요한 단원 |

CS336 전체와 두 전문화 경로를 모두 의무화하지 않는다. 작은 자체 실험과 공식 과제 완료는 구분한다.
smol-course의 예정 날짜를 공개 완료로 해석하지 않으며, 실제 존재하는 단원을 선택한다.
책·강의의 과거 환경이나 대형 GPU 기준을 자신의 환경에 그대로 적용하지 않는다.
공식 과제를 선택하면 [과정별 정책](.agents/references/official-course-policies.md)과 원문을 함께 확인한다.

## 현재 막힌 부분을 보충할 때

| 막힌 내용 | 참고 자료 | 읽을 범위 |
|---|---|---|
| PyTorch API·학습 루프 | [PyTorch Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) | 지금 쓰는 tensor·autograd·최적화 부분 |
| ML 문제 설정·일반화 | [MIT 6.036 Fall 2020](https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/) | 표현, 지도학습, 과적합·일반화의 해당 단원 |
| 행렬·벡터·저랭크 | [MIT 18.06SC Fall 2011](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) | 현재 연산에 필요한 내적·행렬곱·SVD 등 |
| 미분·gradient | [MIT 18.02SC Fall 2010](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/) | 편미분·chain rule·gradient |
| 평가의 확률·통계 | [MIT 18.05 Spring 2022](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/) | 조건부확률·기댓값·불확실성 등 현재 질문 |

이 자료들은 추가 필수 과정이 아니다. 필요한 설명을 얻으면 원래 강의·실습으로 돌아간다.
최신 API 사용법은 외부 실습 레포에 설치된 버전의 공식 문서와 대조한다.

## 학습 방식을 참고할 글

- [Giles Thomas: How I use AI](https://www.gilesthomas.com/2026/07/ai-use): 학습할 코드는 직접 쓰고 AI는 리뷰에 활용하는 경험.
- [Edd Mann의 LLM 학습 회고](https://eddmann.com/posts/weeknotes-going-deeper-on-llms-marginalia-and-agent-toolkit-skills/): 책으로 순서를 정하고 AI로 현재 내용을 이해하는 경험.
- [Andy Timm의 CS336 회고](https://andytimm.github.io/posts/cs336/cs336_review.html): AI 도움 범위를 문서화한 청강 경험과 시간·자원 조건.

개인 회고는 방법을 고르는 참고다. 동일한 학습 효과나 취업 결과를 보장하지 않는다.
허브에는 링크와 재개 위치를 남기고, 실험 설명과 실제 결과는 해당 실습 레포에 둔다.
