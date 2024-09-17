from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import get_user_service
from api.schemas.op_status import Status
from api.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema
from api.services.users import UserService
from api.utils.check_signature import verify_api_key

router = APIRouter()


@router.get(
    path="/users",
    response_model=List[UserCreateSchema],
    summary="Get all users",
    response_description="List of all users",
)
async def get_users(
        _: Annotated[None, Depends(verify_api_key)],
        service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Retrieve a list of all users.

    This asynchronous function retrieves a list of all users from the database using the provided `UserService`. It requires an API key for authentication and access to the user service. The function performs the following steps:

    1. Verifies the API key using the `verify_api_key` dependency to ensure the request is authenticated.
    2. Retrieves a list of all users from the database via the `UserService`.
    3. Returns the list of all users in the response with status code 200 OK.

    - **None**: No input parameters are required for this function.
    - _: Annotated[None, Depends(verify_api_key)]: A dependency to verify the API key used for authentication.
    - service: Annotated[UserService, Depends(get_user_service)]: A dependency that provides access to the UserService instance required to interact with user data.

    Returns:
        - List[UserCreateSchema]: A list of all users in the database as defined by the `UserCreateSchema` model.
    - **HTTP 200**: On successful retrieval, returns a list of all users.
    """
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
        _: Annotated[None, Depends(verify_api_key)],
        service: Annotated[UserService, Depends(get_user_service)],

):
    user = await service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete(
    path="/users/{user_id}",
    response_model=Status,
    summary="Delete a specific user by ID",
    response_description="Specific user",
)
async def delete_user(
        user_id: int,
        _: Annotated[None, Depends(verify_api_key)],
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
        _: Annotated[None, Depends(verify_api_key)],
        service: Annotated[UserService, Depends(get_user_service)]
):
    print(payload)
    return await service.add_user(user=payload)


@router.patch(
    path="/users/{user_id}",
    response_model=UserSchema,
    summary="Add a new user",
    response_description="New user",
)
async def update_user(
        user_id: int,
        payload: UserUpdateSchema,
        # _: Annotated[None, Depends(verify_api_key)],
        service: Annotated[UserService, Depends(get_user_service)]
):
    user = await service.get_user(user_id=user_id)
    return await service.update_user(user=user, user_update=payload)
