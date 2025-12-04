# 🔐 Secret Manager

A secure, self-hosted password and identity manager with local encryption. Your secrets never leave your device unencrypted.

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
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

```bash
cd secret-manager
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
secret-manager/
├── app.py                          # Flask application (routes, API)
├── crypto_utils.py                 # Encryption/decryption utilities
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

## 🔄 Syncing with Google Drive

You can sync your encrypted vault file to Google Drive for backup and multi-device access:

### Option 1: Google Drive Desktop App

1. Install [Google Drive for Desktop](https://www.google.com/drive/download/)
2. Move or symlink your vault file to Google Drive folder:

```bash
# Move vault to Google Drive
mv data/vault.enc ~/Google\ Drive/My\ Drive/secret-vault/

# Create symlink (Linux/Mac)
ln -s ~/Google\ Drive/My\ Drive/secret-vault/vault.enc ./data/vault.enc

# Or set environment variable
export VAULT_FILE_PATH=~/Google\ Drive/My\ Drive/secret-vault/vault.enc
```

### Option 2: Using rclone

1. Install and configure [rclone](https://rclone.org/)

```bash
rclone config  # Setup Google Drive remote
```

2. Sync after changes:

```bash
rclone copy data/vault.enc gdrive:secret-vault/
```

3. Or mount Google Drive:

```bash
rclone mount gdrive:secret-vault /mnt/vault --daemon
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
