from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import get_notify_service, get_boss_service, get_user_service
from api.schemas.notification import BossNotificationSchema
from api.schemas.op_status import OpStatusSchema
from api.schemas.telegram import NotificationAllSchema, NotificationAddSchema
from api.schemas.user import SpecificUserSchema
from api.services.bosses import BossService
from api.services.notification import NotificationService
from api.services.users import UserService
from api.utils.check_signature import check_webapp_signature

router = APIRouter()


@router.post(
    path="/notify",
    response_model=OpStatusSchema,
    summary="Add notifications from Web App",
    response_description="Status operation",
)
async def add_notification(
        init_data: NotificationAddSchema,
        user_service: Annotated[UserService, Depends(get_user_service)],
        notify_service: Annotated[NotificationService, Depends(get_notify_service)],
):
    await check_webapp_signature(init_data.init_data)
    user = await user_service.get_user(user_id=init_data.init_data.user.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await notify_service.add_notifications(user, init_data.boss_id, init_data.is_selected)


@router.post(
    path="/notify/all",
    response_model=OpStatusSchema,
    summary="Add notifications from Web App",
    response_description="Status operation",
)
async def add_notification(
        init_data: NotificationAllSchema,
        boss_service: Annotated[BossService, Depends(get_boss_service)],
        notify_service: Annotated[NotificationService, Depends(get_notify_service)],
):
    await check_webapp_signature(init_data.init_data)
    bosses = await boss_service.get_bosses_list()
    return await notify_service.generate_notification(user_id=init_data.init_data.user.id, bosses=bosses)


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
        # _: Annotated[None, Depends(verify_api_key)],
        boss_service: Annotated[BossService, Depends(get_boss_service)],
        notify_service: Annotated[NotificationService, Depends(get_notify_service)]
):
    next_boss = await boss_service.get_next_boss()
    notify = await notify_service.get_notify_users_by_boss(boss=next_boss)
    return notify
