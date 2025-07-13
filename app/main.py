import os
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.db.init_db import init_db
from app.api.v1.endpoints import auth

# Check for an environment variable to drop tables
if os.environ.get("DROP_TABLES_ON_STARTUP", "false").lower() == "true":
    Base.metadata.drop_all(bind=engine)

init_db(None) # Call init_db to create tables

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

app.include_router(auth.router, prefix=settings.API_V1_STR)