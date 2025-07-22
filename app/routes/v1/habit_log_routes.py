# routes/habit_log.py
from fastapi import APIRouter, Depends
from typing import List
from app.schemas.habit_log_schema import (
    HabitLogCreate,
    HabitLogResponse,
    HabitLogMultipleCreate,
    HabitLogClear,
)
from app.services.habit_log_service import HabitLogService
from app.repositories import HabitLogRepository
from app.services import HabitLogService
from app.services.interface import IHabitLogService
from app.core.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.common_schema import BaseResponse
from app.schemas.habit_log_schema import HabitLogResponse
from app.core.permissions import any_user_role
from starlette import status


router = APIRouter(prefix="/habit-logs", tags=["Habit Logs"])


def get_habit_log_service(db: AsyncSession = Depends(get_db)) -> IHabitLogService:
    return HabitLogService(db)

@router.post("/", response_model=HabitLogResponse, status_code=status.HTTP_201_CREATED)
async def create_log(
    data: HabitLogCreate,
    user: User = Depends(any_user_role),
    service: IHabitLogService = Depends(get_habit_log_service),
):
    return await service.create_log(user.id, data)

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(
    log_id: int,
    user: User = Depends(any_user_role),
    service: IHabitLogService = Depends(get_habit_log_service),
):
    await service.delete_log(log_id)

@router.post("/bulk", status_code=status.HTTP_201_CREATED)
async def create_multiple_logs(
    data: HabitLogMultipleCreate,
    user: User = Depends(any_user_role),
    service: IHabitLogService = Depends(get_habit_log_service),
):
    await service.add_multiple_logs(data)

@router.post("/clear", status_code=status.HTTP_200_OK)
async def clear_logs(
    data: HabitLogClear,
    user: User = Depends(any_user_role),
    service: IHabitLogService = Depends(get_habit_log_service),
):
    await service.clear_logs(data)
