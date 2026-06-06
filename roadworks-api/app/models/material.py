from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    material_code = Column(String(30), unique=True, nullable=False, index=True)
    material_name = Column(String(255), nullable=False)
    unit = Column(String(30), nullable=False)  # kg, ton, litre, bag, cubic_meter, etc.
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    stock_entries = relationship("MaterialStock", back_populates="material", lazy="dynamic")
    transactions = relationship("MaterialTransaction", back_populates="material", lazy="dynamic")

    def __repr__(self):
        return f"<Material id={self.id} code={self.material_code} name={self.material_name}>"
