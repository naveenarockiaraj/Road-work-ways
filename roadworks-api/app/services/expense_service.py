from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.repositories.expense_repository import expense_repository
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.models.expense import ExpenseCategory
from typing import Optional
from datetime import date
from app.utils.pagination import PaginatedResponse, PaginationParams


class ExpenseService:
    def list_expenses(
        self,
        db: Session,
        params: PaginationParams,
        project_id: Optional[int] = None,
        category: Optional[ExpenseCategory] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> PaginatedResponse[ExpenseResponse]:
        items, total = expense_repository.get_all(
            db,
            skip=params.skip,
            limit=params.limit,
            project_id=project_id,
            category=category,
            from_date=from_date,
            to_date=to_date,
        )
        return PaginatedResponse(
            items=[ExpenseResponse.model_validate(e) for e in items],
            total=total,
            page=params.page,
            size=params.limit,
        )

    def get_expense(self, db: Session, expense_id: int) -> ExpenseResponse:
        expense = expense_repository.get_by_id(db, expense_id)
        if not expense:
            raise NotFoundException("Expense", str(expense_id))
        return ExpenseResponse.model_validate(expense)

    def create_expense(
        self, db: Session, payload: ExpenseCreate, created_by: int
    ) -> ExpenseResponse:
        expense = expense_repository.create(db, payload, created_by)
        return ExpenseResponse.model_validate(expense)

    def update_expense(
        self, db: Session, expense_id: int, payload: ExpenseUpdate
    ) -> ExpenseResponse:
        expense = expense_repository.get_by_id(db, expense_id)
        if not expense:
            raise NotFoundException("Expense", str(expense_id))
        expense = expense_repository.update(db, expense, payload)
        return ExpenseResponse.model_validate(expense)

    def delete_expense(self, db: Session, expense_id: int) -> None:
        expense = expense_repository.get_by_id(db, expense_id)
        if not expense:
            raise NotFoundException("Expense", str(expense_id))
        expense_repository.delete(db, expense)


expense_service = ExpenseService()
