# Deep-ML 풀이

이 디렉터리는 `ROADMAP.md`의 **빈 파일 구현 트랙**에 속합니다. 주 3~5문제를
상시로 풀며, 특정 Phase에만 하는 활동이 아닙니다. 목적은 정답 제출이 아니라
아무것도 없는 파일에서 시작하는 능력이므로, 막혔을 때 Agent에게 코드를
요청하지 않습니다. 필요한 연산 이름이나 계약까지만 묻고 구현은 직접 합니다.

VS Code의 Deep-ML 확장에서 **Solve in Editor**를 누르면 이 워크스페이스의
`solutions/` 아래에 문제별 Python 파일이 만들어진다. 그 파일에서
**Run Tests (local)**로 공개 예제를 확인하고, 필요할 때만 **Submit**으로
Deep-ML 서버 채점을 요청한다.

문제 풀이 파일은 그대로 Git에 남겨도 된다. 다만 통과 여부만 남기지 말고,
다시 볼 가치가 있는 파일에는 아래처럼 본인의 짧은 기록을 추가한다.

```python
# Learning note:
# - Contract / shape:
# - Key idea:
# - What I verified:
# - Limitation or next experiment:
```

플랫폼의 문제 원문·해설을 복사하지 말고 원문 링크만 남긴다. 통과 여부뿐
아니라 구현의 핵심 계약과 실제 결과를 해석한다. 관련 학습 기록이 있으면
exact TIL이나 knowledge 링크를 남길 수 있다. 짧은 제출 코드는
`challenges/`에 두며, 데이터 분석·benchmark처럼 Notebook 자체가 학습
산출물인 경우에만 `practice/`를 사용한다.
