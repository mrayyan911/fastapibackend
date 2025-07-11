from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from schemas import UserCreate, UserLogin, ShowUser
from auth import hash_password, verify_password
from fastapi.background import BackgroundTasks
from celery_worker import send_verification_email

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/signup", response_model=ShowUser)
def signup(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Validate that the email and password are provided
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")
    
    # Check if the email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(400, detail="Email already registered")
    
    # Hash the password before saving
    hashed_password = hash_password(user.password)
    
    # Create the new user
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Trigger the email verification in the background
    try:
        background_tasks.add_task(send_verification_email, user.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send verification email: {str(e)}")

    return new_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Validate that the email and password are provided
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # Check if the user exists and password is correct
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(401, detail="Invalid credentials")
    
    # Check if the user has verified their email
    if not db_user.is_verified:
        raise HTTPException(401, detail="Email not verified")
    
    return {"message": "Login successful"}
