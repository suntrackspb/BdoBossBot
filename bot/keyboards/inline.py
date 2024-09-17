from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def notification_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Кнопка 1", callback_data="button1"))
    builder.add(InlineKeyboardButton(text="Кнопка 2", callback_data="button2"))

    return builder.as_markup()



