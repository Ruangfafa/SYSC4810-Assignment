from app.common.constant import ApplicationCons
from app.service.logging_service import get_logger

logger = get_logger(ApplicationCons.LOGGER)

def main(args=None):
    pass

if __name__ == ApplicationCons.MAIN_MODULE:
    main()