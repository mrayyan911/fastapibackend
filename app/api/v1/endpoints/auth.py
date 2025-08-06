from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from firebase_admin import auth as firebase_auth
from firebase_admin import exceptions as firebase_exceptions


from app.core.jwt_handler import create_access_token, decode_access_token
from app.db.session import get_db_session
from app.core.security import verify_password, hash_password
from app.crud.crud_user import create_user, get_user_by_email
from app.schemas.schemas import (
    UserCreate, UserLogin, ShowUser, ResendVerificationRequest
)
from app.celery_tasks.send_verification_email import send_verification_email
router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")




# -------------------
# SIGNUP
# -------------------
@router.post("/signup", response_model=ShowUser)
def signup(user: UserCreate, db: Session = Depends(get_db_session)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(400, detail="Email already registered")

    try:
        # Create user in Firebase
        firebase_user = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )
        
        # Send email verification
        verification_link = firebase_auth.generate_email_verification_link(user.email)
        send_verification_email.delay(user.email, verification_link)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create user in Firebase: {e}")

    # Create user in your backend DB with hashed password and firebase_uid
    new_user = create_user(
        db=db,
        user=user,
        firebase_uid=firebase_user.uid
    )

    return new_user


# -------------------
# LOGIN
# -------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db_session)):
    db_user = get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found in the database.")

    # Verify password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Optional: Check email verification status with Firebase
    if db_user.firebase_uid:
        try:
            firebase_user = firebase_auth.get_user(db_user.firebase_uid)
            if not firebase_user.email_verified:
                raise HTTPException(
                    status_code=401, detail="Email not verified. Please verify your email."
                )
            
        except firebase_exceptions.NotFoundError:
            # This case should ideally not happen if firebase_uid is correctly stored
            print(f"Warning: Firebase user not found for UID {db_user.firebase_uid}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Firebase error during verification check: {e}")

    # Create JWT for your API
    access_token = create_access_token(data={"sub": db_user.email})
    firebase_token = firebase_auth.create_custom_token(db_user.firebase_uid)
    return {

        "firebase_token": firebase_token.decode('utf-8'),
        "jwt_token": access_token,
        "token_type": "bearer"
    }


# -------------------
# RESEND VERIFICATION EMAIL
# -------------------
@router.post("/resend-verification-email")
def resend_verification_email(request: ResendVerificationRequest, db: Session = Depends(get_db_session)):
    db_user = get_user_by_email(db, request.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not db_user.firebase_uid:
        raise HTTPException(status_code=400, detail="User not linked to Firebase for verification.")

    try:
        firebase_user = firebase_auth.get_user(db_user.firebase_uid)
        if firebase_user.email_verified:
            raise HTTPException(status_code=400, detail="Email already verified.")

        verification_link = firebase_auth.generate_email_verification_link(request.email)
        send_verification_email.delay(request.email, verification_link)
        return {"message": "Verification email sent successfully."}
    except firebase_exceptions.NotFoundError:
        raise HTTPException(status_code=404, detail="Firebase user not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to send verification email: {e}")


# -------------------
# CURRENT USER
# -------------------
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
