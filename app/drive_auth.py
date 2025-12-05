#!/usr/bin/env python3
"""
Google Drive OAuth2 Authentication Script
Run this script locally ONCE to authenticate with Google Drive.
It will generate a token that can be used for server deployment.
"""

import os
import sys
import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CREDENTIALS_FILE = os.environ.get(
    "GOOGLE_OAUTH_CREDENTIALS_FILE", "./data/credentials.json"
)
TOKEN_FILE = "./data/google_token.json"
AUTH_PORT = int(os.environ.get("AUTH_PORT", "8888"))  # Ganti port kalau 8080 dipakai


def main():
    print()
    print("=" * 70)
    print("  Google Drive OAuth2 Authentication")
    print("=" * 70)
    print()

    # Check for credentials file
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ ERROR: Credentials file not found!")
        print(f"   Expected: {CREDENTIALS_FILE}")
        print()
        print("📋 To get OAuth credentials:")
        print()
        print("   1. Go to https://console.cloud.google.com/")
        print("   2. Create a project (or use existing)")
        print("   3. Enable 'Google Drive API'")
        print("   4. Go to 'APIs & Services' → 'OAuth consent screen'")
        print("      - Choose 'External', fill app name")
        print("      - Add your email as test user")
        print("   5. Go to 'APIs & Services' → 'Credentials'")
        print("   6. Click 'CREATE CREDENTIALS' → 'OAuth client ID'")
        print("   7. Choose 'Desktop app' as application type")
        print("   8. Download JSON and save to: data/credentials.json")
        print()
        sys.exit(1)

    print(f"✅ Using credentials: {CREDENTIALS_FILE}")
    print()

    # Create OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)

    # Get the authorization URL
    auth_url, _ = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )

    print("=" * 70)
    print("  📋 COPY URL INI DAN BUKA DI BROWSER (Chrome/Firefox/Edge):")
    print("=" * 70)
    print()
    print(auth_url)
    print()
    print("=" * 70)
    print()
    print("⏳ Menunggu kamu login di browser...")
    print("   (Setelah login, browser akan redirect ke localhost)")
    print()

    # Run local server to receive the callback
    try:
        creds = flow.run_local_server(
            host="localhost",
            port=AUTH_PORT,
            open_browser=False,  # Jangan buka browser otomatis
            success_message="✅ Autentikasi berhasil! Kamu bisa tutup tab ini.",
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("   Pastikan:")
        print(f"   - Port {AUTH_PORT} tidak dipakai aplikasi lain")
        print("   - Kamu sudah login dan allow permission di browser")
        print()
        print("   Coba port lain: AUTH_PORT=9999 python drive_auth.py")
        sys.exit(1)

    # Save token to file
    Path(TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())

    print()
    print("=" * 70)
    print("  ✅ SUKSES! Autentikasi selesai!")
    print("=" * 70)
    print()
    print(f"📁 Token tersimpan di: {TOKEN_FILE}")
    print()
    print("-" * 70)
    print("📋 Untuk deploy ke server/Docker, set environment variable ini:")
    print("-" * 70)
    print()

    # Read and minify the token JSON
    with open(TOKEN_FILE, "r") as f:
        token_data = json.load(f)

    token_json = json.dumps(token_data, separators=(",", ":"))
    print(f"GOOGLE_OAUTH_TOKEN='{token_json}'")
    print()
    print("-" * 70)
    print("Juga set folder ID:")
    print("-" * 70)
    print()
    print("GOOGLE_DRIVE_FOLDER_ID=<folder-id-dari-url-google-drive>")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
