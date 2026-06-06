from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base_class import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(255), nullable=False, index=True)
    contact_person = Column(String(255), nullable=True)
    mobile_number = Column(String(15), nullable=True)
    gst_number = Column(String(20), nullable=True, unique=True)
    address = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Vendor id={self.id} name={self.vendor_name}>"
