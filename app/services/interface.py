from typing import Protocol, List
from datetime import date
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from abc import ABC, abstractmethod


class IReminderService(Protocol):
    async def create_reminder(self, user_id: int, data: ReminderCreate) -> Reminder: ...
    async def get_user_reminders(self, user_id: int) -> list[Reminder]: ...
    async def get_reminder_by_id(self, reminder_id: int) -> Reminder: ...
    async def update_reminder(self, reminder_id: int, data: ReminderUpdate) -> Reminder: ...
    async def delete_reminder(self, reminder_id: int) -> None: ...





class IHabitLogService(ABC):
    @abstractmethod
    async def add_logs(self, habit_id: int, dates: List[date]) -> None: ...

    @abstractmethod
    async def delete_log(self, habit_id: int, log_date: date) -> None: ...

    @abstractmethod
    async def clear_logs(self, habit_id: int) -> None: ...
