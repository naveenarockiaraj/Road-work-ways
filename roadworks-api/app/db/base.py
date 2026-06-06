# Re-export Base from base_class for Alembic compatibility
from app.db.base_class import Base  # noqa: F401

# Import all models so Alembic can detect them
from app.models.user import User  # noqa
from app.models.employee import Employee  # noqa
from app.models.attendance import Attendance  # noqa
from app.models.employee_log import EmployeeLog  # noqa
from app.models.project import Project  # noqa
from app.models.material import Material  # noqa
from app.models.material_stock import MaterialStock  # noqa
from app.models.material_transaction import MaterialTransaction  # noqa
from app.models.vendor import Vendor  # noqa
from app.models.expense import Expense  # noqa
