from datetime import datetime, timedelta, timezone
from app.schemas import user_schema
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, TempUserOTP, Profile
from app.schemas.common_schema import RefreshTokenBody, TokenResponse
from app.utils.common import CustomException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_refresh_token,
)
from app.services.common_service import CommonService
from app.services.email_service import EmailService
from app.repositories import UserRepository
from app.core.logger_config import logger as default_logger
from starlette import status

PROFILE_UPLOAD_FOLDER = "profile"


class UserService:
    def __init__(self, email_service: EmailService, db: AsyncSession, logger=None):
        self.email_service = email_service
        self.db = db
        self.logger = logger or default_logger

    async def register_user(self, user_data: user_schema.RegisterSchema):
        otp = await self.get_user_otp(
            user_data.email,
        )
        if otp.otp != user_data.otp:
            raise CustomException(
                "Invalid OTP", status_code=status.HTTP_400_BAD_REQUEST
            )

        existing_user = await UserRepository.get_user_by_email(user_data.email, self.db)

        if existing_user and existing_user.is_active:
            raise CustomException(
                "A user with this username or email already exists.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user_dict = user_data.model_dump(exclude={"otp"})
        hashed_password = await hash_password(user_dict["password"])

        if not existing_user:
            user_dict["password"] = hashed_password
            user = User(**user_dict)
            try:
                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)
                return user
            except Exception as e:
                self.logger.error(f"Error registering user: {e}")
                await self.db.rollback()
                raise CustomException("Failed to register user", 500)

        elif not existing_user.is_active and existing_user.email == user_data.email:
            existing_user.password = hashed_password
            existing_user.role = user_data.role
            await self.db.commit()
            await self.db.refresh(existing_user)
            return existing_user

        raise CustomException(
            "A user with this username already exists.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    async def login_user(
        self,
        user_data: user_schema.LoginEmailSchema,
    ) -> TokenResponse:
        """Authenticate
          user and return access tokens.

        Args:
            user_data: Login credentials
            db: Database session

        Returns:
            Dict containing access_token, refresh_token, token_type and role

        Raises:
            CustomException: If credentials are invalid or user doesn't exist
        """
        existing_user = await UserRepository.get_user_by_email(user_data.email, self.db)
        if not existing_user:
            raise CustomException(
                "Email does not exist", status_code=status.HTTP_400_BAD_REQUEST
            )

        if not await verify_password(user_data.password, existing_user.password):
            raise CustomException(
                "Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED
            )

        access_token = await create_access_token({"user_id": existing_user.id})
        refresh_token = await create_refresh_token({"user_id": existing_user.id})

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            role=existing_user.role,
        )

    async def verify_email(self, data: user_schema.EmailVerifySchema) -> None:
        user = await UserRepository.get_user_by_email(data.email, self.db)
        if user and user.is_active:
            raise CustomException(
                "Email already exists", status_code=status.HTTP_400_BAD_REQUEST
            )

        user_otp = await UserRepository.create_user_otp(data.email, self.db)
        await self.email_service.send_email(
            recipient=data.email,
            subject="Verify Your Account",
            template_name="email/verify_account.html",
            template_data={"otp": user_otp.otp, "name": data.first_name},
            use_admin_email=True,
            db=self.db,
        )

    async def verify_email_otp(self, data: user_schema.EmailVerifyOtpSchema) -> None:
        existing_user = await UserRepository.get_user_by_email(data.email, self.db)
        if existing_user and existing_user.is_active:
            raise CustomException(
                "Email already exists", status_code=status.HTTP_400_BAD_REQUEST
            )

        user_otp = await self.get_user_otp(data.email)
        if user_otp.otp != data.otp:
            raise CustomException(
                "Invalid OTP", status_code=status.HTTP_400_BAD_REQUEST
            )

    async def refresh_to_access_token(
        self, token_data: RefreshTokenBody
    ) -> TokenResponse:
        payload = await verify_refresh_token(token_data.refresh_token)
        user_id = payload.get("user_id")

        if not user_id:
            raise CustomException(
                "Invalid refresh token", status_code=status.HTTP_401_UNAUTHORIZED
            )

        user = await UserRepository.get_user_by_id(user_id, self.db)
        if not user or not user.is_active:
            raise CustomException(
                "User not found or inactive", status_code=status.HTTP_401_UNAUTHORIZED
            )

        access_token = await create_access_token({"user_id": user.id})
        refresh_token = await create_refresh_token({"user_id": user.id})

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            role=user.role,
        )

    # Delegated from OTP service:
    async def get_user_otp(self, email: str) -> TempUserOTP:
        otp = await UserRepository.get_otp_by_email(email, self.db)
        if otp is None:
            raise CustomException(
                "OTP not found", status_code=status.HTTP_400_BAD_REQUEST
            )

        created_at = (
            otp.created_at.replace(tzinfo=timezone.utc)
            if otp.created_at.tzinfo is None
            else otp.created_at
        )
        if created_at < datetime.now(timezone.utc) - timedelta(minutes=5):
            await self.delete_user_otp(email)
            raise CustomException(
                "OTP expired", status_code=status.HTTP_400_BAD_REQUEST
            )

        return otp

    async def delete_user_otp(self, email: str) -> None:
        otp = await UserRepository.get_otp_by_email(email, self.db)
        if otp:
            await self.db.delete(otp)
            await self.db.commit()

    async def update_profile(
        self, user_id: int, data: user_schema.ProfileUpdateSchema
    ) -> Profile:
        profile_picture_url = (
            await CommonService.save_base64_file(
                data.profile_picture, PROFILE_UPLOAD_FOLDER
            )
            if data.profile_picture
            else None
        )

        return await UserRepository.update_profile(
            user_id=user_id,
            bio=data.bio,
            profile_picture_url=profile_picture_url,
            db=self.db,
        )

    async def update_profile_form(
        self,
        user_id: int,
        data: user_schema.ProfileUpdateForm,
    ) -> Profile:
        profile_picture_url = (
            await CommonService.save_upload_file(
                data.profile_picture, PROFILE_UPLOAD_FOLDER
            )
            if data.profile_picture
            else None
        )
        return await UserRepository.update_profile(
            user_id=user_id,
            bio=data.bio,
            profile_picture_url=profile_picture_url,
            db=self.db,
        )
