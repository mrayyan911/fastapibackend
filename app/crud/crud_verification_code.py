from sqlalchemy.orm import Session
from app.models.models import verificationCode
from app.schemas.schemas import VerificationCodeCreate
from datetime import datetime, timedelta

def create_verification_code(db: Session, user_id: int, code: str, expires_at: datetime) -> verificationCode:
    verification_code = verificationCode(user_id=user_id, code=code, expires_at=expires_at)
    db.add(verification_code)
    db.commit()
    db.refresh(verification_code)
    return verification_code

def get_verification_code(db: Session, user_id: int, code: str) -> verificationCode | None:
    return db.query(verificationCode).filter(
        verificationCode.user_id == user_id,
        verificationCode.code == code,
        verificationCode.expires_at > datetime.utcnow()
    ).first()

def delete_verification_code(db: Session, verification_code: verificationCode):
    db.delete(verification_code)
    db.commit()
