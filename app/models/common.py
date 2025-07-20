from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_config import Base
from sqlalchemy import DateTime, Integer, String,  func, ForeignKey
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.habit import Habit
    from app.models.user import User


class HabitCategory(Base):
    __tablename__ = "habit_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    icon_name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user : Mapped["User"] = relationship("User", back_populates="habit_categories")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    habits: Mapped[List["Habit"]] = relationship("Habit", back_populates="category")

    def __repr__(self):
        return f"<HabitCategory(id={self.id}, name={self.name})>"