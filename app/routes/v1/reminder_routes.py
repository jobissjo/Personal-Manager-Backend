from typing import List
from fastapi import  status
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate
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
        if repository is None:
            raise ValueError("Repository cannot be None")
        self.repository = repository
        self.logger = logger or default_logger

    async def create_reminder(self, user_id: int, data: ReminderCreate) -> Reminder:
        """Create a new reminder."""
        try:
            self.logger.info(f"Creating reminder for user_id={user_id}")
            return await self.repository.create(user_id, data)
        except Exception as e:
            self.logger.error(f"Error creating reminder: {str(e)}")
            raise CustomException(
                "Failed to create reminder",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_reminder_by_id(self, reminder_id: int) -> Reminder:
        """Get a reminder by its ID."""
        try:
            reminder = await self.repository.get_by_id(reminder_id)
            if not reminder:
                self.logger.warning(f"Reminder not found: id={reminder_id}")
                raise CustomException(
                    "Reminder not found",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            return reminder
        except CustomException:
            raise
        except Exception as e:
            self.logger.error(f"Error fetching reminder: {str(e)}")
            raise CustomException(
                "Failed to fetch reminder",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_user_reminders(self, user_id: int) -> List[Reminder]:
        """Get all reminders for a user."""
        try:
            self.logger.info(f"Fetching all reminders for user_id={user_id}")
            return await self.repository.get_all_by_user(user_id)
        except Exception as e:
            self.logger.error(f"Error fetching user reminders: {str(e)}")
            raise CustomException(
                "Failed to fetch reminders",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_reminder(self, reminder_id: int, data: ReminderUpdate) -> Reminder:
        """Update a reminder."""
        try:
            reminder = await self.get_reminder_by_id(reminder_id)
            self.logger.info(f"Updating reminder id={reminder_id}")
            return await self.repository.update_remainder(reminder, data)
        except CustomException:
            raise
        except Exception as e:
            self.logger.error(f"Error updating reminder: {str(e)}")
            raise CustomException(
                "Failed to update reminder",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_reminder(self, reminder_id: int) -> None:
        """Delete a reminder."""
        try:
            reminder = await self.get_reminder_by_id(reminder_id)
            self.logger.info(f"Deleting reminder id={reminder_id}")
            await self.repository.delete_remainder(reminder)
        except CustomException:
            raise
        except Exception as e:
            self.logger.error(f"Error deleting reminder: {str(e)}")
            raise CustomException(
                "Failed to delete reminder",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )