# AX 기술 동향의 설계 근거

**조회일: 2026-10-19.** 공식 엔지니어링·아키텍처 본문을 읽고 비교했다. 여기서 AX는 업무를 AI와 데이터·소프트웨어로 개선하는 넓은 목표이며, 에이전트 프레임워크 하나의 이름이 아니다. 아래는 기술 선택의 근거이지 전체 산업의 점유율·성과 통계가 아니다.

| ID·공식 자료 | 원문 날짜·접근 | 실제 관찰 | 커리큘럼에 적용할 판단 |
| --- | --- | --- | --- |
| TREND-01 · [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 2026-01-09, 본문 확인 | 과업·시도·trace·실제 outcome을 구분하고 코드·모델·사람 평가를 조합한다. 평가를 초기에 시작하고 판정기 자체를 검토한다 | 첫 작은 기능부터 성공/실패 사례·회귀 평가를 둔다. 반복 생성과 독립 사례, 말로 보고한 성공과 실제 상태를 구별한다 |
| TREND-02 · [Anthropic — Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) | 2026-04-08, 본문 확인 | 모델 개선으로 harness 가정이 낡을 수 있으며 session·harness·sandbox를 분리한다. 실패 복구·자격정보 경계도 아키텍처 문제다 | 안정된 입출력·도구 계약, 상태 보존과 복구를 가르친다. 이 회사의 관리형 제품·전체 분산 구조를 개인 프로젝트 필수로 복제하지 않는다 |
| TREND-03 · [Anthropic — Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 2025-09-29, 본문 확인 | 프롬프트뿐 아니라 도구·검색·외부 데이터·대화 이력을 제한된 context에 맞게 관리한다. 미리 검색/필요시 검색의 trade-off를 설명한다 | RAG와 도구를 다른 입출력으로 구분하고 근거 선택·메타데이터·길이·불필요한 이력 문제를 실제 실패에 연결한다 |
| TREND-04 · [Microsoft — Design and develop a RAG solution](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide) | 최종 갱신 2026-06-30, 본문 확인. 상단 authorization 안내가 있으나 기사 본문은 제공됨 | 문서 준비·chunk·embedding·검색·답변 평가를 분리한다. 고정 RAG와 agentic RAG의 사용 조건을 구분하고 검색별/종단 평가를 요구한다 | 외부 지식이 필요한 단위에서 단순 검색과 embedding/hybrid를 비교한다. 다단계 검색은 관찰된 필요가 있을 때 확장한다 |
| TREND-05 · [Google Cloud — Choose your agentic AI architecture components](https://docs.cloud.google.com/architecture/choose-agentic-ai-architecture-components) | 검토일 2026-04-21, 본문 확인 | 고정 단계 문제에는 비에이전트 방식이 더 효율적일 수 있다. 단일 agent에서 시작하고 multi-agent의 평가·권한·비용 부담을 설명한다 | 고정 workflow와 제한된 단일 agent를 비교한다. multi-agent·A2A·클라우드 서비스 개수를 학습 완료 조건으로 삼지 않는다 |
| TREND-06 · [Databricks — Enterprise AI agent trends](https://www.databricks.com/blog/enterprise-ai-agent-trends-top-use-cases-governance-evaluations-and-more) | 2026-01-27, 본문 확인 | 자사 고객/제품 사용 자료에서 업무별 에이전트, 평가·거버넌스와 운영 전환의 관계를 보고한다 | UI 데모에 그치지 않고 업무 결과·권한·회귀·관측성을 포트폴리오에서 다룬다. 벤더 표본의 상관관계를 인과 효과나 한국 시장 전체로 일반화하지 않는다 |
| TREND-07 · [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 2024-12-19, 본문 확인. 본문이 도구 생태계 변화와 2026년 후속 글을 안내함 | 단순 호출·고정 workflow·agent를 구별하고 필요할 때 복잡도를 높인다. 추상화 내부를 이해하도록 권한다 | 원리는 참고하되 당시 프레임워크 목록을 최신 표준으로 쓰지 않는다. TREND-02·05와 대조한 뒤 현재 공식 API를 활동 시 확인한다 |
| TREND-08 · [채널톡 — 사내 AI 에이전트 개선기](https://docs.channel.io/tech-blog/ko/articles/tech-ax-channel-labs-b085ab62) | 2026-06-19, 회사 기술 블로그 본문 확인 | 국내 AX 사례에서 API 도구·세션/요청 상태·실행 허용 경계와 context 비용을 다룬다. 파일/도구 응답을 필요한 범위로 제한하며 SDK 교체만으로 문제가 끝나지 않았다고 설명한다 | AX-03/04에 요청 간 격리·실행 경계·context/비용·실패 관찰을 포함한다. 특정 SDK를 산업 공통 의무로 만들거나 이 사례의 운영 성과를 개인 구현으로 옮기지 않는다 |

## 선택 결과

1. **공통 핵심**: 작동하는 업무 기능, 구조화된 입출력, 데이터/API 연결, 검색과 context, 평가·오류 분석, 상태/실패 복구, 권한·재현·관측·비용/지연.
2. **선택 도구**: orchestration 프레임워크 하나를 실제 연결 책임으로 배운다. MCP는 외부 도구 표준화의 필요를 확인한 뒤 한 연결로 제한한다.
3. **현재 공통 의무에서 제외**: multi-agent, A2A, 범용 메모리 플랫폼, 독립 벡터 DB 운영, 모든 프레임워크, 모든 모델 파인튜닝. 분류·학습·복잡한 검색은 관찰한 문제나 지원 직무에 따라 추가한다.

이 선택은 원문들의 공통 고려사항을 학습 목적에 맞게 조합한 **설계안**이다. 특정 벤더가 승인한 교육과정, 산업 전체의 유일한 정답 또는 기능 품질의 검증 결과가 아니다.
