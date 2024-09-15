from datetime import datetime
from typing import List, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import PromoCode


class PromoCodesCrud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_promo_code(self, promo_code: PromoCode) -> PromoCode:
        self.db.add(promo_code)
        await self.db.commit()
        await self.db.refresh(promo_code)
        return promo_code

    async def get_promo_codes(self) -> Sequence[PromoCode]:
        result = await self.db.execute(
            select(PromoCode).where(PromoCode.expiry >= datetime.now)
        )
        return result.scalars().all()

    async def check_promo_code_exist(self, promo_code: PromoCode) -> bool:
        result = await self.db.execute(
            select(PromoCode).where(PromoCode.code >= promo_code.code)
        )
        if result:
            return True
        return False
