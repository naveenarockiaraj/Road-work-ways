from fastapi import APIRouter
from app.api.v1 import auth, employees, attendance, projects, materials, stock, vendors, expenses, reports

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
api_router.include_router(employees.router, prefix="/v1/employees", tags=["Employees"])
api_router.include_router(attendance.router, prefix="/v1/attendance", tags=["Attendance"])
api_router.include_router(projects.router, prefix="/v1/projects", tags=["Projects"])
api_router.include_router(materials.router, prefix="/v1/materials", tags=["Materials"])
api_router.include_router(stock.router, prefix="/v1/stock", tags=["Stock"])
api_router.include_router(vendors.router, prefix="/v1/vendors", tags=["Vendors"])
api_router.include_router(expenses.router, prefix="/v1/expenses", tags=["Expenses"])
api_router.include_router(reports.router, prefix="/v1/reports", tags=["Reports"])
