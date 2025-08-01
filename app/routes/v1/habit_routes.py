from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_config import get_db
from app.models.user import User
from app.core.permissions import any_user_role
from app.services.habit_service import HabitService
from app.schemas import (
    HabitRequestSchema,
    HabitPartialRequestSchema,
    HabitResponseSchema,
    BaseResponse,
)

router = APIRouter(prefix="/habits", tags=["Habits"])
habit_service = HabitService()


@router.post("/")
async def create_habit(
    data: HabitRequestSchema,
    user: Annotated[User, Depends(any_user_role)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BaseResponse[HabitResponseSchema]:
    habit = await habit_service.create_habit(data, db, user)
    return BaseResponse(message="Habit created successfully", data=habit)


@router.get("/")
async def get_all_habits(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(any_user_role)],
) -> BaseResponse[list[HabitResponseSchema]]:
    habits = await habit_service.get_all_habits(db, user)
    return BaseResponse(message="Habits fetched successfully", data=habits)


@router.get("/{habit_id}")
async def get_habit_by_id(
    habit_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(any_user_role)],
) -> BaseResponse[HabitResponseSchema]:
    habit = await habit_service.get_habit_by_id(habit_id, db)
    return BaseResponse(message="Habit fetched successfully", data=habit)


@router.put("/{habit_id}")
async def update_habit(
    habit_id: int,
    data: HabitRequestSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(any_user_role)],
) -> BaseResponse[HabitResponseSchema]:
    habit = await habit_service.update_habit_by_id(habit_id, data, db)
    return BaseResponse(message="Habit updated successfully", data=habit)


@router.patch("/{habit_id}")
async def partial_update_habit(
    habit_id: int,
    data: HabitPartialRequestSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(any_user_role)],
) -> BaseResponse[HabitResponseSchema]:
    habit = await habit_service.update_habit_by_id(habit_id, data, db)
    return BaseResponse(message="Habit updated successfully", data=habit)


@router.delete("/{habit_id}")
async def delete_habit(
    habit_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(any_user_role)],
) -> BaseResponse[HabitResponseSchema]:
    await habit_service.delete_habit_by_id(habit_id, db)
    return BaseResponse(message="Habit deleted successfully", data=None)
