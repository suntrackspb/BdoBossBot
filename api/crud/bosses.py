from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Boss


class BossCrud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_boss(self, boss: Boss) -> Boss:
        self.db.add(boss)
        await self.db.commit()
        return boss

    async def get_bosses_list(self):
        return (
            await self.db.execute(select(Boss))
        ).scalars().fetchall()

    async def get_today_bosses_list(self, weekday: int):
        return (
            await self.db.execute(select(Boss).where(Boss.boss_day == weekday))
        ).scalars().fetchall()

