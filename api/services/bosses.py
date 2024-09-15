from datetime import datetime

from api.config import config as cfg
from api.crud.bosses import BossCrud
from api.models.models import Boss
from api.utils.next_boss import NextBossService


class BossService:
    def __init__(self, crud: BossCrud):
        self.crud = crud
        self.cfg = cfg

    async def get_bosses_list(self):
        bosses = await self.crud.get_bosses_list()
        return bosses

    async def add_boss(self, boss: Boss):
        return await self.crud.add_boss(boss)

    async def get_next_boss(self):
        bosses = await self.get_bosses_list()
        next_boss = NextBossService(bosses)
        return next_boss.get_next_boss()

    async def get_today_bosses(self):
        weekday = datetime.now().weekday() + 1
        return await self.crud.get_today_bosses_list(weekday=weekday)

