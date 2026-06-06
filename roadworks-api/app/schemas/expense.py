from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.expense import ExpenseCategory


class ExpenseCreate(BaseModel):
    project_id: int
    expense_category: ExpenseCategory
    amount: Decimal = Field(..., gt=0)
    expense_date: date
    remarks: Optional[str] = Field(None, max_length=500)


class ExpenseUpdate(BaseModel):
    expense_category: Optional[ExpenseCategory] = None
    amount: Optional[Decimal] = Field(None, gt=0)
    expense_date: Optional[date] = None
    remarks: Optional[str] = Field(None, max_length=500)


class ExpenseResponse(BaseModel):
    id: int
    project_id: int
    expense_category: ExpenseCategory
    amount: Decimal
    expense_date: date
    remarks: Optional[str]
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
