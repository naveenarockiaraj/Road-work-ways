from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.material import MaterialCreate, MaterialUpdate, MaterialResponse
from app.services.material_service import material_service
from app.utils.pagination import PaginationParams, PaginatedResponse
from app.models.user import User

router = APIRouter()


@router.get("", response_model=PaginatedResponse[MaterialResponse])
def list_materials(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return material_service.list_materials(db, PaginationParams(page, size), search)


@router.post("", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
def create_material(
    payload: MaterialCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return material_service.create_material(db, payload)


@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(
    material_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return material_service.get_material(db, material_id)


@router.put("/{material_id}", response_model=MaterialResponse)
def update_material(
    material_id: int,
    payload: MaterialUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return material_service.update_material(db, material_id, payload)


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(
    material_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    material_service.delete_material(db, material_id)
