from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_config import Base
from sqlalchemy import DateTime, Integer, String,  func, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Reminder(Base):
    __tablename__ = "reminders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    reminder_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="reminders")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Reminder(id={self.id}, title={self.title}, description={self.description}, user_id={self.user_id})"