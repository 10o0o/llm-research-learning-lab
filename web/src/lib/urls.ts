import {
  existsSync,
  lstatSync,
  realpathSync,
} from "node:fs";
import path from "node:path";

const REPOSITORY_URL =
  "https://github.com/10o0o/llm-research-learning-lab";

function normalizedBase(base: string): string {
  const segments = base.split("/").filter(Boolean);
  return segments.length === 0 ? "/" : `/${segments.join("/")}/`;
}

export function withBase(
  pathname: string,
  base = import.meta.env.BASE_URL,
): string {
  const prefix = normalizedBase(base);
  const suffix = pathname.replace(/^\/+/, "");
  return suffix.length === 0 ? prefix : `${prefix}${suffix}`;
}

export function noteUrl(
  id: string,
  base = import.meta.env.BASE_URL,
): string {
  const segments = id.split("/");
  if (
    segments.length < 2 ||
    segments.some(
      (segment) =>
        segment.length === 0 ||
        segment === "." ||
        segment === ".." ||
        !/^[a-z0-9][a-z0-9-]*$/u.test(segment),
    )
  ) {
    throw new Error(`Invalid knowledge note id: ${id}`);
  }

  return withBase(
    `knowledge/${segments.map(encodeURIComponent).join("/")}/`,
    base,
  );
}

function isInside(candidate: string, root: string): boolean {
  const relative = path.relative(root, candidate);
  return (
    relative === "" ||
    (!relative.startsWith("..") && !path.isAbsolute(relative))
  );
}

function assertNoSymlink(candidate: string, root: string): void {
  const relative = path.relative(root, candidate);
  if (!isInside(candidate, root)) {
    throw new Error(`Content link escapes the repository: ${relative}`);
  }

  let current = root;
  for (const segment of relative.split(path.sep).filter(Boolean)) {
    current = path.join(current, segment);
    if (lstatSync(current).isSymbolicLink()) {
      throw new Error(`Content links may not traverse symlinks: ${relative}`);
    }
  }
}

function encodeRepositoryPath(repoRelative: string): string {
  return repoRelative.split(path.sep).map(encodeURIComponent).join("/");
}

export function resolveContentLink(
  target: string,
  sourceFile: string,
  repoRoot: string,
  base = import.meta.env.BASE_URL,
): string {
  if (target === "" || target.startsWith("#") || target.startsWith("//")) {
    return target;
  }

  const scheme = target.match(/^([a-z][a-z0-9+.-]*):/iu)?.[1]?.toLowerCase();
  if (scheme !== undefined) {
    if (["http", "https", "mailto", "tel"].includes(scheme)) {
      return target;
    }
    throw new Error(`Unsupported content link scheme: ${scheme}`);
  }

  if (target.startsWith("/")) {
    throw new Error(`Root-absolute content links are not allowed: ${target}`);
  }

  const match = target.match(/^([^?#]*)([?#].*)?$/u);
  if (match === null || match[1] === "") {
    return target;
  }

  let decodedPath: string;
  try {
    decodedPath = decodeURIComponent(match[1]);
  } catch {
    throw new Error(`Content link has invalid percent encoding: ${target}`);
  }
  if (decodedPath.includes("\\") || decodedPath.includes("\0")) {
    throw new Error(`Content link contains an invalid path: ${target}`);
  }

  const root = realpathSync(repoRoot);
  const source = path.isAbsolute(sourceFile)
    ? path.normalize(sourceFile)
    : path.resolve(root, sourceFile);
  if (!existsSync(source)) {
    throw new Error(`Content source file does not exist: ${sourceFile}`);
  }
  assertNoSymlink(source, root);
  if (!lstatSync(source).isFile()) {
    throw new Error(`Content source is not a file: ${sourceFile}`);
  }

  const resolved = path.resolve(path.dirname(source), decodedPath);
  if (!isInside(resolved, root)) {
    throw new Error(`Content link escapes the repository: ${target}`);
  }

  const lexicalRelative = path.relative(root, resolved);
  const pathSegments = lexicalRelative.split(path.sep);
  if (pathSegments.some((segment) => segment.toLowerCase() === "private")) {
    throw new Error(`Content link targets a private path: ${target}`);
  }
  if (!existsSync(resolved)) {
    throw new Error(`Content link target does not exist: ${target}`);
  }
  assertNoSymlink(resolved, root);
  if (!lstatSync(resolved).isFile()) {
    throw new Error(`Content link target is not a file: ${target}`);
  }

  const realTarget = realpathSync(resolved);
  if (!isInside(realTarget, root)) {
    throw new Error(`Content link resolves outside the repository: ${target}`);
  }

  const repoRelative = path.relative(root, realTarget);
  const [topLevel] = repoRelative.split(path.sep);
  const suffix = match[2] ?? "";

  if (topLevel === "knowledge" && path.extname(repoRelative) === ".md") {
    const id = repoRelative
      .slice(`knowledge${path.sep}`.length, -".md".length)
      .split(path.sep)
      .join("/");
    return `${noteUrl(id, base)}${suffix}`;
  }

  if (topLevel === "practice" || topLevel === "til") {
    return `${REPOSITORY_URL}/blob/main/${encodeRepositoryPath(repoRelative)}${suffix}`;
  }

  throw new Error(`Unsupported local content link target: ${target}`);
}
