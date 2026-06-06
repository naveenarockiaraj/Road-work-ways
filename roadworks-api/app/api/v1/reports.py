from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.attendance import Attendance, AttendanceStatus
from app.models.expense import Expense
from app.models.material_stock import MaterialStock
from app.models.project import Project, ProjectStatus
from app.models.employee import Employee, EmployeeStatus
from app.repositories.stock_repository import stock_repository
from app.repositories.expense_repository import expense_repository
from app.repositories.project_repository import project_repository
from app.repositories.employee_repository import employee_repository
from datetime import datetime

router = APIRouter()


@router.get("/dashboard")
def dashboard_summary(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Dashboard KPI summary."""
    today = date.today()
    now = datetime.utcnow()

    total_projects = project_repository.count_total(db)
    active_projects = project_repository.count_active(db)
    total_employees = employee_repository.count_active(db)

    today_attendance = db.query(Attendance).filter(
        Attendance.attendance_date == today,
        Attendance.status == AttendanceStatus.PRESENT,
    ).count()

    low_stock_count = stock_repository.count_low_stock(db)
    today_expenses = expense_repository.get_total_for_date(db, today)
    monthly_expenses = expense_repository.get_monthly_total(db, now.year, now.month)

    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "total_employees": total_employees,
        "today_attendance_count": today_attendance,
        "low_stock_materials": low_stock_count,
        "today_expenses": float(today_expenses),
        "monthly_expenses": float(monthly_expenses),
    }


@router.get("/daily")
def daily_report(
    report_date: Optional[date] = Query(None),
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Daily work report: attendance + expenses for a given date."""
    target_date = report_date or date.today()

    attendance_query = db.query(Attendance).filter(Attendance.attendance_date == target_date)
    if project_id:
        attendance_query = attendance_query.filter(Attendance.project_id == project_id)

    attendance_summary = {
        "present": attendance_query.filter(Attendance.status == AttendanceStatus.PRESENT).count(),
        "absent": attendance_query.filter(Attendance.status == AttendanceStatus.ABSENT).count(),
        "half_day": attendance_query.filter(Attendance.status == AttendanceStatus.HALF_DAY).count(),
        "leave": attendance_query.filter(Attendance.status == AttendanceStatus.LEAVE).count(),
        "total": attendance_query.count(),
    }

    expense_query = db.query(Expense).filter(Expense.expense_date == target_date)
    if project_id:
        expense_query = expense_query.filter(Expense.project_id == project_id)
    total_expense = expense_query.with_entities(func.sum(Expense.amount)).scalar() or 0

    return {
        "report_date": target_date,
        "project_id": project_id,
        "attendance": attendance_summary,
        "total_expenses": float(total_expense),
    }


@router.get("/monthly")
def monthly_report(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Monthly expenses breakdown by category."""
    query = db.query(
        Expense.expense_category,
        func.sum(Expense.amount).label("total"),
        func.count(Expense.id).label("count"),
    ).filter(
        func.extract("year", Expense.expense_date) == year,
        func.extract("month", Expense.expense_date) == month,
    )
    if project_id:
        query = query.filter(Expense.project_id == project_id)
    results = query.group_by(Expense.expense_category).all()

    breakdown = [
        {"category": r.expense_category, "total": float(r.total), "count": r.count}
        for r in results
    ]
    grand_total = sum(r["total"] for r in breakdown)

    return {
        "year": year,
        "month": month,
        "project_id": project_id,
        "breakdown": breakdown,
        "grand_total": grand_total,
    }


@router.get("/material-consumption")
def material_consumption_report(
    project_id: Optional[int] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Material consumption report per project."""
    from app.models.material_transaction import MaterialTransaction, TransactionType
    from app.models.material import Material

    query = (
        db.query(
            Material.material_name,
            Material.unit,
            func.sum(MaterialTransaction.quantity).label("total_used"),
        )
        .join(MaterialTransaction, Material.id == MaterialTransaction.material_id)
        .filter(MaterialTransaction.transaction_type == TransactionType.OUTWARD)
    )
    if project_id:
        query = query.filter(MaterialTransaction.project_id == project_id)
    if from_date:
        query = query.filter(MaterialTransaction.transaction_date >= from_date)
    if to_date:
        query = query.filter(MaterialTransaction.transaction_date <= to_date)
    results = query.group_by(Material.material_name, Material.unit).all()

    return {
        "project_id": project_id,
        "from_date": from_date,
        "to_date": to_date,
        "consumption": [
            {"material": r.material_name, "unit": r.unit, "total_used": float(r.total_used)}
            for r in results
        ],
    }
