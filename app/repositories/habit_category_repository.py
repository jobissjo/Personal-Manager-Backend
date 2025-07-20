from sqlalchemy import select
from app.models  import HabitCategory
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import HabitCategoryModelSchema
from app.core.logger_config import logger as default_logger
from app.schemas.habit_category_schema import HabitCategoryPartialRequestSchema
from app.utils.common import CustomException
from starlette import status

class HabitCategoryRepository:
    def __init__(self, session: AsyncSession, logger=None):
        self.session = session
        self.logger = logger or default_logger

    async def get_all_habit_categories(self, name: str = None, search: str = None):
        query = select(HabitCategory)
        if name:
            query = query.where(HabitCategory.name == name)
        if search:
            query = query.where(HabitCategory.name.contains(search))
        
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_habit_category_by_id(self, category_id: int)->HabitCategory | None:
        response = await self.session.execute(select(HabitCategory).where(HabitCategory.id == category_id))
        return response.scalars().first()
    
    async def create_habit_category(self, category_data: HabitCategoryModelSchema)-> HabitCategory:
        category = HabitCategory(**category_data.model_dump())
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category
    
    async def update_habit_category_by_id(self, category_id: int, category_data: HabitCategoryPartialRequestSchema)->HabitCategory:
        category = await self.get_habit_category_by_id(category_id)
        if not category:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit category not found")
        for key, value in category_data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete_habit_category_by_id(self, category_id: int)->HabitCategory:
        category = await self.get_habit_category_by_id(category_id)
        if not category:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit category not found")
        await self.session.delete(category)
        await self.session.commit()
        return category
    
        