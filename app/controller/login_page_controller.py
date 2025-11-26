from app.common.enum import Role
from app.service.logging_service import get_logger
from app.service.mysql_service import traversal_username_exist, insert_user
from app.service.security_service import password_adhere

logger = get_logger("login_page_controller")

def register(username: str, password: str, name: str, role: Role):
    username = username.lower().strip()

    if traversal_username_exist(username):
        logger.warning("Username %s is already registered", username)
        return

    if not password_adhere(password, username):
        logger.warning("Password does not meet adhere")
        return

    insert_user(username, name, role, password)