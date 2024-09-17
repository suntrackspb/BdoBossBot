from typing import Type, List

from sqlalchemy import select, case, bindparam, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User, Notification, Boss
from api.schemas.boss import UserBossSchema
from api.schemas.user import UserUpdateSchema


class UserCrud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: int) -> Type[User] | None:
        user = await self.db.get(User, user_id)
        if user:
            return user
        return None

    async def get_user_notify(self, user_id: int) -> List[UserBossSchema]:
        subquery = (
            select(Notification.boss_id)
            .where(Notification.chat_id == user_id,
                   Notification.boss_id == Boss.id)
            .correlate(Boss)
            .exists()
        )

        query = (
            select(
                Boss,
                case(
                    (subquery, True),
                    else_=False
                ).label('is_selected')
            )
        )

        result = await self.db.execute(query)
        results = result.all()

        user_bosses = [
            UserBossSchema(
                id=boss.id,
                boss_day=boss.boss_day,
                boss_time=boss.boss_time,
                boss_names=boss.boss_names,
                is_selected=is_selected
            )
            for boss, is_selected in results
        ]
        return user_bosses

    async def get_users(self):
        return (
            await self.db.execute(select(User))
        ).scalars().fetchall()

    async def add_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user: User, user_update: UserUpdateSchema) -> User:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> None:
        await self.db.delete(await self.db.get(User, user_id))
        await self.db.commit()

