from app.common.constants import LogMessageCons, ApplicationCons
from app.service.logging_service import get_logger

logger = get_logger(LogMessageCons.LOGGER_NAME)

def main(args=None):
    pass

if __name__ == ApplicationCons.MAIN_MODUAL:
    main()