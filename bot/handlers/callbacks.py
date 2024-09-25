from aiogram import Router
from aiogram.types import CallbackQuery

from common.schemas.user import UserSchema
from bot.keyboards.inline import notification_keyboard
from bot.utils.constants import get_status_message
from bot.utils.http_client import HttpClient
from bot.utils.types import ProfileCallbackFactory

router = Router()


@router.callback_query(ProfileCallbackFactory.filter())
async def callback_vpn_profile(callback: CallbackQuery, callback_data: ProfileCallbackFactory,  **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_user(user_id=callback.from_user.id)
    user = UserSchema(**request.data)
    update = await client.update_user(user=user, params={callback_data.action: callback_data.status})
    user = UserSchema(**update.data)
    return await callback.message.edit_text(get_status_message(user), reply_markup=notification_keyboard(user=user))
