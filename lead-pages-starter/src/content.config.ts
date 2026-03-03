import { defineCollection, z } from 'astro:content';

const resources = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    headline: z.string(),
    subtitle: z.string(),
    pdfUrl: z.string().url(),
    valueProps: z.array(z.string()),
    ctaText: z.string().default('Get the Free Guide'),
    previewDescription: z.string(),
    pages: z.number(),
    type: z.enum(['guide', 'cheatsheet', 'checklist', 'quick-reference', 'how-to-guide']),
  }),
});

export const collections = { resources };
