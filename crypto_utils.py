"""
Encryption utilities for Secret Manager
Uses AES-256-GCM for encryption and Argon2id for key derivation
"""

import os
import json
import base64
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type


# Argon2id parameters (OWASP recommendations)
ARGON2_TIME_COST = 3
ARGON2_MEMORY_COST = 65536  # 64 MB
ARGON2_PARALLELISM = 4
ARGON2_HASH_LEN = 32  # 256 bits for AES-256

# AES-GCM parameters
NONCE_SIZE = 12  # 96 bits recommended for AES-GCM
SALT_SIZE = 16  # 128 bits


def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Derive encryption key from master password using Argon2id.
    Argon2id is resistant to both side-channel and GPU attacks.
    """
    return hash_secret_raw(
        secret=master_password.encode("utf-8"),
        salt=salt,
        time_cost=ARGON2_TIME_COST,
        memory_cost=ARGON2_MEMORY_COST,
        parallelism=ARGON2_PARALLELISM,
        hash_len=ARGON2_HASH_LEN,
        type=Type.ID,
    )


def encrypt_vault(data: dict, master_password: str) -> bytes:
    """
    Encrypt vault data using AES-256-GCM.

    Output format: salt (16 bytes) || nonce (12 bytes) || ciphertext
    """
    # Generate random salt and nonce
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    # Derive key from master password
    key = derive_key(master_password, salt)

    # Encrypt data
    aesgcm = AESGCM(key)
    plaintext = json.dumps(data, ensure_ascii=False).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # Combine salt + nonce + ciphertext
    return salt + nonce + ciphertext


def decrypt_vault(encrypted_data: bytes, master_password: str) -> Optional[dict]:
    """
    Decrypt vault data using AES-256-GCM.
    Returns None if decryption fails (wrong password or corrupted data).
    """
    try:
        # Extract salt, nonce, and ciphertext
        salt = encrypted_data[:SALT_SIZE]
        nonce = encrypted_data[SALT_SIZE : SALT_SIZE + NONCE_SIZE]
        ciphertext = encrypted_data[SALT_SIZE + NONCE_SIZE :]

        # Derive key from master password
        key = derive_key(master_password, salt)

        # Decrypt data
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        return json.loads(plaintext.decode("utf-8"))
    except Exception:
        return None


def create_empty_vault() -> dict:
    """Create a new empty vault structure."""
    return {"version": 1, "entries": []}


def generate_entry_id() -> str:
    """Generate a random ID for vault entries."""
    return base64.urlsafe_b64encode(os.urandom(12)).decode("ascii")
