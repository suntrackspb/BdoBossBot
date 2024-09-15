import json
from typing import Annotated, List

from fastapi import APIRouter, Depends

from api.dependencies import get_boss_service
from api.models.models import Boss
from api.schemas.boss import BossSchema
from api.services.bosses import BossService
from api.utils.check_signature import verify_api_key

router = APIRouter()


@router.get(
    "/bosses/",
    response_model=List[BossSchema],
)
async def get_bosses_list(
        service: Annotated[BossService, Depends(get_boss_service)]
) -> list[Boss]:
    return await service.get_bosses_list()


@router.get(
    path="/bosses/next",
    response_model=BossSchema,
)
async def get_next_boss(
        service: Annotated[BossService, Depends(get_boss_service)]
):
    return await service.get_next_boss()


@router.get(
    path="/bosses/today",
    response_model=List[BossSchema],
)
async def get_today_boss(
        service: Annotated[BossService, Depends(get_boss_service)]
):
    return await service.get_today_bosses()


@router.get(
    path="/load_data",
    response_model=dict,
)
async def read_root(
        _: Annotated[None, Depends(verify_api_key)],
        service: Annotated[BossService, Depends(get_boss_service)]
) -> dict:
    with open('parts/bdo_bosses_2024_full.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for boss in data:
        await service.add_boss(Boss(
            boss_day=boss['boss_day'],
            boss_time=boss['boss_time'],
            boss_names=", ".join(boss['boss_names']),
            boss_slot=boss['boss_slot']
        ))
    return {"message": "Boss data loaded"}
