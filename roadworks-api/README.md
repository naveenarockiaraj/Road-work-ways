# roadworks-api

FastAPI backend for the Road Work Ways contractor management system.

---

## Prerequisites

| Tool       | Version | Check              |
| ---------- | ------- | ------------------ |
| Python     | 3.11+   | `python --version` |
| PostgreSQL | 15+     | `psql --version`   |
| pip        | any     | `pip --version`    |

---

## 1. Create the database

```bash
# Connect to postgres as superuser
psql -U postgres

# Inside psql:
CREATE DATABASE roadworks_db;
\q
```

---

## 2. Set up Python environment

```bash
cd roadworks-api

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate          # Windows PowerShell
# source .venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

---

## 3. Configure environment

The `.env` file is already present with defaults. Edit it if your PostgreSQL
password or port is different:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/roadworks_db
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
PROJECT_NAME=Road Work Ways
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
FIRST_SUPERUSER_USERNAME=admin
FIRST_SUPERUSER_EMAIL=admin@roadworkways.in
FIRST_SUPERUSER_PASSWORD=Admin@123456
```

---

## 4. Run database migrations

```bash
# From inside roadworks-api/ with venv active
alembic upgrade head
```

This creates all tables and seeds the default admin user.

---

## 5. Start the API server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is now running at **http://localhost:8000**

---

## 6. Test APIs with Swagger UI

FastAPI auto-generates interactive API docs. Open in your browser:

| URL                                 | Description                              |
| ----------------------------------- | ---------------------------------------- |
| **http://localhost:8000/api/docs**  | Swagger UI — try endpoints interactively |
| **http://localhost:8000/api/redoc** | ReDoc — clean reference docs             |
| **http://localhost:8000/health**    | Health check endpoint                    |

### How to use Swagger UI

1. Open **http://localhost:8000/api/docs**
2. Click **POST /api/v1/auth/login**
3. Click **Try it out**
4. Enter credentials:
   ```json
   {
     "username": "admin",
     "password": "Admin@123456"
   }
   ```
5. Click **Execute** — copy the `access_token` from the response
6. Click the **Authorize 🔒** button at the top of the page
7. Enter: `Bearer <paste-token-here>`
8. Click **Authorize** — now all protected endpoints are unlocked
9. Try any endpoint — click it → **Try it out** → **Execute**

---

## Available endpoints (summary)

| Group      | Base path             |
| ---------- | --------------------- |
| Auth       | `/api/v1/auth/`       |
| Users      | `/api/v1/users/`      |
| Employees  | `/api/v1/employees/`  |
| Projects   | `/api/v1/projects/`   |
| Attendance | `/api/v1/attendance/` |
| Materials  | `/api/v1/materials/`  |
| Stock      | `/api/v1/stock/`      |
| Vendors    | `/api/v1/vendors/`    |
| Expenses   | `/api/v1/expenses/`   |
| Reports    | `/api/v1/reports/`    |

---

## Common commands

```bash
# Create a new migration after editing a model
alembic revision --autogenerate -m "describe change"
alembic upgrade head

# Roll back last migration
alembic downgrade -1

# Check current migration version
alembic current
```

---

## Troubleshooting

| Problem                          | Fix                                                      |
| -------------------------------- | -------------------------------------------------------- |
| `psycopg2` install fails         | Run `pip install psycopg2-binary` instead                |
| `alembic upgrade` fails          | Check `DATABASE_URL` in `.env`, confirm DB exists        |
| Port 8000 already in use         | Run with `--port 8001` and update `BACKEND_CORS_ORIGINS` |
| 401 Unauthorized on all requests | Follow Swagger Authorize steps above                     |
