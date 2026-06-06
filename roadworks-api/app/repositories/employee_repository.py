from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.employee import Employee, EmployeeStatus
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository:
    def get_by_id(self, db: Session, employee_id: int) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.id == employee_id).first()

    def get_by_code(self, db: Session, code: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.employee_code == code).first()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        status: Optional[EmployeeStatus] = None,
    ) -> Tuple[List[Employee], int]:
        query = db.query(Employee)
        if search:
            query = query.filter(
                or_(
                    Employee.full_name.ilike(f"%{search}%"),
                    Employee.employee_code.ilike(f"%{search}%"),
                    Employee.mobile_number.ilike(f"%{search}%"),
                    Employee.designation.ilike(f"%{search}%"),
                )
            )
        if status:
            query = query.filter(Employee.status == status)
        total = query.count()
        items = query.order_by(Employee.employee_code).offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, payload: EmployeeCreate) -> Employee:
        employee = Employee(**payload.model_dump())
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee

    def update(self, db: Session, employee: Employee, payload: EmployeeUpdate) -> Employee:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(employee, field, value)
        db.commit()
        db.refresh(employee)
        return employee

    def delete(self, db: Session, employee: Employee) -> None:
        db.delete(employee)
        db.commit()

    def count_active(self, db: Session) -> int:
        return db.query(Employee).filter(Employee.status == EmployeeStatus.ACTIVE).count()


employee_repository = EmployeeRepository()
