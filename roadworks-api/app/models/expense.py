from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
import enum


class ExpenseCategory(str, enum.Enum):
    LABOUR = "LABOUR"
    MATERIAL = "MATERIAL"
    EQUIPMENT = "EQUIPMENT"
    FUEL = "FUEL"
    TRANSPORT = "TRANSPORT"
    MISCELLANEOUS = "MISCELLANEOUS"
    SUBCONTRACTOR = "SUBCONTRACTOR"
    SITE_EXPENSES = "SITE_EXPENSES"


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    expense_category = Column(
        SAEnum(ExpenseCategory, name="expense_category_enum", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    amount = Column(Numeric(12, 2), nullable=False)
    expense_date = Column(Date, nullable=False, index=True)
    remarks = Column(String(500), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="expenses")
