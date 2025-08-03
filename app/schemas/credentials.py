from pydantic import BaseModel
from typing import Optional

class OAuthInitResponse(BaseModel):
    authorization_url: str
    state: str

class OAuthCallbackRequest(BaseModel):
    code: str
    state: str
    error: Optional[str] = None

class OAuthCallbackResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[str] = None

class AuthStatusResponse(BaseModel):
    authenticated: bool
    user_id: str
    message: str