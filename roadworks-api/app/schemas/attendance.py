from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.attendance import AttendanceStatus


class AttendanceCreate(BaseModel):
    employee_id: int
    project_id: Optional[int] = None
    attendance_date: date
    status: AttendanceStatus = AttendanceStatus.PRESENT
    working_hours: Optional[Decimal] = Field(None, ge=0, le=24)
    remarks: Optional[str] = Field(None, max_length=500)


class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None
    working_hours: Optional[Decimal] = Field(None, ge=0, le=24)
    remarks: Optional[str] = Field(None, max_length=500)


class AttendanceBulkCreate(BaseModel):
    project_id: Optional[int] = None
    attendance_date: date
    entries: list[AttendanceCreate]


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    project_id: Optional[int]
    attendance_date: date
    status: AttendanceStatus
    working_hours: Optional[Decimal]
    remarks: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
