from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Boolean, Text,Enum
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship
from app.schemas.schemas import ProjectType

class User(Base):
    """
    SQLAlchemy model for a User.
    Each user can have multiple projects.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)  
    is_admin = Column(Boolean, default=False)
    firebase_uid = Column(String, unique=True, index=True, nullable=True)
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"



class Project(Base):
    """
    SQLAlchemy model for a Project.
    Each project belongs to one user.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    annotation_group = Column(String, nullable=True)
    license = Column(String, default="CC BY 4.0") 
    type =  Column(Enum(ProjectType), default=ProjectType.DETECTION, nullable=False)
    description = Column(Text, nullable=True)

 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


    owner = relationship("User", back_populates="projects")
    images = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', user_id={self.user_id})>"

class ProjectImage(Base):
    """
    SQLAlchemy model for Project Images.
    Each image is related to a Project and stores metadata of the image uploaded to Firebase.
    """
    __tablename__ = "project_images"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Firebase metadata
    file_name = Column(String, nullable=False)
    firebase_path = Column(String, nullable=False)  # e.g., "images/project1/image1.png"
    download_url = Column(Text, nullable=False)  # Public or token-based download URL from Firebase
    content_type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)  # in bytes

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    project = relationship("Project", back_populates="images")

    def __repr__(self):
        return f"<ProjectImage(id={self.id}, file_name='{self.file_name}', project_id={self.project_id})>"

