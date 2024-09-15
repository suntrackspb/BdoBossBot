from datetime import datetime
from typing import List

from api.models import Boss


class NextBossService:
    def __init__(self, boss_list: List[Boss]):
        self.current = datetime.now()
        self.boss_list = boss_list

    def get_bosses_by_day(self, day):
        current_day = day if day < 7 else 0
        return list(filter(lambda boss: boss.boss_day == current_day, self.boss_list))

    def get_next_boss(self):
        current_day = (self.current.weekday() + 1) % 7
        current_time = self.current.strftime('%H:%M:%S')

        boss_by_current_day = next((boss for boss in self.get_bosses_by_day(current_day) if
                                    datetime.now().replace(hour=int(current_time.split(':')[0]),
                                                           minute=int(current_time.split(':')[1])) <
                                    datetime.now().replace(hour=int(boss.boss_time.split(':')[0]),
                                                           minute=int(boss.boss_time.split(':')[1]))), None)

        if boss_by_current_day:
            return boss_by_current_day
        else:
            return self.get_bosses_by_day(current_day + 1)[0]
