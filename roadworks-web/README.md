# roadworks-web

React + TypeScript frontend for the Road Work Ways contractor management system.

---

## Prerequisites

| Tool    | Version | Check            |
| ------- | ------- | ---------------- |
| Node.js | **18+** | `node --version` |
| npm     | 9+      | `npm --version`  |

> **Important:** Node 16 will not work. Vite 5 requires Node 18+.  
> Install: `winget install OpenJS.NodeJS.LTS` (Windows) or https://nodejs.org

---

## 1. Install dependencies

```bash
cd roadworks-web
npm install
```

---

## 2. Configure environment

```bash
# Copy the example file
copy .env.example .env.local   # Windows
# cp .env.example .env.local   # macOS / Linux
```

`.env.local` contents — update only if your API runs on a different port:

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 3. Start the development server

> The backend API must be running first (see `roadworks-api/README.md`)

```bash
npm run dev
```

The app opens at **http://localhost:5173**

---

## 4. Log in

| Field    | Value          |
| -------- | -------------- |
| Username | `admin`        |
| Password | `Admin@123456` |

---

## Available pages

| Page           | URL path           |
| -------------- | ------------------ |
| Login          | `/login`           |
| Dashboard      | `/dashboard`       |
| Employees      | `/employees`       |
| Projects       | `/projects`        |
| Attendance     | `/attendance`      |
| Materials      | `/materials`       |
| Material Stock | `/materials/stock` |
| Vendors        | `/vendors`         |
| Expenses       | `/expenses`        |
| Reports        | `/reports`         |

---

## Other commands

```bash
# Type-check without building
npm run type-check

# Lint
npm run lint

# Production build (outputs to dist/)
npm run build

# Preview the production build locally
npm run preview
```

---

## Project structure

```
src/
├── app/            # Router, theme, providers, query client
├── features/       # One folder per feature (auth, employees, projects …)
│   └── <feature>/
│       ├── services/     # API calls
│       ├── queries/      # TanStack Query read hooks
│       ├── mutations/    # TanStack Query write hooks
│       ├── pages/        # Route-level components
│       └── components/   # Feature-specific UI components
└── shared/         # Reusable across features
    ├── api/        # Axios instance + token storage
    ├── components/ # Layout, tables, feedback components
    ├── constants/  # API endpoints, routes, roles
    ├── types/      # Common TypeScript types
    └── utils/      # formatCurrency, formatDate …
```

---

## Troubleshooting

| Problem                               | Fix                                                                 |
| ------------------------------------- | ------------------------------------------------------------------- |
| `npm run dev` fails with engine error | Upgrade Node to 18+                                                 |
| White screen / 401 errors             | Check backend is running on port 8000                               |
| CORS errors in browser                | Add `http://localhost:5173` to `BACKEND_CORS_ORIGINS` in API `.env` |
| Login fails                           | Run `alembic upgrade head`, then create the admin with `python -m app.cli.create_admin` |
