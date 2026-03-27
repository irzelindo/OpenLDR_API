# OpenLDR API

A RESTful API for managing OpenLDR repository data, providing endpoints for Tuberculosis (TB) GeneXpert, HIV Viral Load, facility/laboratory information, and user authentication.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [API Documentation](#api-documentation)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Tuberculosis GeneXpert Endpoints](#tuberculosis-genexpert-endpoints)
  - [HIV Viral Load Endpoints](#hiv-viral-load-endpoints)
  - [Dictionary Endpoints](#dictionary-endpoints)
- [Common Parameters](#common-parameters)
- [Pagination](#pagination)
- [Authentication](#authentication)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Error Handling](#error-handling)

## Overview

The OpenLDR API provides a comprehensive set of endpoints for accessing and managing laboratory data, particularly focused on Tuberculosis GeneXpert testing and HIV Viral Load monitoring. The API includes JWT-based authentication, Clerk webhook integration for external identity providers, role-based access control, and paginated patient data endpoints.

## Project Structure

```
OpenLDR_API/
├── app.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── .gitignore                 # Git ignore file
├── .env/                      # Environment variables directory
├── Design/                    # Design documentation
├── auth/                      # Authentication module
│   ├── auth_controller.py     # Auth controllers (login, CRUD, Clerk webhook)
│   ├── auth_service.py        # Auth business logic
│   ├── user_model.py          # User & UserLogs SQLAlchemy models
│   └── routes.py              # Auth route definitions
├── tb/                        # Tuberculosis module
│   ├── gxpert/                # TB GeneXpert submodule
│   │   ├── controllers/       # Request handlers
│   │   │   ├── tb_gx_controller_facility.py
│   │   │   ├── tb_gx_controller_laboratory.py
│   │   │   ├── tb_gx_controller_summary.py
│   │   │   └── tb_gx_controller_patients.py
│   │   ├── services/          # Business logic
│   │   │   ├── tb_gx_services_facilities.py
│   │   │   ├── tb_gx_services_laboratory.py
│   │   │   ├── tb_gx_services_summary.py
│   │   │   └── tb_gx_services_patients.py
│   │   ├── models/            # SQLAlchemy models
│   │   │   └── tb_gx_model.py
│   │   └── routes.py          # TB GeneXpert route definitions
│   └── cultura/               # TB Culture submodule
│       ├── controllers/
│       ├── services/
│       ├── models/
│       └── routes.py
├── hiv/                       # HIV Viral Load module
│   ├── vl/                    # HIV VL submodule
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── models/
│   │   └── routes.py
│   └── [other HIV submodules]
├── dict/                      # Dictionary/reference data module
│   ├── controllers/
│   ├── services/
│   ├── models/
│   └── routes.py
├── configs/                   # Configuration files
│   ├── paths.py               # Production config (DB binds, keys)
│   └── paths_local.py         # Local development config
├── db/                        # Database configuration
│   └── database.py            # SQLAlchemy database instance
└── utilities/                 # Shared utilities
    ├── utils.py               # Helper functions & constants
    └── swagger.py             # Swagger/Flasgger template
```

## Tech Stack

### Core Framework
- **Flask 3.1.0** - Web framework
- **Flask-RESTful 0.3.10** - REST API extensions
- **Flask-SQLAlchemy 3.1.1** - Database ORM
- **SQLAlchemy 2.0.40** - Core database toolkit

### Authentication & Security
- **Flask-JWT-Extended 4.7.1** - JWT authentication
- **bcrypt 4.3.0** - Password hashing
- **PyJWT 2.10.1** - JWT handling
- **cryptography 45.0.6** - Cryptographic operations

### Database & Data Processing
- **pyodbc 5.2.0** - SQL Server database driver
- **pandas 2.2.3** - Data manipulation
- **numpy 2.2.4** - Numerical computing
- **openpyxl 3.1.5** - Excel file handling

### API Documentation & CORS
- **flasgger 0.9.7.1** - Swagger UI documentation
- **Flask-CORS 5.0.1** - Cross-origin resource sharing

### External Integrations
- **requests 2.32.3** - HTTP client
- **httpx 0.28.1** - Async HTTP client
- **google-generativeai 0.3.2** - Google AI integration
- **deep-translator 1.11.4** - Translation services

### Production & Deployment
- **gunicorn 23.0.0** - WSGI HTTP server
- **waitress 3.0.2** - WSGI server
- **Docker** - Containerization

### Development & Utilities
- **python-dateutil 2.9.0** - Date/time utilities
- **PyYAML 6.0.2** - YAML parsing
- **beautifulsoup4 4.13.3** - HTML/XML parsing
- **tqdm 4.67.1** - Progress bars

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/login` | Login with username and password, returns JWT token | No |
| `POST` | `/auth/create` | Create a new user (Admin only) | Yes (JWT) |
| `PUT` | `/auth/update` | Update user details (Admin only) | Yes (JWT) |
| `DELETE` | `/auth/delete` | Delete a user (Admin only) | Yes (JWT) |
| `GET` | `/auth/users` | Get all users (Admin only) | Yes (JWT) |
| `POST` | `/auth/clerk` | Clerk webhook handler for external auth events | No (Webhook) |

#### Clerk Webhook Events

The `/auth/clerk` endpoint handles the following Clerk events:

- **`session.created`** — Logs in an existing user or auto-creates a new one
- **`session.removed`** / **`session.ended`** — Logs out the user
- **`user.created`** — Creates a new user from Clerk data
- **`user.updated`** — Updates user info from Clerk data
- **`user.deleted`** — Deletes the user

### Tuberculosis GeneXpert Endpoints

#### Facilities Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tb/gx/facilities/registered_samples/` | Total samples registered by facility |
| `GET` | `/tb/gx/facilities/registered_samples_by_month/` | Registered samples by facility by month |
| `GET` | `/tb/gx/facilities/tested_samples/` | Total samples tested by facility |
| `GET` | `/tb/gx/facilities/tested_samples_by_month/` | Tested samples by facility by month |
| `GET` | `/tb/gx/facilities/tested_samples_disaggregated/` | Tested samples disaggregated by facility |
| `GET` | `/tb/gx/facilities/tested_samples_disaggregated_by_gender/` | Tested samples disaggregated by gender |
| `GET` | `/tb/gx/facilities/tested_samples_disaggregated_by_age/` | Tested samples disaggregated by age |
| `GET` | `/tb/gx/facilities/tested_samples_by_sample_types/` | Tested samples by sample types |
| `GET` | `/tb/gx/facilities/tested_samples_types_disaggregated_by_age/` | Sample types disaggregated by age |
| `GET` | `/tb/gx/facilities/tested_samples_disaggregated_by_drug_type/` | Tested samples by drug type |
| `GET` | `/tb/gx/facilities/tested_samples_disaggregated_by_drug_type_by_age/` | Tested samples by drug type and age |
| `GET` | `/tb/gx/facilities/rejected_samples/` | Rejected samples by facility |
| `GET` | `/tb/gx/facilities/rejected_samples_by_month/` | Rejected samples by facility by month |
| `GET` | `/tb/gx/facilities/rejected_samples_by_reason/` | Rejected samples by reason |
| `GET` | `/tb/gx/facilities/rejected_samples_by_reason_by_month/` | Rejected samples by reason by month |
| `GET` | `/tb/gx/facilities/trl_samples_by_days/` | Turnaround time in days |
| `GET` | `/tb/gx/facilities/trl_samples_by_days_by_month/` | Turnaround time in days by month |
| `GET` | `/tb/gx/facilities/trl_samples_avg_by_days/` | Average turnaround time in days |
| `GET` | `/tb/gx/facilities/trl_samples_avg_by_days_by_month/` | Average turnaround time by month |
| `GET` | `/tb/gx/facilities/trl_samples_by_days_tb/` | Turnaround time in days (TB-specific) |

#### Laboratory Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tb/gx/laboratories/registered_samples/` | Registered samples by laboratory |
| `GET` | `/tb/gx/laboratories/tested_samples/` | Tested samples by laboratory |
| `GET` | `/tb/gx/laboratories/registered_samples_by_month/` | Registered samples by lab by month |
| `GET` | `/tb/gx/laboratories/tested_samples_by_month/` | Tested samples by lab by month |
| `GET` | `/tb/gx/laboratories/tested_samples_by_sample_types/` | Tested samples by sample types |
| `GET` | `/tb/gx/laboratories/tested_samples_by_sample_types_by_month/` | Sample types by month |
| `GET` | `/tb/gx/laboratories/rejected_samples/` | Rejected samples by laboratory |
| `GET` | `/tb/gx/laboratories/rejected_samples_by_month/` | Rejected samples by lab by month |
| `GET` | `/tb/gx/laboratories/rejected_samples_by_reason/` | Rejected samples by reason |
| `GET` | `/tb/gx/laboratories/rejected_samples_by_reason_by_month/` | Rejected by reason by month |
| `GET` | `/tb/gx/laboratories/tested_samples_by_drug_type/` | Tested samples by drug type |
| `GET` | `/tb/gx/laboratories/tested_samples_by_drug_type_by_month/` | Drug type by month |
| `GET` | `/tb/gx/laboratories/trl_samples_by_lab_in_days/` | Turnaround time in days |
| `GET` | `/tb/gx/laboratories/trl_samples_by_lab_in_days_by_month/` | Turnaround time by month |
| `GET` | `/tb/gx/laboratories/trl_samples_avg_by_days/` | Average turnaround time in days |
| `GET` | `/tb/gx/laboratories/trl_samples_avg_by_days_by_month/` | Average turnaround time by month |

#### Summary Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tb/gx/summary/summary_header_component/` | Dashboard header component summary |
| `GET` | `/tb/gx/summary/positivity_by_month/` | Positivity rate by month |
| `GET` | `/tb/gx/summary/positivity_by_lab/` | Positivity rate by laboratory |
| `GET` | `/tb/gx/summary/positivity_by_lab_by_age/` | Positivity rate by lab by age |
| `GET` | `/tb/gx/summary/sample_types_by_month/` | Sample types by month by age |
| `GET` | `/tb/gx/summary/sample_types_by_facility_by_age/` | Sample types by facility by age |

#### Patient Endpoints

All patient endpoints require **Admin** role and support **pagination**.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tb/gx/patients/by_name/` | Search patients by first name or surname (partial match) |
| `GET` | `/tb/gx/patients/by_facility/` | Get patients registered at a specific health facility |
| `GET` | `/tb/gx/patients/by_sample_type/` | Get patients filtered by sample type (`sputum`, `feces`, `urine`, `blood`) |
| `GET` | `/tb/gx/patients/by_result_type/` | Get patients filtered by result type (`detected`, `not_detected`, `indeterminate`, `error`, `invalid`) |

### HIV Viral Load Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/hiv/vl/laboratory/registered_samples/` | Registered samples for HIV viral load testing |

### Dictionary Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dict/laboratories/` | Get all laboratories |
| `GET` | `/dict/laboratories/provinces/` | Get laboratories by province |
| `GET` | `/dict/laboratories/province/districts/` | Get laboratories by district |
| `GET` | `/dict/facilities/` | Get all facilities |
| `GET` | `/dict/facilities/provinces/` | Get facilities by province |
| `GET` | `/dict/facilities/province/districts/` | Get facilities by district |

## Common Parameters

The API accepts several common parameters across endpoints:

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `interval_dates` | string[] | Date range for filtering (format: `["YYYY-MM-DD", "YYYY-MM-DD"]`) |
| `province` | string | Filter by province name (supports multiple) |
| `district` | string | Filter by district name (supports multiple) |
| `health_facility` | string | Filter by health facility name |
| `facility_type` | string | Type of facility (`province`, `district`, `health_facility`) |
| `genexpert_result_type` | string | GeneXpert result type (`Ultra 6 Cores`, `XDR 10 Cores`) |
| `type_of_laboratory` | string | Laboratory type |
| `disaggregation` | string | Whether to include disaggregated data (`True`/`False`) |

### Patient-Specific Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `first_name` | string | Patient first name (partial match) |
| `surname` | string | Patient surname (partial match) |
| `sample_type` | string | Specimen type: `sputum`, `feces`, `urine`, `blood` |
| `result_type` | string | Result category: `detected`, `not_detected`, `indeterminate`, `error`, `invalid` |

## Pagination

Patient endpoints support server-side pagination to handle large datasets efficiently. Pagination is applied at the SQL query level using `OFFSET`/`LIMIT` for optimal performance.

### Pagination Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | `1` | Page number (1-indexed) |
| `per_page` | integer | `50` | Number of records per page |

### Paginated Response Format

```json
{
    "status": "success",
    "page": 1,
    "per_page": 50,
    "total_count": 1234,
    "total_pages": 25,
    "data": [
        {
            "request_id": "REQ001",
            "first_name": "John",
            "last_name": "Doe",
            "health_facility": "CS Example",
            "final_result": "MTB Detected",
            ...
        }
    ]
}
```

### Example Requests

```
GET /tb/gx/patients/by_name/?first_name=Ana&page=1&per_page=20
GET /tb/gx/patients/by_facility/?health_facility=CS%20Mongue&page=2&per_page=50
GET /tb/gx/patients/by_sample_type/?sample_type=sputum&page=1&per_page=100
GET /tb/gx/patients/by_result_type/?result_type=detected&page=3&per_page=50
```

## Authentication

The API uses **JWT (JSON Web Tokens)** for authentication with two integration paths:

### Direct Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

The response includes a JWT token:

```json
{
    "message": "Login successful",
    "data": {
        "user_id": "...",
        "user_name": "admin",
        "first_name": "Admin",
        "last_name": "User",
        "email_address": "admin@example.com",
        "role": "Admin"
    },
    "token": "eyJhbGciOi...",
    "status": 200
}
```

### Using the Token

Include the token in the `Authorization` header for protected endpoints:

```bash
curl -H "Authorization: Bearer eyJhbGciOi..." \
  http://localhost:5000/tb/gx/patients/by_name/?first_name=Ana
```

### Clerk Integration

The API supports [Clerk](https://clerk.com/) as an external identity provider via webhook events at `/auth/clerk`. When a user authenticates through Clerk:

1. **New users** are automatically created in the local database
2. **Existing users** receive a new JWT access token
3. **User updates/deletions** from Clerk are synced to the local database
4. All events are logged to the `UserLogs` table

### Roles

- **Admin** — Full access to all endpoints, including patient data and user management
- **user** — Standard access (default role for Clerk-provisioned users)

## Getting Started

### Prerequisites

- Python 3.10+
- SQL Server (via `pyodbc`)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd OpenLDR_API
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .env
   # Windows
   .env\Scripts\activate
   # Linux/macOS
   source .env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the application:
   - Edit `configs/paths.py` (production) or `configs/paths_local.py` (local development)
   - Set database connection strings in `SQLALCHEMY_BINDS_CDR_OPENLDR_ORG_MZ`
   - Set `SECRET_KEY` for JWT and session management
   - Set `CLERK_SECRET_KEY` and `CLERK_API_URL` for Clerk integration

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the API documentation at: `http://localhost:5000/apidocs/`

## Deployment

### Production (Waitress + NSSM on Windows)

```bash
waitress-serve --host=127.0.0.1 --port=9001 app:app
```

To register as a Windows service using NSSM:

- **Path**: `<venv>\Scripts\python.exe`
- **Startup Directory**: `<project_root>\`
- **Arguments**: `-m waitress --host=127.0.0.1 --port=9001 app:app`
- **Service Name**: `OpenLDR_API`

### Docker

```bash
docker-compose up -d
```

## Environment Setup

### Environment Variables

Create a `.env` file in the project root or configure in `configs/paths_local.py`:

```bash
# Database Configuration
SQLALCHEMY_BINDS_CDR_OPENLDR_ORG_MZ="mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server"

# Security
SECRET_KEY="your-secret-key-here"
CLERK_SECRET_KEY="clerk-secret-key"
CLERK_API_URL="https://your-clerk-instance.clerk.accounts.dev"

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### Database Setup

1. Ensure SQL Server is running and accessible
2. Create the OpenLDR database if it doesn't exist
3. Verify table structure using the provided models
4. Test connection with a simple query

### Testing

The API includes built-in testing capabilities:

```bash
# Test authentication
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'

# Test a public endpoint
curl http://localhost:5000/dict/laboratories/

# Test a protected endpoint (requires token)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:5000/tb/gx/facilities/registered_samples/
```

## Troubleshooting

### Common Issues

#### Database Connection Errors
- **Issue**: `InterfaceError: ('IM002', '[IM002] [Microsoft][ODBC Driver Manager] Data source name not found'`
- **Solution**: Install ODBC Driver 17 for SQL Server and verify connection string format

#### JWT Token Issues
- **Issue**: `401 Unauthorized` despite valid login
- **Solution**: Check `SECRET_KEY` configuration and token expiration time

#### CORS Issues
- **Issue**: Browser blocks API requests from frontend
- **Solution**: Verify `Flask-CORS` configuration and allowed origins

#### Performance Issues
- **Issue**: Slow response times on large datasets
- **Solution**: Use pagination, optimize database queries, add indexes

### Debug Mode

Enable debug mode for detailed error information:

```python
# In app.py
app.run(debug=True)
```

### Logging

Check application logs for detailed error information:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Error Handling

The API uses standard HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Invalid Parameters |
| 401 | Unauthorized (missing or invalid token) |
| 403 | Forbidden (insufficient role permissions) |
| 404 | Resource Not Found |
| 500 | Internal Server Error |

### Error Response Format

```json
{
    "status": 500,
    "error": "Internal Server Error",
    "message": "Detailed error description"
}
```

### Patient Service Error Example

```json
{
    "status": "error",
    "code": 403,
    "message": "Forbidden - User with id abc123 and role user is not authorized to access this resource."
}
```
