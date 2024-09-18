from datetime import datetime, timedelta
from typing import List

from api.config import config as cfg
from api.crud.notifications import NotificationCrud
from api.models import Boss, User
from api.schemas.notification import BossNotificationSchema
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
        if boss.boss_time == "00:00":
            boss_time = boss_time + timedelta(days=1)

        current_time_dt = datetime.strptime(current_time, "%H:%M")
        time_difference = (boss_time - current_time_dt).total_seconds() / 60  # разница в минутах

        # DEBUG & TESTS
        # current_time = datetime.strptime("18:50", "%H:%M")
        # time_difference = (boss_time - current_time).total_seconds() / 60
        # print(time_difference, datetime.now().strftime("%H:%M:%S"))

        if time_difference in [1, 5, 10, 30]:
            # print(f'Difference: {time_difference} minutes')
            data = await self.crud.notify_list(boss_id=boss.id, user_push=Push[time_difference])
            if data:
                return BossNotificationSchema(
                    boss_names=boss.boss_names,
                    time_difference=int(time_difference),
                    users=data
                )
            else:
                return None
