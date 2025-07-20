import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate


class ReminderRepository:
    def __init__(self, db: AsyncSession, logger: logging.Logger | None = None):
        self.db = db
        self.logger = logger or logging.getLogger(__name__)
    
    async def create(self, user_id: int, data: ReminderCreate) -> Reminder:
        reminder = Reminder(**data.model_dump(), user_id=user_id)
        self.db.add(reminder)
        await self.db.flush()
        self.logger.info(f"Created reminder {reminder.id} for user {user_id}")
        return reminder

    async def get_by_id(self, reminder_id: int) -> Reminder | None:
        result = await self.db.execute(select(Reminder).where(Reminder.id == reminder_id))
        reminder = result.scalar_one_or_none()
        if reminder:
            self.logger.debug(f"Fetched reminder ID: {reminder_id}")
        else:
            self.logger.warning(f"Reminder not found: ID {reminder_id}")
        return reminder

    async def get_all_by_user(self, user_id: int) -> list[Reminder]:
        result = await self.db.execute(select(Reminder).where(Reminder.user_id == user_id))
        reminders = result.scalars().all()
        self.logger.debug(f"Fetched {len(reminders)} reminders for user {user_id}")
        return reminders

    async def update_remainder(self, reminder: Reminder, data: ReminderUpdate) -> Reminder:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(reminder, key, value)
        await self.db.flush()
        self.logger.info(f"Updated reminder {reminder.id}")
        return reminder

    async def delete_remainder(self, reminder: Reminder):
        await self.db.delete(reminder)
        await self.db.flush()
        self.logger.info(f"Deleted reminder {reminder.id}")
