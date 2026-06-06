from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import get_password_hash
from app.core.permissions import Role
from app.models.user import User


def init_db(db: Session) -> None:
    """Initialize database with first superuser if not exists."""
    existing = db.query(User).filter(
        User.username == settings.FIRST_SUPERUSER_USERNAME
    ).first()

    if not existing:
        superuser = User(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            full_name=settings.FIRST_SUPERUSER_FULLNAME,
            password_hash=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            role=Role.SUPER_ADMIN,
            is_active=True,
        )
        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        print(f"[init_db] Super admin '{superuser.username}' created.")
    else:
        print("[init_db] Super admin already exists, skipping.")
