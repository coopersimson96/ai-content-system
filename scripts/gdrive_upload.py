#!/usr/bin/env python3
"""
Upload files to Google Drive with shareable link.

Reuses OAuth credentials from gdocs_push.py (~/.config/gdocs/).
The drive.file scope is already granted.

Usage:
    python3 gdrive_upload.py --file hand-raiser.pdf --subfolder "Hand Raisers"
    python3 gdrive_upload.py --file output.pdf  # uploads to default folder root
"""

import argparse
import json
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
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_credentials():
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
                print(f"ERROR: No credentials at {CREDENTIALS_FILE}. Run /gdocs-setup first.", file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds


def get_or_create_subfolder(drive_service, parent_id: str, subfolder_name: str, config: dict) -> str:
    """Get existing subfolder ID or create it. Caches in config."""
    cache_key = f"subfolder_{subfolder_name.lower().replace(' ', '_')}_id"

    # Check cache first
    cached_id = config.get(cache_key)
    if cached_id:
        # Verify it still exists
        try:
            f = drive_service.files().get(fileId=cached_id, fields='id,trashed').execute()
            if not f.get('trashed'):
                return cached_id
        except Exception:
            pass  # Cache stale, create new

    # Search for existing folder
    query = (
        f"name = '{subfolder_name}' and "
        f"'{parent_id}' in parents and "
        f"mimeType = 'application/vnd.google-apps.folder' and "
        f"trashed = false"
    )
    results = drive_service.files().list(q=query, fields='files(id)').execute()
    files = results.get('files', [])

    if files:
        folder_id = files[0]['id']
    else:
        # Create the subfolder
        metadata = {
            'name': subfolder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id],
        }
        folder = drive_service.files().create(body=metadata, fields='id').execute()
        folder_id = folder['id']
        print(f"Created subfolder: {subfolder_name}", file=sys.stderr)

    # Cache for next time
    config[cache_key] = folder_id
    save_config(config)
    return folder_id


def upload_file(file_path: str, folder_id: str, creds) -> str:
    """Upload a file to Drive and return the shareable URL."""
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    drive_service = build('drive', 'v3', credentials=creds)
    path = Path(file_path)

    # Detect MIME type
    mime_map = {
        '.pdf': 'application/pdf',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
    }
    mime_type = mime_map.get(path.suffix.lower(), 'application/octet-stream')

    metadata = {
        'name': path.name,
        'parents': [folder_id],
    }

    media = MediaFileUpload(str(path), mimetype=mime_type, resumable=True)
    uploaded = drive_service.files().create(
        body=metadata,
        media_body=media,
        fields='id,webViewLink',
    ).execute()

    file_id = uploaded['id']

    # Set "anyone with link can view" permission
    drive_service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'},
    ).execute()

    # Get shareable link
    file_info = drive_service.files().get(fileId=file_id, fields='webViewLink').execute()
    return file_info['webViewLink']


def main():
    parser = argparse.ArgumentParser(description='Upload file to Google Drive with shareable link')
    parser.add_argument('--file', required=True, help='Path to file to upload')
    parser.add_argument('--subfolder', default=None, help='Subfolder name (auto-created under default folder)')
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    default_folder_id = config.get('default_folder_id')
    if not default_folder_id:
        print("ERROR: No default_folder_id in config. Run /gdocs-setup first.", file=sys.stderr)
        sys.exit(1)

    creds = get_credentials()

    # Determine target folder
    target_folder_id = default_folder_id
    if args.subfolder:
        from googleapiclient.discovery import build
        drive_service = build('drive', 'v3', credentials=creds)
        target_folder_id = get_or_create_subfolder(drive_service, default_folder_id, args.subfolder, config)

    url = upload_file(str(file_path), target_folder_id, creds)
    print(url)


if __name__ == '__main__':
    main()
