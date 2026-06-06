from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
import enum


class ProjectStatus(str, enum.Enum):
    PLANNING = "PLANNING"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class RoadType(str, enum.Enum):
    NATIONAL_HIGHWAY = "NATIONAL_HIGHWAY"
    STATE_HIGHWAY = "STATE_HIGHWAY"
    DISTRICT_ROAD = "DISTRICT_ROAD"
    RURAL_ROAD = "RURAL_ROAD"
    URBAN_ROAD = "URBAN_ROAD"
    OTHER = "OTHER"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(30), unique=True, nullable=False, index=True)
    project_name = Column(String(500), nullable=False)
    road_type = Column(
        SAEnum(RoadType, name="road_type_enum", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=RoadType.OTHER,
    )
    location = Column(String(500), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=False, default="India")
    contract_value = Column(Numeric(15, 2), nullable=True, default=0)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(
        SAEnum(ProjectStatus, name="project_status_enum", values_callable=lambda x: [e.value for e in x]),
        default=ProjectStatus.PLANNING,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    attendance_records = relationship("Attendance", back_populates="project", lazy="dynamic")
    employee_logs = relationship("EmployeeLog", back_populates="project", lazy="dynamic")
    material_stocks = relationship("MaterialStock", back_populates="project", lazy="dynamic")
    material_transactions = relationship("MaterialTransaction", back_populates="project", lazy="dynamic")
    expenses = relationship("Expense", back_populates="project", lazy="dynamic")

    def __repr__(self):
        return f"<Project id={self.id} code={self.project_code} name={self.project_name}>"
