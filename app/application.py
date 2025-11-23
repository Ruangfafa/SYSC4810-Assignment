from app.common.constant import ApplicationCons
from app.common.enum import Request
from app.service.authorization_service import authorization
from app.service.logging_service import get_logger

logger = get_logger(ApplicationCons.LOGGER)

def main(args=None):
    authorization(Request.AS , "c01176a0-158b-40b8-8712-a8faf89f0cc4")

if __name__ == ApplicationCons.MAIN_MODULE:
    main()