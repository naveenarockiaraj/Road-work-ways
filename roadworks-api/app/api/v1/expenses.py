from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.services.expense_service import expense_service
from app.utils.pagination import PaginationParams, PaginatedResponse
from app.models.expense import ExpenseCategory
from app.models.user import User

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ExpenseResponse])
def list_expenses(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    project_id: Optional[int] = Query(None),
    category: Optional[ExpenseCategory] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return expense_service.list_expenses(
        db, PaginationParams(page, size), project_id, category, from_date, to_date
    )


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return expense_service.create_expense(db, payload, current_user.id)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return expense_service.get_expense(db, expense_id)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return expense_service.update_expense(db, expense_id, payload)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    expense_service.delete_expense(db, expense_id)
