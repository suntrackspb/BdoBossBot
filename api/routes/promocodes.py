from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import get_promo_code_service
from api.schemas.promocodes import PromoCodeSchema
from api.services import PromoCodeService
from api.utils.check_signature import verify_api_key

router = APIRouter()


@router.get(
    path="/promo",
    response_model=List[PromoCodeSchema],
    summary="Get actual promo codes",
    response_description="Actual promo codes",
)
async def get_active_promo_codes(
        service: Annotated[PromoCodeService, Depends(get_promo_code_service)]
):
    return await service.get_actual_promo_code()


@router.get(
    path="/promo/{code}",
    response_model=PromoCodeSchema | None,
    summary="Check promo code existence",
    response_description="Promo code",
)
async def get_specific_promo_codes(
        code: str,
        service: Annotated[PromoCodeService, Depends(get_promo_code_service)]
):
    exists = await service.check_promo_code(promo_code=code)
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found")
    return exists


@router.post(
    path="/promo",
    response_model=PromoCodeSchema,
    summary="Add new promo code",
    response_description="New promo code",
)
async def add_promo_code(
        payload: PromoCodeSchema,
        _: Annotated[None, Depends(verify_api_key)],
        service: Annotated[PromoCodeService, Depends(get_promo_code_service)]
):
    promo = await service.check_promo_code(promo_code=payload.code)
    print(promo)
    if promo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Code already exists")
    return await service.add_promo_code(promo_code=payload)
