from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_config import get_db
from app.core.permissions import any_user_role
from app.models import User
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderOut
from app.services.interface import IReminderService
from app.services.reminder_service import ReminderService

router = APIRouter(prefix="/reminders", tags=["Reminders"])

# Dependency injector
def get_reminder_service(db: AsyncSession = Depends(get_db)) -> IReminderService:
    return ReminderService(db)

@router.post("/", response_model=ReminderOut, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    data: ReminderCreate,
    user: User = Depends(any_user_role),
    service: IReminderService = Depends(get_reminder_service),
):
    return await service.create_reminder(user.id, data)

@router.get("/", response_model=list[ReminderOut])
async def get_all_reminders(
    user: User = Depends(any_user_role),
    service: IReminderService = Depends(get_reminder_service),
):
    return await service.get_user_reminders(user.id)

@router.get("/{reminder_id}", response_model=ReminderOut)
async def get_reminder_by_id(
    reminder_id: int,
    user: User = Depends(any_user_role),
    service: IReminderService = Depends(get_reminder_service),
):
    return await service.get_reminder_by_id(reminder_id)

@router.put("/{reminder_id}", response_model=ReminderOut)
async def update_reminder(
    reminder_id: int,
    data: ReminderUpdate,
    user: User = Depends(any_user_role),
    service: IReminderService = Depends(get_reminder_service),
):
    return await service.update_reminder(reminder_id, data)

@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder(
    reminder_id: int,
    user: User = Depends(any_user_role),
    service: IReminderService = Depends(get_reminder_service),
):
    await service.delete_reminder(reminder_id)
