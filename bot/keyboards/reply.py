from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.utils.constants import BotButtons


def main_keyboard():
    builder = ReplyKeyboardBuilder()
    # builder.row(
    #
    # )
    builder.row(
        KeyboardButton(text=BotButtons.TODAY.value),
        KeyboardButton(text=BotButtons.NEXT.value),
        KeyboardButton(text=BotButtons.WEEK.value),
    )
    builder.row(
        KeyboardButton(text=BotButtons.PROMO.value),
        KeyboardButton(text=BotButtons.ADD_PROMO.value),
    )
    builder.row(
        KeyboardButton(text=BotButtons.NOTIFY.value),
    )

    return builder.as_markup(resize_keyboard=True)


