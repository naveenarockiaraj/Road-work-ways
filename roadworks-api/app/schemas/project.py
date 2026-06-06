from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.project import ProjectStatus, RoadType


class ProjectCreate(BaseModel):
    project_code: str = Field(..., min_length=2, max_length=30)
    project_name: str = Field(..., min_length=3, max_length=500)
    road_type: RoadType = RoadType.OTHER
    location: Optional[str] = Field(None, max_length=500)
    district: Optional[str] = Field(None, max_length=100)
    state: str = Field(default="India", max_length=100)
    contract_value: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: ProjectStatus = ProjectStatus.PLANNING


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = Field(None, min_length=3, max_length=500)
    road_type: Optional[RoadType] = None
    location: Optional[str] = Field(None, max_length=500)
    district: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    contract_value: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ProjectStatus] = None


class ProjectResponse(BaseModel):
    id: int
    project_code: str
    project_name: str
    road_type: RoadType
    location: Optional[str]
    district: Optional[str]
    state: str
    contract_value: Optional[Decimal]
    start_date: Optional[date]
    end_date: Optional[date]
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
