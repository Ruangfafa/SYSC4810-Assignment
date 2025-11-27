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
    """
    Retrieve the role value associated with a given user UUID.

    Args:
        uuid (str): User's UUID.

    Returns:
        Role: Enum value of the user's role.

    Raises:
        ValueError: If the UUID does not exist in the user.ini file.
    """
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
    """
    Fetch the permission vector (list[int]) associated with a given role.

    Args:
        role (Role): Role enum.

    Returns:
        List[int]: The permission vector for this role.
    """
    config = configparser.ConfigParser()
    config.read(ROLE_PERMISSION_FILE)

    row = config[MysqlServiceCons.PERMISSION][role.value]

    permission = [int(item.strip()) for item in row.split(MysqlServiceCons.COMMA)]

    return permission

def get_uuid_by_username(username: str) -> str:
    """
    Search the user.ini file and return the UUID associated with a username.

    Args:
        username (str): Username to search (case-insensitive).

    Returns:
        str: UUID of the matching user.

    Raises:
        ValueError: If the username does not exist.
    """
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
    """
    Retrieve the stored password salt and hash for the given UUID.

    Args:
        uuid (str): User UUID.

    Returns:
        Tuple[str, str]: (salt_hex, hash_hex)

    Raises:
        ValueError: If no password entry exists for this UUID.
    """
    config = configparser.ConfigParser()
    config.read(PASSWD_FILE)

    if uuid not in config:
        raise ValueError(MysqlServiceCons.L_FAIL_FETCH_PASSWD % uuid)

    salt_hex = config[uuid][MysqlServiceCons.SALT].strip()
    hash_hex = config[uuid][MysqlServiceCons.HASH].strip()

    return salt_hex, hash_hex

def traversal_weak_passwd_list(passwd: str) -> bool:
    """
    Check whether a password appears in the weak password blacklist.

    Args:
        passwd (str): Password to test.

    Returns:
        bool: True if password is weak; False otherwise.
    """
    config = configparser.ConfigParser()
    config.read(WEAK_PASSWD_FILE)

    raw = config[MysqlServiceCons.WEAK_PASSED][MysqlServiceCons.LIST]
    weak_set = {item.strip().lower() for item in raw.split(MysqlServiceCons.COMMA)}

    return passwd.strip().lower() in weak_set

def traversal_username_exist(username: str) -> bool:
    """
    Check if a given username already exists in user.ini.

    Args:
        username (str): Username to test.

    Returns:
        bool: True if exists, False otherwise.
    """
    config = configparser.ConfigParser()
    config.read(USER_INI_FILE)

    for uuid in config.sections():
        if config[uuid][MysqlServiceCons.USERNAME].strip().lower() == username.strip().lower():
            logger.warning(MysqlServiceCons.L_USERNAME_EXISTS % username)
            return True

    logger.info(MysqlServiceCons.L_USERNAME_AVAILABLE % username)
    return False

def insert_user(username: str, name: str, role: Role, passwd: str):
    """
    Insert a new user into the user.ini and passwd.txt files.
    A new UUID is generated and associated with the given user info.

    Steps:
        1. Validate username uniqueness.
        2. Create a unique UUID.
        3. Write user data to user.ini.
        4. Hash password (PBKDF2) and store salt+hash to passwd.txt.

    Args:
        username (str): Username.
        name (str): Full name of user.
        role (Role): Assigned role enum.
        passwd (str): Plaintext password.
    """
    config = configparser.ConfigParser()
    config.read(USER_INI_FILE)

    username_clean = username.strip().lower()

    if traversal_username_exist(username):
        logger.warning(MysqlServiceCons.L_USERNAME_EXISTS, username)
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

    logger.info(MysqlServiceCons.L_SUC_INSERT_USER, username, new_uuid, role.value)


def insert_passwd(uuid: str, salt_hex: str, hash_hex: str):
    """
    Insert a password record for a user UUID into passwd.txt.

    Args:
        uuid (str): User UUID.
        salt_hex (str): Hex-encoded salt.
        hash_hex (str): Hex-encoded PBKDF2 hash.
    """
    config = configparser.ConfigParser()
    config.read(PASSWD_FILE)

    config[uuid] = {
        MysqlServiceCons.SALT: salt_hex,
        MysqlServiceCons.HASH: hash_hex
    }

    with open(PASSWD_FILE, "w") as f:
        config.write(f)

    logger.info(MysqlServiceCons.L_SUC_INSERT_PASSWD, uuid)