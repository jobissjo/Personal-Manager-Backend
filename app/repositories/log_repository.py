from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.log import Log
from app.schemas.log_schema import LogCreate


class LogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_log(self, log_data: LogCreate):
        log = Log(**log_data)
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def get_user_logs(self, user_id: int):
        query = select(Log).where(Log.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()
