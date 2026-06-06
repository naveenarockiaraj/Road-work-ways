# Setup Guide

## Prerequisites

| Tool       | Min Version | Install                |
| ---------- | ----------- | ---------------------- |
| Python     | 3.11+       | https://python.org     |
| Node.js    | 18+         | https://nodejs.org     |
| PostgreSQL | 15+         | https://postgresql.org |
| Git        | any         | https://git-scm.com    |

---

## 1. Clone & structure

```bash
git clone <repo-url>
cd Road-work-ways
```

```
Road-work-ways/
├── roadworks-api/    # FastAPI backend
├── roadworks-web/    # React frontend
├── roadworks-db/     # SQL init & seed scripts
└── deployment/       # Docker Compose & Dockerfiles
```

---

## 2. Database

```bash
# Start PostgreSQL, then:
psql -U postgres -f roadworks-db/init.sql

# Verify
psql -U postgres -c "\l" | grep roadworks
```

---

## 3. Backend

```bash
cd roadworks-api

# Virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

# Environment
cp .env.example .env
# Edit .env — set DATABASE_URL and SECRET_KEY at minimum
```

**Minimum `.env` values:**

```env
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/roadworks_db
SECRET_KEY=your-random-32-char-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
FIRST_SUPERUSER_USERNAME=admin
FIRST_SUPERUSER_PASSWORD=Admin@123
FIRST_SUPERUSER_EMAIL=admin@roadworkways.com
```

```bash
# Run migrations (creates all tables + default admin user)
alembic upgrade head

# Optional: load demo data
psql -U postgres -d roadworks_db -f ../roadworks-db/seed.sql

# Start API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs  
Health check: http://localhost:8000/health

---

## 4. Frontend

```bash
cd roadworks-web

npm install

# Environment
cp .env.example .env.local
# .env.local contents:
# VITE_API_BASE_URL=http://localhost:8000

npm run dev
```

App: http://localhost:5173

**Default login:** `admin` / `Admin@123`

---

## 5. Docker (full stack)

```bash
cd deployment

# Build & start all services (postgres + api + web)
docker compose up --build

# First run only — run migrations inside the api container:
docker compose exec api alembic upgrade head

# Load seed data
docker compose exec api python -c "
from app.db.session import SessionLocal
from app.db.init_db import init_db
db = SessionLocal()
init_db(db)
"
```

| Service  | URL                        |
| -------- | -------------------------- |
| Web app  | http://localhost:3000      |
| API      | http://localhost:8000      |
| API docs | http://localhost:8000/docs |

---

## 6. Creating a new migration

After editing any SQLAlchemy model:

```bash
cd roadworks-api
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

---

## 7. Common issues

| Problem                  | Fix                                                              |
| ------------------------ | ---------------------------------------------------------------- |
| `psycopg2` install error | Install `libpq-dev` (Linux) or PostgreSQL client tools (Windows) |
| `alembic upgrade` fails  | Check `DATABASE_URL` in `.env`                                   |
| CORS error in browser    | Add `http://localhost:5173` to `BACKEND_CORS_ORIGINS` in `.env`  |
| 401 on all API calls     | Token expired — log out and log back in                          |
| Node version warning     | Upgrade Node to 18+ (Vite 5 requires it)                         |
