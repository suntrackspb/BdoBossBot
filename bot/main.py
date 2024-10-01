from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiohttp import ClientConnectorError
from environs import Env

from common.config import config
from common.schemas.notification import BossNotificationSchema
from bot.handlers import callback_router, default_router, button_router, promo_router
from bot.middleware.web_api_middleware import WebApiMiddleware
from bot.utils.http_client import HttpClient

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
web_api_url = env('WEB_API_URL')
http_client = HttpClient(api_url=web_api_url, api_key=bot_token)

# session = AiohttpSession(proxy=config.proxy.URL) if config.proxy.URL else None

bot = Bot(
    bot_token + '/test',
    # session=session,
    default=DefaultBotProperties(parse_mode='HTML'),
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.update.middleware(WebApiMiddleware(client=http_client))
dp.callback_query.middleware(CallbackAnswerMiddleware())

dp.include_routers(
    callback_router,
    button_router,
    promo_router,
    default_router,
)


async def set_bot_commands() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Register the bot"),
            BotCommand(command="/reload", description="Reload keyboards"),
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


@dp.startup()
async def on_startup() -> None:
    await bot.delete_webhook(True)
    await set_bot_commands()


async def main() -> None:
    try:
        # scheduler = AsyncIOScheduler()
        # trigger = CronTrigger(second='1')
        # scheduler.add_job(send_notification, trigger=trigger, args=(bot, http_client))
        # scheduler.start()
        await dp.start_polling(bot, polling_timeout=3)

    except (KeyboardInterrupt, SystemExit):
        print("Bye!")
    finally:
        await dp.storage.close()
        await bot.session.close()
