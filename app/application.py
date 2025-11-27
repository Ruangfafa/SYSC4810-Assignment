from app.common.constant import ApplicationCons
from app.service.logging_service import get_logger
from app.view.system_view import system_view

logger = get_logger(ApplicationCons.LOGGER)

def main():
    system_view()

if __name__ == ApplicationCons.MAIN_MODULE:
    main()