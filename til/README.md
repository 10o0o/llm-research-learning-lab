# TIL

그날 무엇을 배우고 어떻게 생각했는지 날짜별로 남깁니다.

```text
til/YYYY/MM/YYYY-MM-DD.md
```

예:

```text
til/2026/08/2026-08-13.md
```

하루에 여러 주제를 공부했다면 한 파일에 함께 적습니다. 최종 TIL은 [TIL 템플릿](./template.md)의 순서에 맞춰 정리하되, 내용이 없는 선택 항목은 생략할 수 있습니다. 각 항목 안에서는 배운 내용·생각이 바뀐 부분·헷갈리는 점·직접 해본 일을 자신의 말로 남깁니다.

TIL은 당시의 생각을 보여주는 시간 기록입니다. 나중에 이해가 달라져도 전체를 완성된 개념 설명으로 다시 쓰지 않습니다. 현재의 이해는 [`knowledge/`](../knowledge/)에서 갱신하고, 실행한 작업은 [`practice/`](../practice/)에 둡니다.

작성할 때부터 형식에 맞출 필요는 없습니다. `til/today.md`에 자유롭게 쓴 뒤, `$coach-llm-research-study`로 오늘 본 자료와 비교해 저장 전 검토합니다. 대화형 수업에서는 이해가 확인된 학습자 답변만 이 초안에 자동으로 추가됩니다. 잘못된 개념은 다시 학습하고, 해결하지 않은 내용은 확실한 사실처럼 고치지 말고 질문이나 불확실성으로 남깁니다. `저장 가능` 판정을 받은 뒤 `$save-today-til`을 사용하면 날짜별 위치와 템플릿에 맞게 저장하고 그 날짜별 TIL만 자동 커밋합니다. `til/today.md`는 미완성 메모이므로 Git에는 포함되지 않습니다.

강의자료를 보고 공부한 날에는 최종 TIL의 `관련 기록`에 실제 자료 링크를 남깁니다. Reviewed handoff를 사용한 local·external 수업은 모두 실제 primary target을 다음 형식으로 남깁니다. Temporary external source라면 exact official HTTPS URL, provider/course, offering 또는 edition, artifact와 studied scope도 함께 보존합니다.

```markdown
- 관련 역량: `CC-...`
```

`TR-*` target이면 위의 `CC-...` 대신 정확한 `TR-...`를 씁니다. 실제로 수업에서 다룬 inline bridge가 있으면 다음 줄을 하나 더 두며, 여기에도 `TR-*` target을 사용할 수 있습니다.

```markdown
- 보충 선수 역량: `CC-...`
```

두 ID는 routing provenance이지 mastery 표기가 아닙니다. 이 날짜별 TIL이 이후 실습의 시작점이 되므로 `$suggest-learning-practice`를 사용할 때는 생성된 `til/YYYY/MM/YYYY-MM-DD.md` 경로를 정확히 지정합니다. 스킬은 그 링크와 stable source identity를 따라 자료를 확인하며, `til/today.md`나 자동으로 고른 최신 TIL은 입력으로 사용하지 않습니다.
