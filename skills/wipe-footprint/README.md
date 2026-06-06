# wipe-footprint

A Claude Code skill that wipes your digital footprint in one prompt. It finds where your
personal data (home address, phone, email, relatives) is exposed across data brokers and
people-search sites, ranks everything by risk, and **auto-writes every CCPA/GDPR opt-out and
deletion request** — filled in and ready to send — then saves it all as a personal removal kit.

It does for free what paid services like Incogni or DeleteMe charge you monthly for.

> **What it does NOT do:** auto-submit forms. Most brokers require a CAPTCHA or an email
> confirmation that a human has to complete. The skill gets you to the "just click submit" line
> for every site. Opting out also reduces spam over time — it doesn't kill 100% of it, and
> brokers can re-list you, so it's worth re-running every few months.

---

## What you need

| Tool | Required? | What it's for |
|---|---|---|
| **Claude Code** | Required | Runs the skill. |
| **Firecrawl** | Recommended | Faster, more thorough recon of where you're exposed. The skill falls back to Claude's built-in web search if you skip it. |
| **Have I Been Pwned API key** | Optional | Auto-checks which breaches your email is in. Without it, the skill just points you to the site to check manually. |
| **Chrome (claude-in-chrome)** | Optional | "Auto-fill" mode that opens each opt-out page and pre-fills it. Off by default. |

You can run the whole skill on Claude Code alone — everything else just makes it faster.

---

## Setup

### 1. Install the skill

If you cloned the full system:
```bash
cp -r ~/ai-content-system/skills/wipe-footprint ~/.claude/skills/
```

Or copy just this folder into `~/.claude/skills/wipe-footprint/`.

Open Claude Code and the `/wipe-footprint` skill will be available.

### 2. (Recommended) Set up Firecrawl

Firecrawl makes the "find what's exposed" step much stronger. Install the Firecrawl CLI and grab
a free API key at [firecrawl.dev](https://firecrawl.dev):

```bash
# install the CLI (see firecrawl.dev for the latest command)
# then set your key:
export FIRECRAWL_API_KEY="fc-your-key-here"
```

Add that line to your `~/.zshrc` or `~/.bashrc` so it persists. If you skip this, the skill
automatically uses Claude Code's built-in web search instead.

### 3. (Optional) Add a Have I Been Pwned key

For automatic breach checking, get a key at
[haveibeenpwned.com/API/Key](https://haveibeenpwned.com/API/Key) and set:

```bash
export HIBP_API_KEY="your-hibp-key"
```

Without it, the skill simply tells you to check the site yourself — everything else still works.

See `config-templates/wipe-footprint-env.example` in this repo for a copy-paste env file.

---

## How to use it

In Claude Code, just say:

```
/wipe-footprint
```

It will ask for your name, email, phone, and city (once), then:

1. **Finds** every data broker / people-search site exposing you, and checks your breaches.
2. **Ranks** everything by risk (anything exposing your home address or phone goes to the top).
3. **Writes** a filled-in, legally-grounded removal request for every site, with the direct
   opt-out link and a 30-day deadline.
4. **Saves** it all to `~/Desktop/footprint-removal-kit-YYYY-MM-DD.md` and opens it.

Then you just work down the list and paste each request into the broker's opt-out page.

### Quick demo

```
/wipe-footprint demo
```

Runs the fastest visible path (one real search + a few filled requests) in about 90 seconds —
handy for screen recordings.

### Auto-fill mode (advanced)

Once you have the kit, you can say *"open them for me"* and, if Chrome is connected, the skill
will open each opt-out page and pre-fill it. You still solve any CAPTCHA / email confirmation
yourself.

---

## What's in this folder

```
wipe-footprint/
├── SKILL.md                       # the skill instructions Claude follows
├── README.md                      # this file
└── references/
    ├── data-brokers.md            # 20+ broker opt-out URLs, ranked by priority
    └── request-templates.md       # CCPA / GDPR / account-deletion letter templates
```

Opt-out URLs change over time — if a link 404s, search "[broker name] opt out" for the current page.
