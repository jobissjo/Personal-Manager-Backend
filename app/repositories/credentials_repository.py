from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload
from typing import Optional, Dict
from datetime import datetime, timedelta, timezone
import json
from app.models import OAuthCredentials
from app.core.crypto import CryptoService
from app.utils.common import CustomException

class OAuthCredentialsRepository:
    
    @staticmethod
    async def create(db: AsyncSession, user_id: str, credentials_data: Dict) -> Optional[OAuthCredentials]:
        """Create new OAuth credentials.
        
        Args:
            db: Database session
            user_id: User ID to create credentials for
            credentials_data: Dictionary containing OAuth credentials
            
        Returns:
            Optional[OAuthCredentials]: Created credentials object
            
        Raises:
            CustomException: If credentials creation fails
        """
        try:
            # Calculate token expiration
            expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
            
            oauth_creds = OAuthCredentials(
                user_id=user_id,
                provider="google_keep",
                encrypted_token=CryptoService.encrypt(credentials_data.get('token')),
                encrypted_refresh_token=CryptoService.encrypt(credentials_data.get('refresh_token')),
                token_uri=credentials_data.get('token_uri'),
                client_id=credentials_data.get('client_id'),
                client_secret=credentials_data.get('client_secret'),
                scopes=json.dumps(credentials_data.get('scopes', [])),
                expires_at=expires_at,
                is_active=True
            )
            
            db.add(oauth_creds)
            await db.commit()
            await db.refresh(oauth_creds)
            return oauth_creds
            
        except Exception as e:
            await db.rollback()
            raise CustomException(
                status_code=500,
                detail=f"Failed to create OAuth credentials: {str(e)}"
            )
    
    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: str) -> Optional[OAuthCredentials]:
        """Get active OAuth credentials by user ID.
        
        Args:
            db: Database session
            user_id: User ID to get credentials for
            
        Returns:
            Optional[OAuthCredentials]: Active credentials if found
        """
        query = select(OAuthCredentials).where(
            and_(
                OAuthCredentials.user_id == user_id,
                OAuthCredentials.is_active.is_(True)
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update(db: AsyncSession, user_id: str, credentials_data: Dict) -> Optional[OAuthCredentials]:
        """Update existing OAuth credentials.
        
        Args:
            db: Database session
            user_id: User ID to update credentials for
            credentials_data: Dictionary containing OAuth credentials
            
        Returns:
            Optional[OAuthCredentials]: Updated credentials object
            
        Raises:
            CustomException: If credentials update fails
        """
        try:
            oauth_creds = await OAuthCredentialsRepository.get_by_user_id(db, user_id)
            
            if oauth_creds:
                # Update existing
                oauth_creds.encrypted_token = CryptoService.encrypt(credentials_data.get('token'))
                oauth_creds.encrypted_refresh_token = CryptoService.encrypt(credentials_data.get('refresh_token'))
                oauth_creds.token_uri = credentials_data.get('token_uri')
                oauth_creds.client_id = credentials_data.get('client_id')
                oauth_creds.client_secret = credentials_data.get('client_secret')
                oauth_creds.scopes = json.dumps(credentials_data.get('scopes', []))
                oauth_creds.expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
                oauth_creds.updated_at = datetime.now(timezone.utc)
                oauth_creds.is_active = True
            else:
                # Create new if doesn't exist
                oauth_creds = await OAuthCredentialsRepository.create(db, user_id, credentials_data)
            
            await db.commit()
            await db.refresh(oauth_creds)
            return oauth_creds
            
        except Exception as e:
            await db.rollback()
            raise CustomException(
                status_code=500,
                detail=f"Failed to update OAuth credentials: {str(e)}"
            )
    
    @staticmethod
    async def delete_by_user_id(db: AsyncSession, user_id: str) -> bool:
        """Soft delete OAuth credentials.
        
        Args:
            db: Database session
            user_id: User ID to delete credentials for
            
        Returns:
            bool: True if credentials were deactivated
            
        Raises:
            CustomException: If deletion fails
        """
        try:
            oauth_creds = await OAuthCredentialsRepository.get_by_user_id(db, user_id)
            
            if oauth_creds:
                oauth_creds.is_active = False
                oauth_creds.updated_at = datetime.now(timezone.utc)
                await db.commit()
                return True
            return False
            
        except Exception as e:
            await db.rollback()
            raise CustomException(
                status_code=500,
                detail=f"Failed to delete OAuth credentials: {str(e)}"
            )
    
    @staticmethod
    async def is_authenticated(db: AsyncSession, user_id: str) -> bool:
        """Check if user has valid OAuth credentials.
        
        Args:
            db: Database session
            user_id: User ID to check credentials for
            
        Returns:
            bool: True if user has valid credentials
        """
        oauth_creds = await OAuthCredentialsRepository.get_by_user_id(db, user_id)
        
        if not oauth_creds:
            return False
        
        # Check if token is not expired
        current_time = datetime.now(timezone.utc)
        if oauth_creds.expires_at and oauth_creds.expires_at < current_time:
            return False
        
        return True
    
    @staticmethod
    async def cleanup_expired(db: AsyncSession) -> int:
        """Clean up expired credentials.
        
        Args:
            db: Database session
            
        Returns:
            int: Number of credentials deactivated
            
        Raises:
            CustomException: If cleanup fails
        """
        try:
            current_time = datetime.now(timezone.utc)
            stmt = (
                select(OAuthCredentials)
                .where(
                    and_(
                        OAuthCredentials.expires_at < current_time,
                        OAuthCredentials.is_active.is_(True)
                    )
                )
            )
            result = await db.execute(stmt)
            expired_creds = result.scalars().all()
            
            count = 0
            for cred in expired_creds:
                cred.is_active = False
                cred.updated_at = current_time
                count += 1
            
            await db.commit()
            return count
            
        except Exception as e:
            await db.rollback()
            raise CustomException(
                status_code=500,
                detail=f"Failed to cleanup expired credentials: {str(e)}"
            )