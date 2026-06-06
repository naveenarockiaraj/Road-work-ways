from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import date
from app.models.expense import Expense, ExpenseCategory
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from decimal import Decimal


class ExpenseRepository:
    def get_by_id(self, db: Session, expense_id: int) -> Optional[Expense]:
        return db.query(Expense).filter(Expense.id == expense_id).first()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        project_id: Optional[int] = None,
        category: Optional[ExpenseCategory] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> Tuple[List[Expense], int]:
        query = db.query(Expense)
        if project_id:
            query = query.filter(Expense.project_id == project_id)
        if category:
            query = query.filter(Expense.expense_category == category)
        if from_date:
            query = query.filter(Expense.expense_date >= from_date)
        if to_date:
            query = query.filter(Expense.expense_date <= to_date)
        total = query.count()
        items = query.order_by(Expense.expense_date.desc()).offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, payload: ExpenseCreate, created_by: int) -> Expense:
        expense = Expense(**payload.model_dump(), created_by=created_by)
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    def update(self, db: Session, expense: Expense, payload: ExpenseUpdate) -> Expense:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(expense, field, value)
        db.commit()
        db.refresh(expense)
        return expense

    def delete(self, db: Session, expense: Expense) -> None:
        db.delete(expense)
        db.commit()

    def get_total_for_date(self, db: Session, target_date: date) -> Decimal:
        result = db.query(func.sum(Expense.amount)).filter(
            Expense.expense_date == target_date
        ).scalar()
        return result or Decimal("0")

    def get_monthly_total(self, db: Session, year: int, month: int) -> Decimal:
        result = db.query(func.sum(Expense.amount)).filter(
            func.extract("year", Expense.expense_date) == year,
            func.extract("month", Expense.expense_date) == month,
        ).scalar()
        return result or Decimal("0")


expense_repository = ExpenseRepository()
