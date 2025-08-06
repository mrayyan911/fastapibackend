from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db_session
from app.schemas.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.crud.crud_project import get_project, get_projects, create_project, update_project, delete_project

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectResponse])
def list_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    """Retrieve all projects (paginated)."""
    return get_projects(db, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db_session)):
    """Retrieve a single project by ID."""
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_new_project(project: ProjectCreate, db: Session = Depends(get_db_session)):
    """Create a new project."""
    return create_project(db, project)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_existing_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db_session)):
    """Update an existing project."""
    updated_project = update_project(db, project_id, project)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project


@router.delete("/{project_id}", status_code=204)
def remove_project(project_id: int, db: Session = Depends(get_db_session)):
    """Delete a project by ID."""
    success = delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
