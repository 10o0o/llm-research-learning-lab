import type {
  Definition,
  Image,
  ImageReference,
  Link,
  Root,
  RootContent,
} from "mdast";
import { toString } from "mdast-util-to-string";
import type { Plugin } from "unified";
import { visit } from "unist-util-visit";

import { resolveContentLink } from "./urls";

export interface KnowledgeMarkdownOptions {
  repoRoot: string;
  base?: string;
}

function ignoreInPagefind(node: RootContent): void {
  const data = node.data as { hProperties?: Record<string, unknown> } | undefined;
  node.data = {
    ...node.data,
    hProperties: {
      ...data?.hProperties,
      "data-pagefind-ignore": "",
    },
  };
}

const remarkKnowledgeLinks: Plugin<[KnowledgeMarkdownOptions], Root> = (
  options,
) => {
  const { repoRoot, base } = options;

  return (tree, file) => {
    const firstHeading = tree.children.findIndex(
      (node) => node.type === "heading" && node.depth === 1,
    );
    if (firstHeading >= 0) {
      tree.children.splice(firstHeading, 1);
    }

    // Related links remain visible navigation, but add little value to body
    // snippets. Mark the complete section for Pagefind without removing it.
    const relatedHeading = tree.children.findIndex(
      (node) =>
        node.type === "heading" &&
        node.depth === 2 &&
        toString(node).trim() === "관련 기록",
    );
    if (relatedHeading >= 0) {
      for (const node of tree.children.slice(relatedHeading)) {
        if (
          node !== tree.children[relatedHeading] &&
          node.type === "heading" &&
          node.depth === 2
        ) {
          break;
        }
        ignoreInPagefind(node);
      }
    }

    // Raw HTML can carry uninspected href/src attributes around the guarded
    // Markdown link pipeline. Knowledge notes deliberately do not support it.
    visit(tree, "html", () => {
      throw new Error("Raw HTML is unsupported in knowledge Markdown");
    });

    const sourceFile = file.path;
    const definitions = new Set<string>();
    visit(tree, (node) => {
      if (node.type === "imageReference") {
        return;
      }
      if (
        node.type !== "link" &&
        node.type !== "image" &&
        node.type !== "definition"
      ) {
        return;
      }
      if (sourceFile === undefined) {
        throw new Error(
          `Cannot resolve relative link without a source file: ${node.url}`,
        );
      }

      if (node.type === "definition") {
        definitions.add(node.identifier.toLowerCase());
      }
      (node as Link | Image | Definition).url = resolveContentLink(
        node.url,
        sourceFile,
        repoRoot,
        base,
      );
    });

    visit(tree, "imageReference", (node: ImageReference) => {
      if (!definitions.has(node.identifier.toLowerCase())) {
        throw new Error(`Image reference has no definition: ${node.identifier}`);
      }
    });
  };
};

export default remarkKnowledgeLinks;
