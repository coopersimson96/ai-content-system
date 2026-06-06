---
name: wipe-footprint
description: >
  One-prompt digital footprint removal. Finds where a person's personal data (home
  address, phone, email, relatives) is exposed across data brokers and people-search
  sites, checks for breaches, ranks everything by risk, and auto-writes every CCPA/GDPR
  opt-out and deletion request filled and ready to send, then saves it all as a personal
  removal kit. Removes the manual searching and letter-writing. Triggers on: "/wipe-footprint",
  "wipe my footprint", "wipe my digital footprint", "erase me from the internet", "delete my
  data", "remove my data from data brokers", "stop the spam calls", "opt me out of data brokers".
---

# Wipe Footprint, One-Prompt Digital Footprint Removal

Turn a single prompt into a complete data-removal kit. The user gives their details once;
this skill does the searching, the categorizing, and writes every legal removal request for
them. The goal is to remove as much manual clicking and typing as possible: by the end the
user has a ranked action list and a copy-paste request for every site, saved to one file.

**Honesty rule (read first):** Be straight about what this does and does not do.
- It DOES: find exposures, rank by risk, and write every opt-out/deletion request, filled in.
- It does NOT auto-submit forms. Most brokers require a CAPTCHA or an email confirmation that
  a human has to complete. This skill gets the user to the "just click submit" line for each one.
- Never claim spam will "stop completely." Opting out of data brokers reduces telemarketing and
  spam-list sources; it does not kill 100% of it. Say "starts to dry up."
- Opt-out URLs change. If a bundled link looks stale, do a quick search for "{broker} opt out"
  and use the current page. Never send the user to a dead link.

---

## Step 0: Collect inputs (ask once, then go)

You need, at minimum:
- **Full name** (and any variations / maiden name / nicknames that appear online)
- **Email address(es)**
- **Phone number**
- **City + state/country** (for disambiguation, and to pick CCPA vs GDPR)

Optional but helpful: previous cities, old usernames/handles, employer.

If the user already gave these in their prompt, do NOT re-ask. If something's missing, ask for
all missing fields in ONE message, then proceed. Default jurisdiction: if US → CCPA framing; if
EU/UK → GDPR (Article 17) framing. If unknown, write both and label them.

**Privacy:** Keep the user's details only in this session and the output file on their machine.
Never send their personal data to any third party beyond the public searches needed to locate
exposures. Do not log it anywhere else.

---

## Step 1: Recon, find what's exposed (automated)

Run these in parallel where possible. Use the `firecrawl` CLI (preferred) or WebSearch.

1. **Broad search:** `firecrawl search "{full name}" "{city} {state}" --limit 10` and a second pass
   with the phone number and with the email. Capture any result that exposes personal info.
2. **Targeted broker sweep:** for each broker in `references/data-brokers.md`, assume the major
   people-search brokers (Spokeo, Whitepages, BeenVerified, MyLife, Radaris, TruePeopleSearch,
   FastPeopleSearch, Intelius, PeopleFinders, etc.) list nearly everyone in the US, include them
   in the kit by default unless the user is non-US. Optionally confirm with a quick
   `firecrawl search "{name} {city} site:{broker_domain}"`.
3. **Breach check:** if `HIBP_API_KEY` is set in the environment, query
   `https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false` with the
   `hibp-api-key` header. Otherwise, tell the user to paste their results from
   https://haveibeenpwned.com (or skip and note it). Never fabricate breach data.

Keep a working list of every exposure found: site, what's exposed, and a guess at risk.

---

## Step 2: Categorize + rank by risk

Build a single table:

| # | Site | Type | What's exposed | Risk | Action |
|---|------|------|----------------|------|--------|
| 1 | Spokeo | Data broker | Address, phone, relatives | HIGH | Opt out |
| … | … | … | … | … | … |

Types: `Data broker / people-search`, `Old account`, `Article / search result`, `Breach`.
Risk: anything exposing **home address or phone = HIGH** and goes to the top. Email-only = MEDIUM.
Old low-value accounts = LOW.

---

## Step 3: Auto-write every removal request (the core value)

For EVERY data broker / people-search site in the kit, generate a filled, copy-paste-ready
request using the user's real details. Use the template in `references/request-templates.md`
(CCPA, GDPR, and account-deletion variants). Each generated request block must include:

- The **direct opt-out URL** for that broker (from `references/data-brokers.md`).
- The **filled request text** (name, email, firm deletion + opt-out demand, the specific legal
  citation, a 30-day deadline, request for written confirmation).
- The **submission method** in one line ("paste into their web form" / "email to privacy@…").

Do not make the user fill in any blanks. Everything is pre-filled from Step 0.

---

## Step 4: Breach triage (if breaches found)

For each breach, tell the user exactly what to do: `change password`, `turn on 2FA`, or
`delete the account`. Group them so it's a short action list, not a wall of text.

---

## Step 5: Suppression plan (for what can't be deleted)

For any article or search result that can't be removed, generate **5 content angles** using the
user's name + profession that target the same keywords, so fresh pages can out-rank the bad
result over 2-3 months. Suggest where to publish (LinkedIn, Medium, personal site).

---

## Step 6: Save the removal kit (one file)

Write everything to a single markdown file at:
`~/Desktop/footprint-removal-kit-{YYYY-MM-DD}.md`

Structure: (1) the ranked action table, (2) every filled request grouped High → Low with its
opt-out link, (3) breach triage, (4) suppression plan, (5) a "dead accounts" pointer to
JustDeleteMe.xyz. Then, unless `CLAUDE_HEADLESS=1` is set, `open` the file so the user sees it.

Tell the user the headline result, e.g. "Found you on 14 data brokers + 3 breaches. Wrote 14
removal requests, ranked by risk. Open the kit and work top to bottom, most take 60 seconds each."

---

## Step 7: Auto-remove mode (actually send the requests)

When the user wants it hands-off ("do it for me", "send them all", "auto", or runs the skill
with an `auto` arg), don't just draft, SUBMIT. Work down the ranked kit, highest risk first, and
for each broker pick the path that matches how that broker actually accepts removals:

1. **Email-method brokers** (the broker's registry entry has an `opt_out_email`, or its opt-out
   page says to email a privacy address): send the filled CCPA/GDPR request from the user's
   connected email tool. Use whatever is available, in this order: the `gws` Gmail CLI, a
   connected email MCP, or SMTP creds in env. Log it as SENT.
2. **Form-method brokers** (most people-search sites): open the broker's opt-out page with the
   claude-in-chrome MCP, fill the form with the user's details, and submit it. Log as SUBMITTED.
3. **Human-gated steps:** when a broker hits a CAPTCHA or a "confirm via email" click, STOP on
   that one, tell the user the single action to take, wait, then continue to the next broker.
   Log as NEEDS-YOU. Never attempt to bypass a CAPTCHA.

**Honesty rule for this mode:** report a clean tally at the end, e.g. "Sent 6 by email, submitted
5 forms, 3 need one click from you (CAPTCHA / email confirmation), listed below." NEVER mark a
broker done while it's still waiting on a human step. Removal is not instant, brokers take days
to weeks to process and can re-list you, so tell the user to re-run this every quarter to stay
clean. (Scheduling is the user's call, just surface that it's worth repeating.)

**Requirements + graceful fallback:** auto-remove needs an email tool (for email-method brokers)
and Chrome connected via claude-in-chrome (for form-method brokers). If neither is available,
say so plainly and fall back to Step 6, hand the user the filled requests + direct opt-out links
to submit themselves. Do not pretend to have sent something you couldn't.

---

## Demo mode (for filming)

If the user says "demo" or "quick demo", run the fastest visible path:
1. Take their name + email + city.
2. Do ONE `firecrawl search` so there's a real result on screen.
3. Generate the ranked table + 3 filled requests (Spokeo, Whitepages, BeenVerified).
4. Save + open the kit.
This produces a real, filmable result in under ~90 seconds without working the full list.

---

## What to report at the end

A tight summary: how many brokers + breaches found, how many requests written, where the kit is
saved, and the single next action ("open the kit, start at #1"). Offer the auto-remove mode (Step 7)
and the suppression plan as follow-ups.
