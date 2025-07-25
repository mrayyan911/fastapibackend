import os
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.api.v1.endpoints import auth
from db.session import SessionLocal
from sqlalchemy.exc import OperationalError
# Check for an environment variable to drop tables
if os.environ.get("DROP_TABLES_ON_STARTUP", "false").lower() == "true":
    Base.metadata.drop_all(bind=engine)





app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
def startup_event():

    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        print(f"⚠️ Skipping init_db during startup. DB may not be ready: {e}")




@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

app.include_router(auth.router, prefix=settings.API_V1_STR)