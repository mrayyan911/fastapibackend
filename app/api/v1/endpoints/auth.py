from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.jwt_handler import create_access_token, decode_access_token
from app.db.session import get_db_session
from app.schemas.schemas import UserCreate, UserLogin, ShowUser, ResendVerificationRequest
from app.crud.crud_user import create_user, get_user_by_email
from app.core.security import verify_password
from app.services.verification_service import VerificationService
from app.task import send_verification_email
from fastapi.security import OAuth2PasswordBearer
from fastapi import status

router = APIRouter()

@router.post("/signup", response_model=ShowUser)
def signup(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db_session)):
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")
    
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(400, detail="Email already registered")
    
    new_user = create_user(db=db, user=user)
    
    background_tasks.add_task(send_verification_email, new_user.email)

    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db_session)):
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")
    
    db_user = get_user_by_email(db, user.email)
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(401, detail="Invalid credentials")
    
    if not db_user.is_verified:
        raise HTTPException(401, detail="Email not verified")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception
    
    email = payload.get("sub")
    if not email:
        raise credentials_exception
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user

@router.get("/me", response_model=ShowUser)
def read_users_me(current_user: ShowUser = Depends(get_current_user)):
    return current_user



@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db_session)):
    verification_service = VerificationService(db)
    if verification_service.verify_email(token):
        return {"message": "Email verified successfully"}
    else:
        raise HTTPException(400, detail="Invalid or expired verification token")
    
@router.post("/resend-verification")
def resend_verification(request: ResendVerificationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db_session)):
    db_user = get_user_by_email(db, request.email)
    if not db_user:
        raise HTTPException(404, detail="User not found")
    if db_user.is_verified:
        raise HTTPException(400, detail="Email already verified")
    
    background_tasks.add_task(send_verification_email, db_user.email)
    return {"message": "Verification email resent"}
