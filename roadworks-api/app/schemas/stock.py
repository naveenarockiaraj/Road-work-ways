from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.material_transaction import TransactionType


class StockUpdate(BaseModel):
    quantity_available: Decimal = Field(..., ge=0)
    minimum_stock: Optional[Decimal] = Field(None, ge=0)


class StockResponse(BaseModel):
    id: int
    material_id: int
    project_id: int
    quantity_available: Decimal
    minimum_stock: Decimal
    last_updated: datetime

    model_config = {"from_attributes": True}


class StockWithMaterial(StockResponse):
    material_name: str
    material_code: str
    unit: str
    is_low_stock: bool

    model_config = {"from_attributes": True}


class MaterialTransactionCreate(BaseModel):
    material_id: int
    project_id: int
    transaction_type: TransactionType
    quantity: Decimal = Field(..., gt=0)
    transaction_date: date
    remarks: Optional[str] = Field(None, max_length=500)


class MaterialTransactionResponse(BaseModel):
    id: int
    material_id: int
    project_id: int
    transaction_type: TransactionType
    quantity: Decimal
    transaction_date: date
    remarks: Optional[str]
    created_by: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}
