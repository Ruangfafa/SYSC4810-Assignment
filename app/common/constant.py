"""
Centralized constants for the whole application — all the fixed strings,
log messages, and config keys live here.
"""
class ApplicationCons:
    LOGGER = "application"

    MAIN_MODULE="__main__"

class MysqlServiceCons:
    LOGGER = "mysql_service"

    L_TRY_FETCH_UUID = "Fetching role for UUID = %s"
    L_FAIL_FETCH_UUID = "UUID '%s' not found in user.ini"
    L_SUC_FETCH_UUID = "UUID '%s' has role '%s'"
    L_SUC_FETCH_USERNAME = "Username '%s' has UUID '%s'"
    L_FAIL_FETCH_USERNAME = "Username '%s' not found in user.ini"
    L_FAIL_FETCH_PASSWD = "UUID '%s' not found in passwd file"
    L_USERNAME_EXISTS = "Username '%s' already exists"
    L_USERNAME_AVAILABLE = "Username '%s' is available"
    L_SUC_INSERT_USER = "Inserted new user '%s' (%s) with role %s"
    L_SUC_INSERT_PASSWD = "Inserted password record for UUID %s"

    ROLE = "role"
    PERMISSION = "permission"
    COMMA = ","
    USERNAME = "username"
    NAME = "name"
    SALT = "salt_hex"
    HASH = "hash_hex"
    WEAK_PASSED = "weak_passwd"
    LIST = "list"

class SecurityServiceCons:
    LOGGER = "authorization_service"

    L_PERM_ALLOW_1 = "Permission granted normally for request %s uuid=%s"
    L_PERM_ALLOW_2 = "Permission granted by time condition at %s for request %s uuid=%s"
    L_PERM_DENIED_2 = "Permission denied by time window at %s for request %s uuid=%s"
    L_PERM_DENIED = "Permission DENIED for request %s role=%s uuid=%s"
    L_SUC_LOGIN = "Login success for user: %s"
    L_FAIL_LOGIN = "Login failed for user: %s, Reason: Wrong Password"
    L_FAIL_LOGIN_2 = "Login failed for user: %s, Reason: Something went wrong[%s]"
    L_FAIL_LOGIN_3 = "Login failed for username '%s': %s"
    L_FAIL_PASSWD_ADHERE_1 = "Password length should be between 8 and 12"
    L_FAIL_PASSWD_ADHERE_2 = "Password must contain capital letters"
    L_FAIL_PASSWD_ADHERE_3 = "Password must contain lowercase letters"
    L_FAIL_PASSWD_ADHERE_4 = "Password must contain numbers"
    L_FAIL_PASSWD_ADHERE_5 = "Password must contain at least one special character {! @ # $ % * &}"
    L_FAIL_PASSWD_ADHERE_6 = "Password must not be same as username"
    L_FAIL_PASSWD_ADHERE_7 = "Password too weak"
    L_FAIL_PASSWD_ADHERE_8 = "Password contains invalid characters"
    L_SUC_PASSWD_ADHERE = "Password_adhere Pass"

    TIME_FORMAT = "%H:%M"
    HASH_TYPE = "sha256"
    DECODE_TYPE = "utf-8"
    RE_1 = r"[A-Z]"
    RE_2 = r"[a-z]"
    RE_3 = r"[0-9]"
    RE_4 = r"[!@#$%*&]"
    RE_5 = r"[A-Za-z0-9!@#$%*&]+"

