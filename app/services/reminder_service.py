from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from app.repositories import ReminderRepository
from app.core.logger_config import logger as default_logger


class ReminderService:
    def __init__(self, db: AsyncSession, repository: ReminderRepository = None, logger=None):
        self.db = db
        self.logger = logger or default_logger
        self.repository = repository or ReminderRepository(db, self.logger)

    async def create_reminder(self, user_id: int, data: ReminderCreate):
        self.logger.info(f"Creating reminder for user_id={user_id}")
        return await self.repository.create(user_id, data)

    async def get_reminder_by_id(self, reminder_id: int):
        reminder = await self.repository.get_by_id(reminder_id)
        if not reminder:
            self.logger.warning(f"Reminder not found: id={reminder_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found"
            )
        return reminder

    async def get_user_reminders(self, user_id: int):
        self.logger.info(f"Fetching all reminders for user_id={user_id}")
        return await self.repository.get_all_by_user(user_id)

    async def update_reminder(self, reminder_id: int, data: ReminderUpdate):
        reminder = await self.get_reminder_by_id(reminder_id)
        self.logger.info(f"Updating reminder id={reminder_id}")
        return await self.repository.update_reminder(reminder, data)

    async def delete_reminder(self, reminder_id: int):
        reminder = await self.get_reminder_by_id(reminder_id)
        self.logger.info(f"Deleting reminder id={reminder_id}")
        await self.repository.delete_reminder(reminder)
