"""
Google Drive Sync for Secret Manager
Handles backup and restore of vault.enc to/from Google Drive
Uses OAuth2 for personal Google accounts
"""

import os
import io
import json
import threading
from typing import Optional
from pathlib import Path

# Google Drive API imports
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# Configuration from environment
GOOGLE_OAUTH_CREDENTIALS = os.environ.get(
    "GOOGLE_OAUTH_CREDENTIALS"
)  # OAuth client JSON
GOOGLE_OAUTH_TOKEN = os.environ.get("GOOGLE_OAUTH_TOKEN")  # Stored refresh token JSON
GOOGLE_DRIVE_FOLDER_ID = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")  # Folder ID in Drive
TOKEN_FILE = os.environ.get("GOOGLE_TOKEN_FILE", "./data/google_token.json")
VAULT_FILENAME = "vault.enc"

# Scopes needed for Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def is_drive_sync_enabled() -> bool:
    """Check if Google Drive sync is properly configured."""
    if not GOOGLE_DRIVE_FOLDER_ID:
        return False
    # Need either token or credentials to authenticate
    if not (
        GOOGLE_OAUTH_TOKEN or os.path.exists(TOKEN_FILE) or GOOGLE_OAUTH_CREDENTIALS
    ):
        return False
    return True


def get_credentials() -> Optional[Credentials]:
    """Get or refresh OAuth2 credentials."""
    creds = None

    # Try to load from environment variable first
    if GOOGLE_OAUTH_TOKEN:
        try:
            token_data = json.loads(GOOGLE_OAUTH_TOKEN)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"[Drive Sync] Error loading token from env: {e}")

    # Try to load from token file
    if not creds and os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                token_data = json.load(f)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"[Drive Sync] Error loading token file: {e}")

    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed token
            save_token(creds)
            print("[Drive Sync] Token refreshed successfully")
        except Exception as e:
            print(f"[Drive Sync] Error refreshing token: {e}")
            creds = None

    # If no valid creds and we have OAuth credentials, need to authenticate
    if not creds or not creds.valid:
        if GOOGLE_OAUTH_CREDENTIALS:
            print(
                "[Drive Sync] No valid token. Run 'python drive_auth.py' to authenticate."
            )
        return None

    return creds


def save_token(creds: Credentials):
    """Save credentials to token file."""
    try:
        Path(TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    except Exception as e:
        print(f"[Drive Sync] Error saving token: {e}")


def get_drive_service():
    """Get authenticated Google Drive service."""
    if not is_drive_sync_enabled():
        return None

    creds = get_credentials()
    if not creds:
        return None

    try:
        service = build("drive", "v3", credentials=creds)
        return service
    except Exception as e:
        print(f"[Drive Sync] Error creating service: {e}")
        return None


def find_vault_in_drive(service) -> Optional[str]:
    """Find vault.enc file ID in Google Drive folder."""
    try:
        query = f"name = '{VAULT_FILENAME}' and '{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed = false"
        results = (
            service.files()
            .list(
                q=query,
                spaces="drive",
                fields="files(id, name, modifiedTime)",
                pageSize=1,
            )
            .execute()
        )

        files = results.get("files", [])
        if files:
            return files[0]["id"]
        return None
    except Exception as e:
        print(f"[Drive Sync] Error finding vault: {e}")
        return None


def download_vault_from_drive(local_path: str) -> bool:
    """
    Download vault.enc from Google Drive to local path.
    Returns True if successful, False otherwise.
    """
    if not is_drive_sync_enabled():
        print("[Drive Sync] Not enabled, skipping download")
        return False

    service = get_drive_service()
    if not service:
        print("[Drive Sync] Could not create Drive service")
        return False

    try:
        file_id = find_vault_in_drive(service)
        if not file_id:
            print("[Drive Sync] No vault.enc found in Drive (fresh install)")
            return False

        # Download file
        request = service.files().get_media(fileId=file_id)

        # Ensure directory exists
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)

        with io.FileIO(local_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

        print(f"[Drive Sync] Downloaded vault.enc from Drive")
        return True
    except Exception as e:
        print(f"[Drive Sync] Error downloading vault: {e}")
        return False


def upload_vault_to_drive(local_path: str) -> bool:
    """
    Upload vault.enc from local path to Google Drive.
    Returns True if successful, False otherwise.
    """
    if not is_drive_sync_enabled():
        print("[Drive Sync] Not enabled, skipping upload")
        return False

    if not os.path.exists(local_path):
        print(f"[Drive Sync] Local file not found: {local_path}")
        return False

    service = get_drive_service()
    if not service:
        print("[Drive Sync] Could not create Drive service")
        return False

    try:
        file_id = find_vault_in_drive(service)
        media = MediaFileUpload(local_path, mimetype="application/octet-stream")

        if file_id:
            # Update existing file
            service.files().update(
                fileId=file_id,
                media_body=media,
            ).execute()
            print(f"[Drive Sync] Updated vault.enc in Drive")
        else:
            # Create new file in folder
            file_metadata = {
                "name": VAULT_FILENAME,
                "parents": [GOOGLE_DRIVE_FOLDER_ID],
            }
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id",
            ).execute()
            print(f"[Drive Sync] Created vault.enc in Drive")

        return True
    except Exception as e:
        print(f"[Drive Sync] Error uploading vault: {e}")
        return False


def upload_vault_async(local_path: str):
    """Upload vault to Drive in background thread."""
    thread = threading.Thread(
        target=upload_vault_to_drive, args=(local_path,), daemon=True
    )
    thread.start()


def sync_on_startup(local_path: str) -> bool:
    """
    Sync vault on application startup.
    - If local vault exists: do nothing (use local)
    - If local vault doesn't exist: try to download from Drive

    Returns True if vault is available after sync, False if fresh install.
    """
    if os.path.exists(local_path):
        print(f"[Drive Sync] Local vault exists, using local copy")
        # Optionally upload to Drive to ensure it's backed up
        if is_drive_sync_enabled():
            upload_vault_async(local_path)
        return True

    # Try to download from Drive
    if download_vault_from_drive(local_path):
        return True

    # No vault anywhere - fresh install
    print("[Drive Sync] No vault found anywhere, fresh install")
    return False
