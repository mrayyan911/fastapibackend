import os
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError, ProgrammingError, IntegrityError

from app.core.config import settings
from app.core.firebase import initialize_firebase
from app.db.session import engine
from app.db.base import Base
from app.api.v1.endpoints import auth, project, project_image
from sqlalchemy import text


def drop_tables_on_startup():
    if os.environ.get("DROP_TABLES_ON_STARTUP", "false").lower() == "true":
        try:
            Base.metadata.drop_all(bind=engine, checkfirst=True)
            
            # Drop ENUM types manually
            with engine.connect() as conn:
                conn.execute(text("DROP TYPE IF EXISTS projecttype CASCADE;"))
                conn.commit()
            
            print("🗑️ All tables and ENUM types dropped successfully.")
        except (OperationalError, ProgrammingError, IntegrityError) as e:
            print(f"⚠️ Skipping drop_all. Tables may not exist or DB not ready: {e}")


def create_tables_on_startup():
    """Create all tables during startup."""
    try:
        Base.metadata.create_all(bind=engine)
        print(" All tables created successfully.")
    except (OperationalError, ProgrammingError, IntegrityError) as e:
        print(f" Skipping init_db during startup. Tables may already exist or DB not ready: {e}")


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.on_event("startup")
def startup_event():
    """Initialize services and database tables on app startup."""
    initialize_firebase()
    drop_tables_on_startup()
    create_tables_on_startup()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


# Register API routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Auth"])
app.include_router(project.router, prefix=settings.API_V1_STR)
app.include_router(project_image.router, prefix=settings.API_V1_STR)
