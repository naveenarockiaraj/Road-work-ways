from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.core.permissions import Role
from app.repositories.user_repository import user_repository
from app.models.user import User
from app.dependencies.database import get_db
from typing import List

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id: int = int(payload.get("sub"))
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user account",
        )
    return user


def require_roles(allowed_roles: List[Role]):
    """Dependency factory: checks that the current user has an allowed role."""
    def _check(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not permitted to perform this action.",
            )
        return current_user
    return _check


# Pre-built role deps
def admin_only(current_user: User = Depends(get_current_user)) -> User:
    return require_roles([Role.SUPER_ADMIN])(current_user)


def manager_and_above(current_user: User = Depends(get_current_user)) -> User:
    return require_roles([Role.SUPER_ADMIN, Role.CONTRACTOR, Role.PROJECT_MANAGER])(current_user)
