from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_config import get_db
from app.core.permissions import any_user_role
from app.models.user import User
from app.services.interface import INotificationService
from app.services.notification_service import NotificationService
from app.schemas.common_schema import BaseResponse
from app.schemas.notification_schema import  NotificationRead

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_notification_service(db: AsyncSession = Depends(get_db)) -> INotificationService:
    return NotificationService(db)


@router.get("/", response_model=BaseResponse[list[NotificationRead]])
async def get_all_notifications(
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
    user: Annotated[User, Depends(any_user_role)],
):
    notifications = await notification_service.get_all_notifications(user.id)
    return BaseResponse(
        message="Notifications fetched successfully", data=notifications
    )


@router.get("/unread", response_model=BaseResponse[list[NotificationRead]])
async def get_unread_notifications(
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
    user: Annotated[User, Depends(any_user_role)],
):
    notifications = await notification_service.get_unread_notifications(user.id)
    return BaseResponse(
        message="Unread notifications fetched successfully", data=notifications
    )


@router.post("/", response_model=BaseResponse[NotificationRead])
async def read_notification(
    notification_id: int,
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
    user: Annotated[User, Depends(any_user_role)],
):
    notification = await notification_service.mark_as_read(notification_id)
    return BaseResponse(message="Notification marked as read", data=notification)


@router.delete("/", response_model=BaseResponse[None])
async def clear_notifications(
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
    user: Annotated[User, Depends(any_user_role)],
):
    await notification_service.clear_all(user.id)
    return BaseResponse(message="Notifications cleared", data=None)

