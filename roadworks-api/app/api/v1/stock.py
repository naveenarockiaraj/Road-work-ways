from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.stock import MaterialTransactionCreate, MaterialTransactionResponse, StockWithMaterial
from app.services.stock_service import stock_service
from app.models.user import User
from typing import List

router = APIRouter()


@router.get("/project/{project_id}", response_model=List[StockWithMaterial])
def get_project_stocks(
    project_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Get all material stocks for a project."""
    return stock_service.get_project_stocks(db, project_id)


@router.get("/low-stock", response_model=List[StockWithMaterial])
def get_low_stocks(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Get all materials that are below minimum stock level."""
    return stock_service.get_low_stocks(db)


@router.post("/transaction", response_model=MaterialTransactionResponse, status_code=status.HTTP_201_CREATED)
def record_transaction(
    payload: MaterialTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record a material inward/outward/return transaction and update stock."""
    return stock_service.record_transaction(db, payload, current_user.id)
