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


def get_habit_log_service(db=Depends(get_db)) -> IHabitLogService:
    repo = HabitLogRepository(db)
    return HabitLogService(repo)


router = APIRouter(prefix="/habit-logs", tags=["Habit Logs"])


@router.post("/", response_model=HabitLogResponse)
async def add_log(
    data: HabitLogCreate, service: IHabitLogService = Depends(get_habit_log_service)
):
    return await service.add_log(data)


@router.delete("/{log_id}")
async def delete_log(
    log_id: int, service: IHabitLogService = Depends(get_habit_log_service)
):
    await service.delete_log(log_id)
    return {"message": "Deleted"}


@router.post("/bulk")
async def add_multiple_logs(
    data: HabitLogMultipleCreate,
    service: IHabitLogService = Depends(get_habit_log_service),
):
    await service.add_multiple_logs(data)
    return {"message": "Multiple logs added"}


@router.post("/clear")
async def clear_logs(
    data: HabitLogClear,
    habit_ids: List[int],
    service: IHabitLogService = Depends(get_habit_log_service),
):
    await service.clear_logs_by_date(data, habit_ids)
    return {"message": "Logs cleared"}
