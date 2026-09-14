import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const knowledge = defineCollection({
  loader: glob({
    base: "../knowledge",
    pattern: "*/*.md",
    generateId: ({ entry }) => entry.replace(/\.md$/u, ""),
  }),
  schema: z.object({
    title: z.string().min(1),
    updated: z
      .union([z.string(), z.date()])
      .transform((value) =>
        value instanceof Date
          ? value.toISOString().slice(0, 10)
          : value,
      )
      .refine((value) => /^\d{4}-\d{2}-\d{2}$/u.test(value), {
        message: "updated must use YYYY-MM-DD",
      }),
    tags: z.array(z.string().min(1)),
  }),
});

export const collections = { knowledge };
