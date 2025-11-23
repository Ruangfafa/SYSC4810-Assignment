'''
database are simulated by ini files
so the database service here are actually ini reader service
'''
import configparser
from typing import List, Tuple

from app.common.config_loader import USER_INI_FILE, ROLE_PERMISSION_FILE, PASSWD_FILE
from app.common.constant import MysqlServiceCons
from app.common.enum import Role
from app.service.logging_service import get_logger

logger = get_logger(MysqlServiceCons.LOGGER)

def get_role(uuid: str) -> Role:
    logger.info(MysqlServiceCons.L_TRY_FETCH_UUID % uuid)

    config = configparser.ConfigParser()
    config.read(USER_INI_FILE)

    if uuid not in config:
        logger.error(MysqlServiceCons.L_FAIL_FETCH_UUID % uuid)
        raise ValueError(MysqlServiceCons.L_FAIL_FETCH_UUID % uuid)

    role = config[uuid][MysqlServiceCons.ROLE].strip()
    logger.info(MysqlServiceCons.L_SUC_FETCH_UUID % (uuid, role))

    return Role(role)

def get_role_permission(role: Role) -> List[int]:
    config = configparser.ConfigParser()
    config.read(ROLE_PERMISSION_FILE)

    row = config[MysqlServiceCons.PERMISSION][role.value]

    permission = [int(item.strip()) for item in row.split(MysqlServiceCons.COMMA)]

    return permission

def get_uuid_by_username(username: str) -> str:
    config = configparser.ConfigParser()
    config.read(USER_INI_FILE)

    username_clean = username.strip().lower()

    for uuid in config.sections():
        stored_username = config[uuid][MysqlServiceCons.USERNAME].strip().lower()
        if stored_username == username_clean:
            logger.info(MysqlServiceCons.L_SUC_FETCH_USERNAME % username, uuid)
            return uuid

    logger.error(MysqlServiceCons.L_FAIL_FETCH_USERNAME % username)
    raise ValueError(MysqlServiceCons.L_FAIL_FETCH_USERNAME % username)

def get_passwd(uuid: str) -> Tuple[str, str]:
    config = configparser.ConfigParser()
    config.read(PASSWD_FILE)

    if uuid not in config:
        raise ValueError(MysqlServiceCons.L_FAIL_FETCH_PASSWD % uuid)

    salt_hex = config[uuid][MysqlServiceCons.SALT].strip()
    hash_hex = config[uuid][MysqlServiceCons.HASH].strip()

    return salt_hex, hash_hex