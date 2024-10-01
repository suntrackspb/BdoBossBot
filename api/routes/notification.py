from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import get_notify_service, get_boss_service, get_user_service
from api.services.bosses import BossService
from api.services.notification import NotificationService
from api.services.users import UserService
from api.utils.check_signature import verify_webapp_signature
from common.schemas.notification import BossNotificationSchema, NotificationAddSchema, NotificationAddAllSchema
from common.schemas.op_status import OpStatusSchema
from common.schemas.user import SpecificUserSchema

router = APIRouter()


@router.post(
    path="/notify",
    response_model=OpStatusSchema,
    summary="Add notifications from Web App",
    response_description="Status operation",
)
async def add_notification(
        payload: NotificationAddSchema,
        user_id: Annotated[int, Depends(verify_webapp_signature)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        notify_service: Annotated[NotificationService, Depends(get_notify_service)],
):
    user = await user_service.get_user(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await notify_service.add_notifications(user, payload.boss_id, payload.is_selected)


@router.post(
    path="/notify/all",
    response_model=OpStatusSchema,
    summary="Add notifications from Web App",
    response_description="Status operation",
)
async def add_notification(
        payload: NotificationAddAllSchema,
        user_id: Annotated[int, Depends(verify_webapp_signature)],
        boss_service: Annotated[BossService, Depends(get_boss_service)],
        notify_service: Annotated[NotificationService, Depends(get_notify_service)],
):
    bosses = await boss_service.get_bosses_list()
    return await notify_service.generate_notification(
        user_id=user_id, bosses=bosses, is_selected=payload.is_selected
    )


@router.get(
    path="/notify/{user_id}",
    response_model=SpecificUserSchema,
    summary="Get notification settings a specific user by ID",
    response_description="Notification settings",
)
async def get_user_info(
        user_id: int,
        _: Annotated[int, Depends(verify_webapp_signature)],
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
        _: Annotated[int, Depends(verify_webapp_signature)],
        boss_service: Annotated[BossService, Depends(get_boss_service)],
        notify_service: Annotated[NotificationService, Depends(get_notify_service)]
):
    next_boss = await boss_service.get_next_boss()
    notify = await notify_service.get_notify_users_by_boss(boss=next_boss)
    return notify
