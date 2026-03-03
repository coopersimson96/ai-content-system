---
name: content-pipeline
description: Manage your content production pipeline — update script statuses, log performance metrics, query what needs filming, manage your posting calendar. Works with your Notion Script Library.
argument-hint: "mark script 3 as filmed" or "log metrics for script 5" or "what needs filming?" or "schedule next week"
context: conversation
---

# Content Pipeline Manager

Manages the production pipeline for scripts stored in the Notion Script Library database. Uses Notion MCP tools to query and update entries.

---

## Setup Check

On every invocation, first verify the pipeline is configured:

1. Read `~/.config/notion-content/config.json` to get the `script_library_db_id`
2. If the file doesn't exist, tell the user:
   > Pipeline isn't set up yet. Run `/notion-setup` first to create your Script Library database.

Store the database ID for use in all subsequent operations.

---

## Intent Detection

Parse `$ARGUMENTS` and detect what the user wants:

### Status Updates
**Trigger:** "mark", "move", "set status", "filmed", "edited", "scheduled", "posted", script number + status word

**Examples:**
- "mark script 3 as filmed" → Status = `Filmed`
- "script 5 is ready to post" → Status = `Ready To Post`
- "move scripts 1-4 to editing" → Status = `Editing` for scripts 1-4
- "posted script 7" → Status = `Posted`
- "idea for a new video" → Status = `Ideas/Topics`

**Action:**
1. Use `notion-query-database-view` with the database ID to find the script(s) by Script Number
2. Use `notion-update-page` to update the Status property
3. Confirm: "Script {N} → {Status}"

**Status mapping (fuzzy match):**
- idea/topic/new → `Ideas/Topics`
- script/scripted/written → `Scripts`
- filming/film/shoot → `Filming`
- filmed/shot/recorded → `Filmed`
- editing/edited/in editing → `Editing`
- ready/ready to post/done → `Ready To Post`
- posted/published/live → `Posted`

---

### Performance Metrics
**Trigger:** "log metrics", "metrics for", "views", "retention", numbers after a script reference

**Examples:**
- "log metrics for script 3: 15K views, 65% retention, 342 likes, 12 comments, 45 shares, 89 saves"
- "script 5 got 10000 views"
- "update retention for script 2: 72%"

**Action:**
1. Find the script by Script Number
2. Use `notion-update-page` to update the metric fields:
   - Views → `Views` property
   - Retention / 3s retention → `3s Retention` property (store as decimal, e.g., 65% → 0.65)
   - Likes → `Likes` property
   - Comments → `Comments` property
   - Shares → `Shares` property
   - Saves → `Saves` property
3. If Status isn't already `Posted`, auto-update to `Posted`
4. Confirm with a summary of what was updated

**Number parsing:**
- "15K" → 15000
- "1.2M" → 1200000
- "65%" → 0.65 (for retention)
- Plain numbers pass through

#### Outlier Auto-Detection (after saving metrics)

After successfully saving metrics with a Views value, automatically check for outlier performance:

1. Read `~/.config/notion-content/config.json` to check for `inspiration_data_source_id`. If missing, skip silently.
2. Query the Script Library for all scripts with Status = `Posted` that share the same Series or Topic as the current script
3. If fewer than 5 posted scripts in the group, skip (not enough baseline)
4. Calculate median views for the group
5. If the current script's Views >= 3x median AND Views >= 100,000:
   - Auto-save to Inspiration Library using `notion-create-pages` with `data_source_id` = `inspiration_data_source_id`:
     - **Title** = Script Title
     - **Type** = `My Content`
     - **Source** = `My Content`
     - **Performance Tier** = `Outlier`
     - **Platform** = same as script
     - **Engagement Metric** = "{Views} views ({X}x median)"
     - **Hook Framework** = Hook Framework A from the script
     - **Hook Text** = extract from script page if available
     - **Topic Tags** = derived from Topic
     - **date:Date Added:start** = today
     - **Notes** = "Auto-detected outlier. {X}x median views in {Series/Topic} group."
   - Report: "Script #{N} hit outlier threshold ({X}x median). Saved to Inspiration Library."
6. If not an outlier, proceed silently

---

### Pipeline Queries
**Trigger:** "what needs", "show me", "list", "how many", "status", "pipeline", "what's next"

**Examples:**
- "what needs filming?" → query Status = `Scripts`
- "show me the pipeline" → count by status
- "what's in editing?" → query Status = `Editing`
- "how many scripts are posted?" → count Status = `Posted`
- "what's filmed?" → query Status = `Filmed`

**Action:**
1. Use `notion-query-database-view` with appropriate filters
2. Format results as a clean list:
   ```
   Approved Scripts (3):
   - Script 2 — "AI Scheduling Pain"
   - Script 5 — "Client Follow-Up Automation"
   - Script 8 — "Invoice Nightmare"
   ```
3. For "show pipeline" / overview, show counts per status:
   ```
   Pipeline Overview:
   - Ideas/Topics: 2
   - Scripts: 4
   - Filming: 1
   - Filmed: 0
   - Editing: 2
   - Ready To Post: 1
   - Posted: 5
   ```

#### Underperformer Nudge

After showing a pipeline overview or metrics summary, check for underperforming posted scripts:

1. From the query results, identify Posted scripts with Views data
2. Calculate median views for the group (need at least 5 Posted scripts)
3. If any Posted scripts have Views < 0.5x the median:
   > {N} scripts are underperforming. Want me to refresh them with new hooks from your library? Just say "refresh SF #{N}" for any of them.

This is a suggestion only — it routes the user back to content-scripting's refresh flow if they act on it.

---

### Calendar Management
**Trigger:** "schedule", "spread", "post date", "next week", "calendar", "when to post"

**Examples:**
- "spread the AI for Service Businesses series across next week"
- "schedule script 3 for Monday"
- "set post dates for scripts 1-5 starting Feb 24"

**Action:**
1. Find the relevant scripts
2. Calculate post dates:
   - Series scripts: space 1-2 days apart
   - If user says "next week": start Monday of next week
   - If user gives a start date: use that
   - Default spacing: every other day (Mon, Wed, Fri, Sun, Tue...)
3. Use `notion-update-page` to set Post Date for each script
4. Also set Status to `Ready To Post` if currently `Scripts` or `Editing`
5. Show the schedule:
   ```
   Scheduled:
   - Mon Feb 24: Script 1 — "AI Scheduling Pain"
   - Wed Feb 26: Script 2 — "Client Follow-Up"
   - Fri Feb 28: Script 4 — "Invoice Automation"
   ```

---

### Batch Operations
**Trigger:** "mark all", "update all", "batch", multiple script numbers

**Examples:**
- "mark scripts 1, 3, 5 as ready to film"
- "all ideas → scripts"

**Action:**
1. Query the relevant scripts
2. Batch update using `notion-update-page` for each
3. Summarize: "Updated {N} scripts → {Status}"

---

### Notes
**Trigger:** "add note", "note for script", "notes"

**Examples:**
- "add note to script 3: need to re-record the hook"
- "note for script 5: waiting on screen recording"

**Action:**
1. Find the script
2. Use `notion-update-page` to update the Notes property
3. Confirm

---

## Conversation Style

- **Quick confirmations.** "Done. Script 3 → Filming." Not "I've successfully updated Script 3's status to Filming in your Notion database."
- **Proactive suggestions.** After updating status, mention what's next: "Script 3 is now in Filming. 2 more scripts are Ready to Film when you're done."
- **Batch-friendly.** If the user updates one script, ask if they want to update related ones: "Scripts 4 and 5 are from the same series — want to move those too?"

---

## Opening (No Arguments)

If invoked without arguments:

> What do you need?
>
> I can:
> - **Update statuses** — "mark script 3 as filmed"
> - **Log metrics** — "script 5: 15K views, 65% retention"
> - **Check pipeline** — "what needs filming?"
> - **Manage calendar** — "schedule the AI series for next week"
> - **Add notes** — "note for script 3: need better hook"
>
> Or just tell me what you're working on.
