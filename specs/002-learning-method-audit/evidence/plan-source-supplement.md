# 계획 조사: 공식 원문 보강과 과정별 확인 범위

조회일: 2026-10-21. [초기 교육 조사](official-education-sources.md)와 [초기 재감사](initial-review.md)를 보존하고, 계획 선택에 필요한 본문만 보강했다. 아래는 공개 원문의 운영 사실과 설계 해석이며 학습 효과·취업 효과의 실험이 아니다. 실무 교육 기관은 FSDL·Made With ML·DataTalksClub의 **3곳**, 대학 강의는 MIT 6.S191·CS224N·CS336의 **3개**다. FSDL의 두 과정을 기관 두 곳으로 세지 않는다.

`확인`은 아래 구간의 공개 설명을 읽었다는 뜻이다. `부분`은 해당 관점 중 확인한 범위만 있다는 뜻이며 관점 전체 검토 완료로 집계하지 않는다. `미확인`은 정책 미기재·접근 한계·미실행이다. 공개 자습자에게 교내 채점·멘토·계정·GPU가 제공된다는 뜻은 아니다. 원문·노트북·답안의 로컬 복제, clone, 설치, 등록, 지출, 실행은 하지 않았다.

## S-01 — FSDL 2022 labs

공식 구간: [Lab Overview](https://fullstackdeeplearning.com/course/2022/lab-0-overview/)의 What are these labs for?·Architecture·Running the labs, 2022-07-25 게시. [공식 setup 안내](https://github.com/the-full-stack/fsdl-text-recognizer-2022-labs/tree/main/setup)의 Colab·Local·환경/의존성 설명도 읽었다. 이전 조직 URL은 공식 연결을 따라 현재 `the-full-stack`으로 이동했다.

| 관점 | 확인 상태와 관찰 |
| --- | --- |
| 1. 판본·단위 | 확인: 2022 손글씨 인식 시스템의 labs. 사이트 하단 2026 표시는 과정 판본이 아니다. |
| 2. 실제 활동 | 확인: 같은 시스템의 학습부터 웹앱까지 코드베이스를 누적 발전. 전체 구조 안내가 먼저 있다. 개별 lab의 학습자 미완성 부분은 미확인. |
| 3. 평가 | 부분: 초기 조사에서 테스트/진단·실험 관리 lab 연결 확인. 개인별 채점표·공식 pass 조건은 미확인. |
| 4. 피드백 | 부분: 구조 설명은 사용자 피드백에 따른 반복을 목적에 둔다. 공개 자습자의 코드 리뷰 제공은 미확인. |
| 5. 코드·공간 | 확인: 노트북 안내와 재사용 코드베이스·실행 스크립트·환경 파일을 함께 사용. 노트북 본문은 미검토. |
| 6. 도움/AI | 미확인: 읽은 안내에 구체 AI 대행 정책 없음. 완성 제공 코드의 탐색과 독립 구현을 동일시하지 않음. |
| 7. 선수 | 부분: 이 안내는 전체 선수 명세가 아니다. Linux 로컬 경로에는 NVIDIA GPU/드라이버 전제. |
| 8. 자원·비용 | 부분: Colab/Google 계정 또는 Linux/GPU 안내. 2022 무료 GPU·유료 플랜 수치의 현행성, 우리 장치 호환은 미확인. |
| 9. 공개·재사용 | 부분: 공식 공개 저장소 존재. 파일별 라이선스·데이터 권리·답안 공개 허용은 이번 구간에서 확정하지 않음. |

적용 해석: [R-01/R-04/R-05](../research.md)의 한 서비스 누적·전체 흐름 설명·준비 마찰 감소에 참고한다. 제공된 큰 구조를 먼저 복제해야 한다는 근거로 쓰지 않는다. 수업 효과나 더 빠른 학습을 입증하지 않는다.

## S-02 — FSDL Spring 2023 LLM Bootcamp

공식 구간: [askFSDL walkthrough](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/askfsdl-walkthrough/), 2023-05-09 게시, Chapter Summaries의 SWE Tooling·Data Cleaning·Embeddings & ETL. [2023 소개](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/)의 선수/질문 채널은 기존 초기 조사의 확인 범위다. 소개 전체를 이번에 다시 검증한 것으로 보고하지 않는다.

| 관점 | 확인 상태와 관찰 |
| --- | --- |
| 1. 판본·단위 | 확인: Spring 2023 LLM 앱 walkthrough. 2022 labs와 별도 과정. |
| 2. 실제 활동 | 확인: 이미 있는 Q&A 봇의 코드·자료 정리·검색·화면·관측을 설명하는 활동. 미완성 구현 과제라고 부르지 않음. |
| 3. 평가 | 미확인: 이 페이지에서 학습자 과제 채점 기준을 확인하지 못함. |
| 4. 피드백 | 부분: 초기 소개의 질문 채널. 자습자별 피드백 보장은 미확인. |
| 5. 코드·공간 | 확인: 프로젝트 저장소와 전체 흐름의 walkthrough. 소스 전체·노트북 본문 미검토. |
| 6. 도움/AI | 미확인: 제공 코드 사용과 AI 답안 대행 정책을 명시적으로 확인하지 못함. |
| 7. 선수 | 부분: 초기 소개는 Python·ML 또는 앱 개발 경험을 안내. 실제 학습자의 해당 역량은 미확인. |
| 8. 자원·비용 | 부분: 사용하는 서비스 계정이 없으면 실행하지 못할 수 있다고 명시. 현재 계정·요금·API 호환 미확인. |
| 9. 공개·재사용 | 부분: 공개 저장소 연결은 확인. 구성요소별 재배포 권리와 과제 답안 공개 권한은 확정하지 않음. |

적용 해석: [R-02/R-03](../research.md)에서 문제·전체 흐름·추상화 책임을 검토하는 비교 사례다. walkthrough 실행을 학습자 직접 구현으로 채점하거나 2023 도구를 최신 필수 기술로 가져오지 않는다.

## S-03 — Made With ML 공개 개정본

공식 구간: [Scripting](https://madewithml.com/courses/mlops/scripting/)의 Intuition·Setup·README·Scripts/Workloads, [Testing](https://madewithml.com/courses/mlops/testing/)의 Intuition·Types of tests·How/What should we test. 고정 2026 기수로 지칭하지 않는다. 환경·평가·지원 설명의 이전 확인 구간은 [초기 E-02](official-education-sources.md#e-02--made-with-ml)다.

| 관점 | 확인 상태와 관찰 |
| --- | --- |
| 1. 판본·단위 | 확인: 상시 개정 공개 MLOps 과정의 scripting/testing 절. 사이트 인용 연도와 고정 release는 다름. |
| 2. 실제 활동 | 확인: 앞 노트북 작업을 workload·함수·설정·실행 안내로 정리. 제공 스크립트가 이미 있다고 명시. |
| 3. 평가 | 부분: 코드·데이터·모델 테스트와 동작/회귀 검사를 구별. 자습자 개인 채점표는 미확인. |
| 4. 피드백 | 부분: 테스트 결과를 개발에 연결. 초기 조사의 cohort/질문 안내와 공개 자습자 리뷰 보장은 다름. |
| 5. 코드·공간 | 확인: 노트북 탐색 후 스크립트·CLI·README. 파일 수·이름을 고정하지 않음. |
| 6. 도움/AI | 부분: 제공 스크립트 존재. 구체 AI 대행 정책은 미확인. |
| 7. 선수 | 부분: 앞 단계의 코드/개념을 누적 사용. 이 두 절만으로 공식 전체 선수 요건을 확정하지 않음. |
| 8. 자원·비용 | 부분: 초기 setup의 로컬/원격·Python 3.10 안내. lab 3.14 실행·개인 비용은 미확인. |
| 9. 공개·재사용 | 부분: 공개 과정/저장소. 파일별 라이선스·데이터/모델 권리는 채택 시 확인할 범위. |

적용 해석: [R-04/R-09/R-11](../research.md)의 재사용 실행·관찰·검사 분리에 참고한다. 본문의 “stateless”를 모든 Python 코드에 상태가 없다는 사실로 일반화하지 않는다. 처음부터 전체 MLOps 구조·Ray·CI를 만들자는 권고로 옮기지 않는다.

## S-04 — DataTalksClub LLM Zoomcamp

공식 구간: [README](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/README.md)의 Prerequisites·Live/Self-Paced·Syllabus, [project.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/project.md)의 Problem statement·Documentation·Peer Reviewing/Review Tips·Evaluation Criteria·Cheating and plagiarism. 두 파일 모두 조회일의 가변 `main`; 특정 commit pin은 확보하지 않았다. [2025 cohort](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/project.md)는 초기 조사 범위로 분리한다.

| 관점 | 확인 상태와 관찰 |
| --- | --- |
| 1. 판본·단위 | 부분: 현재 README 본문에서 `2026` 문자열은 확인되지 않음. 초기 E-03의 2026 소개 관찰을 고정판 근거로 재사용하지 않음. 2025 연결·가변 main·확정 cohort는 구별. |
| 2. 실제 활동 | 확인: 자기 문제/자료의 RAG 또는 agent 앱, 평가·인터페이스·피드백. 강의용 FAQ corpus는 프로젝트에 사용 불가. |
| 3. 평가 | 확인: 문제·검색/최종 응답·실행/재현을 따로 평가. CLI/스크립트/노트북도 인정, cloud 배포는 bonus. 도구 가산점은 개인 의무로 가져오지 않음. |
| 4. 피드백 | 확인: cohort는 동료 평가, self-paced는 공식 점수/동료 평가/인증 없음. 특정 commit의 재현을 검토. |
| 5. 코드·공간 | 확인: 별도 프로젝트 repo 권고, README에 목적·실행·입출력·평가 안내. |
| 6. 도움/AI | 부분: 타인 작업·다른 과정의 자기 프로젝트 등 제출 재사용 금지, 일부 강의 코드 허용. 구체 AI 답안 대행 범위는 미확인. |
| 7. 선수 | 확인: Python·명령줄·기초 Docker, ML/LLM 선행은 필수 아님. |
| 8. 자원·비용 | 부분: 일반 PC와 API credit 비용 안내가 있음. 소개의 예상 비용은 현재 요금·개인 비용 보장이 아님. |
| 9. 공개·재사용 | 부분: 제출 공개/재사용 규칙은 확인. 데이터·모델별 권리까지 허용된 것은 아님. 독립 서비스의 버전 발전은 cohort 제출과 다른 맥락. |

적용 해석: [R-02/R-05/R-09/R-10](../research.md)의 문제 설명·재현·기여·실패 관리에 참고한다. repo 수·동료 평가 횟수·강좌 기간·dashboard 수는 개인 학습의 성공 기준으로 옮기지 않는다. 원문의 clone/reset 예시는 읽기만 했고 실행하지 않았다.

## S-05 — MIT 6.S191 2026

공식 구간: [홈페이지](https://introtodeeplearning.com/)의 Description·2026 Schedule·FAQ grading/prerequisites/license, [공식 README](https://github.com/MITDeepLearning/introtodeeplearning/blob/master/README.md)의 Instructions·Opening/Running labs·License. lab1 링크의 목록만 확인했으며 개별 `.ipynb`·solutions는 읽지 않았다.

| 관점 | 확인 상태와 관찰 |
| --- | --- |
| 1. 판본·단위 | 확인: 2026 홈페이지 및 2026을 명시한 가변 master README. 개별 lab 고정 release는 미확인. |
| 2. 실제 활동 | 확인: Python/music·얼굴 탐지·LLM fine-tuning labs, TODO 채우기와 project proposal. 개별 TODO/채점 본문은 미검토. |
| 3. 평가 | 부분: 2026 학점은 proposal 완료에 기반한 P/D/F; lab competition 제출 안내. 개별 competition 루브릭 미확인. |
| 4. 피드백 | 부분: proposal에 staff/산업 패널 피드백. 외부 자습자의 동일 접근 권한은 미확인. |
| 5. 코드·공간 | 확인: Colab 노트북·제공 편의 package·학습자 TODO. 실행 사실은 없음. |
| 6. 도움/AI | 미확인: 읽은 홈페이지/README에 구체 AI 도움 정책 없음. |
| 7. 선수 | 확인: 기초 행렬 곱·미분/chain rule 기대, Python 경험은 도움. |
| 8. 자원·비용 | 부분: Google 계정·Colab GPU runtime 안내. 현재 할당/비용·개인 장치 실행 미확인. |
| 9. 공개·재사용 | 부분: MIT license와 출처 표기 조건 명시. lab의 공식 답안을 공개할 권한으로 확대하지 않음. |

적용 해석: [R-01/R-06](../research.md)의 최소 선수·제공 도구와 직접 작업 분리에 참고한다. proposal 제출/노트북 실행을 모델 구현·일반화·공식 수료로 바꾸지 않는다. 전체 lab을 AX 선수로 추가하지 않는다.

## S-06 — CS224N Spring 2024, archive 1246

공식 구간: [1246 홈페이지](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html)의 Prerequisites·Coursework/Final Project·AI Tools Policy·Schedule. 새로 보강한 [milestone 지침](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/project/project-milestone-instructions-spr2024.pdf)은 **2024-05-10 수정**, 인쇄 p.2 Approach, p.3 Experiments/Grading, p.4 feedback를 텍스트로 확인했다. p.3 screenshot 요청은 `Cache miss`로 실패했다. 그림/표를 시각적으로 확인했다고 보고하지 않는다.

| 관점 | 확인 상태와 관찰 |
| --- | --- |
| 1. 판본·단위 | 확인: Spring 2024 1246. Winter 1244·2026 milestone과 혼용하지 않음. 홈페이지 milestone 비중 6%, PDF 5%로 **불일치**; 개인 계획에 성적 비중을 이식하지 않음. |
| 2. 실제 활동 | 확인: written/programming 과제·default/custom project·제안/중간/보고. milestone에 baseline·데이터·평가·실험 조건·실제 결과·기여를 요구. |
| 3. 평가 | 부분: 진행·이해·글의 명확성 평가. default의 baseline 향상 요구는 그 과제 조건이며 우리 비교의 강제 향상 gate가 아님. 비중 불일치의 원인은 미확인. |
| 4. 피드백 | 확인: 중간 결과/글에 짧은 피드백, custom mentor와 default 차이. 홈페이지는 TA가 project 코드를 보지 않을 수 있다고 명시; 코드 리뷰 보장 아님. |
| 5. 코드·공간 | 부분: Python/NumPy/PyTorch·code/Colab 안내. starter·채점 코드 전체 미검토. |
| 6. 도움/AI | 확인: 협력자로 AI 사용 가능, 직접 정답 요청/복사·상당 부분 대행 금지. 외부 코드/팀 기여를 밝힘. |
| 7. 선수 | 확인: Python·미적분/선형대수·확률/통계; ML 기반 권장. 과목 전체 선수를 AX 시작 관문으로 옮기지 않음. |
| 8. 자원·비용 | 부분: 등록자 영상/멘토/compute credits. 외부 자습자의 해당 권한·장치 비용은 미확인. |
| 9. 공개·재사용 | 부분: 프로젝트 외부 코드/협력 출처 공개 규칙. 과제 타 구현 참고 제한과 로컬의 공식 답안 private 규칙 유지. |

적용 해석: [R-07/R-09/R-10](../research.md)의 실제 중간 결과·평가·자기 기여 설명을 참고한다. 대학 점수·페이지 수·일정·default 향상 요구를 복제하지 않는다. 홈페이지/handout 불일치는 해당 과제 재선택 시 공식 확인할 항목이다.

## S-07 — CS336 Spring 2026

공식 구간: [홈페이지](https://cs336.stanford.edu/)의 Prerequisites·Assignments·GPU compute for self-study·Honor code·Submitting coursework/Regrade requests. 개별 handout·과제 코드/clone·AI policy의 별도 Google 문서는 추가 열람하지 않았다. 로컬 A1/A2 pin은 현재 [정책](../../../.agents/references/learning-policies.md)의 보존 대상이며 홈페이지의 가변 링크와 같다고 검증한 것이 아니다.

| 관점 | 확인 상태와 관찰 |
| --- | --- |
| 1. 판본·단위 | 확인: Spring 2026 홈페이지. 로컬 A1 v26.0.3·A2 v26.1.3은 별도 pin, 이번 handout 재감사 아님. |
| 2. 실제 활동 | 확인: A1 구성요소/학습, A2가 A1을 재사용해 profiling/최적화/분산, 이후 scaling/data/alignment. optional 구별. |
| 3. 평가 | 부분: Gradescope·마지막 제출 채점·regrade 설명. 개별 테스트·rubric·실행 미확인. |
| 4. 피드백 | 부분: 교내 office hours/Slack/regrade. 공개 자습자의 동일 접근 권한 미확인. |
| 5. 코드·공간 | 확인: 적은 scaffold와 큰 직접 구현량을 명시. 과제 저장소 링크를 확인했지만 코드는 읽지 않음. |
| 6. 도움/AI | 부분: 개념/저수준 도움과 직접 해결을 구별, 타 구현 참고 제한. 로컬의 더 엄격한 명령/답안 제한 유지; 개별 추가 정책 미확인. |
| 7. 선수 | 확인: Python/소프트웨어·PyTorch·systems·미적분/선형대수·확률·ML. |
| 8. 자원·비용 | 부분: CPU correctness와 GPU 학습/benchmark 구별. 홈페이지 가격은 2026-03-28 기준; 현재 비용·개인 장치·전체 공식 실행은 미확인. |
| 9. 공개·재사용 | 부분: 본인 수행·타 코드 제한은 확인. 개별 공개 정책·데이터/모델 권리 전체는 미확인; 공식 원문/답안 private 유지. |

적용 해석: [R-01/R-06/R-09](../research.md)의 LM 내부·학습·실험 깊이와 도움 경계를 참고한다. 큰 구현량을 첫 AX 기능에 복제하지 않으며 자체 LM과 A1을 둘 다 요구하지 않는다.

## S-08 — workflow 도구 보강

[기존 workflow 근거](workflow-framework-sources.md)를 검토한 뒤 [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)의 Overview·Core benefits와 [Anthropic 글](https://www.anthropic.com/research/building-effective-agents)의 What are agents?·When to use agents·frameworks를 다시 확인했다. 후자는 2024-12-19 게시이며 도구 환경 변화 주의문이 있다.

확인 사실: LangGraph는 상태를 유지하는 실행·재개·사람 개입의 runtime 역할을 설명하고 모델/도구를 먼저 익힐 것을 권한다. Anthropic은 정해진 코드 흐름과 모델 주도 도구 선택을 구별하며 복잡도·관측 가능성을 검토한다. **해석**: [R-03](../research.md)은 작은 고정 흐름부터 책임을 확인하고 실제 상태/재개 필요에 한 framework를 선택한다. 공급자의 권고는 교육 효과·현재 채용 요건의 입증이 아니다. API·Python 3.14 호환·성능·비용·외부 tracing은 미확인이다. 교육 기관 표본 수에는 넣지 않는다.

## 채택·조정·제외의 대응

| 공식 요소 | 계획에서의 판단 | 가져오지 않는 조건과 반대 근거 |
| --- | --- | --- |
| S-01 누적 시스템·S-03 workload 정리 | 한 서비스의 기능/평가를 발전, 실행 기준 위치 하나 | S-01/05의 노트북 장점도 있으므로 노트북 금지로 결론 내리지 않음. |
| S-04 프로젝트 rubric·S-06 중간 실험/기여 | 문제·실제 비교·실패·출처·재현을 초기부터 누적 | 개인 성적·동료 3명·도구 가산점·baseline 향상 강제는 제외. |
| S-05 TODO·S-03 제공 스크립트·S-07 적은 scaffold | 목표별 허용 준비·제공 코드·학습자 구현을 분리 | 제공 코드를 독립 구현으로 인정하지 않음. 모든 활동을 백지 과제로 바꾸지도 않음. |
| S-06/07 높은 연구 선수·내부 구현 | RE의 최소 선수와 모델/실험 깊이 유지 | AX 전에 대학 전체 수강·수학 전권·CS336을 의무화하지 않음. |
| S-04 공개 프로젝트와 제출 재사용 제한 | 개인 서비스 지속 발전과 cohort 제출을 분리 | 개인 버전 발전을 표절로 단정하지 않음. 다른 과정 제출 권한을 추정하지 않음. |

fast.ai·CS329S·기업 교육은 기존 초기 관찰을 보존했다. 이번 결정에 필요한 공백을 위 표본으로 다뤘으므로 추가 전체 강좌 조사·수강 목록 확장은 하지 않았다. 과거 보조 관찰을 상세 9관점 확인 완료로 집계하지 않는다.
