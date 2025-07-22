# services/habit_log.py
from app.schemas.habit_log_schema import HabitLogCreate, HabitLogMultipleCreate, HabitLogClear
from app.repositories.interface import IHabitLogRepository
from app.models import HabitLog
from app.services.interface import IHabitLogService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger_config import logger as default_logger
from app.repositories import HabitLogRepository

class HabitLogService(IHabitLogService):
    def __init__(self, db: AsyncSession, repository: HabitLogRepository = None, logger=None):
        self.db = db
        self.logger = logger or default_logger
        self.repository = repository or HabitLogRepository(db, self.logger)

    async def create_log(self, user_id: int, data: HabitLogCreate):
        self.logger.info(f"Creating log for user_id={user_id}")
        return await self.repository.create(data.habit_id, data.completed_date)

    async def delete_log(self, log_id: int):
        self.logger.info(f"Deleting habit log id={log_id}")
        return await self.repository.delete_by_id(log_id)

    async def add_multiple_logs(self, data: HabitLogMultipleCreate):
        self.logger.info("Creating multiple habit logs")
        return await self.repository.add_multiple(data.habit_ids, data.completed_date)

    async def clear_logs(self, data: HabitLogClear):
        self.logger.info("Clearing habit logs")
        return await self.repository.clear_logs_by_date(data.habit_ids, data.completed_date)