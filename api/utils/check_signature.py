import hmac
import hashlib
from typing import Annotated

from fastapi import Header, HTTPException
from starlette import status

from api.config import config as cfg


def check_telegram_signature(init_data: dict) -> bool:
    token = cfg.telegram.bot_token
    # Получаем hash из данных
    received_hash = init_data.pop('hash', None)

    # Создаем строку параметров, отсортированных по алфавиту
    data_check_string = '\n'.join([f'{key}={value}' for key, value in sorted(init_data.items())])

    # Создаем HMAC-SHA256
    secret_key = hmac.new(key=token.encode(), msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    # Сравниваем хеши
    return secret_key == received_hash


async def verify_api_key(x_api_key: Annotated[str, Header()]):
    if x_api_key != cfg.tlg.bot_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )