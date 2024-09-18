from typing import cast, List

from sqlalchemy import Integer, Boolean, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.testing.suite.test_reflection import users

from api.models import Notification, User, Boss
from api.schemas.notification import NotificationSchema


class NotificationCrud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_notification(self, chat_id: int, bosses: list):
        query = delete(Notification).where(Notification.chat_id == chat_id)
        await self.db.execute(query)
        await self.db.commit()

        for boss in bosses:
            notification = Notification(chat_id=chat_id, boss_id=boss)
            self.db.add(notification)

        await self.db.commit()

    async def get_notify_by_user(self, user_id: int):
        result = await self.db.execute(
            select(Notification).where(cast(Notification.chat_id, Integer) == user_id)
        )
        return result.scalars().all()

    async def get_notify_by_boss(self, boss_id: int):
        result = await self.db.execute(
            select(Notification).where(cast(Notification.boss_id, Integer) == boss_id)
        )
        return result.scalars().all()

    async def notify_list(self, boss_id: int, user_push: InstrumentedAttribute):
        query = (
            select(
                User.chat_id,
                User.fullname,
                User.username,
                User.is_subscribed,
                User.push1,
                User.push5,
                User.push10,
                User.push30,
                Boss.boss_names
            )
            .select_from(Notification)
            .join(Boss, Notification.boss_id == Boss.id)
            .join(User, Notification.chat_id == User.chat_id)
            .where(
                Notification.boss_id == boss_id,
                user_push == True,
            )
        )
        print(query)
        result = await self.db.execute(query)
        rows = result.fetchall()
        keys = result.keys()

        data = [dict(zip(keys, row)) for row in rows]

        return data
