from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from api.schemas.user import UserSchema
from bot.utils.types import ProfileCallbackFactory


def notification_keyboard(user: UserSchema):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"🟢 Боссы" if user.is_subscribed else "🔴 Боссы",
            callback_data=ProfileCallbackFactory(
                action="is_subscribed",
                status=not user.is_subscribed
            ).pack()
        ),
        InlineKeyboardButton(
            text=f"🟢 Купоны" if user.is_promoted else "🔴 Купоны",
            callback_data=ProfileCallbackFactory(
                action="is_promoted",
                status=not user.is_promoted
            ).pack()
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"🟢 1мин" if user.push1 else "🔴 1мин",
            callback_data=ProfileCallbackFactory(
                action="push1",
                status=not user.push1
            ).pack()
        ),
        InlineKeyboardButton(
            text=f"🟢 5мин" if user.push5 else "🔴 5мин",
            callback_data=ProfileCallbackFactory(
                action="push5",
                status=not user.push5
            ).pack()
        ),

    )
    builder.row(
        InlineKeyboardButton(
            text=f"🟢 10мин" if user.push10 else "🔴 10мин",
            callback_data=ProfileCallbackFactory(
                action="push10",
                status=not user.push10
            ).pack()
        ),

        InlineKeyboardButton(
            text=f"🟢 30мин" if user.push30 else "🔴 30мин",
            callback_data=ProfileCallbackFactory(
                action="push30",
                status=not user.push30
            ).pack()
        ),
    )
    # builder.row(
    #     InlineKeyboardButton(
    #         text="1 🔴",
    #         callback_data=ProfileCallbackFactory(
    #             action="push1",
    #             status=False
    #         ).pack()
    #     ),
    #     InlineKeyboardButton(
    #         text="5 🔴",
    #         callback_data=ProfileCallbackFactory(
    #             action="push5",
    #             status=False
    #         ).pack()
    #     ),
    #     InlineKeyboardButton(
    #         text="10 🔴",
    #         callback_data=ProfileCallbackFactory(
    #             action="push10",
    #             status=False
    #         ).pack()
    #     ),
    #     InlineKeyboardButton(
    #         text="30 🔴",
    #         callback_data=ProfileCallbackFactory(
    #             action="push30",
    #             status=False
    #         ).pack()
    #     )
    # )

    return builder.as_markup()
