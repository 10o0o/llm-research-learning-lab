# TIL

TIL은 완료된 학습 cycle을 나중에 돌아보기 위한 날짜별 역사 기록입니다.

    til/YYYY/MM/YYYY-MM-DD.md

## Daily full flow

수업 중간에는 TIL을 만들지 않습니다. Confirmed learner evidence는 ignored
tmp/active-learning-flow.json에 보존되고, practice와 knowledge는 그
completed session을 직접 입력으로 사용합니다.

다음 요청이 있을 때만 TIL을 작성하고 날짜별 파일 하나를 커밋합니다.

    오늘 TIL 저장해줘

완료됐지만 아직 기록되지 않은 cycle만 소비합니다. Paused 또는 미완료
cycle은 TIL에서 제외하고 다음 수업에서 계속 해결합니다. 같은 날 여러
번 저장하면 이전 완료 cycle을 보존하면서 새 cycle을 자연스럽게
병합합니다.

Flow-generated TIL은 각 개념을 먼저 제시합니다.

1. 개념과 핵심 정의
2. 성립 조건·작동 원리·한계
3. 어떤 예시와 적용으로 확인했는지
4. practice에서 실제로 관찰하고 해석한 결과
5. exact source·practice·knowledge·target provenance

자동 생성본에는 남은 질문, “내 말로 설명해야 한다”, 학습 지시,
평가 문구, TODO, 내부 marker를 넣지 않습니다. 불확실한 핵심은 TIL로
종료하지 않고 paused cycle에 남깁니다.

## Manual or standalone notes

til/today.md는 사용자가 직접 쓰는 ignored scratchpad입니다. Reviewed
lesson은 이 파일을 수정하지 않습니다. Manual self-study나 standalone
draft를 저장할 때는 exact input을 명시합니다. 수동 내용의 실제
불확실성은 coach의 한 번 검토 뒤 남은 질문으로 보존할 수 있습니다.

## Provenance

Source-based TIL의 관련 기록에는 exact source link와 primary target을
남깁니다.

    - 관련 역량: CC-...

실제로 전달된 inline bridge가 있을 때만 보충 선수 역량 줄을
추가합니다. CC-* 대신 TR-* target도 사용할 수 있습니다. Temporary
external source는 official URL, provider/course, offering or edition,
artifact, exact scope를 함께 보존합니다. 이 ID와 링크는 routing
provenance이지 mastery 표기가 아닙니다.

TIL은 당시의 기록이고 knowledge/는 현재 reusable understanding입니다.
Practice evidence와 knowledge가 TIL보다 먼저 생길 수 있으며, 이는 v9
day flow의 정상적인 순서입니다.
