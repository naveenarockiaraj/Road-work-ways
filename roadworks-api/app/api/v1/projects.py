from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import project_service
from app.utils.pagination import PaginationParams, PaginatedResponse
from app.models.project import ProjectStatus
from app.models.user import User

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ProjectResponse])
def list_projects(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[ProjectStatus] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return project_service.list_projects(db, PaginationParams(page, size), search, status)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return project_service.create_project(db, payload)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return project_service.get_project(db, project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return project_service.update_project(db, project_id, payload)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    project_service.delete_project(db, project_id)
