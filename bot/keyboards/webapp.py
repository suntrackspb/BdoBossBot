from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def webapp_builder() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="Open",
        web_app=WebAppInfo(
            url='https://sntrk.ru/',
        )
    )
    return keyboard.as_markup()
