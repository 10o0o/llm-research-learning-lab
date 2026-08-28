# Deep-ML 풀이

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

플랫폼의 문제 원문·해설을 복사하지 말고 원문 링크만 남긴다. 하루 전체
흐름에서 선택한 challenge라면 exact completed lesson session과 challenge
경로를 연결하고, 통과 여부뿐 아니라 구현의 핵심 계약과 실제 결과를
해석한다. 과거 자율학습은 exact finalized TIL과 연결할 수 있다. 짧은 제출
코드는 `challenges/`에 두며, 데이터 분석·benchmark처럼 Notebook 자체가
학습 산출물인 경우에만 `practice/`를 사용한다.
