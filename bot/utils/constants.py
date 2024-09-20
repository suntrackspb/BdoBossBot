from enum import Enum

from api.schemas.user import UserSchema


class BotButtons(Enum):
    NEXT = 'Когда следующий босс?'
    TODAY = 'Боссы на сегодня'
    WEEK = 'Боссы на неделю'
    NOTIFY = 'Уведомления'
    PROMO = 'Купоны'
    ADD_PROMO = 'Добавить купон'
    HELP = 'Help'


def get_status_message(user: UserSchema):
    return f"Настройки уведомлений для {user.fullname}:"

