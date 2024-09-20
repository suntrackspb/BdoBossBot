from typing import List

from pydantic import BaseModel


class NotificationSchema(BaseModel):
    chat_id: int
    fullname: str
    # boss_names: str


class BossNotificationSchema(BaseModel):
    boss_names: str
    time_difference: int
    users: List[NotificationSchema]


class AddNotification(BaseModel):
    init_data: dict
    boss_list: List[int]
    push_list: List[int]
