"""
Secret Management System - Flask Web Application
A secure, self-hosted password and identity management system
"""

import os
import secrets
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from crypto_utils import (
    encrypt_vault,
    decrypt_vault,
    create_empty_vault,
    generate_entry_id,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

# Security configurations
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=1800,  # 30 minutes
)

VAULT_FILE = os.environ.get("VAULT_FILE_PATH", "./vault.enc")

# Valid entry types
VALID_ENTRY_TYPES = [
    "login",
    "note",
    "credit_card",
    "identity",
    "api_credential",
    "database",
    "server",
    "software_license",
    "ssh_key",
    "wifi",
    "bank_account",
]

# Entry type field definitions
ENTRY_FIELDS = {
    "login": ["url", "username", "password", "notes"],
    "note": ["notes"],
    "credit_card": [
        "cardholder_name",
        "card_number",
        "expiration_date",
        "security_code",
        "pin",
        "notes",
    ],
    "identity": [
        # Personal details
        "prefix_title",
        "full_name",
        "email",
        "phone",
        "birth_date",
        "gender",
        # Address details
        "organization",
        "address",
        "postal_code",
        "city",
        "state",
        "country",
        # Contact details
        "ssn",
        "passport_number",
        "license_number",
        "website",
        "x_handle",
        "linkedin",
        "reddit",
        "facebook",
        "yahoo",
        "instagram",
        # Work details
        "company",
        "job_title",
        "work_website",
        "work_phone",
        "work_email",
        "notes",
    ],
    "api_credential": [
        "api_key",
        "api_secret",
        "expiration_date",
        "permissions",
        "notes",
    ],
    "database": [
        "host",
        "port",
        "username",
        "password",
        "database_type",
        "database_name",
        "notes",
    ],
    "server": ["ip_address", "hostname", "os", "username", "password", "notes"],
    "software_license": ["license_key", "product", "expiry_date", "owner", "notes"],
    "ssh_key": ["public_key", "private_key", "passphrase", "username", "host", "notes"],
    "wifi": ["ssid", "password", "security_type", "notes"],
    "bank_account": [
        "bank_name",
        "account_number",
        "routing_number",
        "account_type",
        "iban",
        "swift_bic",
        "holder_name",
        "notes",
    ],
}


def get_vault_path():
    """Get the vault file path."""
    return VAULT_FILE


def vault_exists():
    """Check if vault file exists."""
    return os.path.exists(get_vault_path())


def load_vault(master_password: str) -> dict | None:
    """Load and decrypt vault from file."""
    if not vault_exists():
        return None

    with open(get_vault_path(), "rb") as f:
        encrypted_data = f.read()

    return decrypt_vault(encrypted_data, master_password)


def save_vault(vault_data: dict, master_password: str):
    """Encrypt and save vault to file."""
    encrypted_data = encrypt_vault(vault_data, master_password)

    with open(get_vault_path(), "wb") as f:
        f.write(encrypted_data)


def login_required(f):
    """Decorator to require authentication."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "authenticated" not in session or not session["authenticated"]:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


def get_entry_preview(entry: dict) -> dict:
    """Get preview fields for an entry based on its type."""
    safe_entry = {
        "id": entry["id"],
        "type": entry["type"],
        "title": entry["title"],
        "created_at": entry.get("created_at", ""),
        "updated_at": entry.get("updated_at", ""),
    }

    entry_type = entry["type"]

    if entry_type == "login":
        safe_entry["username"] = entry.get("username", "")
        safe_entry["url"] = entry.get("url", "")
    elif entry_type == "note":
        notes = entry.get("notes", "")
        safe_entry["preview"] = notes[:50] + "..." if len(notes) > 50 else notes
    elif entry_type == "credit_card":
        card_num = entry.get("card_number", "")
        safe_entry["card_last4"] = card_num[-4:] if len(card_num) >= 4 else ""
        safe_entry["cardholder_name"] = entry.get("cardholder_name", "")
    elif entry_type == "identity":
        safe_entry["full_name"] = entry.get("full_name", "")
        safe_entry["email"] = entry.get("email", "")
    elif entry_type == "api_credential":
        safe_entry["permissions"] = entry.get("permissions", "")
    elif entry_type == "database":
        safe_entry["host"] = entry.get("host", "")
        safe_entry["database_type"] = entry.get("database_type", "")
    elif entry_type == "server":
        safe_entry["ip_address"] = entry.get("ip_address", "")
        safe_entry["hostname"] = entry.get("hostname", "")
    elif entry_type == "software_license":
        safe_entry["product"] = entry.get("product", "")
        safe_entry["expiry_date"] = entry.get("expiry_date", "")
    elif entry_type == "ssh_key":
        safe_entry["host"] = entry.get("host", "")
        safe_entry["username"] = entry.get("username", "")
    elif entry_type == "wifi":
        safe_entry["ssid"] = entry.get("ssid", "")
        safe_entry["security_type"] = entry.get("security_type", "")
    elif entry_type == "bank_account":
        safe_entry["bank_name"] = entry.get("bank_name", "")
        acc_num = entry.get("account_number", "")
        safe_entry["account_last4"] = acc_num[-4:] if len(acc_num) >= 4 else ""

    return safe_entry


def create_entry_from_data(data: dict, entry_type: str) -> dict:
    """Create a new entry dict from request data."""
    now = datetime.utcnow().isoformat() + "Z"

    new_entry = {
        "id": generate_entry_id(),
        "type": entry_type,
        "title": data.get("title", ""),
        "created_at": now,
        "updated_at": now,
    }

    # Add fields based on entry type
    fields = ENTRY_FIELDS.get(entry_type, [])
    for field in fields:
        new_entry[field] = data.get(field, "")

    return new_entry


def update_entry_from_data(entry: dict, data: dict) -> dict:
    """Update an entry dict from request data."""
    now = datetime.utcnow().isoformat() + "Z"

    entry["title"] = data.get("title", entry["title"])
    entry["updated_at"] = now

    # Update fields based on entry type
    fields = ENTRY_FIELDS.get(entry["type"], [])
    for field in fields:
        if field in data:
            entry[field] = data[field]

    return entry


# ============== ROUTES ==============


@app.route("/")
def index():
    """Main page - shows setup or login based on vault existence."""
    if session.get("authenticated"):
        return redirect(url_for("dashboard"))

    return render_template("index.html", vault_exists=vault_exists())


@app.route("/api/setup", methods=["POST"])
def setup():
    """Create new vault with master password."""
    if vault_exists():
        return jsonify({"error": "Vault already exists"}), 400

    data = request.get_json()
    master_password = data.get("master_password", "")
    confirm_password = data.get("confirm_password", "")

    if len(master_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if master_password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # Create and save empty vault
    vault = create_empty_vault()
    save_vault(vault, master_password)

    # Auto login after setup
    session["authenticated"] = True
    session["master_password"] = master_password  # Stored in server-side session
    session.permanent = True

    return jsonify({"success": True, "message": "Vault created successfully"})


@app.route("/api/login", methods=["POST"])
def login():
    """Authenticate with master password."""
    if not vault_exists():
        return jsonify({"error": "No vault found. Please setup first."}), 400

    data = request.get_json()
    master_password = data.get("master_password", "")

    vault = load_vault(master_password)
    if vault is None:
        return jsonify({"error": "Invalid master password"}), 401

    session["authenticated"] = True
    session["master_password"] = master_password
    session.permanent = True

    return jsonify({"success": True})


@app.route("/api/logout", methods=["POST"])
def logout():
    """Clear session and logout."""
    session.clear()
    return jsonify({"success": True})


@app.route("/dashboard")
@login_required
def dashboard():
    """Main dashboard page."""
    return render_template("dashboard.html")


@app.route("/api/entries", methods=["GET"])
@login_required
def get_entries():
    """Get all vault entries (without sensitive data)."""
    master_password = session.get("master_password")
    vault = load_vault(master_password)

    if vault is None:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    # Return entries with preview fields only
    safe_entries = [get_entry_preview(entry) for entry in vault.get("entries", [])]

    return jsonify({"entries": safe_entries})


@app.route("/api/entries/<entry_id>", methods=["GET"])
@login_required
def get_entry(entry_id):
    """Get full entry details including sensitive data."""
    master_password = session.get("master_password")
    vault = load_vault(master_password)

    if vault is None:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    for entry in vault.get("entries", []):
        if entry["id"] == entry_id:
            return jsonify({"entry": entry})

    return jsonify({"error": "Entry not found"}), 404


@app.route("/api/entries", methods=["POST"])
@login_required
def create_entry():
    """Create new vault entry."""
    master_password = session.get("master_password")
    vault = load_vault(master_password)

    if vault is None:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    data = request.get_json()
    entry_type = data.get("type")

    if entry_type not in VALID_ENTRY_TYPES:
        return jsonify({"error": "Invalid entry type"}), 400

    new_entry = create_entry_from_data(data, entry_type)

    vault["entries"].append(new_entry)
    save_vault(vault, master_password)

    return jsonify({"success": True, "entry": new_entry})


@app.route("/api/entries/<entry_id>", methods=["PUT"])
@login_required
def update_entry(entry_id):
    """Update existing vault entry."""
    master_password = session.get("master_password")
    vault = load_vault(master_password)

    if vault is None:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    data = request.get_json()

    for i, entry in enumerate(vault.get("entries", [])):
        if entry["id"] == entry_id:
            updated_entry = update_entry_from_data(entry, data)
            vault["entries"][i] = updated_entry
            save_vault(vault, master_password)

            return jsonify({"success": True, "entry": updated_entry})

    return jsonify({"error": "Entry not found"}), 404


@app.route("/api/entries/<entry_id>", methods=["DELETE"])
@login_required
def delete_entry(entry_id):
    """Delete vault entry."""
    master_password = session.get("master_password")
    vault = load_vault(master_password)

    if vault is None:
        session.clear()
        return jsonify({"error": "Session expired"}), 401

    original_length = len(vault.get("entries", []))
    vault["entries"] = [e for e in vault.get("entries", []) if e["id"] != entry_id]

    if len(vault["entries"]) == original_length:
        return jsonify({"error": "Entry not found"}), 404

    save_vault(vault, master_password)

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
