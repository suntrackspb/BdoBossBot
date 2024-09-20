from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from api.schemas.boss import BossSchema
from api.schemas.user import UserSchema
from bot.keyboards.inline import notification_keyboard
from bot.keyboards.reply import main_keyboard
from bot.utils.constants import BotButtons, get_status_message
from bot.utils.functions import down_counter
from bot.utils.http_client import HttpClient

router = Router()


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
        caption="Расписание боссов на неделю",
        reply_markup=main_keyboard()
    )


@router.message(F.text == BotButtons.NOTIFY.value)
async def notify(message: Message, **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_user(message.from_user.id)
    user = UserSchema(**request.data)
    return await message.answer(get_status_message(user), reply_markup=notification_keyboard(user=user))


