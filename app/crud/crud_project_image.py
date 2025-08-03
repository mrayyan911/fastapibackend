from sqlalchemy.orm import Session
from app.models.models import ProjectImage
from app.schemas.schemas import ProjectImageCreate


def get_project_image(db: Session, image_id: int):
    """Retrieve a single project image by ID."""
    return db.query(ProjectImage).filter(ProjectImage.id == image_id).first()


def get_project_images(db: Session, project_id: int, skip: int = 0, limit: int = 10):
    """Retrieve a list of images for a specific project."""
    return db.query(ProjectImage).filter(ProjectImage.project_id == project_id).offset(skip).limit(limit).all()


def create_project_image(db: Session, image: ProjectImageCreate):
    """Create a new project image record."""
    db_image = ProjectImage(**image.model_dump())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_project_image(db: Session, image_id: int):
    """Delete a project image record."""
    db_image = db.query(ProjectImage).filter(ProjectImage.id == image_id).first()
    if db_image:
        db.delete(db_image)
        db.commit()
        return True
    return False
