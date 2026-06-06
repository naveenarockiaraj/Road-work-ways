from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.core.exceptions import UnauthorizedException
from app.repositories.user_repository import user_repository
from app.schemas.auth import LoginRequest, TokenResponse, UserInToken


class AuthService:
    def login(self, db: Session, payload: LoginRequest) -> TokenResponse:
        user = user_repository.get_by_username_or_email(db, payload.username)
        if not user:
            raise UnauthorizedException("Invalid username or password")
        if not verify_password(payload.password, user.password_hash):
            raise UnauthorizedException("Invalid username or password")
        if not user.is_active:
            raise UnauthorizedException("Account is deactivated. Contact administrator.")

        expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(subject=user.id, expires_delta=expires)

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserInToken.model_validate(user),
        )


auth_service = AuthService()
