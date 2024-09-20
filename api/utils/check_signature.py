import hashlib
import hmac
from operator import itemgetter
from typing import Annotated

from fastapi import Header, HTTPException
from starlette import status

from api.config import config as cfg
from api.schemas.telegram import InitDataSchema, InitData


def check_webapp_signature(init_data: InitDataSchema) -> InitDataSchema:
    token = cfg.tlg.bot_token

    if init_data.init_data.hash is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hash is not specified in the request",
        )

    data = init_data.copy(deep=True)
    init_data.init_data.user = init_data.init_data.user.__str__()
    init_dict = init_data.init_data.model_dump()

    hash_ = init_dict.pop("hash")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(init_dict.items(), key=itemgetter(0))
    )

    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    print(hash_, calculated_hash, sep="\n")

    if hash_ != calculated_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature",
        )

    return data


async def verify_api_key(x_api_key: Annotated[str, Header()]):
    if x_api_key != cfg.tlg.bot_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
