from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from app.models.attendance import Attendance, AttendanceStatus
from app.models.user import User
from app.utils.pagination import PaginationParams, PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[AttendanceResponse])
def list_attendance(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    employee_id: Optional[int] = Query(None),
    project_id: Optional[int] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    params = PaginationParams(page, size)
    query = db.query(Attendance)
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    if project_id:
        query = query.filter(Attendance.project_id == project_id)
    if from_date:
        query = query.filter(Attendance.attendance_date >= from_date)
    if to_date:
        query = query.filter(Attendance.attendance_date <= to_date)
    total = query.count()
    items = query.order_by(Attendance.attendance_date.desc()).offset(params.skip).limit(params.limit).all()
    return PaginatedResponse(
        items=[AttendanceResponse.model_validate(a) for a in items],
        total=total,
        page=params.page,
        size=params.limit,
    )


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    attendance = Attendance(**payload.model_dump())
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return AttendanceResponse.model_validate(attendance)


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    payload: AttendanceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("Attendance", str(attendance_id))
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(attendance, field, value)
    db.commit()
    db.refresh(attendance)
    return AttendanceResponse.model_validate(attendance)
