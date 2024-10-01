from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def webapp_builder() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="Open",
        web_app=WebAppInfo(
            url='http://127.0.0.1:5173',
        )
    )
    return keyboard.as_markup()
