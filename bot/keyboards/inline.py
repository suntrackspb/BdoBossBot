from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from common.schemas.user import UserSchema
from bot.utils.types import ProfileCallbackFactory


def add_promo_code_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Добавить купон",
            callback_data="add_promo_code"
        )
    )
    return builder.as_markup()


def notification_keyboard(user: UserSchema):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="{} Боссы".format("🟢" if user.is_subscribed else "🔴"),
            callback_data=ProfileCallbackFactory(
                action="is_subscribed",
                status=not user.is_subscribed
            ).pack()
        ),
        InlineKeyboardButton(
            text="{} Купоны".format("🟢" if user.is_promoted else "🔴"),
            callback_data=ProfileCallbackFactory(
                action="is_promoted",
                status=not user.is_promoted
            ).pack()
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="{} 1мин".format("🟢" if user.push1 else "🔴"),
            callback_data=ProfileCallbackFactory(
                action="push1",
                status=not user.push1
            ).pack()
        ),
        InlineKeyboardButton(
            text="{} 5мин".format("🟢" if user.push5 else "🔴"),
            callback_data=ProfileCallbackFactory(
                action="push5",
                status=not user.push5
            ).pack()
        ),

    )
    builder.row(
        InlineKeyboardButton(
            text="{} 10мин".format("🟢" if user.push10 else "🔴"),
            callback_data=ProfileCallbackFactory(
                action="push10",
                status=not user.push10
            ).pack()
        ),

        InlineKeyboardButton(
            text="{} 30мин".format("🟢" if user.push30 else "🔴"),
            callback_data=ProfileCallbackFactory(
                action="push30",
                status=not user.push30
            ).pack()
        ),
    )

    return builder.as_markup()
