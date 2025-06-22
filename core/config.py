from pathlib import Path
from pydantic_settings import BaseSettings
import os

container = False

BASE_DIR = Path(__file__).parent.parent

UPLOAD_DIR = "images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Настройка для раздачи статических файлов
STATIC_MOUNT_PATH = "/images"
STATIC_DIR = os.path.join(BASE_DIR, UPLOAD_DIR)


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_host: str = "host.docker.internal" if container else "localhost"

    db_url: str  = f"postgresql+asyncpg://postgres:jamshid007@{db_host}:5432/snovidenie_db"
    db_echo: bool = False


settings = Setting()