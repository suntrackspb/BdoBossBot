from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from common.schemas.user import UserSchema, UserCreateSchema
from bot.keyboards.reply import main_keyboard
from bot.keyboards.webapp import webapp_builder
from bot.utils.http_client import HttpClient

router = Router()


@router.message(CommandStart())
async def start(message: Message, **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_user(user_id=message.from_user.id)
    if request.status_code == 200:
        data = UserSchema(**request.data)
        return await message.answer(f"С возвращением {message.from_user.full_name},\n"
                                    f"ваш аккаунт был создан {data.created_at.strftime('%Y-%m-%d %H:%M:%S')}.",
                                    reply_markup=main_keyboard())
    elif request.status_code == 404:
        await client.add_user(
            user=UserCreateSchema(
                chat_id=message.chat.id,
                fullname=message.from_user.full_name,
                username=message.from_user.username,
            )
        )
        return await message.answer(f'Добро пожаловать {message.from_user.full_name}, вы были зарегистрированы.',)
    else:
        await message.answer(f'{request.status_code} {request.message}')


@router.message(Command(commands='settings'))
async def settings(message: Message):
    await message.answer(
        text="User Settings",
        reply_markup=webapp_builder()
    )


@router.message(Command(commands='help'))
async def settings(message: Message):
    await message.answer(
        text="User Settings",
        reply_markup=webapp_builder()
    )


@router.message(Command(commands='id'))
async def settings(message: Message):
    await message.answer(
        text=f"Ваш ID: `{message.from_user.id}`", parse_mode="Markdown",
    )


@router.message()
async def settings(message: Message):
    if message.forward_from:
        return await message.reply(
            f"Forward ID: `{message.forward_from.id}`\n"
            f"Forward name: `{message.forward_from.full_name}`\n"
            f"Forward username: `{message.forward_from.username}`",
            parse_mode="Markdown"
        )
    if message.forward_from_chat:
        return await message.reply(
            f"Channel ID: `{message.forward_from_chat.id}`\n"
            f"Channel title: `{message.forward_from_chat.title}`\n"
            f"Channel type: `{message.forward_from_chat.type}`",
            parse_mode="Markdown"
        )
    print (message.model_dump_json())
    await message.answer(
        text=message.text,
    )
