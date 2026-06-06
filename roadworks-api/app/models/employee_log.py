from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class EmployeeLog(Base):
    __tablename__ = "employee_logs"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    log_date = Column(Date, nullable=False, index=True)
    task_description = Column(String(1000), nullable=False)
    hours_worked = Column(Numeric(4, 2), nullable=False, default=8.0)
    remarks = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="logs")
    project = relationship("Project", back_populates="employee_logs")
