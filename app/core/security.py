from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"



def create_email_verification_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode = {"exp": expire, "sub": email}
    encoded_jwt = jwt.encode(to_encode, settings.EMAIL_VERIFICATION_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_email_verification_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.EMAIL_VERIFICATION_SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token.get("sub")
    except JWTError:
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
