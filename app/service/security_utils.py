import hashlib
import os
from typing import Tuple


def password_to_pbkdf2(password: str) -> Tuple[str, str]:
    hash_passwd = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt := os.urandom(16),
        100000,
        dklen=32
    )

    return salt.hex(), hash_passwd.hex()