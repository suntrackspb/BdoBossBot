from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from environs import Env

from api.schemas.boss import BossSchema
from api.schemas.user import UserSchema, UserCreateSchema
from bot.utils.constants import BotButtons
from bot.keyboards.reply import main_keyboard
from bot.keyboards.webapp import webapp_builder
from bot.utils.http_client import HttpClient

router = Router()

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
web_api_url = env('WEB_API_URL')


@router.message(CommandStart())
async def start(message: Message, **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_user(user_id=message.from_user.id)
    if request.status_code == 200:
        data = UserSchema(**request.data)
        return await message.answer(f"Welcome back {message.from_user.full_name} {data.created_at}!", reply_markup=main_keyboard())
    elif request.status_code == 404:
        await client.add_user(
            user=UserCreateSchema(
                chat_id=message.chat.id,
                fullname=message.from_user.full_name,
                username=message.from_user.username,
            )
        )
        return await message.answer(f'Welcome {message.from_user.full_name}, you has been registered')
    else:
        await message.answer(f'{request.status_code} {request.message}')


@router.message(Command(commands='settings'))
async def settings(message: Message):
    await message.answer(
        text="User Settings",
        reply_markup=webapp_builder()
    )


@router.message(F.text == BotButtons.TODAY.value)
async def today(message: Message, **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_today_bosses()
    print(request)
    if request.status_code == 200:
        data = [BossSchema(**boss) for boss in request.data]
        bosses = [f'{boss.boss_time} : {", ".join(boss.boss_names)}' for boss in data]
        return await message.answer("\n".join(bosses), reply_markup=main_keyboard())
    else:
        return await message.answer(f'{request.status_code} {request.message}')

