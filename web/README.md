# 기존 사이트 안내

기존 지식 서재를 종료하고 `public/index.html`과 `public/404.html`만 제공한다.
새 학습 시스템이나 별도 작성 의무는 없다. 이전 문서 주소는 404 안내에서
현재 저장소와 복구 기준본으로 연결된다. 검색 색인·노트 상세 페이지는 생성하지 않는다.

런타임·Node 패키지·빌드 단계 없이 정적 HTML을 사용한다.
로컬 확인: 저장소 루트에서 `python -m http.server 8000 --directory web/public`을 실행하고
`http://localhost:8000`을 연다. 로컬 기본 서버의 없는 경로 응답은 Pages의 custom 404와 다르므로
`http://localhost:8000/404.html`도 직접 확인한다.

검사: `uv run --frozen pytest -q tests`.
main push는 기존 Pages 배포를 유발한다. 배포 승인 전에는 비배포 브랜치에서만 준비한다.
