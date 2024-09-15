from typing import Callable, Awaitable, Dict, Any

from aiogram.types import TelegramObject
from bot.utils.http_client import HttpClient


class WebApiMiddleware:
    def __init__(self, client: HttpClient):
        super().__init__()
        self.client = client

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data["client"] = self.client

        result = await handler(event, data)
        return result

