from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.schemas import UserCreate, UserLogin, ShowUser, ResendVerificationRequest
from app.crud.crud_user import create_user, get_user_by_email
from app.core.security import verify_password
from app.services.verification_service import VerificationService
from app.task import send_verification_email

router = APIRouter()

@router.post("/signup", response_model=ShowUser)
def signup(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
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
def login(user: UserLogin, db: Session = Depends(get_db)):
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")
    
    db_user = get_user_by_email(db, user.email)
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(401, detail="Invalid credentials")
    
    if not db_user.is_verified:
        raise HTTPException(401, detail="Email not verified")
    
    return {"message": "Login successful"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    verification_service = VerificationService(db)
    if verification_service.verify_email(token):
        return {"message": "Email verified successfully"}
    else:
        raise HTTPException(400, detail="Invalid or expired verification token")

@router.post("/resend-verification")
def resend_verification(request: ResendVerificationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, request.email)
    if not db_user:
        raise HTTPException(404, detail="User not found")
    if db_user.is_verified:
        raise HTTPException(400, detail="Email already verified")
    
    background_tasks.add_task(send_verification_email, db_user.email)
    return {"message": "Verification email resent"}
