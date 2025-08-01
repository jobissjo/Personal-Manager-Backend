# app/services/habit_service.py

from app.schemas import (
    HabitRequestSchema,
    HabitModelSchema,
    HabitPartialRequestSchema,
)
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import HabitRepository


class HabitService:
    async def create_habit(self, data: HabitRequestSchema, db: AsyncSession, user: User):
        habit_data = HabitModelSchema(**data.model_dump(), user_id=user.id)
        return await HabitRepository(db).create_habit(habit_data)

    async def get_habit_by_id(self, habit_id: int, db: AsyncSession):
        return await HabitRepository(db).get_habit_by_id(habit_id)

    async def get_all_habits(self, db: AsyncSession, user: User):
        return await HabitRepository(db).get_all_habits(user.id)

    async def update_habit_by_id(self, habit_id: int, data: HabitPartialRequestSchema, db: AsyncSession):
        return await HabitRepository(db).update_habit_by_id(habit_id, data)

    async def delete_habit_by_id(self, habit_id: int, db: AsyncSession):
        return await HabitRepository(db).delete_habit_by_id(habit_id)
