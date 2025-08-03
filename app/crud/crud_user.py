from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.schemas import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

from app.core.security import hash_password

def create_user(db: Session, user: UserCreate, firebase_uid: str | None = None):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password, firebase_uid=firebase_uid)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



