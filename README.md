# AI Content System

A complete AI-powered content creation system built on Claude Code. 69 skills across 8 categories — from topic research to script production, SEO audits, ad optimization, blog writing, image generation, e-commerce CRO, Instagram analytics, and 9:16 video production with Hyperframes.

## What's Included

| Category | Skills | What It Does |
|---|---|---|
| Content Creation | 7 | Topic research, script writing, hook frameworks, inspiration library, pipeline management |
| Transcript & Lead Magnets | 2 | Video transcript extraction (any platform), PDF lead magnet generator |
| SEO | 13 | Full site audits, technical SEO, schema, content quality, GEO, programmatic SEO |
| Ads | 13 | Multi-platform audits (Google, Meta, LinkedIn, TikTok, Microsoft, YouTube) |
| Blog | 13 | Blog writing, rewriting, analysis, strategy, calendars, schema, repurposing |
| Image Gen & Design | 2 | AI image generation, frontend design |
| E-commerce | 2 | CRO expertise, Shopify store design |

## Quick Start

### 1. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 2. Clone This Repo

```bash
git clone https://github.com/coopersimson96/ai-content-system.git ~/ai-content-system
```

### 3. Install Skills

```bash
cp -r ~/ai-content-system/skills/* ~/.claude/skills/
```

### 4. Verify

Open Claude Code and type `/hooks` — you should see the skill activate.

## Updating

```bash
cd ~/ai-content-system && git pull && cp -r skills/* ~/.claude/skills/
```

One command. Instant updates.

## Configuration

Most skills work out of the box. For full functionality, connect these integrations:

| Integration | Required For | Setup |
|---|---|---|
| Notion MCP | Content pipeline, inspiration library | See Whop guide: Module 1.2 |
| Google Docs/Drive | Script export, PDF hosting | See Whop guide: Module 1.3 |
| Supadata API | Video transcript extraction | See Whop guide: Module 1.4 |
| Gemini API | Image generation | See Whop guide: Module 1.5 |

Config templates are in `config-templates/`.

## Repo Structure

```
ai-content-system/
├── skills/              # 52 Claude Code skills
├── scripts/             # Shared Python scripts (PDF gen, Google Docs, Drive)
├── config-templates/    # Example config files with placeholders
├── lead-pages-starter/  # Vercel landing page template for lead capture
└── output/              # Default output directory
```

## Getting Help

Full setup guides, video walkthroughs, and community support are available through the [Whop community](https://whop.com/).

## License

For use by active community members only. Do not redistribute.
