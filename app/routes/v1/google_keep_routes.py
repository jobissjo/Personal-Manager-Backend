from typing import Annotated
from google_auth_oauthlib.flow import Flow
# from urllib.parse import urlencode
from fastapi import APIRouter, BackgroundTasks, Depends,  HTTPException, status
from app.core.db_config import get_db
from app.models.user import User
from app.repositories.credentials_repository import OAuthCredentialsRepository
from app.utils.common import CustomException
from sqlalchemy.ext.asyncio import AsyncSession
import os
from app.core.permissions import any_user_role
from app.core.settings import setting
from app.schemas.credentials import AuthStatusResponse, OAuthCallbackRequest, OAuthCallbackResponse, OAuthInitResponse
from app.services.google_keep_service import GoogleKeepService

router = APIRouter(prefix="/google-keep", tags=["Google Keep"])


@router.post("/auth/google-keep", response_model=OAuthInitResponse)
async def initiate_google_keep_auth(
    user: Annotated[User, Depends(any_user_role)]
):
    """Initiate OAuth flow for Google Keep"""
    try:
        result = GoogleKeepService.initiate_oauth_flow(user)
        return OAuthInitResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/auth/callback", response_model=OAuthCallbackResponse)
async def google_keep_auth_callback(
    request_data: OAuthCallbackRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    background_tasks: BackgroundTasks
):
    """Process OAuth callback from Google"""
    try:
        if request_data.error:
            return OAuthCallbackResponse(
                success=False,
                message=f"Authorization failed: {request_data.error}"
            )
        
        result = GoogleKeepService.process_oauth_callback(
            db, request_data.code, request_data.state
        )
        
        # Schedule cleanup task
        background_tasks.add_task(OAuthCredentialsRepository.cleanup_expired, db)
        
        return OAuthCallbackResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/auth/status", response_model=AuthStatusResponse)
async def check_auth_status(
    user: Annotated[User, Depends(any_user_role)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Check Google Keep authentication status"""
    is_authenticated = GoogleKeepService.is_user_authenticated(db, user)
    
    return AuthStatusResponse(
        authenticated=is_authenticated,
        user_id=user.id,
        message="User is connected to Google Keep" if is_authenticated else "User needs to authenticate"
    )