import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.base import Base
import os

#db connection variables
service_name = os.getenv("DB_SERVICE_NAME", "db")
port = os.getenv("DB_PORT", "5432")
username = os.getenv("POSTGRES_USER", "user")
password = os.getenv("POSTGRES_PASSWORD", "password")
database_name = os.getenv("POSTGRES_DB", "app")

# Construct the database URL
DATABASE_URL =  f"postgresql://{username}:{password}@{service_name}:{port}/{database_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
