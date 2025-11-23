import hashlib

from app.common.constant import AccountManagerServiceCons
from app.service.logging_service import get_logger
from app.service.mysql_service import get_uuid_by_username, get_passwd

logger = get_logger(AccountManagerServiceCons.LOGGER)

def authentication(username, password) -> bool:
    salt_hex, expect_hash_hex = get_passwd(get_uuid_by_username(username))

    if not salt_hex or not expect_hash_hex:
        logger.warning(AccountManagerServiceCons.L_FAIL_LOGIN_2 % username, 100)
        return False

    salt_byte = bytes.fromhex(salt_hex)
    expect_hash_byte = bytes.fromhex(expect_hash_hex)

    input_hash_byte = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_byte,
        100000,
        dklen=32
    )

    if input_hash_byte == expect_hash_byte:
        logger.info(AccountManagerServiceCons.L_SUC_LOGIN % username)
        return True
    else:
        logger.warning(AccountManagerServiceCons.L_FAIL_LOGIN % username)
        return False

def register():
    pass

def password_adhere(password: str) -> bool:
    pass