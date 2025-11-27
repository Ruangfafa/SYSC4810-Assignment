import hashlib
import os
from typing import Tuple


def password_to_pbkdf2(password: str) -> Tuple[str, str]:
    """
    Convert a plaintext password into a secure PBKDF2-HMAC hash.

    This function performs the following:
    1. Generates a 16-byte cryptographically secure random salt (os.urandom).
    2. Applies PBKDF2 using HMAC-SHA256 with:
          - 100000 iterations (industry standard, slows down brute force attacks)
          - 32-byte derived key length
    3. Returns the salt and hash in hexadecimal format for storage.

    Args:
        password (str): The plaintext password provided by the user.

    Returns:
        Tuple[str, str]:
            - salt_hex: Hex-encoded 16-byte salt
            - hash_hex: Hex-encoded PBKDF2-HMAC-SHA256 hash of the password
    """
    hash_passwd = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt := os.urandom(16),
        100000,
        dklen=32
    )

    return salt.hex(), hash_passwd.hex()