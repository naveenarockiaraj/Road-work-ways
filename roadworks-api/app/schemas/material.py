from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MaterialCreate(BaseModel):
    material_code: str = Field(..., min_length=2, max_length=30)
    material_name: str = Field(..., min_length=2, max_length=255)
    unit: str = Field(..., min_length=1, max_length=30)
    description: Optional[str] = Field(None, max_length=500)


class MaterialUpdate(BaseModel):
    material_name: Optional[str] = Field(None, min_length=2, max_length=255)
    unit: Optional[str] = Field(None, min_length=1, max_length=30)
    description: Optional[str] = Field(None, max_length=500)


class MaterialResponse(BaseModel):
    id: int
    material_code: str
    material_name: str
    unit: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
