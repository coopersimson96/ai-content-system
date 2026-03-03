#!/usr/bin/env python3
"""
Push markdown content to Google Docs.

Usage:
    python3 gdocs_push.py --title "My Doc" --content-file "/path/to/file.md"
    python3 gdocs_push.py --title "My Doc" --content-file "/path/to/file.md" --folder-id "FOLDER_ID"
    python3 gdocs_push.py --title "My Doc" --content-file "/path/to/file.md" --update-doc-id "DOC_ID"
    python3 gdocs_push.py --setup  # first-time OAuth flow
"""

import argparse
import json
import os
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / '.config' / 'gdocs'
CREDENTIALS_FILE = CONFIG_DIR / 'credentials.json'
TOKEN_FILE = CONFIG_DIR / 'token.json'
CONFIG_FILE = CONFIG_DIR / 'config.json'

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file',
]


def load_config() -> dict:
    """Load config from ~/.config/gdocs/config.json."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    """Save config to ~/.config/gdocs/config.json."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_credentials():
    """Get or refresh OAuth credentials."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: No credentials file found at {CREDENTIALS_FILE}", file=sys.stderr)
                print("Run /gdocs-setup to configure Google Docs integration.", file=sys.stderr)
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next run
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds


def create_doc(title: str, folder_id: str = None, creds=None) -> str:
    """Create a new Google Doc and return its ID."""
    from googleapiclient.discovery import build

    docs_service = build('docs', 'v1', credentials=creds)
    doc = docs_service.documents().create(body={'title': title}).execute()
    doc_id = doc['documentId']

    # Move to folder if specified
    if folder_id:
        drive_service = build('drive', 'v3', credentials=creds)
        # Get current parents
        file = drive_service.files().get(fileId=doc_id, fields='parents').execute()
        previous_parents = ','.join(file.get('parents', []))
        # Move to target folder
        drive_service.files().update(
            fileId=doc_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()

    return doc_id


def clear_doc(doc_id: str, creds=None):
    """Clear all content from an existing doc."""
    from googleapiclient.discovery import build

    docs_service = build('docs', 'v1', credentials=creds)
    doc = docs_service.documents().get(documentId=doc_id).execute()

    content = doc.get('body', {}).get('content', [])
    if len(content) > 1:
        # Get the end index of the last element
        end_index = content[-1]['endIndex'] - 1
        if end_index > 1:
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': [{'deleteContentRange': {
                    'range': {'startIndex': 1, 'endIndex': end_index}
                }}]}
            ).execute()


def push_content(doc_id: str, markdown: str, creds=None):
    """Push formatted content to a Google Doc."""
    from googleapiclient.discovery import build
    from gdocs_formatter import markdown_to_docs_requests

    docs_service = build('docs', 'v1', credentials=creds)
    requests = markdown_to_docs_requests(markdown)

    if requests:
        # Batch requests in chunks of 100 to avoid API limits
        for i in range(0, len(requests), 100):
            chunk = requests[i:i + 100]
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': chunk}
            ).execute()


def run_setup():
    """Run first-time OAuth setup flow."""
    print("=== Google Docs Integration Setup ===\n")

    if not CREDENTIALS_FILE.exists():
        print(f"Place your OAuth credentials file at: {CREDENTIALS_FILE}")
        print("(Download from Google Cloud Console > APIs & Services > Credentials)")
        print("\nThen run this command again.")
        sys.exit(1)

    print("Starting OAuth flow... A browser window will open.")
    creds = get_credentials()

    if creds and creds.valid:
        print(f"\nAuth successful! Token saved to {TOKEN_FILE}")

        # Ask for default folder ID
        config = load_config()
        folder_id = input("\nDefault Drive folder ID (press Enter to skip): ").strip()
        if folder_id:
            config['default_folder_id'] = folder_id

        save_config(config)
        print(f"Config saved to {CONFIG_FILE}")

        # Test by creating a sample doc
        print("\nCreating test document...")
        test_doc_id = create_doc("Test - Google Docs Integration", folder_id or None, creds)
        test_content = "# Google Docs Integration Test\n\nThis doc was created by the content pipeline.\n\n**Setup complete!**"
        push_content(test_doc_id, test_content, creds)
        print(f"Test doc created: https://docs.google.com/document/d/{test_doc_id}/edit")
        print("\nSetup complete!")
    else:
        print("Auth failed. Check your credentials file.", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Push markdown content to Google Docs')
    parser.add_argument('--title', help='Document title')
    parser.add_argument('--content-file', help='Path to markdown file')
    parser.add_argument('--folder-id', help='Google Drive folder ID')
    parser.add_argument('--update-doc-id', help='Existing doc ID to update')
    parser.add_argument('--setup', action='store_true', help='Run first-time setup')

    args = parser.parse_args()

    if args.setup:
        run_setup()
        return

    if not args.title or not args.content_file:
        parser.error("--title and --content-file are required (unless using --setup)")

    content_path = Path(args.content_file)
    if not content_path.exists():
        print(f"ERROR: File not found: {content_path}", file=sys.stderr)
        sys.exit(1)

    markdown = content_path.read_text()
    creds = get_credentials()

    # Resolve folder ID
    folder_id = args.folder_id
    if not folder_id:
        config = load_config()
        folder_id = config.get('default_folder_id')

    if args.update_doc_id:
        # Update existing doc
        doc_id = args.update_doc_id
        clear_doc(doc_id, creds)
        push_content(doc_id, markdown, creds)
    else:
        # Create new doc
        doc_id = create_doc(args.title, folder_id, creds)
        push_content(doc_id, markdown, creds)

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(doc_url)


if __name__ == '__main__':
    main()
