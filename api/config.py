import json
import logging
import logging.config

from environs import Env

from api.schemas.config import Config, AppConfig, PostgresCfg, TelegramConfig

with open('logging_config.json', 'r') as file:
    logging_config = json.load(file)

logging.config.dictConfig(logging_config)


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env()
    return Config(
        app=AppConfig(
            host=env('APP_HOST'),
            port=env('APP_PORT'),
            secret=env('APP_SECRET'),
            logger=logging.getLogger("uvicorn.custom_logger")
        ),
        pgsql=PostgresCfg(
            user=env('POSTGRES_USER'),
            password=env('POSTGRES_PASSWORD'),
            host=env('POSTGRES_HOST'),
            port=int(env('POSTGRES_PORT')),
            name=env('POSTGRES_DB'),
            echo=False
        ),
        tlg=TelegramConfig(
            bot_token=env('BOT_TOKEN'),
            web_api_url=env('WEB_API_URL')
        )
    )


config = load_config()
