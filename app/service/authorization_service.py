from datetime import datetime
from zoneinfo import ZoneInfo

from app.common.config_loader import TIME_ZONE
from app.common.constant import AuthorizationServiceCons
from app.common.enum import Request
from app.service.logging_service import get_logger
from app.service.mysql_service import get_role, get_role_permission

logger = get_logger(AuthorizationServiceCons.LOGGER)

def authorization(request: Request, uuid: str) -> bool:
    user_role = get_role(uuid)
    role_permission = get_role_permission(user_role)

    if role_permission[request.value] == 1:
        logger.info(AuthorizationServiceCons.L_PERM_ALLOW_1 % request.name)
        return True

    if role_permission[request.value] == 2:
        now = datetime.now(ZoneInfo(TIME_ZONE))
        cur_time = now.hour * 100 + now.minute

        if 900 <= cur_time < 1700:
            logger.info(AuthorizationServiceCons.L_PERM_ALLOW_2 % request.name)
            return True
        logger.warning(AuthorizationServiceCons.L_PERM_DENIED_2 % request.name)

    logger.warning(AuthorizationServiceCons.L_PERM_DENIED % (request.name, user_role.name, uuid))
    return False