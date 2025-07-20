from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Habit
from sqlalchemy import select
from app.schemas import HabitModelSchema, HabitPartialRequestSchema


class HabitRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_habit(self, habit_data: HabitModelSchema):
        habit = Habit(**habit_data.model_dump())
        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def get_habit_by_id(self, habit_id: int):
        result = await self.session.execute(select(Habit).where(Habit.id == habit_id))
        return result.scalar_one_or_none()

    async def get_all_habits(self, user_id: int):
        result = await self.session.execute(
            select(Habit).where(Habit.user_id == user_id)
        )
        return result.scalars().all()

    async def update_habit_by_id(self, habit_id: int, data: HabitPartialRequestSchema):
        habit = await self.get_habit_by_id(habit_id)
        if not habit:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(habit, key, value)
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def delete_habit_by_id(self, habit_id: int):
        habit = await self.get_habit_by_id(habit_id)
        if not habit:
            return None
        await self.session.delete(habit)
        await self.session.commit()
        return habit
