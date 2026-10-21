# 명세 근거: 공식 교육 자료의 초기 확인과 본감사 요구

**조회일**: 2026-10-21 · **대상**: [002 명세](../spec.md)

실무 교육 3곳과 대학 강의 3개의 공식 본문을 새로 확인했다. FSDL의 2022 과정과 2023 Bootcamp는 한 기관의 서로 다른 판본/과정으로 구별하며 기관 수를 두 개로 늘리지 않는다. CS329S는 추가 보조 관찰이다. 모든 과정의 강의·개별 과제·도움 정책·권리·현재 환경을 전수 확인한 것은 아니다. 아래 미확인 항목은 완료로 세지 않는다.

공식 웹페이지와 공식 저장소의 설명·디렉터리를 읽었다. GitHub 연결로 저장소 자료를 확인했고, 이전 주소의 이동을 연결에서 따라가지 못한 경우 공식 사이트의 링크로 새 경로를 확인했다. 로컬 clone·원문/노트북 다운로드·설치·등록·모델 실행은 하지 않았다. 원문 전체·과제 답안은 이 저장소에 복제하지 않으며 아래는 짧은 관찰·해석이다.

## E-01 — Full Stack Deep Learning

**판본·구간·공식 URL**:

- [2022 Course](https://fullstackdeeplearning.com/course/2022/): Schedule, Pre-Labs, Lab Overview, Labs 4~8, Project Presentations.
- [2022 Lab Overview](https://fullstackdeeplearning.com/course/2022/lab-0-overview/): What are these labs for?, Architecture, Running the labs.
- [2022 공식 labs 저장소](https://github.com/the-full-stack/fsdl-text-recognizer-2022-labs): 루트의 lab01~08·overview 노트북·환경 파일·설정 디렉터리 목록. 개별 구현·노트북 본문은 미검토.
- [Spring 2023 LLM Bootcamp](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/): 선수에 대한 소개, 주제별 설명·질문/피드백 채널.
- [askFSDL walkthrough](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/askfsdl-walkthrough/): 2023-05-09 게시, Chapter Summaries의 도구·자료 정리·ETL·화면·관측 설명.

**관찰 사실**:

- 2022 labs는 손글씨 인식 모델을 학습하고 웹앱으로 연결하는 코드베이스를 점진적으로 발전시킨다. 전체 구조를 먼저 설명한다. lab에는 실험 관리·테스트/진단·데이터·배포·피드백 관측이 연결되고 별도 그룹 프로젝트 일정이 있다.
- 2022 안내는 Colab 노트북과 Linux/NVIDIA 환경을 제공하며 준비 문제로 본 학습이 막히지 않게 하는 의도를 설명한다. 2023 askFSDL은 제공된 Q&A 앱의 walkthrough이고 관련 서비스 계정 없이는 실행하지 못할 수 있다고 밝힌다.
- 2023 소개에 질문·피드백 채널이 있다. 읽은 페이지에서는 개인별 채점표·자습자 코드 리뷰 보장·구체 AI 도움 정책·전체 자료 재배포 권리를 확인하지 못했다.

**우리 상황의 해석**: 한 산출물을 발전시키고 전체 흐름을 먼저 설명하는 방식, 준비 부담을 줄이는 방법을 AX·저장소 전략의 비교 근거로 쓸 수 있다. 노트북을 활용하면서 프로젝트 코드를 발전시키는 사례이므로 파일 형식 하나로 결론 내릴 근거는 아니다.

**한계·본감사 요구**: 2022 모델 학습과 2023 LLM walkthrough를 동일한 과제/평가로 합치지 않는다. 완성 코드 탐색을 직접 구현으로 세지 않는다. 과거 Colab/GPU·서비스/API 조건을 현재 개인 자원으로 보장하지 않으며, 필요하다면 실제 lab의 제공/미완성 범위·평가·라이선스를 추가 확인한다. 현재 모든 선수를 확인했다는 주장은 하지 않는다.

## E-02 — Made With ML

**판본·구간·공식 URL**:

- [공식 과정](https://madewithml.com/): Design→Data→Model→Develop→Test→Reproducibility→Production의 구성. 상시 개정본이며 고정 2026 기수로 부르지 않는다.
- [Moving from Notebooks to Scripts](https://madewithml.com/courses/mlops/scripting/): Intuition, Setup, README, Scripts, Workloads. 페이지의 인용 연도는 2023이며 현행 접속 본문과 구별한다.
- [Evaluation](https://madewithml.com/courses/mlops/evaluation/): coarse/fine 평가·slicing·Behavioral testing·online evaluation 본문.
- [Setup](https://madewithml.com/courses/mlops/setup/): Local/Anyscale 환경·compute·workspace·notebook.
- [공식 저장소 README](https://github.com/GokuMohandas/Made-With-ML/blob/main/README.md): Overview, Audience, Set up, Notebook 및 루트의 notebooks·모듈·tests·deploy 목록.

**관찰 사실**:

- 대화형·상태 유지·출력 관찰을 위해 노트북을 사용한 뒤 실행 목적별 스크립트와 설명서로 정리하는 흐름이다. 숨은 상태·셀 순서·테스트의 문제를 설명한다. 제공 스크립트가 이미 있다는 점도 밝힌다.
- 평가는 전체 지표뿐 아니라 일부 집단·행동 변화·최소 기능과 실제 결과를 살핀다. 코드·데이터·모델 검사, 버전 관리와 서비스 운영이 같은 과정에 연결된다.
- 환경 안내에는 로컬 CPU와 원격 자원 선택, Python 3.10 권장이 있다. 현재 lab Python 3.14의 호환 실행을 입증하지 않는다. 라이브 cohort의 수업/질문 지원 설명은 있으나 읽은 범위에서 개인별 공식 채점·AI 대행 정책·형식적인 전체 선수 요건은 확인하지 못했다.

**우리 상황의 해석**: 탐색과 반복 가능한 실행의 책임을 비교하고, 평가를 끝으로 미루지 않으며, 제공 코드와 자기 기여를 분리할 근거다. 모듈·테스트가 있다는 이유로 지금 큰 구조·분산 도구·CI를 먼저 만들어야 한다는 결론은 나오지 않는다.

**한계·본감사 요구**: 본문이 사용하는 “stateless”는 스크립트에 상태가 전혀 없다는 보편 명제가 아니다. 실행 간 상태·초기화·입출력 책임으로 해석해 비교해야 한다. 제공 완성 코드의 실행은 독립 구현이 아니다. 라이브 지원·클라우드 권한·라이선스·실제 테스트 요구는 채택 활동별로 추가 확인하며 과정 전체를 필수로 복원하지 않는다.

## E-03 — DataTalksClub LLM Zoomcamp

**판본·구간·공식 URL**:

- [공식 README](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/README.md): 조회 시 2026 표기. Prerequisites, Live/Self-Paced, Syllabus, Capstone, Certificate, Community.
- [프로젝트 지침](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/project.md): Objective, Problem statement, Documentation, Tips, Peer Reviewing, Evaluation Criteria, Cheating and plagiarism. 조회 시 2025 제출 안내로 연결되므로 이를 독립된 확정 2026 과제판으로 부르지 않는다.
- [2025 cohort project](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/project.md): 제출·동료 평가 3개, 공통 평가표 링크.
- [현재 Module 1](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/01-agentic-rag): 데이터·검색·prompt·LLM·도구·loop 설명 파일과 code 디렉터리의 목록. 개별 code 구현·노트북 본문은 미검토.

**관찰 사실**:

- 자료→검색/도구→LLM→평가→인터페이스→피드백을 연결하는 독립 프로젝트를 요구한다. README에 문제·흐름·입출력 예·실행 조건·평가 기준을 설명하고 별도 프로젝트 저장소를 권장한다.
- 평가표는 검색과 최종 응답 평가, 인터페이스·수집·관측·재현 등을 구별하며 CLI/스크립트/노트북도 인정한다. cloud 배포는 bonus다. 동료 프로젝트 3개 평가와 제출 상태의 commit 식별을 명시한다.
- 2026 소개는 Python·명령줄·기초 Docker, 외부 API 비용·일반 PC 조건을 안내한다. cohort의 채점/동료 평가와 self-paced의 자가 확인을 나눈다. 공통 프로젝트 지침은 남의 작업·다른 과정의 자기 프로젝트 재사용을 제출 위반으로 다루면서 일부 강의 코드 재사용은 허용한다.

**우리 상황의 해석**: 별도 저장소·명확한 실행 설명·출력/실패·평가 기준·수정 상태를 검토하는 모델이 비교에 유용하다. 과정 제출용 재사용 금지를 개인 서비스의 버전별 발전 금지로 일반화해서는 안 된다. 저장소 수·대시보드 수·평가 점수를 학습자 역량의 대체로 가져오지 않는다.

**한계·본감사 요구**: 2026 소개·2025 제출 링크·수정 가능한 main의 평가표를 한 고정 판본으로 합치지 않는다. 공식 제출 규칙을 채택하려면 해당 cohort의 확정 지침을 다시 확인한다. AI 도움의 구체 허용 범위·데이터별 공개 권리는 읽은 지침에서 확정되지 않았다. 과정의 비용 안내는 현행 API 요금·우리 실행 비용의 검증이 아니다. Slack 가입·등록·지출은 하지 않았다.

## E-04 — MIT 6.S191

**판본·구간·공식 URL**:

- [공식 2026 홈페이지](https://introtodeeplearning.com/): Description, Schedule의 labs 1~3·Project, FAQ의 grading/prerequisites/open-source.
- [2026 공식 저장소 README](https://github.com/MITDeepLearning/introtodeeplearning/blob/master/README.md): Instructions, Opening/Running labs, License.
- [Lab 1 README](https://github.com/MITDeepLearning/introtodeeplearning/blob/master/lab1/README.md): Python DL 소개·음악 생성. 디렉터리의 TF/PT 노트북 이름도 확인했다. 노트북·solutions 본문은 읽지 않았다.

**관찰 사실**:

- 2026 일정은 DL/sequence 설명과 Python/music·얼굴 탐지·LLM fine-tuning labs를 연결한다. 과목 평가 FAQ는 프로젝트 제안 과제 완료에 따른 P/D/F이며 소개는 교직원·산업 패널의 제안 피드백을 명시한다.
- 공식 README는 Colab 노트북의 TODO를 채워 실행하는 방식, Google 계정·GPU runtime 선택과 lab별 competition 제출 안내를 설명한다. Lab 1은 TF/PT 소개와 문자 단위 음악 생성을 구별한다.
- 최소 행렬 연산·미분/chain rule을 기대하고 Python 경험을 도움으로 안내한다. MIT 라이선스·출처 표기 조건이 README/FAQ에 있지만 학습자의 새 구현·공식 채점과는 별개다. 읽은 범위에서는 구체 AI 도움 정책을 확인하지 못했다.

**우리 상황의 해석**: 최소 선수 설명 뒤 실제 실습·관찰로 연결하는 방식과 제공 스타터/학습자 TODO의 구분을 비교할 수 있다. 노트북·스타터 활용 자체가 부적절하다는 근거는 아니다. 모든 lab을 첫 AX 활동의 선수로 가져오지 않는다.

**한계·본감사 요구**: homepage·README·Lab 1 설명을 확인했을 뿐 개별 lab의 전체 과제·점수·competition 기준·AI 정책·현재 GPU 할당·실행 호환성을 확인하지 않았다. 외부 학습자가 교내 제안 피드백/성적을 받는다고 주장하지 않는다. lab별 조건은 선택 시 원문으로 추가 확인한다.

## E-05 — Stanford CS224N

**판본·구간·공식 URL**:

- [Spring 2024 archive 1246](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html): Prerequisites, Coursework, Final Project, AI Tools Policy, Schedule의 A4 code/Colab 안내. Winter 2024 archive 1244와 혼용하지 않는다.
- [Project Proposal Instructions](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/project/project-proposal-instructions-spr2024-updated.pdf): 2024-05-02 수정, §1~2의 팀/외부 협력·공유 프로젝트 표시·논문 요약 요구를 확인했다. PDF 전체를 저장소에 복제하지 않았다.

**관찰 사실**:

- 4개 과제에 written·programming을 함께 두며 과제 48%, 프로젝트 49%를 구별한다. 프로젝트는 제안·중간 결과·포스터·보고서로 이어진다. custom/default와 멘토 제공 여부가 다르다.
- Python·미적분·선형대수·확률/통계를 기대한다. 과제는 Python/NumPy/PyTorch, A4에는 code와 Colab 실행 안내가 있다. 코드·노트북 중 하나만 강제된 과정이라고 볼 수 없다.
- AI 협업은 허용하되 정답 직접 요청·복사·상당 부분 대행을 금지한다. 프로젝트는 외부 코드·협력·기여를 밝히게 하며 과제 규칙과 구분한다. 교내 office hours·멘토·compute credits는 공개 자습자의 권리가 아니다.

**우리 상황의 해석**: 프로젝트 중간 결과·평가·보고서·기여 공개와 개념/구현의 연결을 참고할 수 있다. 교과목 선수와 업무 앱의 최소 선수를 동일하게 만들지 않고 공식 과제 재선택 시 그 정책을 지킨다.

**한계·본감사 요구**: 일정의 code/Colab 링크 확인은 스타터·채점 코드 전체 검토가 아니다. 과제별 자원·상세 제한은 미확인이 남는다. 공개 과제 답안 금지 등 현재 lab의 더 엄격한 보존 경계는 유지한다. 2024 spring 영상의 등록 제한과 공개된 다른 해 영상도 같은 판본으로 바꾸지 않는다.

## E-06 — Stanford CS336

**판본·구간·공식 URL**:

- [Spring 2026 공식 홈페이지](https://cs336.stanford.edu/): Prerequisites, Assignments 1~5, GPU compute for self-study, Honor code, Submitting coursework, Regrade requests, Schedule.
- 현재 lab의 [학습 정책](../../../.agents/references/learning-policies.md)은 A1 v26.0.3·A2 v26.1.3 pin과 더 엄격한 명령/도움 경계를 보존한다. 이 로컬 pin 확인을 개별 handout 재열람으로 보고하지 않는다.

**관찰 사실**:

- A1에서 tokenizer·모델·optimizer·학습을 구현하고 A2가 A1 모델/층을 진단·최적화·분산 학습으로 발전시킨다. A3 scaling, A4 data, A5 후속학습/RL이 이어지고 optional 범위가 구별된다.
- 적은 scaffolding과 많은 구현량, Python/소프트웨어·PyTorch·systems·수학·확률 기반을 명시한다. 코드 형태의 강의 자료와 과제 저장소가 연결된다.
- Gradescope 제출·마지막 제출본 채점·재채점 요청, office hours/Slack을 안내한다. AI는 저수준 사용법·상위 개념 질문과 직접 문제 풀이를 구별하고 기존 구현 참고도 제한한다. CPU correctness debugging과 GPU 학습/벤치마크를 구별한다.

**우리 상황의 해석**: 앱 연결과 다른 모델 내부·실험·자원 책임의 깊이, 앞 구현을 후속 실험에 재사용하는 방식을 RE의 비교 근거로 쓸 수 있다. 최소 scaffold·많은 구현량이 입문 AX에도 최선이라는 결론은 나오지 않는다.

**한계·본감사 요구**: 이번에는 과제 clone·코드·handout을 새로 다운로드·실행하지 않았다. 개별 테스트·전체 written·세부 장치·저자원 허용 경로·가중치별 채점은 재검증하지 않았다. 홈페이지의 과거 GPU 가격을 현재 가격으로 사용하지 않는다. 자체 LM/A1은 대체 관계이고 모든 과제 완성이 의무가 아니다. 특히 AI의 과제 repo 명령·코드/의사코드/답안·새 명령 시퀀스 금지는 계속 지킨다.

## E-07 — Stanford CS329S, 보조 관찰

**판본·URL·구간**: [공식 홈페이지](https://stanford-cs329s.github.io/) Logistics·Prerequisites·Honor Code·Audit policy, [syllabus](https://stanford-cs329s.github.io/syllabus.html)의 평가/배포/관측 tutorial, [공식 header.js](https://github.com/stanford-cs329s/stanford-cs329s.github.io/blob/main/header.js)의 Winter 2022 표기를 확인했다. 2026 과정으로 부르지 않는다.

**관찰**: ML 앱 프로젝트 65%·짧은 과제 30%·참여 5%이며 demo day를 둔다. 기존 코드·토론은 출처/기여를 밝히되 대행·복사를 금지하고 최종 프로젝트 공개와 과제 답안 비공개를 구별한다. 상당한 프로그램 작성·ML·framework 배경을 기대한다. 외부 audit·채점/조언 접근은 제한된다. syllabus에는 notebook tutorial도 연결된다.

**해석·한계**: 프로젝트 발전·기여·공개 경계에 도움이 되는 비교다. 별도 최종 프로젝트 상세 지침·루브릭·계정/자원·AI 정책은 확인하지 못했고 notebook 본문도 읽지 않았다. 이 보조 관찰을 여섯 기본 표본의 상세 검토 완료를 대신하는 수로 쓰지 않는다.

## 조사 사실에서 명세로의 연결

| 초기 근거 | 재감사에 필요한 요구 | 연결 |
| --- | --- | --- |
| E-01/02/06: 같은 코드베이스의 발전·탐색/실행 형태 혼용 | 파일 확장자 외에 목적·기여·상태·재현·전환 비용을 비교 | FR-005~009, FR-022~028 |
| E-02/03/05: 평가·중간 결과·기여 공개 | 사전 기준·실제 산출물·실패·제안의 검증 행동을 연결 | FR-008/017~020/028/031~034 |
| E-03/05/07: 재사용·도움·공개 규칙이 다름 | 개인 서비스 발전과 과정 제출·공식 답안 경계를 분리 | FR-012~014/017/029/030 |
| E-01/04/05/06: 제공 환경·스타터·자원/피드백 조건이 다름 | 최소 선수·허용 준비·실제 과제·자습자 접근을 구별 | FR-006/010~014/019/025 |
| E-03: 2026 소개와 2025 제출 지침 연결, E-07: 2022 확인 | 판본 혼재·미확인을 공개하고 미확인 2026판을 만들지 않음 | FR-011~014 |

이 자료들은 교육 운영의 목적 표본이다. 특정 방식의 학습 효과·취업률·개인 적합성을 입증하지 않는다. 후속 재감사에서는 9관점별 확인/미확인을 유지하며 실제 단위·불만·산출물과 연결해 적용·제외 이유를 판단해야 한다. fast.ai·다른 MLOps 과정은 비교 공백이 있을 때만 보완하고 새로운 전체 수강 의무로 추가하지 않는다.
