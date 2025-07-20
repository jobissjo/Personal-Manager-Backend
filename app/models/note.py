from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_config import Base
from sqlalchemy import DateTime, Integer, String, ForeignKey, func
from typing import TYPE_CHECKING, List
from app.models.association import note_tag_table

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.tag import Tag


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="notes")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary=note_tag_table,
        back_populates="notes"
    )

    def __repr__(self):
        return f"Note(id={self.id!r}, title={self.title!r}, content={self.description!r})"