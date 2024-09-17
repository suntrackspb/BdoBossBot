from datetime import datetime, timedelta
from typing import List

from api.config import config as cfg
from api.crud.notifications import NotificationCrud
from api.models import Boss, User
from api.schemas.op_status import Status
from api.utils.constants import Push


class NotificationService:
    def __init__(self, crud: NotificationCrud):
        self.crud = crud
        self.cfg = cfg

    async def generate_notification(self, user: User, bosses: List[Boss]):
        bosses_ids = [boss.id for boss in bosses]
        await self.crud.add_notification(chat_id=user.chat_id, bosses=bosses_ids)
        return Status(status='OK', message='Successfully added notification')

    async def add_notifications(self, user: User, bosses: list):
        await self.crud.add_notification(chat_id=user.chat_id, bosses=bosses)
        return Status(status='OK', message='Successfully added notification')

    async def get_notify_users_by_boss(self, boss: Boss):
        current_time = datetime.now().strftime("%H:%M")
        boss_time = datetime.strptime(boss.boss_time, "%H:%M")

        current_time = datetime.strptime("11:50", "%H:%M")

        if boss.boss_time == "00:00":
            boss_time = boss_time + timedelta(days=1)

        # Преобразуем текущие время и время босса в объекты datetime
        # current_time_dt = datetime.strptime(current_time, "%H:%M")

        # print(boss_time, current_time)

        # Рассчитываем разницу во времени
        time_difference = (boss_time - current_time).total_seconds() / 60  # разница в минутах

        print(time_difference)

        if time_difference in [1, 5, 10, 30]:
            print(f'Difference: {time_difference} minutes')
            data = await self.crud.notify_list(boss_id=boss.id, user_push=Push[time_difference])
            print("===", data)
            return data

        # if time_difference == 30:
        #     print("Разница 30 минут")
        #     return await self.crud.notify_list(boss_id=boss.id, push=User.push30)
        # elif time_difference == 10:
        #     print("Разница 10 минут")
        #     return await self.crud.notify_list(boss_id=boss.id, push=User.push10)
        # elif time_difference == 5:
        #     print("Разница 5 минут")
        #     return await self.crud.notify_list(boss_id=boss.id, push=User.push5)
        # elif time_difference == 1:
        #     print("Разница 1 минут")
        #     return await self.crud.notify_list(boss_id=boss.id, push=User.push1)

        return []
