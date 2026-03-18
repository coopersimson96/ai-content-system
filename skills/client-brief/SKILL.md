---
name: client-brief
description: Generate a 2-page interactive client proposal (brief + work plan) with SVG diagrams, accordion deliverables, architecture maps, ROI charts, and Vercel deployment.
argument-hint: "brief for [client name]" or "[client] content automation proposal"
context: conversation
---

# Client Brief Generator

Create professional client proposals in minutes instead of hours.

You hop on a discovery call with a potential client. You take notes. Then instead of spending 3 hours formatting a PDF, you run one command and get a polished, animated web proposal with a live URL you can text to them.

That's what this skill does.

---

## What You Get

Two web pages that make your services look premium:

**Page 1: The Pitch** - Shows the client their problem, your solution, the ROI math, and your implementation plan. Includes animated charts, architecture diagrams, and a timeline.

**Page 2: The Work Plan** - Every deliverable gets its own expandable card with a custom diagram. Plus an architecture map, rollout timeline, and a big "Let's Build This" button with your price.

Both pages work on phones, tablets, and desktop. They have scroll animations, interactive diagrams, and stay private (hidden from Google).

---

## How to Install

You need Claude Code already installed (Module 0 covers this).

**Step 1:** Copy the skill folder to your skills directory:

```bash
cp -r client-brief ~/.claude/skills/client-brief
```

**Step 2 (optional):** If you want to put your proposals on a live URL, install Vercel:

```bash
npm i -g vercel
```

That's it. No API keys. No accounts to set up. No config files.

---

## How to Use

**Step 1:** Open Claude Code:

```
claude
```

**Step 2:** Run the skill with your client's name:

```
/client-brief "Acme Corp content automation proposal"
```

**Step 3:** Answer the questions Claude asks you. Here's what it needs:

| What Claude Asks | Example Answer |
|---|---|
| Client name | Acme Corp |
| Contact person | Jane Smith |
| Their industry | SaaS company, B2B marketing |
| What you're building for them | Content automation system |
| Which platforms | Instagram, TikTok, YouTube |
| What you'll deliver | List each thing with a one-line description |
| Your price | $4,500 |
| Your name and email | Your Name, you@email.com |
| Rollout phases | Phase 1: Setup, Phase 2: Launch, etc. |
| What the client needs to give you | Logins, brand assets, content examples |

**Shortcut:** If you have a transcript from your discovery call, just paste the whole thing. Claude reads it and fills in the answers for you. It'll confirm before building anything.

**Step 4:** Claude generates two HTML files and opens them in your browser. Check that everything looks right.

**Step 5:** Claude deploys to Vercel and gives you a live URL. Send it to your client.

---

## Changing the Colors

The proposals come with a clean default look (cream background, teal and copper accents). To match your own brand:

1. Open the generated `index.html` file
2. Find the `colors` section near the top (around line 15)
3. Swap the color codes for your brand colors
4. Save and refresh the browser

Do the same for `workplan.html`.

No special tools needed. Just edit, save, refresh.

---

## What the Proposal Includes

### Pitch Page
- Navigation bar that follows you as you scroll
- Hero section with key stats about the project
- Time audit showing where the client wastes hours
- Architecture diagram of your solution
- Feature cards with "time saved" badges
- ROI comparison (before vs. after)
- Implementation timeline
- Next steps

### Work Plan Page
- Client logo (if you have a URL for it)
- Project details (who, what, when, how much)
- Expandable deliverable cards - click one to see the details and diagram, click another and the first one closes
- Architecture map you can hover over to see how pieces connect
- Rollout timeline
- What the client needs to provide
- Big pricing section with a call-to-action

Every single deliverable gets its own custom diagram. Not stock images. Diagrams that actually show how that specific feature works.

---

## Common Questions

**Do I need Vercel?**
No. The files work by just opening them in your browser. Vercel gives you a live URL to share, but you can use any hosting (Netlify, GitHub Pages, etc.) or just email the files.

**Can clients find my proposals on Google?**
No. Every proposal has headers that tell Google not to index it. Only people with the direct link can see it.

**Can I edit the proposal after it's generated?**
Yes. The files are plain HTML. Open them in any text editor, make changes, save, and refresh your browser.

**What if I don't have a discovery call transcript?**
No problem. Just answer Claude's questions one at a time. The transcript shortcut is faster but not required.

**Can I use this for any type of service?**
Yes. The skill works for any service-based proposal - web development, content creation, consulting, design, marketing, automation. Claude adapts the diagrams and language to match your industry.

**What if I mess something up?**
Run the skill again. It creates a fresh set of files each time. Your old version stays in its folder.

---

## Tips

- **Longer notes = better proposals.** The more detail you give Claude about the project, the more specific and impressive the deliverables will be.
- **Include your price in the notes.** Claude builds ROI projections around your investment number.
- **Have a logo URL?** Drop it in. The work plan page puts it at the top. No logo? It skips that section cleanly.
- **Review the diagrams.** Each deliverable gets a custom diagram. Make sure they match what you're actually building before sending to the client.
