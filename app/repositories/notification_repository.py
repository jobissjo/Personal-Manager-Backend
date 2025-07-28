from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models.notification import Notification
from typing import List, Optional


class NotificationRepository:
    @staticmethod
    async def create(db: AsyncSession, notification: Notification) -> Notification:
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification

    @staticmethod
    async def get_by_user(
        db: AsyncSession, user_id: int, is_read: Optional[bool] = None
    ) -> List[Notification]:
        query = select(Notification).where(Notification.user_id == user_id)
        if is_read is not None:
            query = query.where(Notification.is_read == is_read)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_one(
        db: AsyncSession, notification_id: int, user_id: int
    ) -> Notification | None:
        result = await db.execute(
            select(Notification).where(
                Notification.id == notification_id, Notification.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def mark_as_read(
        db: AsyncSession, notification_id: int, user_id: int
    ) -> None:
        await db.execute(
            update(Notification)
            .where(Notification.id == notification_id, Notification.user_id == user_id)
            .values(is_read=True)
        )
        await db.commit()

    @staticmethod
    async def clear_all(db: AsyncSession, user_id: int) -> None:
        await db.execute(delete(Notification).where(Notification.user_id == user_id))
        await db.commit()
