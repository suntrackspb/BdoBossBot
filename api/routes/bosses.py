import json
from typing import Annotated, List

from fastapi import APIRouter, Depends

from api.dependencies import get_boss_service
from api.models.models import Boss
from api.services.bosses import BossService
from common.schemas.boss import BossSchema

router = APIRouter()


@router.get(
    "/bosses/",
    response_model=List[BossSchema],
    summary="Get list of all bosses",
)
async def get_bosses_list(
        service: Annotated[BossService, Depends(get_boss_service)]
) -> list[Boss]:
    return await service.get_bosses_list()


@router.get(
    path="/bosses/next",
    response_model=BossSchema,
    summary="Get next boss",
)
async def get_next_boss(
        service: Annotated[BossService, Depends(get_boss_service)]
):
    return await service.get_next_boss()


@router.get(
    path="/bosses/today",
    response_model=List[BossSchema],
    summary="Get today bosses",
)
async def get_today_boss(
        service: Annotated[BossService, Depends(get_boss_service)]
):
    return await service.get_today_bosses()


# @router.get(
#     path="/load_data",
#     response_model=dict,
# )
# async def read_root(
#         _: Annotated[None, Depends(verify_webapp_signature)],
#         service: Annotated[BossService, Depends(get_boss_service)]
# ) -> dict:
#     with open('parts/bdo_bosses_2024_full.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#
#     for boss in data:
#         await service.add_boss(Boss(
#             boss_day=boss['boss_day'],
#             boss_time=boss['boss_time'],
#             boss_names=", ".join(boss['boss_names']),
#             boss_slot=boss['boss_slot']
#         ))
#     return {"message": "Boss data loaded"}
