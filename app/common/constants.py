import os

from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()


class CommonConstants:
    SERVICE_NAME = os.getenv("SERVICE_NAME")
    DEFAULT_REJECTION = "Не совсем понял, задай вопрос еще раз, пожалуйста"


class ModelsConstants:
    GROQ_CLIENT = AsyncGroq(api_key=os.getenv("API_KEY"))
    FILE_SIZE_LIMIT_IN_MB = int(os.getenv("FILE_SIZE_LIMIT_IN_MB")) * 1024 * 1024
    LLM_STRUCTURED_OUTPUT_NAME = os.getenv("LLM_STRUCTURED_OUTPUT_NAME")
    LLM_NAME = os.getenv("LLM_NAME")
    ASR_NAME = os.getenv("ASR_NAME")
    API_IMAGE_KEY=os.getenv("API_IMAGE_KEY")
    IMAGE_GENERATION_NAME = os.getenv("IMAGE_GENERATION_NAME")


class DbConstants:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    DB_URL = (f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}"
              f"@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    DB_CONFIG = {
        "autoflush": False,
        "autocommit": False,
        "expire_on_commit": False,
        "close_resets_only": True
    }

    PYWAY_ENABLED = bool(int(os.getenv("PYWAY_ENABLED")))

    PYWAY_TABLE = os.getenv("PYWAY_TABLE")
    PYWAY_TYPE = os.getenv("PYWAY_TYPE")
    PYWAY_DATABASE_MIGRATION_DIR = os.getenv("PYWAY_DATABASE_MIGRATION_DIR")
