from typing import List
from fastapi import HTTPException, status
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderOut
from app.repositories import ReminderRepository
from app.core.logger_config import logger as default_logger
from app.services.interface import IReminderService
from app.utils.common import CustomException


class ReminderService(IReminderService):
    """Service for managing reminders."""
    
    def __init__(self, repository: ReminderRepository, logger=None):
        """Initialize the reminder service.
        
        Args:
            repository: Repository for reminder operations
            logger: Optional logger instance
        """
        self.repository = repository
        self.logger = logger or default_logger

    async def create_reminder(self, user_id: int, data: ReminderCreate) -> Reminder:
        """Create a new reminder.
        
        Args:
            user_id: ID of the user creating the reminder
            data: Reminder creation data
            
        Returns:
            Created reminder instance
            
        Raises:
            CustomException: If creation fails
        """
        try:
            self.logger.info(f"Creating reminder for user_id={user_id}")
            return await self.repository.create(user_id, data)
        except Exception as e:
            self.logger.error(f"Error creating reminder: {str(e)}")
            raise CustomException(
                "Failed to create reminder",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_reminder_by_id(self, reminder_id: int)-> ReminderOut:
        reminder = await self.repository.get_by_id(reminder_id)
        if not reminder:
            self.logger.warning(f"Reminder not found: id={reminder_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found"
            )
        return reminder

    async def get_user_reminders(self, user_id: int)-> List[ReminderOut]:
        self.logger.info(f"Fetching all reminders for user_id={user_id}")
        return await self.repository.get_all_by_user(user_id)

    async def update_reminder(self, reminder_id: int, data: ReminderUpdate)-> ReminderOut:
        reminder = await self.get_reminder_by_id(reminder_id)
        self.logger.info(f"Updating reminder id={reminder_id}")
        return await self.repository.update_remainder(reminder, data)

    async def delete_reminder(self, reminder_id: int)-> None:
        reminder = await self.get_reminder_by_id(reminder_id)
        self.logger.info(f"Deleting reminder id={reminder_id}")
        await self.repository.delete_remainder(reminder)
