from sqlalchemy.orm import Session
from app.models.models import Project
from app.schemas.schemas import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int):
    """Retrieve a single project by ID."""
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve a list of projects."""
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: ProjectCreate):
    """Create a new project."""
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: ProjectUpdate):
    """Update an existing project with partial fields."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        return None

    update_data = project.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    """Delete a project."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
        return True
    return False
