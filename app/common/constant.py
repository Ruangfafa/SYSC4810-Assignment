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

    ROLE = "role"
    PERMISSION = "permission"
    COMMA = ","
    USERNAME = "username"
    SALT = "salt_hex"
    HASH = "hash_hex"

class SecurityServiceCons:
    LOGGER = "authorization_service"

    L_PERM_ALLOW_1 = "Permission granted normally for request %s uuid=%s"
    L_PERM_ALLOW_2 = "Permission granted by time condition at %s for request %s uuid=%s"
    L_PERM_DENIED_2 = "Permission denied by time window at %s for request %s uuid=%s"
    L_PERM_DENIED = "Permission DENIED for request %s role=%s uuid=%s"
    L_SUC_LOGIN = "Login success for user: %s"
    L_FAIL_LOGIN = "Login failed for user: %s, Reason: Wrong Password"
    L_FAIL_LOGIN_2 = "Login failed for user: %s, Reason: Something went wrong[%s]"

    TIME_FORMAT = "%H:%M"