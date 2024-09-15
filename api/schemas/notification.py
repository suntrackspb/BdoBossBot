from typing import List

from pydantic import BaseModel


class NotificationSchema(BaseModel):
    chat_id: int
    username: str
    boss_names: str


class AddNotification(BaseModel):
    chat_id: int
    boss_list: List[int]
    push_list: List[int]
