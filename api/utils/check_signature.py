import hashlib
import hmac
import json
from operator import itemgetter
from urllib.parse import parse_qsl

from fastapi import HTTPException, Request
from starlette import status

from common.config import config as cfg
from common.schemas.telegram import InitData
from common.utils.security import decrypt_data


async def verify_webapp_signature(request: Request) -> int:
    # print(request.headers)
    if request.headers.get("Authorization"):
        init_data = request.headers.get("Authorization")
        try:
            parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
            print(parsed_data)
        except ValueError:  # pragma: no cover
            # Init data is not a valid query string
            return False
        if "hash" not in parsed_data:
            # Hash is not present in init data
            return False
        hash_ = parsed_data.pop("hash")

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
        )

        secret_key = hmac.new(key=b"WebAppData", msg=cfg.tlg.bot_token.encode(), digestmod=hashlib.sha256)
        calculated_hash = hmac.new(
            key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()

        print(hash_)
        print(calculated_hash)

        if hash_ != calculated_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid signature",
            )

        json_user = json.loads(parsed_data.get("user"))
        return int(json_user.get("id"))

    if request.headers.get("X-Api-Key"):
        x_api_key = request.headers.get("X-Api-Key")
        print('x_api_key', x_api_key)
        user, token = decrypt_data(x_api_key, cfg.app.secret).split("_", maxsplit=1)
        print(user)
        print('token', token)
        print('cfg.token', cfg.tlg.bot_token)
        if token != cfg.tlg.bot_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key",
            )
        if not bool(int(user)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid User ID",
            )
        return int(user)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No API key provided")


async def check_webapp_signature(init_data: InitData | str) -> InitData | bool:
    token = cfg.tlg.bot_token

    if isinstance(init_data, str):
        if init_data != cfg.tlg.bot_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key",
            )
        return True

    if init_data.hash is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hash is not specified in the request",
        )

    data = init_data.copy(deep=True)
    init_data.user = init_data.user.__str__()

    init_dict = init_data.model_dump()
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
