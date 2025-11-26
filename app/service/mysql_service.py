'''
database are simulated by ini files
so the database service here are actually ini reader service
'''
import configparser
from typing import List, Tuple
from uuid import uuid4

from app.common.config_loader import USER_INI_FILE, ROLE_PERMISSION_FILE, PASSWD_FILE, WEAK_PASSWD_FILE
from app.common.constant import MysqlServiceCons
from app.common.enum import Role
from app.service.logging_service import get_logger
from app.service.security_utils import password_to_pbkdf2

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
            logger.info(MysqlServiceCons.L_SUC_FETCH_USERNAME % (username_clean, uuid))
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

def traversal_weak_passwd_list(passwd: str) -> bool:
    config = configparser.ConfigParser()
    config.read(WEAK_PASSWD_FILE)

    raw = config["weak_passwd"]["list"]
    weak_set = {item.strip().lower() for item in raw.split(",")}

    return passwd.strip().lower() in weak_set

def traversal_username_exist(username: str) -> bool:
    config = configparser.ConfigParser()
    config.read(USER_INI_FILE)

    for uuid in config.sections():
        if config[uuid][MysqlServiceCons.USERNAME].strip().lower() == username.strip().lower():
            logger.warning(MysqlServiceCons.L_USERNAME_EXISTS % username)
            return True

    logger.info(MysqlServiceCons.L_USERNAME_AVAILABLE % username)
    return False

def insert_user(username: str, name: str, role: Role, passwd: str):
    config = configparser.ConfigParser()
    config.read(USER_INI_FILE)

    username_clean = username.strip().lower()

    if traversal_username_exist(username):
        logger.warning("Username %s is already registered", username)
        return

    while True:
        new_uuid = str(uuid4())
        if new_uuid not in config:
            break

    config[new_uuid] = {
        MysqlServiceCons.USERNAME: username_clean,
        MysqlServiceCons.NAME: name,
        MysqlServiceCons.ROLE: role.value
    }

    with open(USER_INI_FILE, "w") as f:
        config.write(f)

    salt_hex, hash_hex = password_to_pbkdf2(passwd)
    insert_passwd(new_uuid, salt_hex, hash_hex)

    logger.info("Inserted new user '%s' (%s) with role %s", username, new_uuid, role.value)


def insert_passwd(uuid: str, salt_hex: str, hash_hex: str):
    config = configparser.ConfigParser()
    config.read(PASSWD_FILE)

    config[uuid] = {
        MysqlServiceCons.SALT: salt_hex,
        MysqlServiceCons.HASH: hash_hex
    }

    with open(PASSWD_FILE, "w") as f:
        config.write(f)

    logger.info("Inserted password record for UUID %s", uuid)