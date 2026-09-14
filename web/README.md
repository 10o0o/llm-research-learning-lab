# Knowledge 웹

루트 `knowledge/`의 개념 문서를 직접 읽는 Astro 정적 사이트입니다. 원본 Markdown은 복사하지 않습니다. 홈, 문서 목록과 본문 검색, 상세, 소개, 다크 모드를 제공합니다.

## 실행

Node 22.12 이상과 npm 9.6.5 이상이 필요합니다. 저장소 루트에서:

```bash
cd web
npm ci
npm run build
npm run preview
```

`http://127.0.0.1:4321/`에서 검색까지 확인할 수 있습니다. UI를 수정할 때는 `npm run dev`를 사용합니다. Pagefind 인덱스는 **빌드 후** 생성되므로 문서 수정 후 본문 검색을 확인하려면 다시 빌드합니다. 개발 서버에서 검색하면 빌드 미리보기가 필요하다는 안내가 나옵니다.

이번 작업 환경에는 npm이 없어 공식 Node 배포본을 사용자 영역에 설치했습니다. 해당 환경에서는 명령 실행 전에 다음 PATH를 사용할 수 있습니다. 셸 설정 파일과 시스템 Node는 변경하지 않았습니다.

```bash
export PATH="$HOME/.local/share/knowledge-web-tools/node-v22.23.2-linux-x64/bin:$PATH"
```

브라우저는 시스템 글꼴을 사용하며 원격 글꼴 요청은 하지 않습니다. 이번 WSL 화면 검증에는 한국어 글꼴이 없어 사용자 영역에 Noto Sans CJK KR을 설치했습니다. 다른 Linux 환경에서도 한국어가 네모로 보이면 시스템 한국어 글꼴을 준비해야 합니다.

## 검증

```bash
npm run check
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

Linux에서 브라우저 시스템 라이브러리가 없으면 Playwright의 `install --with-deps chromium`으로 준비합니다. CI에서는 이 명령을 사용합니다. 단위 테스트는 콘텐츠 추출과 URL 규칙을, 브라우저 테스트는 실제 빌드의 검색·필터·문서 렌더링·테마·모바일 탐색을 검사합니다. 스크린샷과 실패 trace는 무시되는 `test-results/`에 저장합니다.

## 콘텐츠와 경로

- `knowledge/*/*.md`만 상세 페이지와 검색 대상입니다. README·템플릿은 제외하고, README의 추천 개념 표만 홈의 읽기 묶음에 사용합니다.
- `title`, `updated`, `tags`는 원본 값을 사용합니다. 파일 경로가 URL을 결정하므로 제목 변경으로 주소가 바뀌지 않습니다.
- 요약은 Markdown AST의 `핵심 요약` 절에서 추출합니다. 카드의 표시 길이는 CSS로 줄이며 원문 요약은 보존합니다.
- 본문 첫 H1은 렌더링 때 제거하고 페이지 헤더에 제목을 한 번 표시합니다. 실제 Markdown 제목 ID로 목차를 만듭니다.
- 수식·표·코드와 Markdown 링크를 지원합니다. 링크 검사 우회를 막기 위해 raw HTML은 빌드 오류로 처리합니다. 코드 블록 안의 HTML 예시는 그대로 표시합니다.
- 개념 상대 링크는 사이트 내부로, 실습·TIL 상대 링크는 GitHub `blob/main` 원문으로 연결합니다. 비공개·저장소 밖·없는 파일 링크는 빌드를 실패시킵니다. 비공개 자료는 읽거나 배포 산출물에 복사하지 않습니다.
- 검색어·분야·태그·정렬은 목록 URL에 반영합니다. 검색 결과는 관련도순이며, 검색하지 않을 때는 수정일 또는 제목으로 정렬합니다. 검색과 필터는 JavaScript가 필요하고 문서 본문과 기본 탐색은 정적 HTML로 제공합니다.

[Pagefind](https://pagefind.app/docs/multilingual/)는 한국어 검색을 지원하지만 어간 추출은 지원하지 않습니다. 따라서 활용형·동의어가 자동으로 일치한다고 가정하지 않습니다. 수정일·출처 링크·관련 기록 목록은 검색 구절을 방해하지 않도록 인덱스에서 제외합니다.

하위 경로에서 확인하려면 빌드와 미리보기에 같은 값을 지정합니다.

```bash
SITE_BASE=/lab/ npm run build
SITE_BASE=/lab/ npm run preview
```

이 경우 `http://127.0.0.1:4321/lab/`으로 접속합니다.

## 공개 배포

이 사이트는 [GitHub Pages](https://10o0o.github.io/llm-research-learning-lab/)에서
`/llm-research-learning-lab/` 하위 경로로 공개됩니다. `main`에 push하면
`public-validation` workflow의 검증을 통과한 뒤 자동 배포됩니다. 재배포가 필요하면
GitHub 저장소의 **Actions**에서 `public-validation`을 열고 `main`을 선택해
**Run workflow**를 실행합니다. Pull request와 다른 branch는 검증만 실행하며
배포하지 않습니다. 검증 또는 배포가 실패하면 해당 job 로그에서 원인을 확인하고
수정한 뒤 `main`에 push하거나 workflow를 다시 실행합니다.

Pages와 같은 하위 경로를 로컬에서 확인하려면 다음처럼 같은 `SITE_BASE`를 빌드,
미리보기와 브라우저 테스트에 전달합니다.

```bash
SITE_BASE=/llm-research-learning-lab/ npm run build
SITE_BASE=/llm-research-learning-lab/ npm run test:e2e
```

기존 `npm run preview` 프로세스가 실행 중이면 브라우저 테스트 전에 종료합니다.
Playwright가 현재 `SITE_BASE`에 맞는 새 미리보기 서버를 시작해야 합니다.

Python 환경과 기존 지식 작성·검증 절차는 저장소 루트에서 그대로 사용합니다.
