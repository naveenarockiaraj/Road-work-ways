from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VendorCreate(BaseModel):
    vendor_name: str = Field(..., min_length=2, max_length=255)
    contact_person: Optional[str] = Field(None, max_length=255)
    mobile_number: Optional[str] = Field(None, min_length=10, max_length=15)
    gst_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)


class VendorUpdate(BaseModel):
    vendor_name: Optional[str] = Field(None, min_length=2, max_length=255)
    contact_person: Optional[str] = Field(None, max_length=255)
    mobile_number: Optional[str] = Field(None, min_length=10, max_length=15)
    gst_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)


class VendorResponse(BaseModel):
    id: int
    vendor_name: str
    contact_person: Optional[str]
    mobile_number: Optional[str]
    gst_number: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
