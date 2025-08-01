from fastapi import APIRouter, Depends, status
from app.core.db_config import get_db
from app.core.permissions import any_user_role
from app.models.user import User
from app.repositories.reminder_repository import ReminderRepository
from app.schemas.common_schema import BaseResponse
from app.schemas.reminder import (
    ReminderCreate,
    ReminderUpdate,
    ReminderOut,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.reminder_service import ReminderService
from typing import List

router = APIRouter(
    prefix="/reminder",
    tags=["Reminder"]
)
def get_reminder_service(db: AsyncSession = Depends(get_db)) -> ReminderService:
    return ReminderService(repository=ReminderRepository(db))    

@router.post("/", response_model=ReminderOut, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    data: ReminderCreate,
    user: User = Depends(any_user_role),
    reminder_service: ReminderService = Depends(get_reminder_service)
) -> BaseResponse[ReminderOut]:
    reminder = await reminder_service.create_reminder(user.id, data)
    return BaseResponse(message="Reminder created successfully", data=reminder)


@router.get("/{reminder_id}", response_model=ReminderOut)
async def get_reminder(
    reminder_id: int,
    reminder_service: ReminderService = Depends(get_reminder_service)
) -> BaseResponse[ReminderOut]:
    reminder = await reminder_service.get_reminder_by_id(reminder_id)
    return BaseResponse(message="Reminder fetched successfully", data=reminder)

@router.get("/", response_model=BaseResponse[List[ReminderOut]])
async def get_user_reminders(
    user: User = Depends(any_user_role),    
    reminder_service: ReminderService = Depends(get_reminder_service)
) -> BaseResponse[List[ReminderOut]]:
    reminders = await reminder_service.get_user_reminders(user.id)
    return BaseResponse(message="Reminders fetched successfully", data=reminders)


@router.patch("/{reminder_id}", response_model=ReminderOut)
async def update_reminder(
    reminder_id: int,
    data: ReminderUpdate,
    reminder_service: ReminderService = Depends(get_reminder_service)
) -> BaseResponse[ReminderOut]:
    updated_reminder = await reminder_service.update_reminder(reminder_id, data)
    return BaseResponse(message="Reminder updated successfully", data=updated_reminder)


@router.delete("/{reminder_id}", status_code=status.HTTP_200_OK)
async def delete_reminder(
    reminder_id: int,
    reminder_service: ReminderService = Depends(get_reminder_service)
) -> BaseResponse[None]:
    await reminder_service.delete_reminder(reminder_id)
    return BaseResponse(message="Reminder deleted successfully", data=None)


