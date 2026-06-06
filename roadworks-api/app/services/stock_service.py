from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.repositories.stock_repository import stock_repository
from app.schemas.stock import (
    MaterialTransactionCreate,
    MaterialTransactionResponse,
    StockResponse,
    StockWithMaterial,
)
from app.models.material_transaction import TransactionType
from typing import List
from decimal import Decimal


class StockService:
    def get_project_stocks(self, db: Session, project_id: int) -> List[StockWithMaterial]:
        stocks = stock_repository.get_project_stocks(db, project_id)
        result = []
        for s in stocks:
            result.append(
                StockWithMaterial(
                    id=s.id,
                    material_id=s.material_id,
                    project_id=s.project_id,
                    quantity_available=s.quantity_available,
                    minimum_stock=s.minimum_stock,
                    last_updated=s.last_updated,
                    material_name=s.material.material_name,
                    material_code=s.material.material_code,
                    unit=s.material.unit,
                    is_low_stock=s.quantity_available <= s.minimum_stock,
                )
            )
        return result

    def get_low_stocks(self, db: Session) -> List[StockWithMaterial]:
        stocks = stock_repository.get_low_stocks(db)
        result = []
        for s in stocks:
            result.append(
                StockWithMaterial(
                    id=s.id,
                    material_id=s.material_id,
                    project_id=s.project_id,
                    quantity_available=s.quantity_available,
                    minimum_stock=s.minimum_stock,
                    last_updated=s.last_updated,
                    material_name=s.material.material_name,
                    material_code=s.material.material_code,
                    unit=s.material.unit,
                    is_low_stock=True,
                )
            )
        return result

    def record_transaction(
        self,
        db: Session,
        payload: MaterialTransactionCreate,
        created_by: int,
    ) -> MaterialTransactionResponse:
        # Determine stock delta based on transaction type
        if payload.transaction_type == TransactionType.INWARD:
            delta = payload.quantity
        elif payload.transaction_type in (TransactionType.OUTWARD, TransactionType.RETURN):
            delta = -payload.quantity
        else:  # ADJUSTMENT — can be positive or negative based on remarks
            delta = payload.quantity

        stock_repository.upsert_stock(db, payload.material_id, payload.project_id, delta)
        txn = stock_repository.create_transaction(db, payload, created_by)
        return MaterialTransactionResponse.model_validate(txn)


stock_service = StockService()
