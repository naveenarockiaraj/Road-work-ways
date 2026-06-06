# Road Work Ways

A production-ready full-stack web application for Indian road construction contractors to manage employees, projects, materials, stock, expenses, attendance, and daily work logs.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, MUI, React Router, Axios, React Hook Form |
| Backend | Node.js, Express.js, JWT, bcrypt |
| Database | PostgreSQL |

## Repository Structure

```
Road-work-ways/
+-- roadworks-web/     # React frontend
+-- roadworks-api/     # Node.js + Express backend
+-- roadworks-db/      # PostgreSQL schema & seed scripts
+-- docs/              # Documentation
+-- deployment/        # Docker & deployment configs
+-- README.md
+-- .gitignore
```

## Quick Start

### Prerequisites
- Node.js 18+
- PostgreSQL 14+
- npm or yarn

### 1. Database Setup
```bash
cd roadworks-db
psql -U postgres -f schema.sql
psql -U postgres -d roadworks_db -f seed.sql
```

### 2. Backend Setup
```bash
cd roadworks-api
npm install
cp .env.example .env
npm run dev
```

### 3. Frontend Setup
```bash
cd roadworks-web
npm install
cp .env.example .env
npm run dev
```

## Modules

- **Authentication** — JWT login, role-based access
- **Employees** — Profile, daily wage, Aadhaar, designation
- **Attendance** — Daily entry per project, working hours
- **Projects** — Road construction project lifecycle
- **Materials** — Stock tracking, inward/outward transactions
- **Expenses** — Category-wise expense entry and reporting
- **Vendors** — Supplier management with GST details
- **Reports** — Daily, monthly, attendance, stock, expense reports
- **Dashboard** — KPI cards, stock alerts, activity feed

## Default Login (after seed)

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@roadworks.in | Admin@123 |

## License
MIT
