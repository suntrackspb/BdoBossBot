from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.utils.types import ProfileCallbackFactory


def notification_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Subscribe On",
            callback_data=ProfileCallbackFactory(
                action="is_subscribed",
                status=True
            ).pack()
        ),
        InlineKeyboardButton(
            text="Subscribe Off",
            callback_data=ProfileCallbackFactory(
                action="is_subscribed",
                status=False
            ).pack()
        )
    )

    return builder.as_markup()
