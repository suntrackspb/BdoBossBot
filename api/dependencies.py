from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import UserCrud, BossCrud, NotificationCrud, PromoCodesCrud
from api.database.connect import get_db
from api.services import UserService, BossService, NotificationService, PromoCodeService


async def get_user_crud(db: Annotated[AsyncSession, Depends(get_db)]):
    return UserCrud(db)


async def get_user_service(
        crud: Annotated[UserCrud, Depends(get_user_crud)],
):
    return UserService(crud)


async def get_boss_crud(db: Annotated[AsyncSession, Depends(get_db)]):
    return BossCrud(db)


async def get_boss_service(
        crud: Annotated[BossCrud, Depends(get_boss_crud)],
):
    return BossService(crud)


async def get_notify_crud(db: Annotated[AsyncSession, Depends(get_db)]):
    return NotificationCrud(db)


async def get_notify_service(
        crud: Annotated[NotificationCrud, Depends(get_notify_crud)],
):
    return NotificationService(crud)

async def get_promo_code_crud(db: Annotated[AsyncSession, Depends(get_db)]):
    return PromoCodesCrud(db)


async def get_promo_code_service(
        crud: Annotated[PromoCodesCrud, Depends(get_promo_code_crud)],
):
    return PromoCodeService(crud)

