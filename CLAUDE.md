# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenLDR API is a RESTful API for laboratory data management in Mozambique, built with Flask + Flask-RESTful. It serves TB GeneXpert and HIV Viral Load testing data with JWT authentication and Swagger documentation.

- **Production server:** Waitress on Windows (port 9001), managed by NSSM
- **Dev server:** Flask built-in (`python app.py`) or Gunicorn/Docker
- **API docs:** `http://localhost:5000/apidocs/` (Swagger UI)
- **Root redirects** to `/apidocs/`

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Development
python app.py

# Production (Linux/Docker)
gunicorn --bind 0.0.0.0:5000 app:app

# Production (Windows via Waitress)
waitress-serve --host=127.0.0.1 --port=9001 app:app
```

No test suite or linter configuration currently exists.

## Environment Variables

All required variables must be set before running:

| Variable | Purpose |
|---|---|
| `FLASK_SECRET_KEY` | Flask session secret |
| `DB_USER` / `DB_PASSWORD` | SQL Server credentials (shared across all DBs) |
| `LOCAL_DOMAIN` / `CDR_DOMAIN` / `CLOUD_DOMAIN` | SQL Server hostnames per environment |
| `TB_DASHBOARD_DOMAIN` | TB dashboard server |
| `DB_VL_DATA`, `DB_VL_SMS`, `DB_DPI`, `DB_HIV_AD`, `DB_TB_DATA`, `DB_DICT`, `DB_USERS` | Database names |

The active environment binding is selected in `app.py` by assigning one of the three `SQLALCHEMY_BINDS_*` dicts from `configs/paths.py` to `app.config["SQLALCHEMY_BINDS"]`.

## Architecture

### Multi-Database Setup

The app connects to **6 SQL Server databases** simultaneously using SQLAlchemy binds. Each ORM model specifies which database it belongs to via `__bind_key__`:

- `vl` — HIV Viral Load data
- `dpi` — Drug Program Information
- `ad` — HIV Additional (CD4, CRAG, TBLAM)
- `tb` — TB GeneXpert data
- `dict` — Reference data (facilities/laboratories)
- `users` — Authentication & user logs

Connection strings use `mssql+pyodbc` with ODBC Driver 17 for SQL Server.

### Code Organization Pattern

Each feature module follows a strict 3-layer pattern:

```
feature/
├── routes.py          # Registers Flask-RESTful Resources onto the API object
├── controllers/       # Flask-RESTful Resource classes — parse args, call services, return JSON
├── services/          # Business logic — SQLAlchemy queries, data transformation
└── models/            # SQLAlchemy ORM model definitions
```

Request flow: `HTTP → routes.py → controller (reqparse) → service (SQLAlchemy) → SQL Server → JSON response`

### Module Structure

- `tb/gxpert/` — TB GeneXpert (most complete; 40+ endpoints across facility, laboratory, summary controllers)
- `hiv/vl/` — HIV Viral Load (only 1 endpoint implemented)
- `hiv/ad/` — HIV Additional tests (CD4, CRAG, TBLAM; partially implemented)
- `dict/` — Reference data (laboratories and facilities, filterable by province/district)
- `auth/` — JWT authentication, user CRUD, login/logout logging
- `utilities/utils.py` — Shared SQL query builders, token helpers, parameter processors
- `utilities/swagger.py` — Swagger/OpenAPI template and parameter definitions
- `configs/paths.py` — Environment variable loading and SQLAlchemy bind dict definitions
- `db/database.py` — SQLAlchemy `db` instance (imported everywhere models need it)
- `app.py` — App factory: binds config, registers routes, initializes JWT/Swagger/CORS

### Authentication

- JWT tokens via `flask-jwt-extended`, 60-minute expiration
- Tokens obtained via `POST /auth/login`
- Role-based access: `Admin` role has elevated privileges in some endpoints
- Token user info extracted in services using `get_user_token_info()` from `utilities/utils.py`

### Common API Parameters

Most endpoints share these query parameters (defined as reqparse arguments in controllers):
- `interval_dates` — JSON array `["YYYY-MM-DD", "YYYY-MM-DD"]`
- `province` / `district` — geographic filters
- `facility_type` — `province`, `district`, or `health_facility`
- `type_of_laboratory` — laboratory type filter
- `disaggregation` — boolean, enables disaggregated response
- `genexpert_result_type` — `Ultra 6 Cores` or `XDR 10 Cores`

Helper `PROCESS_COMMON_PARAMS_FACILITY()` and `PROCESS_COMMON_PARAMS_LABORATORY()` in `utilities/utils.py` parse and validate these consistently.

## Adding a New Endpoint

1. Add the SQLAlchemy model in `<module>/models/` with the correct `__bind_key__`
2. Add query logic in `<module>/services/`
3. Create a Flask-RESTful `Resource` class in `<module>/controllers/`
4. Register it in `<module>/routes.py` using `api.add_resource()`
5. Add the route function call in `app.py` if it's a new module

## Switching Environments

In `app.py`, change the active bind dict:
```python
# CDR (current production)
app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS_CDR_OPENLDR_ORG_MZ

# Local development
# app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS_APHL_OPENLDR_ORG_MZ

# Cloud
# app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS_CLOUD_QUEUE_OPENLDR_ORG_MZ
```

Alternatively, swap the import between `configs/paths.py` (production) and `configs/paths_local.py` (local dev).
