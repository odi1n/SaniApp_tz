import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    ACCESS_LOG: bool = True
    AUTO_RELOAD: bool = True

    TIMEZONE = "Europe/Moscow"

    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT')
    DB_URL: str = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


APP_MODELS: dict = [
    'sanic_app.models',
    'aerich.models'
]

TORTOISE_ORM = {
    "connections": {"default": Config.DB_URL},
    "apps": {
        "models": {
            "models": APP_MODELS,
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": Config.TIMEZONE
}
