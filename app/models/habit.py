from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_config import Base
from sqlalchemy import DateTime, Integer, String,  func, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.common import HabitCategory
    from app.models.user import User


class Habit(Base):
    __tablename__ = "habits"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("habit_categories.id", ondelete="CASCADE"), nullable=False)
    category: Mapped["HabitCategory"] = relationship("HabitCategory", back_populates="habits")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="habits")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Habit(id={self.id}, title={self.title}, category_id={self.category_id}, user_id={self.user_id})>"