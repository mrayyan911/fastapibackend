from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine

def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables uncommenting the next line
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
