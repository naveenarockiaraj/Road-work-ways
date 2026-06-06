from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services.employee_service import employee_service
from app.utils.pagination import PaginationParams, PaginatedResponse
from app.models.employee import EmployeeStatus
from app.models.user import User

router = APIRouter()


@router.get("", response_model=PaginatedResponse[EmployeeResponse])
def list_employees(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[EmployeeStatus] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return employee_service.list_employees(db, PaginationParams(page, size), search, status)


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return employee_service.create_employee(db, payload)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return employee_service.get_employee(db, employee_id)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return employee_service.update_employee(db, employee_id, payload)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    employee_service.delete_employee(db, employee_id)
