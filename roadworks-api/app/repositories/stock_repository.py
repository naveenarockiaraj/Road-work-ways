from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models.material_stock import MaterialStock
from app.models.material_transaction import MaterialTransaction, TransactionType
from app.models.material import Material
from app.schemas.stock import StockUpdate, MaterialTransactionCreate
from decimal import Decimal


class StockRepository:
    def get_stock(self, db: Session, material_id: int, project_id: int) -> Optional[MaterialStock]:
        return db.query(MaterialStock).filter(
            and_(MaterialStock.material_id == material_id, MaterialStock.project_id == project_id)
        ).first()

    def get_stock_by_id(self, db: Session, stock_id: int) -> Optional[MaterialStock]:
        return db.query(MaterialStock).filter(MaterialStock.id == stock_id).first()

    def get_project_stocks(self, db: Session, project_id: int) -> List[MaterialStock]:
        return (
            db.query(MaterialStock)
            .options(joinedload(MaterialStock.material))
            .filter(MaterialStock.project_id == project_id)
            .all()
        )

    def get_low_stocks(self, db: Session) -> List[MaterialStock]:
        return (
            db.query(MaterialStock)
            .options(joinedload(MaterialStock.material))
            .filter(MaterialStock.quantity_available <= MaterialStock.minimum_stock)
            .all()
        )

    def upsert_stock(
        self, db: Session, material_id: int, project_id: int, qty_delta: Decimal
    ) -> MaterialStock:
        stock = self.get_stock(db, material_id, project_id)
        if stock:
            stock.quantity_available = max(Decimal("0"), stock.quantity_available + qty_delta)
        else:
            stock = MaterialStock(
                material_id=material_id,
                project_id=project_id,
                quantity_available=max(Decimal("0"), qty_delta),
                minimum_stock=Decimal("0"),
            )
            db.add(stock)
        db.commit()
        db.refresh(stock)
        return stock

    def create_transaction(
        self, db: Session, payload: MaterialTransactionCreate, created_by: int
    ) -> MaterialTransaction:
        txn = MaterialTransaction(
            **payload.model_dump(),
            created_by=created_by,
        )
        db.add(txn)
        db.commit()
        db.refresh(txn)
        return txn

    def count_low_stock(self, db: Session) -> int:
        return db.query(MaterialStock).filter(
            MaterialStock.quantity_available <= MaterialStock.minimum_stock
        ).count()


stock_repository = StockRepository()
