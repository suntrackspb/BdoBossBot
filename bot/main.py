from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiohttp import ClientConnectorError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from environs import Env

from bot.handlers import default
from bot.middleware.web_api_middleware import WebApiMiddleware
from bot.utils.http_client import HttpClient

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
web_api_url = env('WEB_API_URL')
http_client = HttpClient(api_url=web_api_url, api_key=bot_token)

bot = Bot(bot_token, default=DefaultBotProperties(parse_mode='HTML'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.update.middleware(WebApiMiddleware(client=http_client))
dp.callback_query.middleware(CallbackAnswerMiddleware())

dp.include_routers(
    default.router
)


async def set_bot_commands() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Register the bot"),
            BotCommand(command="/settings", description="Open settings WebApp"),
            BotCommand(command="/id", description="Get the user and chat ids"),
        ],
    )


async def send_notification(bot: Bot, http_client: HttpClient) -> None:
    try:
        data = await http_client.get_notify_list()
        print(data)
    except ClientConnectorError:
        print("No connection")

    # await bot.send_message(chat_id=CHAT_ID, text="Это ваше запланированное уведомление!")


@dp.startup()
async def on_startup() -> None:
    await bot.delete_webhook(True)
    await set_bot_commands()



async def main() -> None:
    try:
        # scheduler = AsyncIOScheduler()
        # scheduler.add_job(send_notification, "interval", seconds=5, args=(bot, http_client))
        # scheduler.start()
        await dp.start_polling(bot, polling_timeout=3)
    finally:
        await dp.storage.close()
        await bot.session.close()



