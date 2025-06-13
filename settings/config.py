from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
import logging
import os


log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bot_logs.txt")

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"


# Хранение задач и товаров по пользователю
user_tasks = {}
user_products = {}

ITEMS_PER_PAGE = 1  # Кол-во отзывов на одной странице


class Settings(BaseSettings):
    bot_token: SecretStr
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_config: ClassVar[SettingsConfigDict] = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


config = Settings()


def media_file():
    return os.path.join(config.BASE_DIR, "assets", "IMG_0934.MP4")
