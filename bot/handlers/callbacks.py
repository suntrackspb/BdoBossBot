from aiogram import Router
from aiogram.types import CallbackQuery

from api.schemas.user import UserSchema
from bot.utils.http_client import HttpClient
from bot.utils.types import ProfileCallbackFactory

router = Router()


@router.callback_query(ProfileCallbackFactory.filter())
async def callback_vpn_profile(callback: CallbackQuery, callback_data: ProfileCallbackFactory,  **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_user(user_id=callback.from_user.id)
    user = UserSchema(**request.data)
    print(callback_data)
    return await callback.answer()
