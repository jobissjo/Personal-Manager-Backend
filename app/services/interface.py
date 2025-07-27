from typing import Protocol, List
from datetime import date
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from app.schemas.habit_log_schema import HabitLogCreate, HabitLogMultipleCreate, HabitLogClear
from app.schemas.notification_schema import NotificationCreate, NotificationRead
from abc import ABC, abstractmethod


class IReminderService(Protocol):
    async def create_reminder(self, user_id: int, data: ReminderCreate) -> Reminder: ...
    async def get_user_reminders(self, user_id: int) -> list[Reminder]: ...
    async def get_reminder_by_id(self, reminder_id: int) -> Reminder: ...
    async def update_reminder(self, reminder_id: int, data: ReminderUpdate) -> Reminder: ...
    async def delete_reminder(self, reminder_id: int) -> None: ...








class IHabitLogService(ABC):
    @abstractmethod
    async def create_log(self, user_id: int, data: HabitLogCreate): ...
    
    @abstractmethod
    async def delete_log(self, log_id: int): ...
    
    @abstractmethod
    async def add_multiple_logs(self, data: HabitLogMultipleCreate): ...
    
    @abstractmethod
    async def clear_logs(self, data: HabitLogClear): ...



class INotificationService(ABC):

    @abstractmethod
    def create_notification(self, user_id: int, data: NotificationCreate) -> NotificationRead:
        """Create a new notification for a user."""
        pass

    @abstractmethod
    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[NotificationRead]:
        """Fetch all (or unread) notifications for a user."""
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: int) -> bool:
        """Mark a single notification as read."""
        pass

    @abstractmethod
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all user notifications as read."""
        pass

    @abstractmethod
    def clear_all(self, user_id: int) -> int:
        """Clear (delete) all notifications for a user."""
        pass

    @abstractmethod
    def get_unread_notifications(self, user_id: int) -> List[NotificationRead]:
        """Fetch all unread notifications for a user."""
        pass