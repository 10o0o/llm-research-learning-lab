type Note = { id: string; title: string; updated: string; tags: string[]; area: string; summary: string; url: string };
type SearchData = { url: string; excerpt: string; meta: Record<string, string> };
type Pagefind = { options: (options: { baseUrl: string }) => Promise<void>; search: (query: string) => Promise<{ results: { data: () => Promise<SearchData> }[] }> };
const { notes, base, areas } = JSON.parse(document.querySelector('#note-data')!.textContent!) as { notes: Note[]; base: string; areas: { id: string; label: string }[] };
const form = document.querySelector<HTMLFormElement>('#library-form')!;
const query = form.elements.namedItem('q') as HTMLInputElement;
const area = form.elements.namedItem('area') as HTMLSelectElement;
const tag = form.elements.namedItem('tag') as HTMLSelectElement;
const sort = form.elements.namedItem('sort') as HTMLSelectElement;
const cards = document.querySelector<HTMLElement>('#note-results')!;
const results = document.querySelector<HTMLElement>('#search-results')!;
const status = document.querySelector<HTMLElement>('#result-status')!;
const empty = document.querySelector<HTMLElement>('#empty-results')!;
let generation = 0;
let pagefind: Promise<Pagefind> | undefined;
const matchesFilters = (note: Note) => (!area.value || note.area === area.value) && (!tag.value || note.tags.includes(tag.value));

function readState() {
  const params = new URLSearchParams(location.search);
  query.value = params.get('q') || '';
  area.value = params.get('area') || '';
  tag.value = params.get('tag') || '';
  sort.value = params.get('sort') === 'title' ? 'title' : 'updated';
}
function writeState() {
  const params = new URLSearchParams();
  for (const field of [query, area, tag, sort]) {
    if (field.value && !(field === sort && field.value === 'updated')) params.set(field.name, field.value.trim());
  }
  history.pushState(null, '', `${location.pathname}${params.size ? `?${params}` : ''}`);
}
function snippet(excerpt: string) {
  // Preserve Pagefind's highlights; all other markup becomes plain text.
  const template = document.createElement('template');
  template.innerHTML = excerpt;
  const fragment = document.createDocumentFragment();
  function append(node: Node, parent: Node) {
    if (node.nodeType === Node.TEXT_NODE) parent.appendChild(document.createTextNode(node.textContent || ''));
    else if (node instanceof Element && node.tagName === 'MARK') {
      const mark = document.createElement('mark'); mark.textContent = node.textContent; parent.appendChild(mark);
    } else node.childNodes.forEach((child) => append(child, parent));
  }
  template.content.childNodes.forEach((node) => append(node, fragment));
  return fragment;
}
async function update() {
  const current = ++generation;
  const text = query.value.trim();
  empty.hidden = true;
  results.replaceChildren();
  cards.hidden = !!text;
  results.hidden = !text;
  sort.disabled = !!text;
  if (!text) {
    const sorted = [...notes].sort((a, b) => (sort.value === 'title' ? 0 : b.updated.localeCompare(a.updated)) || a.title.localeCompare(b.title, 'ko'));
    let count = 0;
    for (const note of sorted) {
      const card = cards.querySelector<HTMLElement>(`[data-note-id="${CSS.escape(note.id)}"]`)!;
      card.hidden = !matchesFilters(note);
      if (!card.hidden) count++;
      cards.append(card);
    }
    empty.hidden = count > 0;
    status.textContent = `${count}개의 문서`;
    return;
  }
  status.textContent = '본문에서 검색하고 있습니다…';
  try {
    const moduleUrl = `${base}pagefind/pagefind.js`;
    pagefind ??= (import(/* @vite-ignore */ moduleUrl) as Promise<Pagefind>).then(async (engine) => {
      await engine.options({ baseUrl: base });
      return engine;
    });
    const engine = await pagefind;
    const response = await engine.search(text);
    const found = await Promise.all(response.results.map((result) => result.data()));
    if (current !== generation) return;
    let count = 0;
    for (const data of found) {
      const pathname = new URL(data.url, location.origin).pathname;
      const note = notes.find((item) => decodeURI(item.url) === decodeURI(pathname));
      if (!note || !matchesFilters(note)) continue;
      count++;
      const article = document.createElement('article'); article.className = 'search-result';
      const meta = document.createElement('p'); meta.className = 'card-meta'; meta.textContent = `${areas.find((a) => a.id === note.area)?.label ?? note.area} · ${note.updated}`;
      const heading = document.createElement('h3');
      const link = document.createElement('a'); link.href = note.url; link.textContent = note.title; heading.append(link);
      const excerpt = document.createElement('p'); excerpt.className = 'search-excerpt'; excerpt.append(snippet(data.excerpt));
      article.append(meta, heading, excerpt); results.append(article);
    }
    empty.hidden = count > 0;
    status.textContent = `“${text}” 검색 결과 ${count}개 · 관련도순`;
  } catch {
    if (current !== generation) return;
    pagefind = undefined;
    status.textContent = import.meta.env.DEV ? '본문 검색은 빌드 후 미리보기에서 사용할 수 있습니다.' : '검색을 불러오지 못했습니다. 잠시 후 다시 검색해 주세요.';
  }
}
form.addEventListener('submit', (event) => { event.preventDefault(); writeState(); void update(); });
for (const select of [area, tag, sort]) select.addEventListener('change', () => { writeState(); void update(); });
window.addEventListener('popstate', () => { readState(); void update(); });
readState();
void update();
