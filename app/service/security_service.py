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
    try:
        uuid = get_uuid_by_username(username)
        salt_hex, expect_hash_hex = get_passwd(uuid)
    except Exception as e:
        logger.warning(SecurityServiceCons.L_FAIL_LOGIN_3 % (username, str(e)))
        return False

    salt_byte = bytes.fromhex(salt_hex)
    expect_hash_byte = bytes.fromhex(expect_hash_hex)

    input_hash_byte = hashlib.pbkdf2_hmac(
        SecurityServiceCons.HASH_TYPE,
        password.encode(SecurityServiceCons.DECODE_TYPE),
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
        logger.warning(SecurityServiceCons.L_FAIL_PASSWD_ADHERE_1)
        return False

    if not re.search(SecurityServiceCons.RE_1, password):
        logger.warning(SecurityServiceCons.L_FAIL_PASSWD_ADHERE_2)
        return False

    if not re.search(SecurityServiceCons.RE_2, password):
        logger.warning(SecurityServiceCons.L_FAIL_PASSWD_ADHERE_3)
        return False

    if not re.search(SecurityServiceCons.RE_3, password):
        logger.warning(SecurityServiceCons.L_FAIL_PASSWD_ADHERE_4)
        return False

    if not re.search(SecurityServiceCons.RE_4, password):
        logger.warning(SecurityServiceCons.L_FAIL_PASSWD_ADHERE_5)
        return False

    if username and password.lower() == username.lower():
        logger.warning(SecurityServiceCons.L_FAIL_PASSWD_ADHERE_6)
        return False

    if traversal_weak_passwd_list(password):
        logger.warning(SecurityServiceCons.L_FAIL_PASSWD_ADHERE_7)
        return False

    if not re.fullmatch(SecurityServiceCons.RE_5, password):
        logger.warning(SecurityServiceCons.L_FAIL_PASSWD_ADHERE_8)
        return False

    logger.info(SecurityServiceCons.L_SUC_PASSWD_ADHERE)
    return True

