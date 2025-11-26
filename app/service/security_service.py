import hashlib
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from app.common.config_loader import TIME_ZONE
from app.common.constant import SecurityServiceCons
from app.common.enum import Request
from app.service.logging_service import get_logger
from app.service.mysql_service import get_role, get_role_permission, get_passwd, get_uuid_by_username, \
    traversal_weak_passwd_list

logger = get_logger(SecurityServiceCons.LOGGER)

def authorization(request: Request, uuid: str) -> bool:
    user_role = get_role(uuid)
    role_permission = get_role_permission(user_role)

    if role_permission[request.value] == 1:
        logger.info(SecurityServiceCons.L_PERM_ALLOW_1 % (request, uuid))
        return True

    if role_permission[request.value] == 2:
        now = datetime.now(ZoneInfo(TIME_ZONE))
        cur_time = now.hour * 100 + now.minute
        time_str = now.strftime(SecurityServiceCons.TIME_FORMAT)

        if 900 <= cur_time < 1700:
            logger.info(SecurityServiceCons.L_PERM_ALLOW_2 % (time_str, request, uuid))
            return True
        logger.warning(SecurityServiceCons.L_PERM_DENIED_2 % (time_str, request, uuid))

    logger.warning(SecurityServiceCons.L_PERM_DENIED % (request, user_role, uuid))
    return False

def authentication(username, password) -> bool:
    salt_hex, expect_hash_hex = get_passwd(get_uuid_by_username(username))

    if not salt_hex or not expect_hash_hex:
        logger.warning(SecurityServiceCons.L_FAIL_LOGIN_2 % username, 100)
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
        logger.info(SecurityServiceCons.L_SUC_LOGIN % username)
        return True
    else:
        logger.warning(SecurityServiceCons.L_FAIL_LOGIN % username)
        return False

def password_adhere(password: str, username: str) -> bool:
    if not (8 <= len(password) <= 12):
        logger.warning("Password length should be between 8 and 12")
        return False

    if not re.search(r"[A-Z]", password):
        logger.warning("Password must contain capital letters")
        return False

    if not re.search(r"[a-z]", password):
        logger.warning("Password must contain lowercase letters")
        return False

    if not re.search(r"[0-9]", password):
        logger.warning("Password must contain numbers")
        return False

    if not re.search(r"[!@#$%*&]", password):
        logger.warning("Password must contain at least one special character {! @ # $ % * &}")
        return False

    if username and password.lower() == username.lower():
        logger.warning("Password must not be same as username")
        return False

    if traversal_weak_passwd_list(password):
        logger.warning("Password too weak")
        return False

    if not re.fullmatch(r"[A-Za-z0-9!@#$%*&]+", password):
        logger.warning("Password contains invalid characters")
        return False

    logger.info("Password_adhere Pass")
    return True

