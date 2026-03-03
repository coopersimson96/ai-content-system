---
name: gdocs-setup
description: One-time setup for Google Docs integration. Walks through creating a Google Cloud project, enabling APIs, setting up OAuth, and testing the connection.
argument-hint: (no arguments needed)
context: conversation
---

# Google Docs Integration Setup

Walk the user through setting up Google Docs integration for the content pipeline.

---

## Step 1: Google Cloud Project

Tell the user:

> **Let's set up Google Docs integration.** This is a one-time setup that takes about 5 minutes.
>
> First, we need a Google Cloud project with the Docs and Drive APIs enabled.
>
> 1. Go to [Google Cloud Console](https://console.cloud.google.com/)
> 2. Create a new project (or use an existing one) — name it something like "Content Pipeline"
> 3. In the left sidebar, go to **APIs & Services > Library**
> 4. Search for and enable **Google Docs API**
> 5. Search for and enable **Google Drive API**
>
> Done? Let me know.

Wait for confirmation before proceeding.

---

## Step 2: Create OAuth Credentials

Tell the user:

> Now we need OAuth credentials so the script can act on your behalf.
>
> 1. Go to **APIs & Services > Credentials**
> 2. Click **+ CREATE CREDENTIALS > OAuth client ID**
> 3. If prompted to configure the consent screen:
>    - Choose **External** (unless you have a Workspace org)
>    - App name: "Content Pipeline"
>    - Add your email as a test user
>    - Save and continue through the screens
> 4. Back in Credentials, click **+ CREATE CREDENTIALS > OAuth client ID**
> 5. Application type: **Desktop app**
> 6. Name: "Content Pipeline Desktop"
> 7. Click **Create**
> 8. Click **Download JSON** on the popup
>
> Save the downloaded file — I'll place it in the right location.

Wait for the user to confirm they have the JSON file. Then:

```bash
mkdir -p ~/.config/gdocs
```

Ask the user for the path to their downloaded JSON file, then:

```bash
cp "{USER_PROVIDED_PATH}" ~/.config/gdocs/credentials.json
```

---

## Step 3: Run OAuth Flow

Run the setup command:

```bash
cd ~/.claude/skills/scripts && python3 gdocs_push.py --setup
```

This will:
1. Open a browser window for Google OAuth consent
2. The user authorizes the app
3. Token is saved to `~/.config/gdocs/token.json`
4. User is prompted for a default Drive folder ID (optional)
5. A test document is created

If the required Python packages aren't installed, install them first:

```bash
pip3 install google-auth google-auth-oauthlib google-api-python-client
```

---

## Step 4: Set Default Folder (Optional)

If the user wants scripts to go to a specific Google Drive folder:

> Want to set a default Drive folder for your scripts?
>
> 1. Go to Google Drive
> 2. Open (or create) the folder you want scripts saved to
> 3. Copy the folder ID from the URL: `drive.google.com/drive/folders/{THIS_PART}`
>
> Give me that ID and I'll save it as your default.

If they provide one, update the config:

```python
import json
config_path = "~/.config/gdocs/config.json"
# Read existing config, add/update default_folder_id, write back
```

---

## Step 5: Verify

Confirm setup is complete by checking:
1. `~/.config/gdocs/credentials.json` exists
2. `~/.config/gdocs/token.json` exists
3. Test doc was created successfully

Tell the user:

> Google Docs integration is ready! When you run `/content-master`, scripts will automatically be pushed to a Google Doc.
>
> You can also push any markdown file manually:
> ```bash
> python3 ~/.claude/skills/scripts/gdocs_push.py --title "My Scripts" --content-file "/path/to/scripts.md"
> ```
