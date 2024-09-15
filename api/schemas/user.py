from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator

from api.schemas.boss import BossSchema, UserBossSchema


class UserSchema(BaseModel):
    chat_id: int
    username: str | None = None
    fullname: str | None = None

    is_admin: bool
    is_subscribed: bool
    is_promoted: bool
    is_banned:bool
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
