# 🔐 Secret Management System

A secure, self-hosted password and identity management-system with local encryption. Your secrets never leave your device unencrypted.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🔒 Strong Encryption**: AES-256-GCM encryption with Argon2id key derivation
- **🏠 Self-Hosted**: Your data stays on your machine
- **💾 Portable Vault**: Single encrypted file, easy to backup/sync
- **📱 Responsive UI**: Works on desktop and mobile browsers
- **🔍 Search & Filter**: Quickly find your secrets
- **📋 Copy to Clipboard**: One-click copy for sensitive data
- **🎨 Modern Dark UI**: Beautiful interface with Tailwind CSS

### 📦 Supported Entry Types

| Type                    | Fields                                                      |
| ----------------------- | ----------------------------------------------------------- |
| 🔑 **Login**            | URL, username, password, notes                              |
| 📝 **Note**             | Secure notes                                                |
| 💳 **Credit Card**      | Cardholder, card number, expiry, CVV, PIN                   |
| 👤 **Identity**         | Personal details, address, contact, social media, work info |
| 🔌 **API Credential**   | API key, secret, expiration, permissions                    |
| 🗄️ **Database**         | Host, port, type, name, username, password                  |
| 🖥️ **Server**           | IP address, hostname, OS, username, password                |
| 📜 **Software License** | Product, license key, expiry, owner                         |
| 🔐 **SSH Key**          | Public key, private key, passphrase, host                   |
| 📶 **WiFi Network**     | SSID, password, security type                               |
| 🏦 **Bank Account**     | Bank name, account number, routing, IBAN, SWIFT             |

## 🛡️ Security

### Encryption Details

| Component      | Algorithm                                           |
| -------------- | --------------------------------------------------- |
| Key Derivation | Argon2id (3 iterations, 64MB memory, 4 parallelism) |
| Encryption     | AES-256-GCM (authenticated encryption)              |
| Nonce          | 96-bit random per encryption                        |
| Salt           | 128-bit random per encryption                       |

### Security Notes

- **Master password** is never stored - only used to derive encryption key
- **Vault file** (`vault.enc`) contains only encrypted data
- **Session timeout** after 30 minutes of inactivity
- **No telemetry** or external connections (except CDN for CSS/JS)

### ⚠️ Important Warnings

1. **DO NOT forget your master password** - there is no recovery option
2. **BACKUP your vault file** regularly to prevent data loss
3. **USE HTTPS** in production (set `SESSION_COOKIE_SECURE=True`)
4. **DO NOT expose** this app to the public internet without proper security measures

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package management-system)

### Installation

1. **Clone or download this repository**

```bash
cd secret-management-system
```

2. **Create virtual environment (recommended)**

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python app.py
```

5. **Open your browser**

Navigate to `http://127.0.0.1:5000`

### 🐳 Docker

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build
```

Open `http://localhost:5000`

## 📁 Project Structure

```
secret-management-system/
├── app.py                          # Flask application (routes, API)
├── crypto_utils.py                 # Encryption/decryption utilities
├── drive_sync.py                   # Google Drive sync module
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project metadata
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose configuration
│
├── data/
│   └── vault.enc                   # Encrypted vault (created after setup)
│
├── static/
│   ├── css/
│   │   ├── index.css               # Login page styles
│   │   └── dashboard.css           # Dashboard styles
│   └── js/
│       ├── index.js                # Login page logic
│       └── dashboard.js            # Dashboard logic
│
└── templates/
    ├── base.html                   # Base template
    ├── index.html                  # Login/setup page
    ├── dashboard.html              # Main dashboard
    └── partials/
        ├── head.html               # Shared head elements
        └── forms/
            ├── login.html          # Login form fields
            ├── note.html           # Note form fields
            ├── credit_card.html    # Credit card form fields
            ├── identity.html       # Identity form fields
            ├── api_credential.html # API credential form fields
            ├── database.html       # Database form fields
            ├── server.html         # Server form fields
            ├── software_license.html
            ├── ssh_key.html        # SSH key form fields
            ├── wifi.html           # WiFi form fields
            └── bank_account.html   # Bank account form fields
```

## 🔄 Auto-Sync with Google Drive

Secret Management supports **automatic sync** to Google Drive. Perfect for ephemeral hosting (Render, Railway, Fly.io) where files are lost on restart.

### How it works:

```
┌─────────────────────────────────────────────────────────────────┐
│  Server Startup                                                 │
│  ─────────────────                                              │
│  1. Check if vault.enc exists locally                           │
│  2. If not → Download from Google Drive                         │
│  3. If not in Drive → Fresh install (create new vault)          │
├─────────────────────────────────────────────────────────────────┤
│  On Save                                                        │
│  ─────────────────                                              │
│  1. Save vault.enc locally                                      │
│  2. Upload to Google Drive (background, non-blocking)           │
└─────────────────────────────────────────────────────────────────┘
```

### Setup Google Drive Sync (OAuth2)

> ⚠️ **Note**: As of April 2025, Google changed their policy. Service Accounts can no longer own Drive items. We use **OAuth2** instead, which works with personal Google accounts.

---

#### Step 1: Create Google Cloud Project & Enable API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project:
   - Click dropdown at top → **"New Project"**
   - Name: `secret-manager` (or any name)
   - Click **"Create"**
3. Enable **Google Drive API**:
   - Go to **"APIs & Services"** → **"Library"**
   - Search **"Google Drive API"**
   - Click → **"Enable"**

---

#### Step 2: Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Choose **"External"** → Click **"Create"**
3. Fill in:
   - **App name**: `secret-manager` (or any name)
   - **User support email**: your email
   - **Developer contact email**: your email
4. Click **"Save and Continue"**
5. **Scopes**: Skip, click **"Save and Continue"**
6. **Test users**:
   - Click **"+ ADD USERS"**
   - Add your email (e.g., `yourname@gmail.com`)
   - Click **"Save and Continue"**
7. Click **"Back to Dashboard"**

---

#### Step 3: Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Application type: **Desktop app**
4. Name: `secret-manager-sync`
5. Click **"Create"**
6. Click **"DOWNLOAD JSON"**
7. Save file as `data/credentials.json` in project folder

---

#### Step 4: Create Google Drive Folder

1. Open [Google Drive](https://drive.google.com/)
2. Create new folder: `secret-vault`
3. Open folder, copy **Folder ID** from URL:

```
https://drive.google.com/drive/folders/1ABCxyzDEF123456789
                                        ^^^^^^^^^^^^^^^^^^^
                                        THIS IS FOLDER ID
```

---

#### Step 5: Generate OAuth Token (Run Locally)

```bash
# Install dependencies (if not already)
pip install google-auth-oauthlib google-api-python-client

# Run auth script
python drive_auth.py
```

The script will:

1. Display a URL for login
2. **Copy the URL** and open in browser (Chrome/Firefox/Edge)
3. Login with Google account that was added as Test User
4. Click **"Continue"** → **"Allow"**
5. Browser redirects to localhost → Script receives token
6. **Copy the `GOOGLE_OAUTH_TOKEN` output** for deployment

Example output:

```
GOOGLE_OAUTH_TOKEN='{"token":"ya29.xxx","refresh_token":"1//xxx","client_id":"xxx.apps.googleusercontent.com",...}'
```

---

#### Step 6: Deploy to Server/Hosting

Set these **2 environment variables** on your hosting platform (Render/Railway/Fly.io):

| Variable                 | Value                   | Example                                        |
| ------------------------ | ----------------------- | ---------------------------------------------- |
| `GOOGLE_OAUTH_TOKEN`     | Entire JSON from step 5 | `{"token":"ya29...","refresh_token":"1//..."}` |
| `GOOGLE_DRIVE_FOLDER_ID` | Folder ID from step 4   | `1ABCxyzDEF123456789`                          |

**⚠️ Important:**

- `GOOGLE_OAUTH_TOKEN` must be in **1 line** (minified JSON)
- No need to upload `credentials.json` to server
- No need to upload `google_token.json` to server
- Token will auto-refresh, no need to regenerate

---

### Environment Variables Summary

| Variable                 | Required      | Description                                |
| ------------------------ | ------------- | ------------------------------------------ |
| `GOOGLE_OAUTH_TOKEN`     | ✅ For sync   | OAuth token JSON (from `drive_auth.py`)    |
| `GOOGLE_DRIVE_FOLDER_ID` | ✅ For sync   | Google Drive folder ID                     |
| `FLASK_SECRET_KEY`       | ⚠️ Production | Secret key for session                     |
| `VAULT_FILE_PATH`        | ❌ Optional   | Custom vault path (default: `./vault.enc`) |

---

### Troubleshooting

**Error: "Access blocked: app has not completed verification"**

- Make sure your email is added as a **Test User** in OAuth consent screen

**Error: "Address already in use"**

- Port 8888 is in use, try: `AUTH_PORT=9999 python drive_auth.py`

**Error: "invalid_grant" or "Token expired"**

- Generate a new token by running `python drive_auth.py` again

**Sync not working on server**

- Make sure `GOOGLE_OAUTH_TOKEN` is copied completely (including `{}`)
- Make sure `GOOGLE_DRIVE_FOLDER_ID` is correct (ID only, not full URL)

---

### Manual Sync (Alternative)

If you prefer not to use auto-sync, you can use rclone:

```bash
# Install rclone and configure
rclone config

# Sync vault to Drive
rclone copy data/vault.enc gdrive:secret-vault/
```

## ⚙️ Configuration

Set environment variables to customize:

```bash
# Flask secret key (CHANGE IN PRODUCTION!)
export FLASK_SECRET_KEY=your-random-secret-key-here

# Vault file location
export VAULT_FILE_PATH=/path/to/your/vault.enc

# Port (default: 5000)
export PORT=5000
```

## 🧪 Development

```bash
# Run with debug mode
FLASK_DEBUG=1 python app.py

# Or use Flask CLI
flask run --debug
```

## 📝 API Endpoints

| Method | Endpoint            | Description       |
| ------ | ------------------- | ----------------- |
| POST   | `/api/setup`        | Create new vault  |
| POST   | `/api/login`        | Authenticate      |
| POST   | `/api/logout`       | Lock vault        |
| GET    | `/api/entries`      | List all entries  |
| GET    | `/api/entries/<id>` | Get entry details |
| POST   | `/api/entries`      | Create entry      |
| PUT    | `/api/entries/<id>` | Update entry      |
| DELETE | `/api/entries/<id>` | Delete entry      |

### Entry Types

Valid entry types for POST `/api/entries`:

```
login, note, credit_card, identity, api_credential,
database, server, software_license, ssh_key, wifi, bank_account
```

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, Tailwind CSS, Alpine.js
- **Encryption**: cryptography (AES-GCM), argon2-cffi
- **Server**: Gunicorn (production)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

MIT License - feel free to use this for personal or commercial purposes.

---

**Made with ❤️ for privacy-conscious people**
