from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db_session
from app.schemas.schemas import ProjectImageCreate, ProjectImageResponse
from app.crud.crud_project_image import get_project_image, get_project_images, create_project_image, delete_project_image

router = APIRouter(prefix="/project-images", tags=["Project Images"])


@router.get("/{project_id}", response_model=List[ProjectImageResponse])
def list_project_images(project_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """Retrieve all images for a specific project (paginated)."""
    return get_project_images(db, project_id=project_id, skip=skip, limit=limit)


@router.get("/{image_id}", response_model=ProjectImageResponse)
def read_project_image(image_id: int, db: Session = Depends(get_db_session)):
    """Retrieve a single project image by ID."""
    image = get_project_image(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Project image not found")
    return image


@router.post("/", response_model=ProjectImageResponse, status_code=201)
def create_new_project_image(image: ProjectImageCreate, db: Session = Depends(get_db_session)):
    """Create a new project image record."""
    return create_project_image(db, image)


@router.delete("/{image_id}", status_code=204)
def remove_project_image(image_id: int, db: Session = Depends(get_db_session)):
    """Delete a project image by ID."""
    success = delete_project_image(db, image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project image not found")
