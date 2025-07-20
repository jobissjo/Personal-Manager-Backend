from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ReminderCreate(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_date: datetime


class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    reminder_date: Optional[datetime] = None


class ReminderOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    reminder_date: datetime
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
