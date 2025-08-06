from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ShowUser(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    firebase_uid: str | None = None

    class Config:
        from_attributes = True

class ResendVerificationRequest(BaseModel):
    email: EmailStr





class ProjectType(str, Enum):
    """
    Enum for project types.
    This can be extended to include more types as needed.
    """
    DETECTION = "detection"
    CLASSIFICATION = "classification"


class ProjectBase(BaseModel):
    """Common fields shared across all project schemas."""
    name: str
    annotation_group: Optional[str] = None
    license: str = "CC BY 4.0"
    type: ProjectType = ProjectType.DETECTION
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Fields required for creating a project."""
    user_id: int


class ProjectUpdate(BaseModel):
    """All fields optional for partial updates."""
    name: Optional[str] = None
    annotation_group: Optional[str] = None
    license: Optional[str] = None
    type: Optional[ProjectType] = None
    description: Optional[str] = None
    user_id: Optional[int] = None


class ProjectResponse(ProjectBase):
    """Response schema including ID and owner info."""
    id: int
    user_id: int

    class Config:
        from_attributes = True  # enables ORM compatibility (Pydantic v2)


class ProjectImageBase(BaseModel):
    """Common fields for project images."""
    download_url: str
    file_name: str
    firebase_path: str
    content_type: Optional[str] = None
    size: Optional[int] = None


class ProjectImageCreate(ProjectImageBase):
    """Fields required for creating a project image."""
    project_id: int


class ProjectImageResponse(ProjectImageBase):
    """Response schema for project images."""
    id: int
    project_id: int

    class Config:
        from_attributes = True
