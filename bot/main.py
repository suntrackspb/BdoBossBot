from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiohttp import ClientConnectorError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from environs import Env

from api.schemas.notification import NotificationSchema, BossNotificationSchema
from bot.handlers import default_router, callback_router
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
    callback_router,
    default_router
)


async def set_bot_commands() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Register the bot"),
            BotCommand(command="/settings", description="Open settings WebApp"),
            BotCommand(command="/id", description="Get the user and chat ids"),
        ],
    )


async def send_notification(bot_: Bot, http_client_: HttpClient) -> None:
    try:
        request = await http_client_.get_notify_list()
        if request.data is not None:
            notify = BossNotificationSchema(**request)
            for user in notify.users:
                await bot_.send_message(
                    chat_id=user.chat_id,
                    text=f"Через {notify.time_difference} минут появятся {notify.boss_names}"
                )
    except ClientConnectorError:
        print("No connection")
    except AttributeError:
        print("Empty data")

    # await bot.send_message(chat_id=CHAT_ID, text="Это ваше запланированное уведомление!")


@dp.startup()
async def on_startup() -> None:
    await bot.delete_webhook(True)
    await set_bot_commands()


async def main() -> None:
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_notification, "interval", seconds=5, args=(bot, http_client))
        # trigger = CronTrigger(second='1')
        # scheduler.add_job(send_notification, args=(bot, http_client))
        scheduler.start()
        await dp.start_polling(bot, polling_timeout=3)
    finally:
        await dp.storage.close()
        await bot.session.close()



