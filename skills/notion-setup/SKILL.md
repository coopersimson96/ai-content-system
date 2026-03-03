---
name: notion-setup
description: One-time setup that creates the Script Library database in Notion with all production pipeline properties, views, and configuration.
argument-hint: (no arguments needed)
context: conversation
---

# Notion Content Pipeline Setup

Creates the full content production infrastructure in Notion using the Notion MCP tools.

---

## Pre-flight Check

Before anything, verify the Notion MCP is connected:

1. Use `notion-get-teams` to check which workspace is connected
2. If it returns a workspace → proceed
3. If it fails or returns an error → STOP and tell the user:

> The Notion MCP isn't connected. To fix this:
> 1. Go to [claude.ai/settings](https://claude.ai/settings)
> 2. Find **Integrations > Notion**
> 3. Click **Connect** and authorize with your Notion account
> 4. Then run `/notion-setup` again.

---

## Step 1: Create Parent Page

Use `notion-search` to check if a "Content Production Hub" page already exists.

If not, use `notion-create-pages` to create a new page:
- **Title:** "Content Production Hub"
- **Content:** Brief description: "Central hub for all content production — scripts, pipeline, analytics."

Save the page ID — the database will be created inside this page.

---

## Step 2: Create Script Library Database

Use `notion-create-database` to create a database inside the Content Production Hub page with these properties:

**Database title:** "Script Library"

**Properties:**

| Property Name | Type | Configuration |
|---|---|---|
| Script Title | `title` | (default title property) |
| Script Number | `number` | number format: `number` |
| Status | `select` | Options: `Ideas/Topics`, `Scripts`, `Filming`, `Filmed`, `Editing`, `Ready To Post`, `Posted` |
| Platform | `multi_select` | Options: `Instagram Reels`, `TikTok`, `YouTube Shorts`, `Facebook Reels` |
| Series | `select` | (empty — populated as scripts are added) |
| Topic | `rich_text` | |
| Hook Framework A | `select` | Options: `Curiosity Gap`, `Proof-First`, `Pain Point`, `Contrarian`, `This Cost Me Thousands`, `Unexpected Confession`, `Question Hook`, `Pattern Interrupt`, `Before vs After`, `Test / Experiment` |
| Hook Framework B | `select` | Same options as Hook Framework A |
| Hook Framework C | `select` | Same options as Hook Framework A |
| Pain Point Source | `rich_text` | |
| Batch | `rich_text` | |
| Post Date | `date` | |
| Google Doc URL | `url` | |
| Views | `number` | number format: `number_with_commas` |
| 3s Retention | `number` | number format: `percent` |
| Likes | `number` | number format: `number_with_commas` |
| Comments | `number` | number format: `number_with_commas` |
| Shares | `number` | number format: `number_with_commas` |
| Saves | `number` | number format: `number_with_commas` |
| Notes | `rich_text` | |

---

## Step 3: Save Configuration

After creating the database, save the IDs for other skills to use:

```bash
mkdir -p ~/.config/notion-content
```

Write `~/.config/notion-content/config.json`:

```json
{
  "workspace": "YOUR_WORKSPACE_NAME",
  "hub_page_id": "{THE_HUB_PAGE_ID}",
  "script_library_db_id": "{THE_DATABASE_ID}"
}
```

Replace `YOUR_WORKSPACE_NAME` with the actual workspace name returned from the pre-flight check.

Also run `notion-update-data-source` with the database ID so the MCP can query it efficiently.

---

## Step 4: Explain Manual View Setup

Tell the user:

> The Script Library database is created! Now set up these views in Notion for the best experience:
>
> ### Board View (Production Pipeline)
> 1. Open the Script Library database in Notion
> 2. Click **+ Add a view** → **Board**
> 3. Group by: **Status**
> 4. This gives you a kanban board: Ideas/Topics → Scripts → Filming → Filmed → Editing → Ready To Post → Posted
>
> ### Calendar View (Content Calendar)
> 1. Click **+ Add a view** → **Calendar**
> 2. Date property: **Post Date**
> 3. Now you can see your posting schedule visually
>
> ### Table View (Performance Dashboard)
> 1. Click **+ Add a view** → **Table**
> 2. Filter: Status **is** `Posted`
> 3. Show columns: Script Title, Platform, Views, 3s Retention, Likes, Comments, Shares, Saves
> 4. Sort by: Views (descending)
>
> These views are best set up manually in Notion since the API doesn't support creating views directly.

---

## Step 5: Verify

Confirm everything worked:

1. Use `notion-search` to find the "Script Library" database
2. Verify the config file exists at `~/.config/notion-content/config.json`
3. Tell the user:

> Notion pipeline is ready! Your Script Library database is set up with all properties.
>
> When you run `/content-master`, scripts will automatically flow into Notion as individual entries with status tracking.
>
> Use `/content-pipeline` to manage your production pipeline — update statuses, log metrics, manage your posting calendar.
