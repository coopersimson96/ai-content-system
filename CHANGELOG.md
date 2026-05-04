# Changelog

All notable changes to the AI Content System will be documented in this file.

## [1.2.0] - 2026-05-04

### Added
- **`ig-analytics`** - Hourly Instagram analytics pipeline. Pulls per-post and account-level insights from the Meta Graph API into Supabase, mirrors live values into a Notion dashboard, and runs a daily Claude routine that classifies each post into Outlier / Average / Underperformer tiers with a 2-3 sentence "why" note. Includes Vercel cron handler, 5 utility scripts, init migration with RLS, and a parameterized Creative Director prompt template.
- **`video-editor`** - 9:16 short-form video pipeline using Hyperframes. Workflow wrapper that ships three style archetypes (sage-stack, editorial-magazine, screen-face-split) with deconstruction docs and pattern catalogs, the orange frosted-glass + karaoke pill overlay defaults, render contract gotchas, and a build-your-own-style-guide methodology.
- **Hyperframes suite (6 skills)** by Nate Herkai / Heygen, Apache 2.0 upstream: `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `gsap`, `website-to-hyperframes`, `claude-design-hyperframes`. Bundled so users can `git pull && cp -r skills/*` once and have the whole video stack. Attribution in `skills/THIRD_PARTY.md`.
- **`skills/THIRD_PARTY.md`** - Top-level attribution document covering all third-party skills (Hyperframes Suite, SEO Suite, Ads Suite, Blog Suite, last30days).

### Changed
- **`hooks`** - Major upgrade. Added 100-point 4-dimension ranking rubric (Scroll Stop / Word Economy / Pattern Interrupt / Authority Pack), tier gates (88+ Outlier, 78-87 Strong, 68-77 iterate, <68 reject), pre-flight checklist, triple-stacked hook rule (text + visual + verbal at second 0), Zeigarnik open-loop principle, outcome-over-audience framing, B/A vs open-loop framework choice, conversational glue rule, visual hook scoring layer, and dual CTA stack.
- **`content-scripting`** - Major upgrade. Cross-links to the new `hooks` rubric. Mandatory voice check pre-write step. Pre-flight + scored hook table required before script body. Refreshed voice and density rules. Dual CTA stack. References `carousel-builder`, `newsletter`, `blog-write`, `hand-raiser`.
- **`content-master`** - Minor cross-references to the new rubric.
- **README.md** - Bumped skill count to 69 (from 52). Added Instagram Analytics + Video Production categories to description.

### Repo
- The dual-repo experiment from the v1.0.0 release (`coopersimson96/ai-content-system-dev`) is being archived. This repo is the single source of truth.

## [1.0.0] - 2026-03-03

### Added
- Initial release with 52 skills across 7 categories
- Content Creation: content-master, content-scripting, content-pipeline, topic-researcher, hooks, inspiration-library, last30days
- Transcript & Lead Magnets: transcript, hand-raiser
- SEO: 13 skills (seo, seo-audit, seo-technical, seo-content, seo-schema, seo-sitemap, seo-page, seo-geo, seo-hreflang, seo-programmatic, seo-competitor-pages, seo-images, seo-plan)
- Ads: 13 skills (ads, ads-audit, ads-google, ads-meta, ads-linkedin, ads-tiktok, ads-microsoft, ads-youtube, ads-budget, ads-creative, ads-competitor, ads-landing, ads-plan)
- Blog: 13 skills (blog, blog-write, blog-rewrite, blog-analyze, blog-audit, blog-brief, blog-calendar, blog-chart, blog-geo, blog-outline, blog-repurpose, blog-schema, blog-seo-check, blog-strategy)
- Image Gen & Design: nano-banana, frontend-design
- E-commerce: ecommerce-cro, shopify-store-design
- Setup Skills: notion-setup, gdocs-setup
- Generic PDF generator (scripts/pdf_generator.py)
- Lead pages starter template (lead-pages-starter/)
- Config templates for Notion, Google Docs, and Supadata
- Shared scripts: gdocs_push.py, gdocs_formatter.py, gdrive_upload.py

