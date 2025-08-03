from fastapi import APIRouter, Depends
from app.schemas import BaseResponse, TokenResponse
from app.schemas.common_schema import RefreshTokenBody
from app.schemas.user_schema import (
    EmailVerifyOtpSchema,
    RegisterSchema,
    LoginEmailSchema,
    EmailVerifySchema,
)
from fastapi.security import OAuth2PasswordRequestForm
from app.services import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_config import get_db
from typing import Annotated
from app.services import EmailService


router = APIRouter(prefix="/auth", tags=["Auth"])


def get_user_service(
    db: AsyncSession = Depends(get_db),
    email_service: EmailService = Depends(EmailService),
) -> UserService:
    return UserService(email_service=email_service, db=db)


@router.post("/verify-email")
async def verify_email(
    data: EmailVerifySchema, user_service: Annotated[UserService, Depends(get_user_service)],
) -> BaseResponse[None]:
    await user_service.verify_email(data)
    return BaseResponse( message="OTP sent successfully", data=None)


@router.post("/verify-email-otp")
async def verify_email_otp(
    data: EmailVerifyOtpSchema, user_service: Annotated[UserService, Depends(get_user_service)],
) -> BaseResponse[None]:
    await user_service.verify_email_otp(data)
    return BaseResponse(
        message="Email verified successfully", data=None
    )


@router.post("/register")
async def register(
    data: RegisterSchema, user_service: Annotated[UserService, Depends(get_user_service)],
) -> BaseResponse[None]:
    _user = await user_service.register_user(data)
    return BaseResponse(
         message="User registered successfully", data=None
    )


@router.post("/login")
async def login(
    data: LoginEmailSchema, user_service: Annotated[UserService, Depends(get_user_service)],
) -> BaseResponse[TokenResponse]:
    token_data = await user_service.login_user(data)
    return BaseResponse(
        message="User logged in successfully",
        data=token_data,
    )


@router.post("/token")
async def token(
    user_service: Annotated[UserService, Depends(get_user_service)],
    data: OAuth2PasswordRequestForm = Depends(),
) -> TokenResponse:
    token_data = await user_service.login_user(
        LoginEmailSchema(email=data.username, password=data.password)
    )
    return TokenResponse(**token_data)


@router.post("/refresh")
async def refresh(
    user_service: Annotated[UserService, Depends(get_user_service)],
    data: RefreshTokenBody,
) -> BaseResponse[TokenResponse]:
    token_data = await user_service.refresh_to_access_token(data)
    return BaseResponse(
        message="Token refreshed successfully",
        data=token_data,
    )
