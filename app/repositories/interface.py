# repositories/interfaces/habit_log.py
from abc import ABC, abstractmethod
from typing import List
from datetime import date
from app.models import HabitLog

class IHabitLogRepository(ABC):
    @abstractmethod
    async def add(self, log: HabitLog) -> HabitLog: ...
    
    @abstractmethod
    async def delete_by_id(self, log_id: int) -> None: ...
    
    @abstractmethod
    async def add_many(self, logs: List[HabitLog]) -> None: ...
    
    @abstractmethod
    async def clear_by_date(self, habit_ids: List[int], log_date: date) -> None: ...
