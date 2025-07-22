# schemas/habit_log.py
from pydantic import BaseModel
from datetime import date
from typing import List

class HabitLogBase(BaseModel):
    habit_id: int
    completed_date: date

class HabitLogCreate(HabitLogBase):
    pass

class HabitLogMultipleCreate(BaseModel):
    habit_ids: List[int]
    completed_date: date

class HabitLogClear(BaseModel):
    completed_date: date

class HabitLogResponse(HabitLogBase):
    id: int

    class Config:
        from_attributes = True
