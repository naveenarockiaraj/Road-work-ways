from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.employee import EmployeeStatus


class EmployeeCreate(BaseModel):
    employee_code: str = Field(..., min_length=2, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=255)
    mobile_number: str = Field(..., min_length=10, max_length=15)
    aadhaar_number: Optional[str] = Field(None, min_length=12, max_length=12)
    designation: str = Field(..., min_length=2, max_length=100)
    daily_wage: Decimal = Field(..., ge=0)
    address: Optional[str] = Field(None, max_length=500)
    joining_date: date
    status: EmployeeStatus = EmployeeStatus.ACTIVE


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    mobile_number: Optional[str] = Field(None, min_length=10, max_length=15)
    designation: Optional[str] = Field(None, min_length=2, max_length=100)
    daily_wage: Optional[Decimal] = Field(None, ge=0)
    address: Optional[str] = Field(None, max_length=500)
    status: Optional[EmployeeStatus] = None


class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    full_name: str
    mobile_number: str
    aadhaar_number: Optional[str]
    designation: str
    daily_wage: Decimal
    address: Optional[str]
    joining_date: date
    status: EmployeeStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
