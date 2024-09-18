from enum import Enum

from api.schemas.user import UserSchema


class BotButtons(Enum):
    NEXT = 'Следующий'
    TODAY = 'На сегодня'
    WEEK = 'На неделю'
    NOTIFY = 'Уведомления'
    PROMO = 'Купоны'
    ADD_PROMO = 'Добавить купон'
    HELP = 'Help'


def get_status_message(user: UserSchema):
    return f"Настройки уведомлений для {user.fullname}:"

