import json
from typing import Optional, Dict, Any

import aiohttp

from api.schemas.boss import BossSchema
from api.schemas.op_status import OpStatusSchema
from api.schemas.promocodes import PromoCodeSchema
from api.schemas.user import UserSchema, UserCreateSchema


class HttpClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    async def request(self, path: str, method: str = 'GET', params: Optional[Dict] = None) -> Optional[Any]:
        if params is None:
            params = {}

        url = f'{self.api_url}{path}'
        headers = {'x-api-key': self.api_key}

        async with aiohttp.ClientSession() as session:
            try:
                if method == 'GET':
                    async with session.get(url, headers=headers) as response:
                        return await self._handle_response(response)
                elif method == 'POST':
                    async with session.post(url, headers=headers, json=params) as response:
                        return await self._handle_response(response)
                elif method == 'PATCH':
                    async with session.patch(url, headers=headers, json=params) as response:
                        return await self._handle_response(response)
            except aiohttp.ClientError as e:
                print(f"An error occurred: {e}")
                return None

    @staticmethod
    async def _handle_response(response: aiohttp.ClientResponse):
        return OpStatusSchema(
            status_code=response.status,
            message=response.reason,
            data=await response.json()
        )

    async def get_notify_list(self):
        data = await self.request('/api/notify')
        return data

    async def get_user(self, user_id: int) -> OpStatusSchema:
        data = await self.request(f'/api/users/{user_id}')
        return data

    async def add_user(self, user: UserCreateSchema) -> OpStatusSchema:
        print(user.model_dump())
        data = await self.request('/api/users', method='POST', params=user.model_dump())
        return data

    async def get_today_bosses(self) -> OpStatusSchema:
        data = await self.request('/api/bosses/today')
        return data

    async def get_next_boss(self):
        data = await self.request('/api/bosses/next')
        return data

    async def update_user(self, user: UserSchema, params: dict) -> OpStatusSchema:
        data = await self.request(f'/api/users/{user.chat_id}', method='PATCH', params=params)
        return data

    async def get_promos(self):
        data = await self.request('/api/promo')
        return data

    async def add_promo(self, promo: PromoCodeSchema):
        data = await self.request('/api/promo', method='POST', params=promo.model_dump())
        return data

    async def check_promo(self, code: str):
        data = await self.request(f'/api/promo/{code}')
        return data
