from datetime import datetime
from typing import List

from pydantic import BaseModel

from common.schemas.boss import UserBossSchema
from common.schemas.telegram import InitData
from api.utils.case_converter import camel_to_snake


class UserSchema(BaseModel):
    chat_id: int
    username: str | None = None
    fullname: str | None = None

    is_admin: bool
    is_subscribed: bool
    is_promoted: bool
    is_banned: bool
    is_deleted: bool

    created_at: datetime

    push1: bool
    push5: bool
    push10: bool
    push30: bool


class SpecificUserSchema(BaseModel):
    chat_id: int
    push1: bool
    push5: bool
    push10: bool
    push30: bool
    bosses: List[UserBossSchema] | None = None


class UserCreateSchema(BaseModel):
    chat_id: int
    username: str | None = None
    fullname: str | None = None


class UserUpdateDataSchema(BaseModel):
    is_subscribed: bool | None = None
    is_promoted: bool | None = None

    push1: bool | None = None
    push5: bool | None = None
    push10: bool | None = None
    push30: bool | None = None

    model_config = camel_to_snake


class UserUpdateSchema(BaseModel):
    init_data: InitData
    payload: UserUpdateDataSchema

    model_config = camel_to_snake
