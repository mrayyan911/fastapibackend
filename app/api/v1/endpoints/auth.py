from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.schemas import UserCreate, UserLogin, ShowUser
from app.crud.crud_user import create_user, get_user_by_email,get_user_by_id
from app.core.security import verify_password
from app.models.models import User # Import User model for type hinting
from app.celery_worker import send_verification_email # Assuming celery_worker.py remains in app/

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
    
    try:
        background_tasks.add_task(send_verification_email, new_user.email, new_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send verification email: {str(e)}")

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

@router.get("/verify/{user_id}/{code}")
def verify_email(user_id: int, code: str, db: Session = Depends(get_db)):
    from app.services.verification_code_service import VerificationCodeService
    
    verification_service = VerificationCodeService(db)
    
    if verification_service.verify_code(user_id, code):
        user = get_user_by_id(db, user_id)
        if user:
            user.is_verified = True
            db.commit()
            return {"message": "Email verified successfully"}
        else:
            raise HTTPException(404, detail="User not found")
    else:
        raise HTTPException(400, detail="Invalid or expired verification code")