import { getCollection, type CollectionEntry } from "astro:content";
import { readFile } from "node:fs/promises";
import path from "node:path";
import type { Link, Root, RootContent } from "mdast";
import { toString } from "mdast-util-to-string";
import { unified } from "unified";
import { visit } from "unist-util-visit";
import remarkGfm from "remark-gfm";
import remarkParse from "remark-parse";

export const AREAS = [
  {
    id: "math",
    label: "수학",
    description: "확률, 선형대수와 미분의 핵심 개념",
  },
  {
    id: "ml",
    label: "머신러닝",
    description: "데이터 분할과 모델 선택 원칙",
  },
  {
    id: "deep-learning",
    label: "딥러닝",
    description: "자동미분, 학습 반복과 시퀀스 모델",
  },
  {
    id: "llm",
    label: "언어 모델",
    description: "문자 언어 모델의 학습, 평가와 생성",
  },
] as const;

export interface Note {
  id: string;
  title: string;
  updated: string;
  tags: string[];
  area: string;
  summary: string;
  relatedIds: string[];
  entry: CollectionEntry<"knowledge">;
}

export interface ReadingPath {
  title: string;
  description: string;
  ids: string[];
}

function parseMarkdown(body: string): Root {
  return unified().use(remarkParse).use(remarkGfm).parse(body) as Root;
}

function sectionNodes(tree: Root, title: string): RootContent[] {
  const start = tree.children.findIndex(
    (node) =>
      node.type === "heading" &&
      node.depth === 2 &&
      toString(node).trim() === title,
  );
  if (start < 0) {
    return [];
  }

  const nodes: RootContent[] = [];
  for (const node of tree.children.slice(start + 1)) {
    if (node.type === "heading" && node.depth === 2) {
      break;
    }
    nodes.push(node);
  }
  return nodes;
}

export function extractSummary(body: string): string {
  const nodes = sectionNodes(parseMarkdown(body), "핵심 요약");
  return nodes
    .map((node) => toString(node).trim())
    .filter(Boolean)
    .join(" ")
    .replace(/\s+/gu, " ")
    .trim();
}

export function normalizeDate(value: string | Date): string {
  if (value instanceof Date && Number.isNaN(value.getTime())) {
    throw new Error(`Invalid knowledge updated date: ${String(value)}`);
  }
  const normalized = value instanceof Date
    ? value.toISOString().slice(0, 10)
    : value.trim();
  if (!/^\d{4}-\d{2}-\d{2}$/u.test(normalized)) {
    throw new Error(`Invalid knowledge updated date: ${String(value)}`);
  }
  const parsed = new Date(`${normalized}T00:00:00.000Z`);
  if (
    Number.isNaN(parsed.getTime()) ||
    parsed.toISOString().slice(0, 10) !== normalized
  ) {
    throw new Error(`Invalid knowledge updated date: ${String(value)}`);
  }
  return normalized;
}

function linkTargetToId(url: string, sourceId: string): string | undefined {
  // Related notes are repository-relative Markdown links. External and
  // root-absolute URLs must never be mistaken for collection IDs.
  if (
    url.startsWith("/") ||
    url.startsWith("//") ||
    /^[a-z][a-z0-9+.-]*:/iu.test(url)
  ) {
    return undefined;
  }
  const [pathname] = url.split(/[?#]/u, 1);
  if (!pathname.endsWith(".md")) {
    return undefined;
  }

  let decodedPath: string;
  try {
    decodedPath = decodeURIComponent(pathname);
  } catch {
    throw new Error(`Related knowledge link has invalid encoding: ${url}`);
  }
  if (decodedPath.includes("\\") || decodedPath.includes("\0")) {
    throw new Error(`Related knowledge link has an invalid path: ${url}`);
  }

  const sourceDirectory = sourceId.split("/").slice(0, -1).join("/");
  const id = new URL(decodedPath, `https://knowledge.invalid/${sourceDirectory}/`)
    .pathname.replace(/^\/+|\.md$/gu, "");
  return AREAS.some(({ id: area }) => id.startsWith(`${area}/`))
    ? id
    : undefined;
}

function extractRelatedIds(body: string, sourceId: string): string[] {
  const section = sectionNodes(parseMarkdown(body), "관련 기록");
  const root: Root = { type: "root", children: section };
  const ids = new Set<string>();
  visit(root, "link", (node: Link) => {
    const id = linkTargetToId(node.url, sourceId);
    if (id !== undefined) {
      ids.add(id);
    }
  });
  return [...ids];
}

export async function getNotes(): Promise<Note[]> {
  const entries = await getCollection("knowledge");
  const notes = entries.map((entry) => {
    const body = entry.body ?? "";
    const area = entry.id.split("/", 1)[0];
    if (!AREAS.some(({ id }) => id === area)) {
      throw new Error(`Unknown knowledge area for ${entry.id}: ${area}`);
    }

    const summary = extractSummary(body);
    if (summary === "") {
      throw new Error(`Knowledge note has no 핵심 요약: ${entry.id}`);
    }

    return {
      id: entry.id,
      title: entry.data.title,
      updated: normalizeDate(entry.data.updated),
      tags: [...entry.data.tags],
      area,
      summary,
      relatedIds: extractRelatedIds(body, entry.id),
      entry,
    } satisfies Note;
  });

  const ids = new Set(notes.map(({ id }) => id));
  for (const note of notes) {
    for (const relatedId of note.relatedIds) {
      if (!ids.has(relatedId)) {
        throw new Error(
          `Knowledge note ${note.id} links to unknown note ${relatedId}`,
        );
      }
    }
  }

  return notes.sort(
    (left, right) =>
      right.updated.localeCompare(left.updated) ||
      left.title.localeCompare(right.title, "ko"),
  );
}

function headingText(node: RootContent): string | undefined {
  return node.type === "heading" ? toString(node).trim() : undefined;
}

function markdownLinks(node: RootContent): Link[] {
  const root: Root = { type: "root", children: [node] };
  const links: Link[] = [];
  visit(root, "link", (link: Link) => links.push(link));
  return links;
}

export async function getReadingPaths(): Promise<ReadingPath[]> {
  const repositoryRoot = path.resolve(
    process.env.KNOWLEDGE_REPO_ROOT ?? path.join(process.cwd(), ".."),
  );
  const readmePath = path.join(repositoryRoot, "knowledge", "README.md");
  const body = await readFile(readmePath, "utf8");
  const tree = parseMarkdown(body);
  const paths: ReadingPath[] = [];

  for (let index = 0; index < tree.children.length; index += 1) {
    const node = tree.children[index];
    if (node.type !== "heading" || node.depth !== 2) {
      continue;
    }
    const title = headingText(node);
    if (title === undefined || !title.endsWith("에서 연결한 개념")) {
      continue;
    }

    const section: RootContent[] = [];
    for (const candidate of tree.children.slice(index + 1)) {
      if (candidate.type === "heading" && candidate.depth === 2) {
        break;
      }
      section.push(candidate);
    }

    const tableIndex = section.findIndex((candidate) => candidate.type === "table");
    if (tableIndex < 0) {
      continue;
    }
    const description = section
      .slice(0, tableIndex)
      .map((candidate) => toString(candidate).trim())
      .filter(Boolean)
      .join(" ")
      .replace(/\s+/gu, " ");
    const ids = markdownLinks(section[tableIndex])
      .map((link) => linkTargetToId(link.url, "README"))
      .filter((id): id is string => id !== undefined);

    paths.push({ title, description, ids });
  }

  const availableIds = new Set((await getNotes()).map(({ id }) => id));
  for (const path of paths) {
    for (const id of path.ids) {
      if (!availableIds.has(id)) {
        throw new Error(`Reading path ${path.title} links to unknown note ${id}`);
      }
    }
  }
  return paths;
}
