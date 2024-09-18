from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import get_notify_service, get_boss_service, get_user_service
from api.schemas.notification import NotificationSchema, AddNotification, BossNotificationSchema
from api.schemas.op_status import Status
from api.schemas.user import SpecificUserSchema
from api.services.bosses import BossService
from api.services.notification import NotificationService
from api.services.users import UserService
from api.utils.check_signature import verify_api_key

router = APIRouter()


@router.post(
    path="/notify/all_bosses",
    response_model=Status,
    summary="Generate notifications for all bosses",
    response_description="Status operation",
)
async def gen_all(
        user_id: int,
_: Annotated[None, Depends(verify_api_key)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        boss_service: Annotated[BossService, Depends(get_boss_service)],
        notify_service: Annotated[NotificationService, Depends(get_notify_service)]
):
    """
    Generate notifications for all bosses.

    This asynchronous function handles the generation of notifications for a user's list of bosses. It requires several dependencies including services for users, bosses, and notifications. The function performs the following steps:

    1. Retrieves the user information using the `user_service` based on the provided `user_id`.
    2. If the user is not found, returns a 404 Not Found HTTP exception with an appropriate message.
    3. Retrieves the list of bosses using the `boss_service`.
    4. Calls the `notify_service.generate_notification` method to create notifications for each boss in the list and returns the result.

    ### Parameters:
    - **user_id**: An integer representing the ID of the user for whom notifications are being generated.
    - **user_service**: A dependency injected UserService instance used to retrieve user information.
    - **boss_service**: A dependency injected BossService instance used to retrieve boss information.
    - **notify_service**: A dependency injected NotificationService instance used to generate notifications.

    ### Returns:
    - On success, returns the result of `notify_service.generate_notification` which includes status and details about the operation. If the user is not found, raises an HTTPException with a 404 status code.

    ### Raises:
    - **HTTPException**: Raised if the specified user is not found, returning a 404 Not Found response with "User not found" as the detail message.
    """
    user = await user_service.get_user(user_id)
    if user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    bosses = await boss_service.get_bosses_list()
    return await notify_service.generate_notification(user=user, bosses=bosses)


@router.post(
    path="/notify",
    response_model=Status,
    summary="Add notifications from Web App",
    response_description="Status operation",
)
async def add_notification(
        payload: AddNotification,
_: Annotated[None, Depends(verify_api_key)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        notify_service: Annotated[NotificationService, Depends(get_notify_service)],
):
    user = await user_service.get_user(user_id=payload.chat_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await notify_service.add_notifications(user.chat_id, payload.boss_list)


@router.get(
    path="/notify/{user_id}",
    response_model=SpecificUserSchema,
    summary="Get notification settings a specific user by ID",
    response_description="Notification settings",
)
async def get_user_info(
        user_id: int,
        service: Annotated[UserService, Depends(get_user_service)]
):
    return await service.get_specific_user(user_id=user_id)


@router.get(
    path="/notify",
    response_model=BossNotificationSchema | None,
    summary="Get list of users to notify about the next boss",
    response_description="List of users to notify about the next boss",
)
async def get_notify_list(
_: Annotated[None, Depends(verify_api_key)],
        boss_service: Annotated[BossService, Depends(get_boss_service)],
        notify_service: Annotated[NotificationService, Depends(get_notify_service)]
):
    next_boss = await boss_service.get_next_boss()
    notify = await notify_service.get_notify_users_by_boss(boss=next_boss)
    return notify
