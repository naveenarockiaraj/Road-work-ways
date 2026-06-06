from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
import enum


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    TERMINATED = "TERMINATED"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    mobile_number = Column(String(15), nullable=False)
    aadhaar_number = Column(String(12), unique=True, nullable=True)
    designation = Column(String(100), nullable=False)
    daily_wage = Column(Numeric(10, 2), nullable=False, default=0)
    address = Column(String(500), nullable=True)
    joining_date = Column(Date, nullable=False)
    status = Column(
        SAEnum(EmployeeStatus, name="employee_status_enum", values_callable=lambda x: [e.value for e in x]),
        default=EmployeeStatus.ACTIVE,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    attendance_records = relationship("Attendance", back_populates="employee", lazy="dynamic")
    logs = relationship("EmployeeLog", back_populates="employee", lazy="dynamic")

    def __repr__(self):
        return f"<Employee id={self.id} code={self.employee_code} name={self.full_name}>"
