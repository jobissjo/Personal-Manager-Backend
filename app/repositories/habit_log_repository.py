# repositories/habit_log.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from datetime import date
from app.models import HabitLog
from app.repositories.interface import IHabitLogRepository

class HabitLogRepository(IHabitLogRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, log: HabitLog) -> HabitLog:
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log

    async def delete_by_id(self, log_id: int) -> None:
        await self.db.execute(delete(HabitLog).where(HabitLog.id == log_id))
        await self.db.commit()


    async def clear_by_date(self, habit_id: int, log_date: date) -> None:
        await self.db.execute(
            delete(HabitLog)
            .where(HabitLog.habit_id == habit_id, HabitLog.completed_date == log_date)
        )
        await self.db.commit()
