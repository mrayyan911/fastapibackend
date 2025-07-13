#A service which will handle the verification code logic
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import verificationCode
from app.schemas.schemas import VerificationCodeCreate  
from app.crud.crud_verification_code import create_verification_code,get_verification_code, delete_verification_code
#would need to use celery and send a random code to the user save that in db and if user enters the code we will check if it matches
class VerificationCodeService:  
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def generate_random_code(length: int = 6) -> str:
        import random
        return ''.join(random.choices('0123456789', k=length))



    
    def create_code(self, user_id: int) -> verificationCode:
        code = self.generate_random_code()
        expires_at = datetime.utcnow() + timedelta(minutes=10)  # Code valid for 10 minutes
        return create_verification_code(self.db, user_id, code, expires_at)

    def verify_code(self, user_id: int, code: str) -> bool:
        verification_code = get_verification_code(self.db, user_id, code)
        
        if verification_code:
            delete_verification_code(self.db, verification_code)
            return True
        return False
