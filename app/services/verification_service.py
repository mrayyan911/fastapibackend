from sqlalchemy.orm import Session
from app.core.security import create_email_verification_token, verify_email_verification_token
from app.crud.crud_user import get_user_by_email

class VerificationService:
    def __init__(self, db: Session):
        self.db = db

    def send_verification_link(self, email: str):
        token = create_email_verification_token(email)
        # In a real application, you would send an email with this link
        verification_link = f"http://localhost:8000/api/v1/verify-email?token={token}"
        print(f"Verification link for {email}: {verification_link}")

    def verify_email(self, token: str) -> bool:
        email = verify_email_verification_token(token)
        if email:
            user = get_user_by_email(self.db, email)
            if user and not user.is_verified:
                user.is_verified = True
                self.db.commit()
                return True
        return False
