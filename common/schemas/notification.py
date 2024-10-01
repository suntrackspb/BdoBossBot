from typing import List

from pydantic import BaseModel

from api.utils.case_converter import camel_to_snake


class NotificationSchema(BaseModel):
    chat_id: int
    fullname: str
    # boss_names: str


class BossNotificationSchema(BaseModel):
    boss_names: str
    time_difference: int
    users: List[NotificationSchema]


class NotificationAddAllSchema(BaseModel):
    is_selected: bool

    model_config = camel_to_snake


class NotificationAddSchema(NotificationAddAllSchema):
    boss_id: int

    model_config = camel_to_snake
