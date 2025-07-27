# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER','user')}:"
    f"{os.getenv('POSTGRES_PASSWORD','password')}@"
    f"{os.getenv('DB_SERVICE_NAME','db')}:"
    f"{os.getenv('DB_PORT','5432')}/"
    f"{os.getenv('POSTGRES_DB','app')}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_session():
    try:
        db = SessionLocal()  
        yield db
    finally:
        db.close()