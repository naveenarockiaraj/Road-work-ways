from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
import enum


class TransactionType(str, enum.Enum):
    INWARD = "INWARD"
    OUTWARD = "OUTWARD"
    RETURN = "RETURN"
    ADJUSTMENT = "ADJUSTMENT"


class MaterialTransaction(Base):
    __tablename__ = "material_transactions"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    transaction_type = Column(
        SAEnum(TransactionType, name="transaction_type_enum", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    quantity = Column(Numeric(12, 3), nullable=False)
    transaction_date = Column(Date, nullable=False, index=True)
    remarks = Column(String(500), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    material = relationship("Material", back_populates="transactions")
    project = relationship("Project", back_populates="material_transactions")
