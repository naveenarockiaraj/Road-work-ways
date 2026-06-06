from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from app.services.vendor_service import vendor_service
from app.utils.pagination import PaginationParams, PaginatedResponse
from app.models.user import User

router = APIRouter()


@router.get("", response_model=PaginatedResponse[VendorResponse])
def list_vendors(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return vendor_service.list_vendors(db, PaginationParams(page, size), search)


@router.post("", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
def create_vendor(
    payload: VendorCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return vendor_service.create_vendor(db, payload)


@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return vendor_service.get_vendor(db, vendor_id)


@router.put("/{vendor_id}", response_model=VendorResponse)
def update_vendor(
    vendor_id: int,
    payload: VendorUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return vendor_service.update_vendor(db, vendor_id, payload)


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    vendor_service.delete_vendor(db, vendor_id)
