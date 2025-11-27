"""
This configuration loader module is reused from my previous projects.
It centralizes all file path resolutions and environment variable loading
so that the rest of the application can access configuration values
without hard-coding paths or relying on fixed directory structures.

It simply provides convenient access to INI files, password files,
and .env variables, and does not introduce logic specific to this assignment.
"""
import os, sys
from pathlib import Path
from dotenv import load_dotenv


if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent


USER_INI_FILE = BASE_DIR / "resources/user.ini"
ROLE_PERMISSION_FILE = BASE_DIR / "resources/role_permission.ini"
PASSWD_FILE = BASE_DIR / "resources/passwd.txt"
WEAK_PASSWD_FILE = BASE_DIR / "resources/weak_passwd.ini"
load_dotenv(BASE_DIR / ".env")

TIME_ZONE = os.getenv("TIME_ZONE")

#SAMPLE_CONST = os.getenv("SAMPLE_CONST")