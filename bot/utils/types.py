from typing import Literal

from aiogram.filters.callback_data import CallbackData


class ProfileCallbackFactory(CallbackData, prefix="profile"):
    action: Literal["is_subscribed", "is_promoted", "push1", "push5", "push10", "push30"]
    status: bool

