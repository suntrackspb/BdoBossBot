from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.utils.types import ProfileCallbackFactory


def notification_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Bosses On",
            callback_data=ProfileCallbackFactory(
                action="is_subscribed",
                status=True
            ).pack()
        ),
        InlineKeyboardButton(
            text="Bosses Off",
            callback_data=ProfileCallbackFactory(
                action="is_subscribed",
                status=False
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Promo codes On",
            callback_data=ProfileCallbackFactory(
                action="is_promoted",
                status=True
            ).pack()
        ),
        InlineKeyboardButton(
            text="Promo codes Off",
            callback_data=ProfileCallbackFactory(
                action="is_promoted",
                status=False
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Push 1 min On",
            callback_data=ProfileCallbackFactory(
                action="push1",
                status=True
            ).pack()
        ),
        InlineKeyboardButton(
            text="Push 1 min Off",
            callback_data=ProfileCallbackFactory(
                action="push1",
                status=False
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Push 5 min On",
            callback_data=ProfileCallbackFactory(
                action="push5",
                status=True
            ).pack()
        ),
        InlineKeyboardButton(
            text="Push 5 min Off",
            callback_data=ProfileCallbackFactory(
                action="push5",
                status=False
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Push 10 min On",
            callback_data=ProfileCallbackFactory(
                action="push10",
                status=True
            ).pack()
        ),
        InlineKeyboardButton(
            text="Push 10 min Off",
            callback_data=ProfileCallbackFactory(
                action="push10",
                status=False
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Push 30 min On",
            callback_data=ProfileCallbackFactory(
                action="push30",
                status=True
            ).pack()
        ),
        InlineKeyboardButton(
            text="Push 30 min Off",
            callback_data=ProfileCallbackFactory(
                action="push30",
                status=False
            ).pack()
        )
    )

    return builder.as_markup()
