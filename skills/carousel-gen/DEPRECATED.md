# DEPRECATED — Use `carousel-builder` instead

The `carousel-gen` skill has been replaced by `carousel-builder`.

## What changed

| | `carousel-gen` (old) | `carousel-builder` (new) |
|---|---|---|
| Rendering | HTML/CSS via Playwright | Real images via kie.ai gpt-image-2 MCP |
| Workflow | Plan → render all slides | Reference-first: copy → brief → 3 anchors → locked anchor → matched slides one at a time |
| Output | Browser-rendered slide PNGs | Editorial AI-generated slides with locked visual DNA |
| Style system | One templated HTML skin | Pluggable style skins (build your own per `build-your-own-skin.md`) |

The new skill is at `skills/carousel-builder/`. Read its `README.md` and `SKILL.md` to get started.

## Migration

If you have a `carousel-gen` workflow currently running:

1. Install the kie.ai MCP (sign up at kie.ai for an API key)
2. Switch your skill invocation to `carousel-builder`
3. Use `references/style-field-manual.md` as a starting reference, then build your own skin per `references/build-your-own-skin.md`

This deprecation tombstone will be removed in a future release.
