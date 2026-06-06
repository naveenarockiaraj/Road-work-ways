from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
import enum


class AttendanceStatus(str, enum.Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    HALF_DAY = "HALF_DAY"
    LEAVE = "LEAVE"
    HOLIDAY = "HOLIDAY"


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)
    attendance_date = Column(Date, nullable=False, index=True)
    status = Column(
        SAEnum(AttendanceStatus, name="attendance_status_enum", values_callable=lambda x: [e.value for e in x]),
        default=AttendanceStatus.PRESENT,
        nullable=False,
    )
    working_hours = Column(Numeric(4, 2), nullable=True, default=8.0)
    remarks = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="attendance_records")
    project = relationship("Project", back_populates="attendance_records")

    def __repr__(self):
        return f"<Attendance employee_id={self.employee_id} date={self.attendance_date} status={self.status}>"
