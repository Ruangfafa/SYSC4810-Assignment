class ApplicationCons:
    LOGGER = "application"

    MAIN_MODULE="__main__"

class MysqlServiceCons:
    LOGGER = "mysql_service"

    L_TRY_FETCH_UUID = "Fetching role for UUID = %s"
    L_FAIL_GET_UUID = "UUID '%s' not found in user.ini"
    L_SUC_GET_UUID = "UUID '%s' has role '%s'"

    ROLE = "role"
    PERMISSION = "permission"

class AuthorizationServiceCons:
    LOGGER = "authorization_service"

    L_PERM_ALLOW_1 = "Permission granted normally for request %s"
    L_PERM_ALLOW_2 = "Permission granted by time condition for request %s"
    L_PERM_DENIED_2 = "Permission denied by time window for request %s"
    L_PERM_DENIED = "Permission DENIED for request %s role=%s uuid=%s"