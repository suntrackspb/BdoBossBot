from typing import List

from pydantic import BaseModel, field_validator


class BossSchema(BaseModel):
    id: int
    boss_day: int
    boss_time: str
    boss_names: List[str]

    @field_validator('boss_names', mode='before')
    def split_boss_names(cls, value):
        if isinstance(value, str):
            return value.split(', ')  # Разделяем строку по запятым
        return value


class UserBossSchema(BossSchema):
    is_selected: bool
