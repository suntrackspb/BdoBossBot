from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from api.schemas.boss import BossSchema
from api.schemas.user import UserSchema, UserCreateSchema
from bot.keyboards.inline import notification_keyboard
from bot.utils.constants import BotButtons, get_status_message
from bot.keyboards.reply import main_keyboard
from bot.keyboards.webapp import webapp_builder
from bot.utils.http_client import HttpClient
from bot.utils.functions import down_counter

router = Router()


@router.message(CommandStart())
async def start(message: Message, **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_user(user_id=message.from_user.id)
    if request.status_code == 200:
        data = UserSchema(**request.data)
        return await message.answer(f"Welcome back {message.from_user.full_name},\n"
                                    f"you registered {data.created_at.strftime('%Y-%m-%d %H:%M:%S')}.",
                                    reply_markup=main_keyboard())
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
        bosses = [f'<b>{boss.boss_time}</b> - {", ".join(boss.boss_names)}' for boss in data]
        return await message.answer("\n".join(bosses), reply_markup=main_keyboard())
    else:
        return await message.answer(f'{request.status_code} {request.message}')


@router.message(F.text == BotButtons.NEXT.value)
async def next_boss(message: Message, **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_next_boss()
    print(request)
    if request.status_code == 200:
        boss = BossSchema(**request.data)
        boss_string = f'{boss.boss_time}:00'
        return await message.answer(
            f"Осталось <b>{down_counter(boss_string)}</b> до появления <b>{', '.join(boss.boss_names)}</b>",
            reply_markup=main_keyboard())
    else:
        return await message.answer(f'{request.status_code} {request.message}')


@router.message(F.text == BotButtons.WEEK.value)
async def week(message: Message):
    return await message.answer_photo(
        photo=FSInputFile('bot/images/boss2024.jpg'),
        caption="Week bosses",
        reply_markup=main_keyboard()
    )


@router.message(F.text == BotButtons.NOTIFY.value)
async def notify(message: Message, **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_user(message.from_user.id)
    user = UserSchema(**request.data)
    return await message.answer(get_status_message(user), reply_markup=notification_keyboard(user=user))
