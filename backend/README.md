# Multi-Tenant HRMS SaaS Platform - Backend

Production-grade Django backend for multi-tenant HRMS SaaS platform.

## Features

- ✅ Multi-tenancy with complete data isolation
- ✅ JWT authentication with access & refresh tokens
- ✅ Role-based access control (RBAC)
- ✅ Employee management
- ✅ Attendance tracking
- ✅ Leave management
- ✅ Payroll structure (MVP)
- ✅ Document management
- ✅ PostgreSQL-compatible schema
- ✅ RESTful API with OpenAPI documentation

## Tech Stack

- Django 5.0
- Django REST Framework
- PostgreSQL/SQLite
- JWT Authentication
- UUID Primary Keys

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

## API Documentation

- Swagger UI: http://localhost:8000/api/docs/
- OpenAPI Schema: http://localhost:8000/api/schema/

## Project Structure

```
backend/
├── core/                   # Core configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL config
│   ├── middleware/        # Custom middleware
│   ├── models/            # Base models
│   └── utils/             # Utilities
├── apps/                  # Business apps
│   ├── tenants/          # Multi-tenancy
│   ├── users/            # User management
│   ├── roles/            # RBAC
│   ├── employees/        # Employee info
│   ├── attendance/       # Time tracking
│   ├── leave/            # Leave management
│   ├── payroll/          # Payroll (MVP)
│   └── documents/        # Document management
└── api/v1/               # API endpoints
    └── auth/             # Authentication
```

## Multi-Tenancy

All business data is tenant-scoped. Tenant context is extracted from JWT token and enforced via middleware.

## Authentication

JWT-based authentication with custom claims:

- `user_id`: User UUID
- `tenant_id`: Tenant UUID
- `roles`: List of role codes

### Login

```bash
POST /api/v1/auth/login/
{
  "email": "user@example.com",
  "password": "password"
}
```

### Refresh Token

```bash
POST /api/v1/auth/refresh/
{
  "refresh": "refresh_token_here"
}
```

## Database

### Development (SQLite)

```
DATABASE_URL=sqlite:///db.sqlite3
```

### Production (PostgreSQL)

```
DATABASE_URL=postgresql://user:password@localhost:5432/hrms_db
```

## License

Proprietary - All Rights Reserved
