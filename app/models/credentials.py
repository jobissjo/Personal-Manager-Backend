from sqlalchemy import String, DateTime, Text, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import  Mapped, mapped_column
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from app.core.db_config import Base

if TYPE_CHECKING:
    from app.models.user import User


class OAuthCredentials(Base):
    __tablename__ = "oauth_credentials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),  index=True)
    provider: Mapped[str] = mapped_column(String(50), default="google_keep")
    encrypted_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    encrypted_refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    token_uri: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    client_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    client_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    scopes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship("User", back_populates="oauth_credentials")


    def __repr__(self):
        return f"<OAuthCredentials(user_id={self.user_id}, provider={self.provider}, is_active={self.is_active})>"