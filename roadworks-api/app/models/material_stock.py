from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class MaterialStock(Base):
    __tablename__ = "material_stock"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    quantity_available = Column(Numeric(12, 3), nullable=False, default=0)
    minimum_stock = Column(Numeric(12, 3), nullable=False, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    material = relationship("Material", back_populates="stock_entries")
    project = relationship("Project", back_populates="material_stocks")
