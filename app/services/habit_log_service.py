# services/habit_log.py
from app.schemas.habit_log_schema import HabitLogCreate, HabitLogMultipleCreate, HabitLogClear
from app.repositories.interface import IHabitLogRepository
from app.models import HabitLog

class HabitLogService:
    def __init__(self, repo: IHabitLogRepository):
        self.repo = repo

    async def add_log(self, data: HabitLogCreate):
        log = HabitLog(**data.dict())
        return await self.repo.add(log)

    async def delete_log(self, log_id: int):
        await self.repo.delete_by_id(log_id)

    async def add_multiple_logs(self, data: HabitLogMultipleCreate):
        logs = [HabitLog(habit_id=id_, completed_date=data.completed_date) for id_ in data.habit_ids]
        await self.repo.add_many(logs)

    async def clear_logs_by_date(self, data: HabitLogClear, habit_ids: list[int]):
        await self.repo.clear_by_date(habit_ids, data.completed_date)
