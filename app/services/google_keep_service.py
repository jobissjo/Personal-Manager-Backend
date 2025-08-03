# service.py
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import secrets
import json
import asyncio
from app.repositories import OAuthCredentialsRepository
from app.core.crypto import CryptoService
from app.models import User
from app.core.settings import setting
from app.utils.common import CustomException
from fastapi import status

class GoogleKeepService:
    """Service for handling Google Keep integration."""
    
    SCOPES = ['https://www.googleapis.com/auth/keep']
    GOOGLE_CLIENT_CONFIG = {
        "web": {
            "client_id": setting.GOOGLE_CLIENT_ID,
            "client_secret": setting.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [setting.GOOGLE_REDIRECT_URI]
        }
    }
    
    # Temporary state storage (in production, use Redis)
    _auth_states: Dict[str, str] = {}
    
    @staticmethod
    async def initiate_oauth_flow(user: User) -> Dict[str, str]:
        """Initiate OAuth flow for Google Keep.
        
        Args:
            user: The user initiating the OAuth flow
            
        Returns:
            Dict containing authorization_url and state
            
        Raises:
            CustomException: If OAuth flow initialization fails
        """
        try:
            state = secrets.token_urlsafe(32)
            GoogleKeepService._auth_states[state] = user.id
            
            flow = Flow.from_client_config(
                GoogleKeepService.GOOGLE_CLIENT_CONFIG,
                scopes=GoogleKeepService.SCOPES
            )
            flow.redirect_uri = setting.GOOGLE_REDIRECT_URI
            
            authorization_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=state,
                prompt='consent'
            )
            
            return {
                "authorization_url": authorization_url,
                "state": state
            }
            
        except Exception as e:
            raise CustomException(
                status_code=400,
                detail=f"Failed to initiate OAuth flow: {str(e)}"
            )
    
    @staticmethod
    async def process_oauth_callback(db: AsyncSession, code: str, state: str) -> Dict[str, Any]:
        """Process OAuth callback and store credentials.
        
        Args:
            db: Database session
            code: Authorization code from Google OAuth
            state: State parameter to verify request
            
        Returns:
            Dict containing OAuth credentials
            
        Raises:
            CustomException: If state verification fails or OAuth process fails
        """
        try:
            # Validate state
            if state not in GoogleKeepService._auth_states:
                raise CustomException(
                    status_code=400,
                    detail="Invalid or expired state parameter"
                )
            
            user_id = GoogleKeepService._auth_states[state]
            
            # Exchange code for tokens
            flow = Flow.from_client_config(
                GoogleKeepService.GOOGLE_CLIENT_CONFIG,
                scopes=GoogleKeepService.SCOPES,
                state=state
            )
            # Get redirect URI from settings
            flow.redirect_uri = str(setting.GOOGLE_REDIRECT_URI)
            flow.fetch_token(code=code)
            
            credentials = flow.credentials
            credentials_data = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            
            # Save credentials to database
            await OAuthCredentialsRepository.update(db, user_id, credentials_data)
            
            # Clean up temporary state
            del GoogleKeepService._auth_states[state]
            
            return {
                "success": True,
                "message": "Successfully connected to Google Keep",
                "user_id": user_id
            }
            
        except Exception as e:
            raise CustomException(
                status_code=400,
                detail=f"Failed to process OAuth callback: {str(e)}"
            )
    
    @staticmethod
    async def get_user_credentials(db: AsyncSession, user: User) -> Optional[Dict]:
        """Get decrypted user credentials.
        
        Args:
            db: Database session
            user: User to get credentials for
            
        Returns:
            Optional[Dict]: Decrypted credentials if found, None otherwise
            
        Raises:
            CustomException: If credentials cannot be decrypted
        """
        oauth_creds = await OAuthCredentialsRepository.get_by_user_id(db, user.id)
        
        if not oauth_creds:
            return None
        
        return {
            'token': CryptoService.decrypt(oauth_creds.encrypted_token),
            'refresh_token': CryptoService.decrypt(oauth_creds.encrypted_refresh_token),
            'token_uri': oauth_creds.token_uri,
            'client_id': oauth_creds.client_id,
            'client_secret': oauth_creds.client_secret,
            'scopes': json.loads(oauth_creds.scopes) if oauth_creds.scopes else []
        }
    
    @staticmethod
    async def refresh_token_if_needed(db: AsyncSession, user: User) -> bool:
        """Refresh access token if expired.
        
        Args:
            db: Database session
            user: User to refresh token for
            
        Returns:
            bool: True if token was refreshed successfully
            
        Raises:
            CustomException: If token refresh fails
        """
        try:
            credentials_dict = await GoogleKeepService.get_user_credentials(db, user)
            if not credentials_dict:
                return False
            
            credentials = Credentials(
                token=credentials_dict['token'],
                refresh_token=credentials_dict['refresh_token'],
                token_uri=credentials_dict['token_uri'],
                client_id=credentials_dict['client_id'],
                client_secret=credentials_dict['client_secret'],
                scopes=credentials_dict['scopes']
            )
            
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                
                updated_creds = {
                    'token': credentials.token,
                    'refresh_token': credentials.refresh_token,
                    'token_uri': credentials.token_uri,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'scopes': credentials.scopes
                }
                
                OAuthCredentialsRepository.update(db, user.id, updated_creds)
            
            return True
            
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return False
    
    @staticmethod
    @staticmethod
    async def create_note(db: AsyncSession, user: User, title: str, body: str) -> Dict[str, Any]:
        """Create a note in Google Keep.
        
        Args:
            db: Database session
            user: User creating the note
            title: Note title
            body: Note content
            
        Returns:
            Dict[str, Any]: Created note details
            
        Raises:
            CustomException: If note creation fails or user is not authenticated
        """
        try:
            # Refresh token if needed
            await GoogleKeepService.refresh_token_if_needed(db, user)
            
            # Get fresh credentials
            credentials_dict = await GoogleKeepService.get_user_credentials(db, user)
            if not credentials_dict:
                raise CustomException(
                    status_code=401,
                    detail="User not authenticated with Google Keep"
                )
            
            # Create Google credentials
            credentials = Credentials(
                token=credentials_dict['token'],
                refresh_token=credentials_dict['refresh_token'],
                token_uri=credentials_dict['token_uri'],
                client_id=credentials_dict['client_id'],
                client_secret=credentials_dict['client_secret'],
                scopes=credentials_dict['scopes']
            )
            
            # Build Keep service
            service = build('keep', 'v1', credentials=credentials)
            
            # Create note
            note_body = {
                'title': title,
                'body': {
                    'text': {
                        'text': body
                    }
                }
            }
            
            result = service.notes().create(body=note_body).execute()
            
            return {
                'success': True,
                'note_id': result.get('name', ''),
                'message': 'Note created successfully in Google Keep'
            }
            
        except Exception as e:
            return {
                'success': False,
                'note_id': None,
                'message': f'Failed to create note: {str(e)}'
            }
    
    @staticmethod
    async def is_user_authenticated(db: AsyncSession, user: User) -> bool:
        """Check if user is authenticated with Google Keep.
        
        Args:
            db: Database session
            user: User to check authentication for
            
        Returns:
            bool: True if user is authenticated with Google Keep
        """
        return await OAuthCredentialsRepository.is_authenticated(db, user.id)
    
    @staticmethod
    async def disconnect_user(db: AsyncSession, user: User) -> bool:
        """Disconnect user from Google Keep.
        
        Args:
            db: Database session
            user: User to disconnect
            
        Returns:
            bool: True if user was successfully disconnected
            
        Raises:
            CustomException: If disconnection fails
        """
        return await OAuthCredentialsRepository.delete_by_user_id(db, user.id)