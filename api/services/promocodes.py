from api.crud import PromoCodesCrud
from api.models import PromoCode
from common.config import config as cfg
from common.schemas.promocodes import PromoCodeSchema


class PromoCodeService:
    def __init__(self, crud: PromoCodesCrud):
        self.crud = crud
        self.cfg = cfg

    async def add_promo_code(self, promo_code: PromoCodeSchema):
        return await self.crud.add_promo_code(promo_code=PromoCode(**promo_code.model_dump()))

    async def get_actual_promo_code(self):
        return await self.crud.get_promo_codes()

    async def check_promo_code(self, promo_code: str):
        return await self.crud.check_promo_code_exist(promo_code=promo_code)
