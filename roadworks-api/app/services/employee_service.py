from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ConflictException
from app.repositories.employee_repository import employee_repository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.models.employee import EmployeeStatus
from typing import Optional, List
from app.utils.pagination import PaginatedResponse, PaginationParams


class EmployeeService:
    def list_employees(
        self,
        db: Session,
        params: PaginationParams,
        search: Optional[str] = None,
        status: Optional[EmployeeStatus] = None,
    ) -> PaginatedResponse[EmployeeResponse]:
        items, total = employee_repository.get_all(
            db, skip=params.skip, limit=params.limit, search=search, status=status
        )
        return PaginatedResponse(
            items=[EmployeeResponse.model_validate(e) for e in items],
            total=total,
            page=params.page,
            size=params.limit,
        )

    def get_employee(self, db: Session, employee_id: int) -> EmployeeResponse:
        employee = employee_repository.get_by_id(db, employee_id)
        if not employee:
            raise NotFoundException("Employee", str(employee_id))
        return EmployeeResponse.model_validate(employee)

    def create_employee(self, db: Session, payload: EmployeeCreate) -> EmployeeResponse:
        if employee_repository.get_by_code(db, payload.employee_code):
            raise ConflictException(f"Employee with code '{payload.employee_code}' already exists")
        employee = employee_repository.create(db, payload)
        return EmployeeResponse.model_validate(employee)

    def update_employee(
        self, db: Session, employee_id: int, payload: EmployeeUpdate
    ) -> EmployeeResponse:
        employee = employee_repository.get_by_id(db, employee_id)
        if not employee:
            raise NotFoundException("Employee", str(employee_id))
        employee = employee_repository.update(db, employee, payload)
        return EmployeeResponse.model_validate(employee)

    def delete_employee(self, db: Session, employee_id: int) -> None:
        employee = employee_repository.get_by_id(db, employee_id)
        if not employee:
            raise NotFoundException("Employee", str(employee_id))
        employee_repository.delete(db, employee)


employee_service = EmployeeService()
