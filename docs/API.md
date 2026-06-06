# API Reference

Base URL: `http://localhost:8000/api/v1`

All endpoints except `/auth/login` require:

```
Authorization: Bearer <access_token>
```

---

## Authentication

### POST `/auth/login`

Login and receive an access token.

**Body:**

```json
{ "username": "admin", "password": "Admin@123" }
```

**Response:**

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { "id": 1, "username": "admin", "role": "SUPER_ADMIN" }
}
```

### GET `/auth/me`

Returns the current authenticated user.

---

## Users

| Method | Path          | Description            |
| ------ | ------------- | ---------------------- |
| GET    | `/users`      | List users (paginated) |
| POST   | `/users`      | Create user            |
| GET    | `/users/{id}` | Get user               |
| PUT    | `/users/{id}` | Update user            |
| DELETE | `/users/{id}` | Delete user            |

**Roles:** `SUPER_ADMIN`, `ADMIN`, `MANAGER`, `SUPERVISOR`, `VIEWER`

---

## Employees

| Method | Path              | Description                                     |
| ------ | ----------------- | ----------------------------------------------- |
| GET    | `/employees`      | List employees (`?search=&status=&page=&size=`) |
| POST   | `/employees`      | Create employee                                 |
| GET    | `/employees/{id}` | Get employee                                    |
| PUT    | `/employees/{id}` | Update employee                                 |
| DELETE | `/employees/{id}` | Soft delete                                     |

**Employee object:**

```json
{
  "id": 1,
  "employee_code": "EMP001",
  "full_name": "Raju Singh",
  "phone": "9001234567",
  "designation": "Mason",
  "daily_wage": 650.0,
  "status": "ACTIVE"
}
```

---

## Projects

| Method | Path             | Description                        |
| ------ | ---------------- | ---------------------------------- |
| GET    | `/projects`      | List projects (`?status=&search=`) |
| POST   | `/projects`      | Create project                     |
| GET    | `/projects/{id}` | Get project                        |
| PUT    | `/projects/{id}` | Update project                     |
| DELETE | `/projects/{id}` | Delete project                     |

**Statuses:** `PLANNING`, `IN_PROGRESS`, `ON_HOLD`, `COMPLETED`, `CANCELLED`  
**Road types:** `NATIONAL_HIGHWAY`, `STATE_HIGHWAY`, `DISTRICT_ROAD`, `VILLAGE_ROAD`, `URBAN_ROAD`

---

## Attendance

| Method | Path               | Description                                      |
| ------ | ------------------ | ------------------------------------------------ |
| GET    | `/attendance`      | List records (`?employee_id=&project_id=&date=`) |
| POST   | `/attendance`      | Mark attendance                                  |
| PUT    | `/attendance/{id}` | Update record                                    |

**Statuses:** `PRESENT`, `ABSENT`, `HALF_DAY`, `LEAVE`, `HOLIDAY`

**Create body:**

```json
{
  "employee_id": 1,
  "project_id": 1,
  "date": "2024-06-01",
  "status": "PRESENT",
  "working_hours": 8.0,
  "remarks": ""
}
```

---

## Materials

| Method | Path              | Description     |
| ------ | ----------------- | --------------- |
| GET    | `/materials`      | List materials  |
| POST   | `/materials`      | Create material |
| GET    | `/materials/{id}` | Get material    |
| PUT    | `/materials/{id}` | Update material |
| DELETE | `/materials/{id}` | Delete material |

---

## Material Stock

| Method | Path                          | Description                |
| ------ | ----------------------------- | -------------------------- |
| GET    | `/stock/project/{project_id}` | Stock levels for a project |
| GET    | `/stock/low`                  | All low-stock items        |
| POST   | `/stock/transaction`          | Record stock movement      |

**Transaction types:** `INWARD`, `OUTWARD`, `RETURN`, `ADJUSTMENT`

**Transaction body:**

```json
{
  "project_id": 1,
  "material_id": 1,
  "transaction_type": "INWARD",
  "quantity": 10.0,
  "unit_price": 1800.0,
  "vendor_id": 1,
  "remarks": "Delivery from supplier"
}
```

---

## Vendors

| Method | Path            | Description   |
| ------ | --------------- | ------------- |
| GET    | `/vendors`      | List vendors  |
| POST   | `/vendors`      | Create vendor |
| GET    | `/vendors/{id}` | Get vendor    |
| PUT    | `/vendors/{id}` | Update vendor |
| DELETE | `/vendors/{id}` | Delete vendor |

---

## Expenses

| Method | Path             | Description                                         |
| ------ | ---------------- | --------------------------------------------------- |
| GET    | `/expenses`      | List (`?project_id=&category=&from_date=&to_date=`) |
| POST   | `/expenses`      | Record expense                                      |
| GET    | `/expenses/{id}` | Get expense                                         |
| DELETE | `/expenses/{id}` | Delete expense                                      |

**Categories:** `LABOUR`, `MATERIAL`, `EQUIPMENT`, `TRANSPORT`, `FUEL`, `MAINTENANCE`, `OFFICE`, `OTHER`

---

## Reports

| Method | Path                                         | Description                      |
| ------ | -------------------------------------------- | -------------------------------- |
| GET    | `/reports/dashboard`                         | Summary stats for dashboard      |
| GET    | `/reports/daily?date=YYYY-MM-DD&project_id=` | Daily attendance + wage report   |
| GET    | `/reports/monthly?year=&month=&project_id=`  | Monthly labour & expense summary |
| GET    | `/reports/material-consumption?project_id=`  | Material inward/outward/balance  |

---

## Pagination

All list endpoints support:

```
?page=1&size=20&search=keyword
```

Response envelope:

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

---

## Error responses

| Code | Meaning                  |
| ---- | ------------------------ |
| 400  | Validation error         |
| 401  | Missing / expired token  |
| 403  | Insufficient permissions |
| 404  | Resource not found       |
| 409  | Conflict (duplicate)     |
| 422  | Unprocessable entity     |
| 500  | Internal server error    |
