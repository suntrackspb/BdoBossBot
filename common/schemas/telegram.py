import json
from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator

from api.utils.case_converter import camel_to_snake


class InitUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
    allows_write_to_pm: bool

    model_config = camel_to_snake

    def __str__(self):
        return json.dumps(self.dict(), ensure_ascii=False, separators=(',', ':'))


class InitData(BaseModel):
    hash: str
    query_id: str
    user: InitUser | str
    auth_date: int

    model_config = camel_to_snake

    @field_validator('auth_date', mode='before')
    @classmethod
    def validate_field(cls, input_value):
        if input_value is None:
            return None
        return int(datetime.strptime(input_value, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp() + 10800)


class NotificationAddSchema(BaseModel):
    boss_id: int
    is_selected: bool

    model_config = camel_to_snake


class NotificationAllSchema(BaseModel):
    is_selected: bool

    model_config = camel_to_snake

