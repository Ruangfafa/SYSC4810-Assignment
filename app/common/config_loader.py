import os, sys
from pathlib import Path
from dotenv import load_dotenv


if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent


USER_INI_FILE = BASE_DIR / "resources/user.ini"
ROLE_PERMISSION_FILE = BASE_DIR / "resources/role_permission.ini"
load_dotenv(BASE_DIR / ".env")

TIME_ZONE = os.getenv("TIME_ZONE")

#SAMPLE_CONST = os.getenv("SAMPLE_CONST")