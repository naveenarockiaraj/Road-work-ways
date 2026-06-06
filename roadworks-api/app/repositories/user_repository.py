from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserRepository:
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username_or_email(self, db: Session, identifier: str) -> Optional[User]:
        return db.query(User).filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def count(self, db: Session) -> int:
        return db.query(User).count()

    def create(self, db: Session, payload: UserCreate) -> User:
        user = User(
            username=payload.username,
            email=payload.email,
            full_name=payload.full_name,
            password_hash=get_password_hash(payload.password),
            role=payload.role,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User, payload: UserUpdate) -> User:
        update_data = payload.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        for field, value in update_data.items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()


user_repository = UserRepository()
