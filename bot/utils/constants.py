from enum import Enum

from api.schemas.user import UserSchema


class BotButtons(Enum):
    NEXT = 'Next Boss'
    TODAY = 'Today Bosses'
    WEEK = 'Weekly Bosses'
    NOTIFY = 'Notification'
    PROMO = 'Promo codes'
    ADD_PROMO = 'Add promo code'
    HELP = 'Help'


def get_status_message(user: UserSchema):
    return f"""
<b>{"🟢" if user.is_subscribed else "🔴"}</b> Bosses

<b>{"🟢" if user.is_promoted else "🔴"}</b> Promo codes

<b>{"🟢" if user.push1 else "🔴"}</b> Push 1 min

<b>{"🟢" if user.push5 else "🔴"}</b> Push 5 min

<b>{"🟢" if user.push10 else "🔴"}</b> Push 10 min

<b>{"🟢" if user.push30 else "🔴"}</b> Push 30 min
    """
