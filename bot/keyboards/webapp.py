from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def webapp_builder() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="Open",
        web_app=WebAppInfo(
            url='https://e3a1-2a0e-8086-0-301-e055-bc0d-ae20-a886.ngrok-free.app/',
        )
    )
    return keyboard.as_markup()
