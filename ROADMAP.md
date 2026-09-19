# LLM Research Engineer Roadmap

이 문서는 상세한 진도표가 아니라 **장기 공부 방향을 잃지 않기 위한 참고 지도**입니다. 역량별 목표 깊이, 선수 관계, 현재 강의자료의 충족도와 보완 기준은 [`CURRICULUM.md`](./CURRICULUM.md)에서 관리합니다. 현재 학습 범위와 다음 행동은 [`STATE.md`](./STATE.md)만 정합니다.

```text
수학과 Tensor
-> 머신러닝 기본과 실험
-> PyTorch와 딥러닝
-> RNN·LSTM Sequence Modeling
-> Transformer와 Language Modeling
-> LLM Systems / Post-training / Evaluation
```

## 주강의 경로와 자료의 역할

목표는 **1년 내 ML Engineer 취업**이며, 고전 ML을 제대로 다진 뒤 그 위에 LLM과
추론 시스템을 얹습니다. 기초를 건너뛰지 않는 것이 이 경로의 설계 원칙입니다.
현재 위치는 `STATE.md`를 따르며, 이 경로가 다른 과정으로 자동 전환할 권한은
아닙니다.

```text
P0 기초 수학·통계 완성
-> P1 고전 ML 제대로
-> P2 딥러닝과 PyTorch 숙련
-> P3 NLP와 Transformer
-> P4 LLM 직접 구현과 시스템
-> P5 포트폴리오와 면접
```

이번 경로에서 뺀 자료는 [`DEFERRED.md`](./DEFERRED.md)에 복귀 조건과 함께
있습니다. 조건이 실제로 발생하면 필요한 범위만 꺼내고 사용자 승인 뒤에
`STATE.md`를 바꿉니다.

### 참고한 공개 커리큘럼과 반영 내용

개발 경력은 있지만 AI는 입문인 사람을 위해 널리 쓰이는 커리큘럼을 확인하고
세 가지를 반영했습니다. 확인 시점은 2026-09-19입니다.

| 커리큘럼 | 성격 | 이 경로에 반영한 것 |
|---|---|---|
| [fast.ai Practical Deep Learning for Coders](https://course.fast.ai/) | "some coding experience"를 가진 사람 대상, **top-down**. 동작하는 state-of-the-art 모델을 먼저 쓰게 하고 점차 내부로 파고든다. 9강 | `P0`에 편성. 아래 설명 참고 |
| [Made With ML](https://madewithml.com/) | Design·Data·Model·Development·Utilities·Testing·Reproducibility·Production 8개 절. MLOps, 테스트, 배포, 모니터링, CI/CD | `P1`에 편성. Kaggle 프로젝트를 배포 가능한 형태로 만드는 데 사용 |
| [Full Stack Deep Learning](https://fullstackdeeplearning.com/course/) | 학습 troubleshooting, 데이터 관리, 배포·모니터링, foundation model. 2022판 + 2023 LLM Bootcamp | `P5`의 ML 시스템 설계 면접 준비에 사용 |
| [roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer) | 직무 구분 참고 | AI Engineer(사전학습 모델 활용)와 ML Engineer(모델 제작)를 구분한다. 이 경로의 목표는 후자다 |

**top-down을 앞에 넣은 이유.** 현재 경로는 수학 → 고전 ML → 딥러닝 순의
bottom-up입니다. 기초를 놓치지 않겠다는 목표에는 맞지만, 그것만 하면 처음으로
동작하는 결과물을 보기까지 몇 달이 걸립니다. 개발 경력자를 대상으로 설계된
커리큘럼은 예외 없이 반대로 시작합니다. 그래서 `P0`에서 fast.ai Part 1을 먼저
돌려 전체 그림과 배포까지 한 번 경험한 뒤, 같은 `P0` 안에서 Karpathy로 내부를
뜯습니다. bottom-up을 대체하는 것이 아니라 **앞에 짧게 붙이는** 구성입니다.

**프로덕션을 넣은 이유.** ML Engineer 면접에는 ML 시스템 설계가 나오고, 모델
학습만으로는 답할 수 없습니다. 이전 계획에는 배포·테스트·모니터링·CI/CD가
한 줄도 없었습니다. Made With ML을 `P1`의 Kaggle 프로젝트에 붙여 "학습한 모델"이
아니라 "운영 가능한 시스템"을 산출물로 남깁니다.

**판본 주의.** fast.ai 현행 Part 1은 2022년, Full Stack Deep Learning 무료 자료는
2022년(LLM Bootcamp 2023) 기준입니다. 도구와 API는 낡았을 수 있으므로 구체적인
라이브러리 사용법이 아니라 구성과 판단 기준을 가져옵니다. 최신 구현은 `P2`
이후의 공식 과정과 공식 문서를 따릅니다. Made With ML은 현행입니다.

### 시간 예산의 근거

학습자가 하루 12시간을 계획하지만, 예산은 **주 60시간(실효)** 기준으로 잡습니다.
12시간 중 깊은 기술 학습으로 실제 전환되는 시간은 그보다 적고, 그 차이를 계획에
미리 넣어 두어야 미달이 곧 붕괴가 되지 않습니다. 초과 달성분은 버퍼입니다.

Phase별 시간의 합은 3,120시간(52주분)입니다. 48주 × 60시간 = 2,880시간이 그보다
작으므로, 이 계획에는 애초에 버퍼가 없습니다. "48주 계획에 52주가 든다"고
정직하게 두거나, Phase 시간을 실제로 줄여야 합니다. 이 문서는 후자를 택해
아래 배분표에서 각 Phase 시간을 재조정했습니다.

날짜는 마감이 아니라 **예산**입니다. 크게 밀리면 실력이 아니라 범위가 틀렸거나
공부 외 작업이 시간을 먹고 있다는 신호로 읽습니다. 어떤 Phase도 자동으로 다음
Phase를 선택하지 않습니다.

| Phase | 예산 | 시간 | 범위 |
|---|---|---:|---|
| `P0` 전체 경험 + 기초 | ~2026-11-08 | ~420h | **fast.ai Part 1**(top-down으로 동작하는 모델을 먼저 만든다), Karpathy makemore 마무리(Part 2 E01~E03, Part 3, Part 4), Stat110 연속분포·기댓값·MLE, OpenIntro Statistics 신뢰구간·bootstrap·가설검정 |
| `P1` 고전 ML + 프로덕션 | ~2027-01-10 | ~540h | CS229 완주(공개 강의·notes·problem set. 아래 자료 표 참고), numpy 빈 파일 재구현, Kaggle end-to-end 프로젝트 1개, **Made With ML로 그 프로젝트를 배포·테스트·모니터링까지** |
| `P2` 딥러닝·PyTorch | ~2027-02-21 | ~380h | CS231n **선별 수강**(CNN·최적화·학습 진단까지. detection·segmentation·생성모델 제외), PyTorch 숙련, Karpathy "Let's build GPT"와 Tokenizer |
| `P3` NLP·Transformer | ~2027-04-18 | ~480h | CS224N A1~A4 전부(written·수학·프로그래밍) |
| `P4` LLM 구현·시스템 | ~2027-07-04 | ~640h | 시스템 기초(메모리 계층·GPU 실행 모델), CS336 A1 Basics, CS336 A2 Systems |
| `P5` 포트폴리오·면접 | ~2027-09-19 | ~660h(학습 340h + 취업활동 320h) | 추론 최적화 프로젝트, 논문 재현, **ML 시스템 설계**, 지원·코딩테스트·면접. 취업 활동은 학습 시간이 아니다 |

합계 3,120h는 그대로 두고 배분을 조정했습니다. `P0`~`P4`는 15%씩 줄이고,
그 여유를 지원 활동이 실제로 몰리는 `P5`에 더했습니다. `P1`이 여전히 학습
시간 기준 가장 긴 단일 구간입니다. ML Engineer 면접의 개념 질문은 대부분
여기서 나오고, 나중에 보충하기 가장 어려운 부분이기도 합니다. 지원은 `P5`를
기다리지 않고 `P4` 후반부터 병행하며, 그 활동은 `P4`가 아니라 `P5`의 취업활동
시간에 잡습니다.

### Phase 내부 시간 배분

각 Phase 안에서 활동별 비중의 기준입니다. 새 추적 시스템을 만들지 않고
전환 점검에서 실제 시간과 비교하는 참고선으로만 씁니다.

| 구분 | 비중 | 내용 |
|---|---:|---|
| 주과정·과제 | 55~65% | 그 Phase의 표에 적힌 강의·과제 |
| 프로젝트 | 15~20% | Kaggle, 배포, 자기 구현 모델 등 그 Phase의 산출물 |
| 복습·재구현 | 10% | 무보조 설명 준비, 빈 파일 재구현, deep-ml |
| 논문 | 5% | 그 Phase의 논문 편수 |
| 버퍼 | 5~10% | 막힌 디버깅, 재시도, 예상 밖 보충 |

`P1`처럼 프로젝트가 산출물의 핵심인 Phase는 프로젝트 비중을 위쪽으로,
`P3`처럼 과제 자체가 무거운 Phase는 주과정 비중을 위쪽으로 씁니다.

### 직무 사다리와 최종 목표

최종 목표는 **대기업 LLM Research Engineer**입니다. 아래는 그 목표를 유지하되
1년 안에 실제로 지원 가능한 지점부터 밟아 올라가는 경로이며, 저자의 판단이지
채용 공고의 인용이 아닙니다. 지원 시점에 실제 공고의 요구사항으로 다시
확인해야 합니다.

| 단계 | 직무 | 진입 가능 시점 | 이 경로가 제공하는 근거 |
|---|---|---|---|
| 1 | ML Engineer / AI Engineer (주니어) | `P3` 후반 | 고전 ML 유도, 학습 파이프라인, 배포·테스트·모니터링까지 갖춘 프로젝트 |
| 2 | LLM Application Engineer | `P3`~`P4` | Transformer 직접 구현, tokenizer, fine-tuning 이해 |
| 3 | **LLM Systems / Inference Engineer** | `P4`~`P5` | 자기 구현 LM, Triton kernel, KV cache·batching·quantization 측정 |
| 4 | LLM Research Engineer | `P5` 이후, 재직 병행 | 논문 재현, 실험 설계, OSS 기여 |

**3단계가 이 경로의 전략적 핵심입니다.** 추론 최적화는 수요 대비 인력이 적고,
Research Scientist와 달리 Research Engineer 계열은 학위보다 실제 구현·측정
능력을 봅니다. 4단계로 가는 가장 현실적인 문은 논문 실적이 아니라 **희소한
시스템 역량 + 논문 재현 능력**입니다.

1년 안에 4단계에 바로 닿는 것은 현실적이지 않습니다. AI 입문에서 시작해
12개월이면 1~2단계 지원이 현실적인 목표이고, 3단계는 `P4`·`P5`의 산출물
품질에 달려 있습니다. 취업 후에도 `DEFERRED.md`의 2순위 트랙과 논문 트랙을
이어가는 것을 전제로 설계했습니다. 단계를 건너뛰어 지원하는 것은 자유지만,
낮은 단계를 **포기**로 기록하지 않습니다.

### 실전 competition 트랙

구현·실전 중심을 유지하기 위해 Phase마다 competition을 한 번씩 체험합니다.
순위가 목적이 아니라 **정해진 데이터와 평가지표 아래에서 baseline을 세우고
개선을 측정하는 경험**이 목적입니다.

| Phase | 수준 | 추천 근거 — 이걸 이미 보였을 때 제안한다 | 기간 |
|---|---|---|---|
| `P0` | Getting Started (Titanic·House Prices 급) | 데이터 준비부터 예측·제출까지 한 번 통과. 점수는 무시 | 2~3일 |
| `P1` | Playground Series 또는 tabular 정식 대회 1개 | **누수 없는 검증 분할과 baseline 비교를 직접 수행**했을 때. `P1` 산출물 | 3~4주 |
| `P2` | 이미지 분류 대회 | **전이학습과 과적합 진단을 직접 수행**했을 때 | 1~2주 |
| `P3` | NLP 대회 | **토큰화·평가·오류 분석을 직접 수행**했을 때 | 1~2주 |
| `P4` | 없음 | CS336가 무겁다. 대신 자기 구현 모델의 추론 벤치마크 | — |
| `P5` | 없음 | 면접 준비와 지원에 집중 | — |

추천 근거는 **별도 입장시험이 아닙니다.** 그 Phase의 공식 실습에서 이미 보여
준 결과를 근거로 씁니다. 근거가 아직 없으면 대회를 제안하지 않고 무엇이
비었는지 말합니다. 근거가 확인되면 그때 실제로 열려 있는 대회 중에서
**데이터 규모·필요 연산량·남은 기간·이번 학습 목적**에 맞는 후보를
제안합니다. 연산량 판단에는 현재 GPU 가용성(아래 하드웨어 절)을 함께 봅니다.

대회 목록과 난이도는 수시로 바뀌므로 이 문서에 특정 대회를 고정하지 않습니다.
해당 Phase에 도달했을 때 [Kaggle Competitions](https://www.kaggle.com/competitions)에서
실제로 열려 있는 것을 확인하고 고릅니다. 마감·상금·데이터 라이선스를 먼저
읽습니다. 순위 정체를 학습 실패로 기록하지 않으며, 기간을 넘기면 중단하고
그때까지의 결과를 해석해 남깁니다.

`P1` 프로젝트를 배포할 때는 **"누가 어떤 입력으로 이 모델을 사용하는가"를 한
문장으로 먼저 적습니다.** 그 문장이 없으면 무엇을 테스트하고 무엇을 모니터링할지
정할 수 없어서 Made With ML의 절차가 형식만 남습니다. 그 문장에서 입력 스키마와
허용 범위(테스트할 것), 입력 분포와 응답 지연(모니터링할 것), 실패 시 동작이
따라 나옵니다.

### 논문 읽기 트랙

Research Engineer의 실질적 입장권은 학위가 아니라 **논문을 읽고, 주장을
검증하고, 재현하는 능력**입니다. 빈 파일 구현 트랙과 마찬가지로 상시입니다.

읽는 방법은 [S. Keshav, "How to Read a Paper"](https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf)의
3-pass를 기본으로 합니다. 1회독은 제목·초록·결론과 그림으로 무엇을 주장하는지,
2회독은 그림·표와 방법으로 어떻게 보였는지, 3회독은 가정을 의심하며 직접
재구성합니다.

| Phase | 편수 | 대상 | 산출 |
|---|---:|---|---|
| `P1` | 월 1편 | 고전 ML·최적화 (Dropout, Batch Normalization, Adam 급) | 한 문단 요약: 주장·근거·한계 |
| `P2` | 월 1~2편 | 아키텍처·학습 기법 | 3회독 1편, 핵심 수식 직접 유도 |
| `P3` | 월 2편 | Attention Is All You Need, BERT, GPT 계열. CS224N 지정 논문 포함 | 논문의 구조를 빈 파일에서 구현 |
| `P4` | 월 2편 | FlashAttention, PagedAttention, quantization | 논문의 측정을 자기 구현으로 재현 시도 |
| `P5` | 1편 집중 | 자유 선택 | **재현 보고서 1편.** 성공·실패·차이의 원인을 모두 기록 |

`P5`의 재현 보고서가 4단계 직무 지원의 핵심 근거입니다. 재현 실패도 원인을
규명했다면 유효한 산출물이며, 실패를 성공으로 바꿔 기록하지 않습니다.
논문 요약은 학습자가 직접 쓰고, Agent는 오독을 지적하는 역할만 합니다.

### Phase별 자료

`SRC-KBM-*`와 `SRC-HARV-STAT110-*`는 보유 자료이며 `CURRICULUM.md` registry에
등록돼 있습니다. `SRC-KAM-*`와 `SRC-KDL-*`는 주제 대조용으로만 두고 주자료로
쓰지 않으므로, `P1`·`P2`는 CS229와 CS231n을 확보해 진행합니다.

| Phase | 주자료 | 역할 |
|---|---|---|
| `P0` | [fast.ai Practical Deep Learning for Coders](https://course.fast.ai/), [Karpathy — Zero to Hero](https://karpathy.ai/zero-to-hero.html), `SRC-HARV-STAT110-2E-00-01`, [OpenIntro Statistics](https://www.openintro.org/book/os/) | fast.ai로 전체 그림과 동작하는 결과물을 먼저 만들고, Karpathy로 내부를 뜯고, Stat110으로 확률을, **OpenIntro Statistics 5~7장으로 신뢰구간·bootstrap·가설검정을** 메움 |
| `P1` | CS229 공개 강의·자료(아래 참고), [Made With ML](https://madewithml.com/) | CS229는 유도와 problem set, Made With ML은 design·testing·CI/CD·monitoring. `SRC-KAM-*`는 주제 대조에만 사용 |
| `P2` | [CS231n](https://cs231n.stanford.edu/), [PyTorch Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) | PyTorch 숙련도는 CS336 공식 선수 조건. `SRC-KDL-*`는 주제 대조에만 사용 |
| `P3` | [CS224N Spring 2024](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html) | CS336이 명시한 선수 배경 중 하나 |
| `P4` | [CS336 Spring 2026](https://cs336.stanford.edu/) A1, A2 | A2가 1순위 전문화 `TR-SYS-03`·`TR-SYS-04`의 본체 |
| `P5` | 자기 구현 모델 위의 직접 실험, [Full Stack Deep Learning](https://fullstackdeeplearning.com/course/) | baseline·통제 비교·ablation·한계 보고와 ML 시스템 설계 면접 준비 |

### Karpathy 수행 강의

| 순서 | 강의 | 공개 영상 | 공식 구현 자료 | Phase |
|---|---|---|---|---|
| 1 | micrograd | [영상](https://www.youtube.com/watch?v=VMj-3S1tku0) | [노트북](https://github.com/karpathy/nn-zero-to-hero/tree/master/lectures/micrograd) | 완료 |
| 2 | makemore: Bigram | [영상](https://www.youtube.com/watch?v=PaCmpygFfXo) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part1_bigrams.ipynb) | 완료 |
| 3 | makemore Part 2: MLP | [영상](https://www.youtube.com/watch?v=TCH_1BHY58I) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part2_mlp.ipynb) | `P0` 진행 중 |
| 4 | makemore Part 3: Activations, Gradients, BatchNorm | [영상](https://www.youtube.com/watch?v=P6sfmUTpUmc) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part3_bn.ipynb) | `P0` |
| 5 | makemore Part 4: Becoming a Backprop Ninja | [영상](https://www.youtube.com/watch?v=q8SA3rM6ckI) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part4_backprop.ipynb) | `P0` |
| 6 | Let's build GPT from scratch | [영상](https://www.youtube.com/watch?v=kCc8FmEb1nY) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/ng-video-lecture) | `P2` |
| 7 | Let's build the GPT Tokenizer | [영상](https://www.youtube.com/watch?v=zduSFxRajkE) | [minbpe](https://github.com/karpathy/minbpe) | `P2` |

Part 4는 MLP 전체 backward를 손으로 씁니다. `P4`에서 Triton kernel을 쓰려면
backward를 손으로 쓸 수 있어야 하므로 systems 트랙의 직접 선수입니다.
makemore Part 5(WaveNet)는 뺐고 복귀 조건은 `DEFERRED.md`에 있습니다.
[Let's reproduce GPT-2 (124M)](https://www.youtube.com/watch?v=l8pRSuU81PU)은
`P4` 진입 전 **Optional**입니다.

### 중간 점검

점검은 두 종류이며 새 추적 시스템을 만들지 않습니다. 결과는 대화로 보고하고,
재개 지점이 바뀌었을 때만 `STATE.md`를 교체합니다.

**주간 점검 (10분).** Phase 예산 대비 실제 진도, 지난주 개념 3개 무보조 구술,
빈 파일 재구현·deep-ml·논문이 실제로 돌고 있는지. 밀렸으면 실력이 아니라
범위나 시간 배분을 의심합니다.

**Phase 전환 점검.** Phase가 끝났다고 생각될 때 아래를 모두 확인합니다.
하나라도 비면 Phase를 닫지 않고, 무엇이 비었는지 그대로 보고합니다.

| 항목 | 확인 내용 |
|---|---|
| 산출물 | 그 Phase의 산출물이 실제로 존재하고 재현 가능한가 |
| 무보조 설명 | Phase 전체를 노트 없이 설명했는가 |
| 빈 파일 재구현 | 해당 Phase 목록을 도움 없이 완주했는가 |
| 논문 | 편수와 산출 형태를 채웠는가 |
| 시간 | 예산 대비 실제. 초과분이 다음 Phase에 미치는 영향 |
| **직무** | 아래 참조 |
| 범위 | 다음 Phase의 범위를 그대로 갈지, 줄일지, `DEFERRED.md`에서 꺼낼지 |

점검이 끝나면 Agent가 `STATE.md` 전체 교체안을 먼저 보여 줍니다. 닫히는 Phase,
그 근거, 다음에 열리는 범위가 그 안에 들어갑니다. **자동으로 쓰이지 않으며
승인해야 반영됩니다.**

**직무 점검이 이 점검의 핵심입니다.** Phase가 끝날 때마다 다음을 같이 봅니다.

1. 직무 사다리에서 지금 어느 단계에 해당하는가
2. **지금 당장 찔러볼 수 있는 공고는 무엇인가** — 합격 가능성이 아니라
   지원 자격을 충족하는지 기준
3. 실제 공고 3~5건을 직접 열어 요구사항과 현재 산출물을 대조한다
4. 공고가 요구하는데 이 경로에 없는 항목이 있으면 그 자리에서 기록한다
5. 다음 단계로 가기 위해 가장 부족한 한 가지

Agent는 어떤 종류의 공고를 볼지와 무엇을 대조할지를 제안하고, 공고 자체는
학습자가 엽니다. Agent는 특정 회사의 채용 여부, 요구 학위, 연봉, 공고 존재를
확인 없이 진술하지 않습니다. 사다리의 단계 구분은 저자의 판단이므로 실제
공고와 어긋나면 **공고가 맞고 사다리가 틀린 것**으로 처리하고 사다리를
고칩니다.

찔러보는 것은 이릅니다. 1단계 공고는 `P3` 후반이 아니라 **`P2` 끝에 한 번
지원해 보는 편이 낫습니다.** 떨어져도 그 과정에서 얻는 요구사항 정보가
다음 Phase의 범위를 조정해 주기 때문입니다. 불합격을 학습 실패로 기록하지
않습니다.

### 하드웨어 전제와 결정 시점

2026-09-19 기준 학습 환경에 **NVIDIA GPU가 없습니다.** `nvidia-smi`가 없고
`torch.cuda.is_available()`이 `False`입니다. 설치된 torch는 CUDA 빌드지만
CPU로만 실행됩니다.

| Phase | GPU 필요도 | 판단 |
|---|---|---|
| `P0` | 불필요 | fast.ai는 클라우드 노트북으로 진행 가능. makemore는 CPU로 충분 |
| `P1` | 거의 불필요 | 고전 ML과 tabular 대회는 CPU로 된다 |
| `P2` | 있으면 좋음 | CNN 학습과 이미지 대회. 무료 클라우드 노트북으로 가능 |
| `P3` | 있으면 좋음 | CS224N 과제 일부. 무료 클라우드 노트북으로 가능 |
| `P4` | **필수** | CS336 A2는 Triton kernel과 다중 GPU 분산 학습을 요구한다. NVIDIA GPU 없이는 수행 불가 |
| `P5` | **필수** | latency·throughput·메모리 측정에 실제 가속기가 필요하다 |

`P4`·`P5`가 직무 사다리 3단계의 근거를 만드는 구간이므로, GPU 확보는 선택이
아니라 경로의 전제입니다. 다만 `P0`·`P1` 약 16주(420h+540h=960h) 동안은 막히지 않으므로
**지금 시작하는 데는 장애가 없습니다.**

결정 시점을 두 개로 나눕니다.

- **`P1`이 끝나고 `P2`가 시작되기 전(~2027-01-10)**: 무료·저가 클라우드
  노트북 환경을 하나 정해 실제로 학습이 도는지 확인한다. 이 시점에는 단일
  GPU면 충분하다.
- **`P3`이 끝나고 `P4`가 시작되기 전(~2027-04-18)**: 다중 GPU를 쓸 수 있는
  유료 수단을 확보한다.
  CS336 A2의 분산 학습 과제는 단일 GPU로 대체되지 않는다.

후보는 무료 클라우드 노트북(Kaggle·Colab), 유료 구독, 시간당 과금 GPU 대여,
로컬 GPU 구매입니다. 무료 할당량·가격·사용 가능 GPU는 수시로 바뀌므로 이
문서에 고정하지 않고 결정 시점에 직접 확인합니다. `P4` 이전에 확보하지
못하면 `P4`·`P5`를 미완료로 두고 `DEFERRED.md`로 옮깁니다. 대체 과제로
완료 처리하지 않습니다.

### CS229 접근성

[cs229.stanford.edu](https://cs229.stanford.edu/)의 강의 자료 링크 상당수는
Stanford 계정 로그인이 필요합니다. 문제 세트 원문에 접근하지 못하면 "CS229
완주"가 실행 불가능한 목표가 되므로 아래로 범위를 확정합니다.

- **강의 영상**: [2018 Autumn, Andrew Ng](https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU) — 로그인 없이 공개
- **강의 노트**: [cs229.stanford.edu/main_notes.pdf](https://cs229.stanford.edu/main_notes.pdf) — 로그인 없이 공개, supervised learning·generalized linear model·generative learning·SVM·학습이론까지 포함
- **문제 세트**: 위 두 자료로 다루는 각 주제마다 numpy 빈 파일 재구현으로 대체한다.
  공식 problem set 원문을 확보하지 못하는 한 "problem set을 푼다"를 완료
  기준으로 쓰지 않는다

CS229 공식 선수 조건은 "다변수 미적분·선형대수를 MATH51 수준, 확률을 CS109
수준"입니다. `P0`의 기초수학·Stat110이 이를 담당하며, `P1` 진입 전 재확인
대상입니다.

### 빈 파일 구현 트랙

공식 exercises는 대부분 강의를 따라가거나 TODO를 채우는 형태입니다. 그것만으로는
**아무것도 없는 파일에서 시작하는 능력**이 생기지 않고, 면접의 실기는 정확히 그
형태입니다. 그래서 이 트랙은 특정 Phase가 아니라 **모든 Phase에 상시로** 붙습니다.

개념은 기억으로 써 보고 코드는 빈 파일에서 다시 짜는 것이 같은 원리의 양쪽입니다.
`AGENTS.md`의 무보조 검증 규칙과 짝을 이룹니다.

| 방식 | 언제 | 내용 |
|---|---|---|
| **재구현** | 모듈이 끝날 때마다 | 강의·노트북·노트를 전부 닫고 빈 파일에서 같은 것을 다시 구현한다. 막히는 지점이 실제로 이해하지 못한 지점이다 |
| **deep-ml 챌린지** | 주 3~5문제, 상시 | [Deep-ML](https://www.deep-ml.com/)의 from-scratch 구현 문제. 이미 `challenges/deep-ml/`에 환경이 있다 |
| **시간 제한 구현** | `P2`부터 간헐적, `P5`에 집중 | 45~60분 제한을 걸고 지정 구현을 완성한다. 면접 조건 |
| **알고리즘 코딩 테스트** | `P4` 후반부터 상시 | ML Engineer 채용의 1차 관문. 마지막에 몰아서 하지 않는다 |

Phase별 재구현 대상입니다. 목록을 늘리기보다 **참고 없이 되는지**가 기준입니다.

| Phase | 빈 파일에서 다시 짜는 것 |
|---|---|
| `P0` | micrograd의 `Value`와 backward, makemore bigram 카운트 모델, MLP 문자 언어모델 전체 |
| `P1` | 경사하강 로지스틱 회귀, 선형회귀 정규방정식과 규제, k-means, PCA, 의사결정트리 분할, k-fold 교차검증 루프 — 전부 numpy |
| `P2` | MLP와 학습 루프, backprop 수기 구현, 작은 CNN, scaled dot-product attention |
| `P3` | Transformer block(멀티헤드·residual·LayerNorm·FFN), positional encoding, beam search |
| `P4` | BPE tokenizer, causal mask와 KV cache. CS336 과제 자체가 빈 파일 구현이다 |
| `P5` | 위 항목 중 무작위 선택 + 시간 제한 |

재구현은 새 학습이 아니라 검증입니다. 별도 Phase 시간을 잡지 않고 각 Phase 예산
안에서 소화하며, 통과하지 못한 항목은 완료로 기록하지 않습니다. Agent는 재구현
중에 코드를 제공하지 않고, 끝난 뒤 원본과의 차이만 지적합니다.

### 이 경로가 지키는 선수 조건

CS336 공식 선수 조건은 "strong familiarity with PyTorch", "basic systems
concepts like the memory hierarchy", "comfort with the basics of machine
learning and deep learning"(CS221·CS229·CS230·CS124·CS224N 중 하나)입니다.
`P1`이 CS229를, `P2`가 PyTorch 숙련을, `P3`가 CS224N을, `P4` 도입부가 시스템
기초를 각각 담당합니다. 이 순서를 앞당기지 않습니다.

### 산출물

각 Phase는 이력서에 쓸 수 있는 산출물을 하나씩 남깁니다. 강의 수강 자체는
산출물이 아닙니다.

| Phase | 산출물 |
|---|---|
| `P0` | fast.ai로 배포한 동작하는 모델 하나, makemore MLP 구현과 초기화·학습 실험 보고 |
| `P1` | Kaggle 프로젝트를 테스트·CI·모니터링까지 갖춘 배포 가능한 형태로. **누가 어떤 입력으로 쓰는지를 먼저 한 문장으로 적고 시작한다.** numpy 빈 파일 구현 모음 |
| `P2` | 소규모 DL 프로젝트와 처음부터 구현한 GPT·BPE |
| `P3` | CS224N A1~A4 |
| `P4` | 자기 구현 Transformer LM과 FlashAttention2 Triton kernel |
| `P5` | 추론 최적화 프로젝트: latency·throughput·메모리 측정과 개선 보고. 논문 재현 보고서 1편. 시간 제한 재구현 통과 기록 |

공식 저장소의 완성 노트북은 참고 자료입니다. 강의 속 전체 구현을 수행하고
별도 exercises도 직접 시도합니다. 영상·문서·공식 자료 기반 대화를 허용하며,
설명 매체를 바꾸어도 공식 내용과 실습을 축소하지 않습니다. 완성 노트북 실행이나
AI 보충 예제로 공식 실습을 대체하지 않습니다. 접근·실행 제약은 명시하고 해당 실습은 미완료로
남깁니다. Optional·Bonus는 선택 항목으로 표시합니다.

CS336 assignment는 공식 AI 정책을 엄격히 따르며 제약은 `AGENTS.md`에 있습니다.
CS224N 공식 AI 정책도 수행 시점에 그대로 적용됩니다. KANT는 진도·주제 대조용이며
기본 실습이나 완료 기준으로 사용하지 않습니다.


## 전문화 우선순위

현재의 1순위 전문화 방향은 **LLM Systems와 Inference Optimization**입니다. latency, throughput, memory, batching, KV cache와 quantization을 실제 측정·구현·디버깅하는 역량을 우선합니다.

2순위는 **Post-training과 LLM Evaluation**입니다. SFT·LoRA·preference optimization을 평가 설계, failure analysis, contamination 점검과 연결합니다.

Modeling과 Computer Vision은 별도 주력 트랙이 아니라 위 전문화를 이해하거나 검증하는 데 필요한 선수개념·연결 학습으로 다룹니다. 이 우선순위는 공통 핵심의 선수 관계를 건너뛴다는 뜻이 아닙니다. 필요한 prerequisite가 확인되면 현재 범위 안에서 보충을 제안하고 사용자 승인 뒤에만 `STATE.md`의 다음 행동을 바꿉니다.

## 정적 목표 endpoint

아래 표는 전문화 방향의 도착점을 고정할 뿐, 완료 여부나 현재 진도를 기록하거나 다음 목표를 자동으로 선택하지 않습니다. Pilot 중 실제 다음 목표는 `STATE.md`에 사용자가 승인한 내용만 사용합니다.

| 우선순위 | 단계 | 방향 | Endpoint |
|---:|---:|---|---|
| 1 | `1A` | Systems·Inference | `TR-SYS-03` |
| 1 | `1B` | Systems·Inference | `TR-SYS-04` |
| 2 | `2A` | Post-training·Evaluation | `TR-MOD-03` |
| 2 | `2B` | Post-training·Evaluation | `TR-EVAL-02` |
| 2 | `2C` | Post-training·Evaluation | `TR-EVAL-05` |

Modeling과 Computer Vision은 이 endpoint에 필요한 선수개념 또는 연결 학습으로만 선택합니다.

## 1. 수학과 Tensor

- 선형대수, 미분, 확률
- Tensor shape, broadcasting
- softmax, cross entropy, gradient

## 2. 머신러닝 기본과 실험

- train/validation/test와 data leakage
- loss, metric, generalization
- baseline과 error analysis
- 필요할 때 Kaggle 프로젝트 하나

## 3. PyTorch와 딥러닝

- forward, backward, optimizer
- 학습 루프와 디버깅
- normalization과 regularization
- RNN recurrence·unroll과 LSTM state·gate를 직접 구현하고 실제 sequence task에서 비교

## 4. Transformer와 Language Modeling

- `CC-SEQ-01`은 sequence 개념의 참고 역량이며, 전체 구현 완료를 일률적인 진입 조건으로 삼지 않음
- tokenization과 embedding
- attention과 Transformer block
- autoregressive training과 generation

## 5. 전문 분야

- LLM Systems: latency, throughput, memory, batching, KV cache
- Post-training: SFT, LoRA, preference optimization
- Evaluation: metric, failure analysis, contamination

누적 구현 골격과 module별 assignment·주요 phase capstone은 `CURRICULUM.md`의 정적 catalog가 관리합니다. 이 catalog와 ROADMAP endpoint는 진도나 mastery를 기록하지 않습니다.

TIL, `knowledge/`, 실제 실습 결과는 설명 수준과 보충 필요성을 판단하는 참고 근거입니다. 현재 source나 과제가 끝나면 Agent는 다음 선택지를 제안하고, 사용자가 승인한 뒤에만 `STATE.md`를 교체합니다. 어떤 기록도 새 강의나 추가 실습을 자동으로 선택하지 않습니다.
