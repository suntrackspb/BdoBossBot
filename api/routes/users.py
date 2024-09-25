from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import get_user_service
from api.services.users import UserService
from api.utils.check_signature import check_webapp_signature, verify_webapp_signature
from common.schemas.op_status import OpStatusSchema
from common.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema

router = APIRouter()


@router.get(
    path="/users",
    response_model=List[UserCreateSchema],
    summary="Get all users",
    response_description="List of all users",
)
async def get_users(
        user_id: Annotated[int, Depends(verify_webapp_signature)],
        service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Get a list of all registered users.

    Returns:
        List[UserCreateSchema]: List of all users.
    """
    print(user_id)
    return await service.get_all_users()


@router.get(
    path="/users/{user_id}",
    response_model=UserSchema,
    summary="Get a specific user by ID",
    response_description="Specific user",
    responses={404: {"description": "Not found"}},
)
async def get_user_info(
        user_id: int,
        # _: Annotated[None, Depends(verify_api_key)],
        service: Annotated[UserService, Depends(get_user_service)],

):
    user = await service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete(
    path="/users/{user_id}",
    response_model=OpStatusSchema,
    summary="Delete a specific user by ID",
    response_description="Specific user",
)
async def delete_user(
        user_id: int,
        _: Annotated[None, Depends(verify_webapp_signature)],
        service: Annotated[UserService, Depends(get_user_service)]
):
    return await service.del_user(user_id=user_id)


@router.post(
    path="/users",
    response_model=UserSchema,
    summary="Add a new user",
    response_description="New user",
)
async def create_user(
        payload: UserCreateSchema,
        _: Annotated[None, Depends(verify_webapp_signature)],
        service: Annotated[UserService, Depends(get_user_service)]
):
    print(payload)
    return await service.add_user(user=payload)


@router.patch(
    path="/users/{user_id}",
    response_model=UserSchema,
    summary="Update a specific user by ID",
    response_description="New user",
)
async def update_user(
        user_id: int,
        payload: UserUpdateSchema,
        service: Annotated[UserService, Depends(get_user_service)]
):
    await check_webapp_signature(payload.init_data)
    user = await service.get_user(user_id=user_id)
    return await service.update_user(user=user, user_update=payload.payload)
