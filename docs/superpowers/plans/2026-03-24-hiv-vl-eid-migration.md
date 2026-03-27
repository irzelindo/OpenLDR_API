# HIV VL & EID Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate HIV Viral Load (35 endpoints) and EID (35 endpoints) from legacy Node.js backends into api_openldr_python, following TB GeneXpert patterns with full TDD test coverage.

**Architecture:** MVC pattern (models → services → controllers → routes) using Flask-RESTful, SQLAlchemy ORM, and shared utility functions. VL refactors existing module; EID creates new module. All endpoints use standardized query parameters matching TB GeneXpert convention.

**Tech Stack:** Python 3.12, Flask 3.1, Flask-RESTful, SQLAlchemy 2.0, Flask-JWT-Extended, pytest, SQL Server via pyodbc

**Spec:** `docs/superpowers/specs/2026-03-24-hiv-vl-eid-migration-design.md`

**Branch:** `feature/hiv-vl-eid-migration`

---

## File Structure

### New Files
- `tests/__init__.py`
- `tests/conftest.py` — Shared test fixtures (Flask app, client, JWT token, mock data)
- `tests/test_utils.py` — Utility function tests
- `tests/hiv/__init__.py`
- `tests/hiv/test_vl_laboratory.py`
- `tests/hiv/test_vl_facility.py`
- `tests/hiv/test_vl_summary.py`
- `tests/hiv/test_eid_laboratory.py`
- `tests/hiv/test_eid_facility.py`
- `tests/hiv/test_eid_summary.py`
- `hiv/eid/__init__.py`
- `hiv/eid/routes.py` — Stub created in Task 1, populated in Task 8
- `hiv/eid/models/__init__.py`
- `hiv/eid/models/eid_master_model.py`
- `hiv/eid/controllers/__init__.py`
- `hiv/eid/controllers/eid_controller_laboratory.py`
- `hiv/eid/controllers/eid_controller_facility.py`
- `hiv/eid/controllers/eid_controller_summary.py`
- `hiv/eid/services/__init__.py`
- `hiv/eid/services/eid_services_laboratory.py`
- `hiv/eid/services/eid_services_facilities.py`
- `hiv/eid/services/eid_services_summary.py`
- `pytest.ini`

### Modified Files
- `app.py` — Add EID route registration
- `requirements.txt` — Add pytest, pytest-cov
- `utilities/utils.py` — Add POSITIVITY(), LAB_TYPE_EID(), EQUIPMENT_COUNT(), PROCESS_COMMON_PARAMS()
- `hiv/vl/routes.py` — Expand from 1 to 35 endpoints, rename paths
- `hiv/vl/controllers/laboratory_controller.py` → renamed to `hiv/vl/controllers/vl_controller_laboratory.py`
- `hiv/vl/controllers/facilities_controller.py` → renamed to `hiv/vl/controllers/vl_controller_facility.py`
- `hiv/vl/controllers/summary_controller.py` → renamed to `hiv/vl/controllers/vl_controller_summary.py`
- `hiv/vl/services/laboratory_services.py` → renamed to `hiv/vl/services/vl_services_laboratory.py`
- `hiv/vl/services/facilities_services.py` → renamed to `hiv/vl/services/vl_services_facilities.py`
- `hiv/vl/services/summary_services.py` → renamed to `hiv/vl/services/vl_services_summary.py`

### Deleted
- `hiv/dpi/` — Empty placeholder directories

---

## Task 1: Test Infrastructure Setup

**Files:**
- Create: `pytest.ini`
- Create: `tests/__init__.py`
- Create: `tests/hiv/__init__.py`
- Create: `tests/conftest.py`
- Create: `hiv/eid/__init__.py` (stub)
- Create: `hiv/eid/routes.py` (stub with empty function)
- Modify: `requirements.txt`

- [ ] **Step 1: Add test dependencies to requirements.txt**

Append to the end of `requirements.txt`:

```
pytest==8.1.1
pytest-cov==5.0.0
```

- [ ] **Step 2: Create pytest.ini**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

- [ ] **Step 3: Create test package init files**

Create empty `tests/__init__.py` and `tests/hiv/__init__.py`.

Also create the EID module stub so conftest.py can import it:

`hiv/eid/__init__.py` — empty file

`hiv/eid/routes.py`:
```python
def eid_routes(api):
    """EID routes — stub, populated in Task 8."""
    pass
```

- [ ] **Step 4: Create conftest.py with shared fixtures**

File: `tests/conftest.py`

```python
import pytest
import json
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from db.database import db


@pytest.fixture(scope="session")
def app():
    """Create Flask app with test configuration."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_BINDS"] = {
        "vlSMS": "sqlite:///:memory:",
        "vl": "sqlite:///:memory:",
        "dpi": "sqlite:///:memory:",
        "tb": "sqlite:///:memory:",
        "dict": "sqlite:///:memory:",
        "users": "sqlite:///:memory:",
        "ad": "sqlite:///:memory:",
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test-secret-key"
    app.config["JWT_SECRET_KEY"] = "test-jwt-secret"

    jwt = JWTManager(app)
    db.init_app(app)

    api = Api(app)

    # Import and register routes
    from hiv.vl.routes import vl_routes
    from hiv.eid.routes import eid_routes

    vl_routes(api)
    eid_routes(api)

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def auth_headers(app):
    """Valid JWT authorization headers."""
    with app.app_context():
        token = create_access_token(
            identity="test-user",
            additional_claims={
                "user_id": "test-123",
                "user_name": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@openldr.org",
                "role": "Admin",
            },
        )
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_vl_query_params():
    """Standard VL query parameters."""
    return {
        "interval_dates": ["2024-01-01", "2024-12-31"],
        "province": ["Maputo"],
        "facility_type": "province",
    }


@pytest.fixture
def sample_eid_query_params():
    """Standard EID query parameters."""
    return {
        "interval_dates": ["2024-01-01", "2024-12-31"],
        "province": ["Maputo"],
        "facility_type": "province",
        "lab_type": "all",
    }


@pytest.fixture
def mock_vl_service_response():
    """Sample VL service response for mocking."""
    return [
        {
            "year": 2024,
            "month": 1,
            "month_name": "January",
            "total": 150,
            "total_not_null": 140,
            "total_null": 10,
            "suppressed": 120,
            "not_suppressed": 20,
            "male_suppressed": 60,
            "male_not_suppressed": 10,
            "female_suppressed": 60,
            "female_not_suppressed": 10,
        }
    ]


@pytest.fixture
def mock_eid_service_response():
    """Sample EID service response for mocking."""
    return [
        {
            "year": 2024,
            "month": 1,
            "month_name": "January",
            "total": 200,
            "tested": 180,
            "positive": 15,
            "negative": 165,
            "rejected": 10,
            "pending": 10,
            "female": 95,
            "male": 85,
        }
    ]
```

- [ ] **Step 5: Install test dependencies**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && pip install pytest==8.1.1 pytest-cov==5.0.0`

- [ ] **Step 6: Commit**

```bash
git add pytest.ini tests/ requirements.txt hiv/eid/__init__.py hiv/eid/routes.py
git commit -m "feat: add test infrastructure for VL and EID migration"
```

---

## Task 2: Utility Functions — Add VL/EID Helpers

**Files:**
- Modify: `utilities/utils.py`
- Create: `tests/test_utils.py`

- [ ] **Step 1: Write failing tests for new utility functions**

File: `tests/test_utils.py`

```python
import pytest
from unittest.mock import MagicMock
from sqlalchemy import Column, String, DateTime, Integer


def test_positivity_returns_case_expression():
    """POSITIVITY should return a CASE WHEN expression for counting positive results."""
    from utilities.utils import POSITIVITY

    mock_field = Column("PCR_Result", String)
    result = POSITIVITY(mock_field, "Positive")
    # Should be a SQLAlchemy expression (not None)
    assert result is not None


def test_process_common_params_extracts_standard_params():
    """PROCESS_COMMON_PARAMS should extract interval_dates, province, facility_type, disaggregation."""
    from utilities.utils import PROCESS_COMMON_PARAMS

    req_args = {
        "interval_dates": ["2024-01-01", "2024-12-31"],
        "province": ["Maputo", "Sofala"],
        "district": None,
        "health_facility": None,
        "facility_type": "province",
        "disaggregation": "True",
    }
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS(req_args)
    assert dates == ["2024-01-01", "2024-12-31"]
    assert facilities == ["Maputo", "Sofala"]
    assert facility_type == "province"
    assert disaggregation is True
    assert health_facility is None


def test_process_common_params_defaults():
    """PROCESS_COMMON_PARAMS should handle missing/None parameters gracefully."""
    from utilities.utils import PROCESS_COMMON_PARAMS

    req_args = {
        "interval_dates": None,
        "province": None,
        "district": None,
        "health_facility": None,
        "facility_type": None,
        "disaggregation": None,
    }
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS(req_args)
    # Should default to last 12 months
    assert len(dates) == 2
    assert facility_type == "province"
    assert disaggregation is False
    assert facilities == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/test_utils.py -v`
Expected: FAIL — functions not found

- [ ] **Step 3: Implement utility functions**

Add to the end of `utilities/utils.py`:

```python
def POSITIVITY(field, value):
    """
    Count records where field matches value (for EID positive/negative counting).
    Analogous to SUPPRESSION() but with generic naming.

    Parameters
    ----------
    field : sqlalchemy.Column
        The column to check (e.g., PCR_Result, POC_Result)
    value : str
        The value to match (e.g., "Positive", "Negative")

    Returns
    -------
    sqlalchemy.sql.expression
        A CASE expression that counts matching records
    """
    return func.count(case((field.like(f"%{value}%"), 1)))


def LAB_TYPE_EID(Model, lab_type):
    """
    Filter EID records by test type (conventional PCR vs Point of Care).

    Parameters
    ----------
    Model : sqlalchemy.Model
        The EIDMaster model class
    lab_type : str
        "conventional", "poc", or "all"

    Returns
    -------
    sqlalchemy.sql.expression or None
        A filter condition, or None if lab_type is "all"
    """
    if lab_type.lower() == "poc":
        return Model.IsPoc == "Yes"
    elif lab_type.lower() == "conventional":
        return Model.IsPoc != "Yes"
    return None


def EQUIPMENT_COUNT(Model, equipment_name):
    """
    Count records by equipment/analyzer type.

    Parameters
    ----------
    Model : sqlalchemy.Model
        The model class with LIMSAnalyzerCode column
    equipment_name : str
        Equipment code (e.g., "CAPCTM", "ALINITY", "M2000")

    Returns
    -------
    sqlalchemy.sql.expression
        A CASE expression counting matching records
    """
    return func.count(case((Model.ResultLIMSAnalyzerCode == equipment_name, 1)))


def PROCESS_COMMON_PARAMS(req_args):
    """
    Extract and normalize common query parameters used across all modules.
    Standardizes parameter handling for VL, EID, and TB endpoints.

    Parameters
    ----------
    req_args : dict
        Parsed request arguments from reqparse

    Returns
    -------
    tuple
        (dates, facilities, facility_type, disaggregation, health_facility)
    """
    # Date range — default to last 12 months
    dates = req_args.get("interval_dates")
    if not dates or len(dates) < 2:
        dates = [twelve_months_ago, today]

    # Facility type — default to province
    facility_type = req_args.get("facility_type") or "province"

    # Disaggregation — default to False
    disaggregation_raw = req_args.get("disaggregation")
    disaggregation = disaggregation_raw == "True" if disaggregation_raw else False

    # Health facility
    health_facility = req_args.get("health_facility")

    # Facilities list — from province, district, or health_facility depending on type
    facilities = []
    if facility_type == "province":
        facilities = req_args.get("province") or []
    elif facility_type == "district":
        facilities = req_args.get("district") or []
    elif facility_type == "health_facility" and health_facility:
        facilities = [health_facility]

    # Clean up facilities list
    facilities = [f.strip() for f in facilities if f and f.strip()]

    return dates, facilities, facility_type, disaggregation, health_facility
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/test_utils.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add utilities/utils.py tests/test_utils.py
git commit -m "feat: add POSITIVITY, LAB_TYPE_EID, EQUIPMENT_COUNT, PROCESS_COMMON_PARAMS utilities"
```

---

## Task 3: VL Module Restructure — Rename Files & Standardize Parameters

**Files:**
- Rename: `hiv/vl/controllers/laboratory_controller.py` → `hiv/vl/controllers/vl_controller_laboratory.py`
- Rename: `hiv/vl/controllers/facilities_controller.py` → `hiv/vl/controllers/vl_controller_facility.py`
- Rename: `hiv/vl/controllers/summary_controller.py` → `hiv/vl/controllers/vl_controller_summary.py`
- Rename: `hiv/vl/services/laboratory_services.py` → `hiv/vl/services/vl_services_laboratory.py`
- Rename: `hiv/vl/services/facilities_services.py` → `hiv/vl/services/vl_services_facilities.py`
- Rename: `hiv/vl/services/summary_services.py` → `hiv/vl/services/vl_services_summary.py`
- Modify: `hiv/vl/routes.py`
- Delete: `hiv/dpi/` (empty placeholder)

- [ ] **Step 1: Rename VL files to match convention**

```bash
cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python
git mv hiv/vl/controllers/laboratory_controller.py hiv/vl/controllers/vl_controller_laboratory.py
git mv hiv/vl/controllers/facilities_controller.py hiv/vl/controllers/vl_controller_facility.py
git mv hiv/vl/controllers/summary_controller.py hiv/vl/controllers/vl_controller_summary.py
git mv hiv/vl/services/laboratory_services.py hiv/vl/services/vl_services_laboratory.py
git mv hiv/vl/services/facilities_services.py hiv/vl/services/vl_services_facilities.py
git mv hiv/vl/services/summary_services.py hiv/vl/services/vl_services_summary.py
```

- [ ] **Step 2: Remove empty dpi placeholder directories**

```bash
rm -rf hiv/dpi/
```

- [ ] **Step 3: Update imports in existing VL service to use standardized parameters**

In `hiv/vl/services/vl_services_laboratory.py`, update `get_registered_samples_service()` to use `PROCESS_COMMON_PARAMS()` and the new parameter names (`interval_dates`, `province`, `facility_type` instead of `dates`, `provinces`, `filter_by`).

- [ ] **Step 4: Update VL routes.py imports**

Replace the content of `hiv/vl/routes.py` with updated imports pointing to renamed files:

```python
from hiv.vl.controllers.vl_controller_laboratory import *


def vl_routes(api):
    """
    Registers the routes for HIV Viral Load API endpoints.

    Args:
        api: A flask_restful Api instance to which the routes are registered
    """
    # Laboratory Endpoints
    # Legacy: GET /samples
    api.add_resource(VlRegisteredSamples, "/hiv/vl/laboratories/registered_samples/")
```

Note: Controller class name changes from `RegisteredSamples` to `VlRegisteredSamples` — update the class name in the controller file accordingly.

- [ ] **Step 5: Verify VlData model has required columns**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -c "from hiv.vl.models.vl import VlData; cols = [c.name for c in VlData.__table__.columns]; required = ['ViralLoadResultCategory', 'HL7SexCode', 'AgeInYears', 'Pregnant', 'BreastFeeding', 'ReasonForTest', 'RequestingProvinceName', 'RequestingDistrictName', 'RequestingFacilityName', 'TestingFacilityName', 'SpecimenDatetime', 'RegisteredDateTime', 'ReceivedDateTime', 'AnalysisDateTime', 'AuthorisedDateTime', 'LIMSRejectionCode']; missing = [c for c in required if c not in cols]; print('Missing columns:', missing) if missing else print('All required columns present')"`

If any columns are missing, add them to `hiv/vl/models/vl.py`.

- [ ] **Step 6: Smoke test — verify imports work after rename**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -c "from hiv.vl.routes import vl_routes; print('VL routes import OK')"`
Expected: "VL routes import OK"

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "refactor: rename VL files to match TB GeneXpert convention, remove empty dpi placeholder"
```

---

## Task 4: VL Laboratory Endpoints — Services & Tests

**Files:**
- Modify: `hiv/vl/services/vl_services_laboratory.py`
- Create: `tests/hiv/test_vl_laboratory.py`
- Modify: `hiv/vl/controllers/vl_controller_laboratory.py`

- [ ] **Step 1: Write failing tests for VL laboratory services**

File: `tests/hiv/test_vl_laboratory.py`

```python
import pytest
from unittest.mock import patch, MagicMock


class TestVlLaboratoryRoutes:
    """Test that VL laboratory routes exist and require correct parameters."""

    def test_registered_samples_returns_200(self, client, auth_headers, mock_vl_service_response):
        with patch(
            "hiv.vl.controllers.vl_controller_laboratory.registered_samples_service",
            return_value=mock_vl_service_response,
        ):
            response = client.get(
                "/hiv/vl/laboratories/registered_samples/",
                query_string={
                    "interval_dates": ["2024-01-01", "2024-12-31"],
                    "province": ["Maputo"],
                    "facility_type": "province",
                },
                headers=auth_headers,
            )
            assert response.status_code == 200

    def test_tested_samples_returns_200(self, client, auth_headers, mock_vl_service_response):
        with patch(
            "hiv.vl.controllers.vl_controller_laboratory.tested_samples_service",
            return_value=mock_vl_service_response,
        ):
            response = client.get(
                "/hiv/vl/laboratories/tested_samples/",
                query_string={
                    "interval_dates": ["2024-01-01", "2024-12-31"],
                    "province": ["Maputo"],
                    "facility_type": "province",
                },
                headers=auth_headers,
            )
            assert response.status_code == 200

    def test_tested_samples_by_month_returns_200(self, client, auth_headers, mock_vl_service_response):
        with patch(
            "hiv.vl.controllers.vl_controller_laboratory.tested_samples_by_month_service",
            return_value=mock_vl_service_response,
        ):
            response = client.get(
                "/hiv/vl/laboratories/tested_samples_by_month/",
                query_string={
                    "interval_dates": ["2024-01-01", "2024-12-31"],
                    "province": ["Maputo"],
                    "facility_type": "province",
                },
                headers=auth_headers,
            )
            assert response.status_code == 200

    def test_tested_samples_by_gender_returns_200(self, client, auth_headers, mock_vl_service_response):
        with patch(
            "hiv.vl.controllers.vl_controller_laboratory.tested_samples_by_gender_service",
            return_value=mock_vl_service_response,
        ):
            response = client.get(
                "/hiv/vl/laboratories/tested_samples_by_gender/",
                query_string={
                    "interval_dates": ["2024-01-01", "2024-12-31"],
                    "province": ["Maputo"],
                    "facility_type": "province",
                },
                headers=auth_headers,
            )
            assert response.status_code == 200

    def test_tested_samples_by_age_returns_200(self, client, auth_headers, mock_vl_service_response):
        with patch(
            "hiv.vl.controllers.vl_controller_laboratory.tested_samples_by_age_service",
            return_value=mock_vl_service_response,
        ):
            response = client.get(
                "/hiv/vl/laboratories/tested_samples_by_age/",
                query_string={
                    "interval_dates": ["2024-01-01", "2024-12-31"],
                    "province": ["Maputo"],
                    "facility_type": "province",
                },
                headers=auth_headers,
            )
            assert response.status_code == 200

    def test_tested_samples_by_test_reason_returns_200(self, client, auth_headers, mock_vl_service_response):
        with patch(
            "hiv.vl.controllers.vl_controller_laboratory.tested_samples_by_test_reason_service",
            return_value=mock_vl_service_response,
        ):
            response = client.get(
                "/hiv/vl/laboratories/tested_samples_by_test_reason/",
                query_string={
                    "interval_dates": ["2024-01-01", "2024-12-31"],
                    "province": ["Maputo"],
                    "facility_type": "province",
                },
                headers=auth_headers,
            )
            assert response.status_code == 200

    def test_rejected_samples_returns_200(self, client, auth_headers, mock_vl_service_response):
        with patch(
            "hiv.vl.controllers.vl_controller_laboratory.rejected_samples_service",
            return_value=mock_vl_service_response,
        ):
            response = client.get(
                "/hiv/vl/laboratories/rejected_samples/",
                query_string={
                    "interval_dates": ["2024-01-01", "2024-12-31"],
                    "province": ["Maputo"],
                    "facility_type": "province",
                },
                headers=auth_headers,
            )
            assert response.status_code == 200

    def test_tat_by_lab_returns_200(self, client, auth_headers, mock_vl_service_response):
        with patch(
            "hiv.vl.controllers.vl_controller_laboratory.tat_by_lab_service",
            return_value=mock_vl_service_response,
        ):
            response = client.get(
                "/hiv/vl/laboratories/tat_by_lab/",
                query_string={
                    "interval_dates": ["2024-01-01", "2024-12-31"],
                    "province": ["Maputo"],
                    "facility_type": "province",
                },
                headers=auth_headers,
            )
            assert response.status_code == 200

    def test_unauthenticated_returns_401(self, client):
        """Verify that unauthenticated requests return 401."""
        response = client.get("/hiv/vl/laboratories/registered_samples/")
        assert response.status_code == 401

    def test_response_json_structure(self, client, auth_headers, mock_vl_service_response):
        """Verify response contains expected VL fields."""
        with patch(
            "hiv.vl.controllers.vl_controller_laboratory.registered_samples_service",
            return_value=mock_vl_service_response,
        ):
            response = client.get(
                "/hiv/vl/laboratories/registered_samples/",
                query_string={
                    "interval_dates": ["2024-01-01", "2024-12-31"],
                    "province": ["Maputo"],
                    "facility_type": "province",
                },
                headers=auth_headers,
            )
            data = response.get_json()
            assert isinstance(data, list)
            if data:
                record = data[0]
                assert "year" in record
                assert "month" in record
                assert "suppressed" in record
                assert "not_suppressed" in record
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_vl_laboratory.py -v`
Expected: FAIL — routes and services not found

- [ ] **Step 3: Implement VL laboratory service functions**

File: `hiv/vl/services/vl_services_laboratory.py`

Implement the following service functions (each follows the pattern from the existing `get_registered_samples_service` but uses `PROCESS_COMMON_PARAMS`):

1. `registered_samples_service(req_args)` — Refactor existing, use standardized params
2. `registered_samples_by_month_service(req_args)` — Group by year/month + testing facility
3. `tested_samples_service(req_args)` — Group by testing facility, count tested (AnalysisDateTime not null)
4. `tested_samples_by_month_service(req_args)` — Group by year/month with suppression counts
5. `tested_samples_by_gender_service(req_args)` — Gender-stratified suppression using GENDER_SUPPRESSION()
6. `tested_samples_by_gender_by_lab_service(req_args)` — Gender by lab
7. `tested_samples_by_age_service(req_args)` — Age group stratification
8. `tested_samples_by_test_reason_service(req_args)` — Count routine, treatment_failure, reason_not_specified
9. `tested_samples_pregnant_service(req_args)` — Filter Pregnant == "Yes"
10. `tested_samples_breastfeeding_service(req_args)` — Filter BreastFeeding == "Yes"
11. `rejected_samples_service(req_args)` — Count where LIMSRejectionCode IS NOT NULL
12. `rejected_samples_by_month_service(req_args)` — Rejected by month
13. `tat_by_lab_service(req_args)` — TAT using DATE_DIFF_AVG() for 4 segments (collection→reception→registration→analysis→validation)
14. `tat_by_month_service(req_args)` — TAT by month
15. `suppression_service(req_args)` — Suppression trend data

Each service function follows this template:

```python
def tested_samples_service(req_args):
    """Retrieve tested samples grouped by testing facility."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS(req_args)

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
        VlData.TestingFacilityName.is_not(None),
    ]

    if facilities:
        if facility_type == "province":
            filters.append(VlData.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(VlData.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(VlData.TestingFacilityName.in_(facilities))

    try:
        query = VlData.query.with_entities(
            VlData.TestingFacilityName.label("facility_name"),
            TOTAL_ALL,
            TOTAL_NOT_NULL(VlData.ViralLoadResultCategory).label("total_not_null"),
            SUPPRESSION(VlData.ViralLoadResultCategory, "Suppressed").label("suppressed"),
            SUPPRESSION(VlData.ViralLoadResultCategory, "Not Suppressed").label("not_suppressed"),
        ).filter(
            and_(*filters)
        ).group_by(
            VlData.TestingFacilityName
        ).order_by(
            VlData.TestingFacilityName
        )

        data = query.all()
        return [
            dict(
                facility_name=row.facility_name,
                total=row.total,
                total_not_null=row.total_not_null,
                suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}
```

- [ ] **Step 4: Implement VL laboratory controllers**

File: `hiv/vl/controllers/vl_controller_laboratory.py`

Each controller follows this template:

```python
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from hiv.vl.services.vl_services_laboratory import (
    registered_samples_service,
    tested_samples_service,
    tested_samples_by_month_service,
    tested_samples_by_gender_service,
    tested_samples_by_gender_by_lab_service,
    tested_samples_by_age_service,
    tested_samples_by_test_reason_service,
    tested_samples_pregnant_service,
    tested_samples_breastfeeding_service,
    rejected_samples_service,
    rejected_samples_by_month_service,
    tat_by_lab_service,
    tat_by_month_service,
    suppression_service,
    registered_samples_by_month_service,
)


def _parse_common_args():
    """Parse standardized query parameters."""
    parser = reqparse.RequestParser()
    parser.add_argument("interval_dates", type=lambda x: x, location="args", action="append")
    parser.add_argument("province", type=lambda x: x, location="args", action="append")
    parser.add_argument("district", type=lambda x: x, location="args", action="append")
    parser.add_argument("health_facility", type=str, location="args")
    parser.add_argument("facility_type", type=str, location="args")
    parser.add_argument("disaggregation", type=str, location="args")
    return parser.parse_args()


class VlRegisteredSamples(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve registered samples by laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityTypeParameter'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Registered samples by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(registered_samples_service(req_args))


class VlTestedSamples(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        """
        req_args = _parse_common_args()
        return jsonify(tested_samples_service(req_args))


# Repeat for all 15 controllers:
# VlRegisteredSamplesByMonth, VlTestedSamples, VlTestedSamplesByMonth,
# VlTestedSamplesByGender, VlTestedSamplesByGenderByLab, VlTestedSamplesByAge,
# VlTestedSamplesByTestReason, VlTestedSamplesPregnant, VlTestedSamplesBreastfeeding,
# VlRejectedSamples, VlRejectedSamplesByMonth, VlTatByLab, VlTatByMonth,
# VlSuppression
```

Each controller class follows the same pattern: parse args → call service → return jsonify.

- [ ] **Step 5: Register all VL laboratory routes**

Update `hiv/vl/routes.py` to register all 15 laboratory endpoints:

```python
def vl_routes(api):
    # Laboratory Endpoints
    # Legacy: GET /samples
    api.add_resource(VlRegisteredSamples, "/hiv/vl/laboratories/registered_samples/")
    # Legacy: GET /lab_samples_tested_by_month (partial - registered)
    api.add_resource(VlRegisteredSamplesByMonth, "/hiv/vl/laboratories/registered_samples_by_month/")
    # Legacy: GET /lab_samples_tested_by_lab
    api.add_resource(VlTestedSamples, "/hiv/vl/laboratories/tested_samples/")
    # Legacy: GET /lab_samples_tested_by_month
    api.add_resource(VlTestedSamplesByMonth, "/hiv/vl/laboratories/tested_samples_by_month/")
    # Legacy: GET /lab_samples_tested_by_gender
    api.add_resource(VlTestedSamplesByGender, "/hiv/vl/laboratories/tested_samples_by_gender/")
    # Legacy: GET /lab_samples_tested_by_gender_and_labs
    api.add_resource(VlTestedSamplesByGenderByLab, "/hiv/vl/laboratories/tested_samples_by_gender_by_lab/")
    # Legacy: GET /lab_samples_tested_by_age
    api.add_resource(VlTestedSamplesByAge, "/hiv/vl/laboratories/tested_samples_by_age/")
    # Legacy: GET /lab_samples_by_test_reason
    api.add_resource(VlTestedSamplesByTestReason, "/hiv/vl/laboratories/tested_samples_by_test_reason/")
    # Legacy: GET /lab_samples_tested_pregnant
    api.add_resource(VlTestedSamplesPregnant, "/hiv/vl/laboratories/tested_samples_pregnant/")
    # Legacy: GET /lab_samples_tested_breastfeeding
    api.add_resource(VlTestedSamplesBreastfeeding, "/hiv/vl/laboratories/tested_samples_breastfeeding/")
    # Legacy: GET /lab_samples_rejected
    api.add_resource(VlRejectedSamples, "/hiv/vl/laboratories/rejected_samples/")
    # Legacy: GET /lab_samples_rejected_by_month
    api.add_resource(VlRejectedSamplesByMonth, "/hiv/vl/laboratories/rejected_samples_by_month/")
    # Legacy: GET /lab_tat
    api.add_resource(VlTatByLab, "/hiv/vl/laboratories/tat_by_lab/")
    # Legacy: GET /lab_tat_by_month
    api.add_resource(VlTatByMonth, "/hiv/vl/laboratories/tat_by_month/")
    # Legacy: GET /suppression
    api.add_resource(VlSuppression, "/hiv/vl/laboratories/suppression/")
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_vl_laboratory.py -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add hiv/vl/ tests/hiv/test_vl_laboratory.py
git commit -m "feat: implement VL laboratory endpoints (15 routes) with tests"
```

---

## Task 5: VL Facility Endpoints — Services, Controllers & Tests

**Files:**
- Modify: `hiv/vl/services/vl_services_facilities.py`
- Modify: `hiv/vl/controllers/vl_controller_facility.py`
- Create: `tests/hiv/test_vl_facility.py`
- Modify: `hiv/vl/routes.py` (add facility routes)

- [ ] **Step 1: Write failing tests for VL facility endpoints**

File: `tests/hiv/test_vl_facility.py`

Follow same pattern as `test_vl_laboratory.py` but test these 14 routes:
- `/hiv/vl/facilities/registered_samples/`
- `/hiv/vl/facilities/tested_samples_by_month/`
- `/hiv/vl/facilities/tested_samples_by_facility/`
- `/hiv/vl/facilities/tested_samples_by_gender/`
- `/hiv/vl/facilities/tested_samples_by_gender_by_facility/`
- `/hiv/vl/facilities/tested_samples_by_age/`
- `/hiv/vl/facilities/tested_samples_by_age_by_facility/`
- `/hiv/vl/facilities/tested_samples_by_test_reason/`
- `/hiv/vl/facilities/tested_samples_pregnant/`
- `/hiv/vl/facilities/tested_samples_breastfeeding/`
- `/hiv/vl/facilities/rejected_samples_by_month/`
- `/hiv/vl/facilities/rejected_samples_by_facility/`
- `/hiv/vl/facilities/tat_by_month/`
- `/hiv/vl/facilities/tat_by_facility/`

Each test mocks the corresponding service function and verifies 200 response.

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_vl_facility.py -v`
Expected: FAIL

- [ ] **Step 3: Implement VL facility services**

File: `hiv/vl/services/vl_services_facilities.py`

14 service functions following same pattern as laboratory services but using `Requesting*` columns instead of `Testing*`:
- Filter on `RequestingProvinceName`, `RequestingDistrictName`, `RequestingFacilityName`
- Group by requesting facility hierarchy
- Supports disaggregation (province→district, district→facility)

- [ ] **Step 4: Implement VL facility controllers**

File: `hiv/vl/controllers/vl_controller_facility.py`

14 Resource classes: `VlFacilityRegisteredSamples`, `VlFacilityTestedSamplesByMonth`, etc. Same pattern as laboratory controllers.

- [ ] **Step 5: Register facility routes in routes.py**

Add to `hiv/vl/routes.py`:

```python
    # Facility Endpoints
    # Legacy: GET /clinic_registered_samples_by_facility
    api.add_resource(VlFacilityRegisteredSamples, "/hiv/vl/facilities/registered_samples/")
    # Legacy: GET /clinic_samples_tested_by_month
    api.add_resource(VlFacilityTestedSamplesByMonth, "/hiv/vl/facilities/tested_samples_by_month/")
    # Legacy: GET /clinic_samples_tested_by_facility
    api.add_resource(VlFacilityTestedSamplesByFacility, "/hiv/vl/facilities/tested_samples_by_facility/")
    # Legacy: GET /clinic_samples_tested_by_gender
    api.add_resource(VlFacilityTestedSamplesByGender, "/hiv/vl/facilities/tested_samples_by_gender/")
    # Legacy: GET /clinic_samples_tested_by_gender_and_facility
    api.add_resource(VlFacilityTestedSamplesByGenderByFacility, "/hiv/vl/facilities/tested_samples_by_gender_by_facility/")
    # Legacy: GET /clinic_samples_tested_by_age
    api.add_resource(VlFacilityTestedSamplesByAge, "/hiv/vl/facilities/tested_samples_by_age/")
    # Legacy: GET /clinic_samples_tested_by_age_and_facility
    api.add_resource(VlFacilityTestedSamplesByAgeByFacility, "/hiv/vl/facilities/tested_samples_by_age_by_facility/")
    # Legacy: GET /clinic_samples_by_test_reason
    api.add_resource(VlFacilityTestedSamplesByTestReason, "/hiv/vl/facilities/tested_samples_by_test_reason/")
    # Legacy: GET /clinic_tests_by_pregnancy
    api.add_resource(VlFacilityTestedSamplesPregnant, "/hiv/vl/facilities/tested_samples_pregnant/")
    # Legacy: GET /clinic_tests_by_breastfeeding
    api.add_resource(VlFacilityTestedSamplesBreastfeeding, "/hiv/vl/facilities/tested_samples_breastfeeding/")
    # Legacy: GET /clinic_samples_rejected_by_month
    api.add_resource(VlFacilityRejectedSamplesByMonth, "/hiv/vl/facilities/rejected_samples_by_month/")
    # Legacy: GET /clinic_samples_rejected_by_facility
    api.add_resource(VlFacilityRejectedSamplesByFacility, "/hiv/vl/facilities/rejected_samples_by_facility/")
    # Legacy: GET /clinic_tat
    api.add_resource(VlFacilityTatByMonth, "/hiv/vl/facilities/tat_by_month/")
    # Legacy: GET /clinic_tat_by_facility
    api.add_resource(VlFacilityTatByFacility, "/hiv/vl/facilities/tat_by_facility/")
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_vl_facility.py -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add hiv/vl/ tests/hiv/test_vl_facility.py
git commit -m "feat: implement VL facility endpoints (14 routes) with tests"
```

---

## Task 6: VL Summary Endpoints — Services, Controllers & Tests

**Files:**
- Modify: `hiv/vl/services/vl_services_summary.py`
- Modify: `hiv/vl/controllers/vl_controller_summary.py`
- Create: `tests/hiv/test_vl_summary.py`
- Modify: `hiv/vl/routes.py` (add summary routes)

- [ ] **Step 1: Write failing tests for VL summary endpoints**

File: `tests/hiv/test_vl_summary.py`

Test these 6 routes:
- `/hiv/vl/summary/header_indicators/`
- `/hiv/vl/summary/number_of_samples/`
- `/hiv/vl/summary/viral_suppression/`
- `/hiv/vl/summary/tat/`
- `/hiv/vl/summary/suppression_by_province/`
- `/hiv/vl/summary/samples_history/`

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_vl_summary.py -v`

- [ ] **Step 3: Implement VL summary services**

File: `hiv/vl/services/vl_services_summary.py`

6 service functions:
1. `header_indicators_service(req_args)` — Counts: registered, tested, suppressed, not_suppressed, rejected
2. `number_of_samples_service(req_args)` — Monthly sample counts
3. `viral_suppression_service(req_args)` — Monthly suppression trend
4. `tat_service(req_args)` — TAT summary (4 segments)
5. `suppression_by_province_service(req_args)` — Suppression grouped by province (for map)
6. `samples_history_service(req_args)` — Historical sample counts

- [ ] **Step 4: Implement VL summary controllers**

File: `hiv/vl/controllers/vl_controller_summary.py`

6 Resource classes following the standard pattern.

- [ ] **Step 5: Register summary routes**

Add to `hiv/vl/routes.py`:

```python
    # Summary/Dashboard Endpoints
    # Legacy: GET /dash_indicators
    api.add_resource(VlSummaryHeaderIndicators, "/hiv/vl/summary/header_indicators/")
    # Legacy: GET /dash_number_of_samples
    api.add_resource(VlSummaryNumberOfSamples, "/hiv/vl/summary/number_of_samples/")
    # Legacy: GET /dash_viral_suppression
    api.add_resource(VlSummaryViralSuppression, "/hiv/vl/summary/viral_suppression/")
    # Legacy: GET /dash_tat
    api.add_resource(VlSummaryTat, "/hiv/vl/summary/tat/")
    # Legacy: GET /dash_map
    api.add_resource(VlSummarySuppressionByProvince, "/hiv/vl/summary/suppression_by_province/")
    # Legacy: GET /sampleshistory
    api.add_resource(VlSummarySamplesHistory, "/hiv/vl/summary/samples_history/")
```

- [ ] **Step 6: Run all VL tests**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_vl_*.py -v`
Expected: All PASS

- [ ] **Step 7: Commit**

```bash
git add hiv/vl/ tests/hiv/test_vl_summary.py
git commit -m "feat: implement VL summary endpoints (6 routes) with tests"
```

---

## Task 7: EID Model — Create EIDMaster

**Files:**
- Create: `hiv/eid/__init__.py`
- Create: `hiv/eid/models/__init__.py`
- Create: `hiv/eid/models/eid_master_model.py`
- Create: `hiv/eid/controllers/__init__.py`
- Create: `hiv/eid/services/__init__.py`

- [ ] **Step 1: Create EID package structure**

Create empty `__init__.py` files:
- `hiv/eid/__init__.py`
- `hiv/eid/models/__init__.py`
- `hiv/eid/controllers/__init__.py`
- `hiv/eid/services/__init__.py`

- [ ] **Step 2: Create EIDMaster model**

File: `hiv/eid/models/eid_master_model.py`

```python
from db.database import db


class EIDMaster(db.Model):
    __bind_key__ = "dpi"
    __tablename__ = "EIDMaster"
    __table_args__ = {"extend_existing": True}

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RequestID = db.Column(db.String(26), nullable=True)

    # Patient demographics
    SURNAME = db.Column(db.String(100), nullable=True)
    FIRSTNAME = db.Column(db.String(100), nullable=True)
    DOB = db.Column(db.DateTime, nullable=True)
    AgeInYears = db.Column(db.Integer, nullable=True)
    AgeInDays = db.Column(db.Integer, nullable=True)
    HL7SexCode = db.Column(db.String(10), nullable=True)
    NATIONALID = db.Column(db.String(50), nullable=True)
    NATIONALITY = db.Column(db.String(50), nullable=True)

    # Clinical info
    ClinicalInfo = db.Column(db.String(500), nullable=True)
    RapidHivTest = db.Column(db.String(50), nullable=True)
    PcrPreviouslyDone = db.Column(db.String(50), nullable=True)
    PtvChild = db.Column(db.String(50), nullable=True)
    PtvMother = db.Column(db.String(50), nullable=True)
    BreastfeedingInfo = db.Column(db.String(50), nullable=True)

    # Specimen
    SpecimenDatetime = db.Column(db.DateTime, nullable=True)
    LIMSSpecimenSourceCode = db.Column(db.String(20), nullable=True)
    LIMSSpecimenSourceDesc = db.Column(db.String(200), nullable=True)
    CollectionVolume = db.Column(db.String(50), nullable=True)

    # Results
    PCR_Result = db.Column(db.String(100), nullable=True)
    POC_Result = db.Column(db.String(100), nullable=True)
    Viral_Load_Result = db.Column(db.String(100), nullable=True)
    CAPCTM = db.Column(db.String(100), nullable=True)
    LogValue = db.Column(db.String(50), nullable=True)
    IsPoc = db.Column(db.String(10), nullable=True)
    HL7ResultStatusCode = db.Column(db.String(10), nullable=True)

    # Rejection
    LIMSRejectionCode = db.Column(db.String(20), nullable=True)
    LIMSRejectionDesc = db.Column(db.String(200), nullable=True)
    ResultLIMSRejectionCode = db.Column(db.String(20), nullable=True)
    ResultLIMSRejectionDesc = db.Column(db.String(200), nullable=True)

    # Requesting facility
    RequestingFacilityCode = db.Column(db.String(50), nullable=True)
    RequestingFacilityName = db.Column(db.String(200), nullable=True)
    RequestingProvinceName = db.Column(db.String(100), nullable=True)
    RequestingDistrictName = db.Column(db.String(100), nullable=True)
    RequestingLatitude = db.Column(db.String(50), nullable=True)
    RequestingLongitude = db.Column(db.String(50), nullable=True)

    # Receiving facility
    ReceivingFacilityCode = db.Column(db.String(50), nullable=True)
    ReceivingFacilityName = db.Column(db.String(200), nullable=True)
    ReceivingProvinceName = db.Column(db.String(100), nullable=True)
    ReceivingDistrictName = db.Column(db.String(100), nullable=True)

    # Testing facility
    TestingFacilityCode = db.Column(db.String(50), nullable=True)
    TestingFacilityName = db.Column(db.String(200), nullable=True)
    TestingProvinceName = db.Column(db.String(100), nullable=True)
    TestingDistrictName = db.Column(db.String(100), nullable=True)
    TestingLatitude = db.Column(db.String(50), nullable=True)
    TestingLongitude = db.Column(db.String(50), nullable=True)

    # LIMS facility
    LIMSFacilityCode = db.Column(db.String(50), nullable=True)
    LIMSFacilityName = db.Column(db.String(200), nullable=True)

    # Result-prefixed columns (used in queries)
    ResultRequestingFacilityName = db.Column(db.String(200), nullable=True)
    ResultRequestingProvinceName = db.Column(db.String(100), nullable=True)
    ResultRequestingDistrictName = db.Column(db.String(100), nullable=True)
    ResultTestingFacilityCode = db.Column(db.String(50), nullable=True)
    ResultTestingFacilityName = db.Column(db.String(200), nullable=True)
    ResultSpecimenDatetime = db.Column(db.DateTime, nullable=True)
    ResultRegisteredDateTime = db.Column(db.DateTime, nullable=True)
    ResultReceivedDatetime = db.Column(db.DateTime, nullable=True)
    ResultAnalysisDateTime = db.Column(db.DateTime, nullable=True)
    ResultAuthorisedDateTime = db.Column(db.DateTime, nullable=True)
    ResultLIMSAnalyzerCode = db.Column(db.String(50), nullable=True)
    ResultLIMSAnalyzerName = db.Column(db.String(100), nullable=True)

    # Timeline dates
    RegisteredDateTime = db.Column(db.DateTime, nullable=True)
    ReceivedDateTime = db.Column(db.DateTime, nullable=True)
    AnalysisDateTime = db.Column(db.DateTime, nullable=True)
    AuthorisedDateTime = db.Column(db.DateTime, nullable=True)

    # Hub/Pre-registration
    LIMSPreReg_ReceivedDateTime = db.Column(db.DateTime, nullable=True)
    LIMSPreReg_RegistrationDateTime = db.Column(db.DateTime, nullable=True)
    LIMSPreReg_RegistrationFacilityCode = db.Column(db.String(50), nullable=True)
    HubLatitude = db.Column(db.String(50), nullable=True)
    HubLongitude = db.Column(db.String(50), nullable=True)

    # DISA flags
    IS_DISALINK = db.Column(db.String(10), nullable=True)
    IS_DISAPOC = db.Column(db.String(10), nullable=True)
```

- [ ] **Step 3: Commit**

```bash
git add hiv/eid/
git commit -m "feat: create EID module structure with EIDMaster model"
```

---

## Task 8: EID Laboratory Endpoints — Services, Controllers & Tests

**Files:**
- Create: `hiv/eid/services/eid_services_laboratory.py`
- Create: `hiv/eid/controllers/eid_controller_laboratory.py`
- Modify: `hiv/eid/routes.py` (replace stub from Task 1 with actual routes)
- Create: `tests/hiv/test_eid_laboratory.py`

- [ ] **Step 1: Write failing tests for EID laboratory endpoints**

File: `tests/hiv/test_eid_laboratory.py`

Test these 11 routes (each with mock service, verify 200 status):
- `/hiv/eid/laboratories/tested_samples_by_month/`
- `/hiv/eid/laboratories/registered_samples_by_month/`
- `/hiv/eid/laboratories/tested_samples/`
- `/hiv/eid/laboratories/tat/`
- `/hiv/eid/laboratories/tat_samples/`
- `/hiv/eid/laboratories/rejected_samples/`
- `/hiv/eid/laboratories/rejected_samples_by_month/`
- `/hiv/eid/laboratories/samples_by_equipment/`
- `/hiv/eid/laboratories/samples_by_equipment_by_month/`
- `/hiv/eid/laboratories/sample_routes/`
- `/hiv/eid/laboratories/sample_routes_viewport/`

Also test `lab_type` parameter filtering: verify that `lab_type=conventional`, `lab_type=poc`, and `lab_type=all` are accepted.

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_eid_laboratory.py -v`

- [ ] **Step 3: Implement EID laboratory services**

File: `hiv/eid/services/eid_services_laboratory.py`

11 service functions. Key differences from VL:
- Uses `EIDMaster` model with `__bind_key__ = 'dpi'`
- Uses `ResultTestingFacilityName` (Result-prefixed) for lab grouping
- Uses `ResultAnalysisDateTime` for tested status
- Uses `LAB_TYPE_EID()` to filter by `IsPoc` field
- Uses `POSITIVITY()` instead of `SUPPRESSION()`
- TAT has 6 segments (includes hub steps): collection→hubReceive→hubRegister→labReceive→labRegister→analysis→validation
- Equipment counting uses `EQUIPMENT_COUNT()` for CAPCTM, ALINITY, M2000, C6800, PANTHER, MPIMA, MANUAL
- Sample routes return geographic coordinates

Template for EID service:

```python
from hiv.eid.models.eid_master_model import EIDMaster
from utilities.utils import *
from sqlalchemy import and_, or_, func, case


def tested_samples_by_month_service(req_args):
    """Retrieve tested samples grouped by month, filtered by lab_type."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS(req_args)
    lab_type = req_args.get("lab_type") or "all"

    filters = [
        EIDMaster.ResultRegisteredDateTime.between(dates[0], dates[1]),
        EIDMaster.ResultAnalysisDateTime.is_not(None),
    ]

    # Apply lab_type filter
    lab_filter = LAB_TYPE_EID(EIDMaster, lab_type)
    if lab_filter is not None:
        filters.append(lab_filter)

    # Apply facility filters
    if facilities:
        if facility_type == "province":
            filters.append(EIDMaster.ResultRequestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(EIDMaster.ResultRequestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(EIDMaster.ResultRequestingFacilityName.in_(facilities))

    try:
        query = EIDMaster.query.with_entities(
            YEAR(EIDMaster.ResultAnalysisDateTime),
            MONTH(EIDMaster.ResultAnalysisDateTime),
            DATE_PART("month", EIDMaster.ResultAnalysisDateTime),
            TOTAL_ALL,
            POSITIVITY(EIDMaster.PCR_Result, "Pos").label("positive"),
            POSITIVITY(EIDMaster.PCR_Result, "Neg").label("negative"),
            func.count(case((EIDMaster.HL7SexCode == "F", 1))).label("female"),
            func.count(case((EIDMaster.HL7SexCode == "M", 1))).label("male"),
        ).filter(
            and_(*filters)
        ).group_by(
            YEAR(EIDMaster.ResultAnalysisDateTime),
            MONTH(EIDMaster.ResultAnalysisDateTime),
            DATE_PART("month", EIDMaster.ResultAnalysisDateTime),
        ).order_by(
            YEAR(EIDMaster.ResultAnalysisDateTime),
            MONTH(EIDMaster.ResultAnalysisDateTime),
        )

        data = query.all()
        return [
            dict(
                year=row.year,
                month=row.month,
                month_name=row.month_name,
                total=row.total,
                positive=row.positive,
                negative=row.negative,
                female=row.female,
                male=row.male,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}
```

- [ ] **Step 4: Implement EID laboratory controllers**

File: `hiv/eid/controllers/eid_controller_laboratory.py`

11 Resource classes. Use `_parse_eid_common_args()` which extends `_parse_common_args()` with `lab_type` and `category` parameters:

```python
def _parse_eid_common_args():
    """Parse standardized query parameters for EID endpoints."""
    parser = reqparse.RequestParser()
    parser.add_argument("interval_dates", type=lambda x: x, location="args", action="append")
    parser.add_argument("province", type=lambda x: x, location="args", action="append")
    parser.add_argument("district", type=lambda x: x, location="args", action="append")
    parser.add_argument("health_facility", type=str, location="args")
    parser.add_argument("facility_type", type=str, location="args")
    parser.add_argument("disaggregation", type=str, location="args")
    parser.add_argument("lab_type", type=str, location="args", default="all")
    parser.add_argument("category", type=int, location="args")
    parser.add_argument("viewport", type=str, location="args")
    return parser.parse_args()
```

- [ ] **Step 5: Create EID routes.py with laboratory endpoints**

File: `hiv/eid/routes.py`

```python
from hiv.eid.controllers.eid_controller_laboratory import *


def eid_routes(api):
    """
    Registers the routes for HIV EID API endpoints.
    """
    # Laboratory Endpoints
    # Legacy: GET /eid/lab/all/samples_tested_by_month + /eid/lab/conventional/samples_tested_by_month + /eid/lab/poc/samples_tested_by_month
    api.add_resource(EidTestedSamplesByMonth, "/hiv/eid/laboratories/tested_samples_by_month/")
    # Legacy: GET /eid/lab/all/samples_registered_by_month
    api.add_resource(EidRegisteredSamplesByMonth, "/hiv/eid/laboratories/registered_samples_by_month/")
    # Legacy: GET /eid/lab/conventional/samples_tested + /eid/lab/poc/samples_tested
    api.add_resource(EidTestedSamples, "/hiv/eid/laboratories/tested_samples/")
    # Legacy: GET /eid/lab/conventional/tat + /eid/lab/poc/tat
    api.add_resource(EidTat, "/hiv/eid/laboratories/tat/")
    # Legacy: GET /eid/lab/tat_samples
    api.add_resource(EidTatSamples, "/hiv/eid/laboratories/tat_samples/")
    # Legacy: GET /eid/lab/rejected_samples
    api.add_resource(EidRejectedSamples, "/hiv/eid/laboratories/rejected_samples/")
    # Legacy: GET /eid/lab/rejected_samples_monthly
    api.add_resource(EidRejectedSamplesByMonth, "/hiv/eid/laboratories/rejected_samples_by_month/")
    # Legacy: GET /eid/lab/samples_by_equipment
    api.add_resource(EidSamplesByEquipment, "/hiv/eid/laboratories/samples_by_equipment/")
    # Legacy: GET /eid/lab/samples_by_equipment_monthly
    api.add_resource(EidSamplesByEquipmentByMonth, "/hiv/eid/laboratories/samples_by_equipment_by_month/")
    # Legacy: GET /eid/lab/sample_routes
    api.add_resource(EidSampleRoutes, "/hiv/eid/laboratories/sample_routes/")
    # Legacy: GET /eid/lab/sample_routes_viewport
    api.add_resource(EidSampleRoutesViewport, "/hiv/eid/laboratories/sample_routes_viewport/")
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_eid_laboratory.py -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add hiv/eid/ tests/hiv/test_eid_laboratory.py
git commit -m "feat: implement EID laboratory endpoints (11 routes) with tests"
```

---

## Task 9: EID Facility Endpoints — Services, Controllers & Tests

**Files:**
- Create: `hiv/eid/services/eid_services_facilities.py`
- Create: `hiv/eid/controllers/eid_controller_facility.py`
- Create: `tests/hiv/test_eid_facility.py`
- Modify: `hiv/eid/routes.py`

- [ ] **Step 1: Write failing tests for EID facility endpoints**

Test these 14 routes:
- `/hiv/eid/facilities/registered_samples/`
- `/hiv/eid/facilities/registered_samples_by_month/`
- `/hiv/eid/facilities/tested_samples/`
- `/hiv/eid/facilities/tested_samples_by_month/`
- `/hiv/eid/facilities/tested_samples_by_gender/`
- `/hiv/eid/facilities/tested_samples_by_gender_by_month/`
- `/hiv/eid/facilities/tat_avg_by_month/`
- `/hiv/eid/facilities/tat_avg/`
- `/hiv/eid/facilities/tat_days_by_month/`
- `/hiv/eid/facilities/tat_days/`
- `/hiv/eid/facilities/rejected_samples_by_month/`
- `/hiv/eid/facilities/rejected_samples/`
- `/hiv/eid/facilities/key_indicators/`
- `/hiv/eid/facilities/tested_samples_by_age/`

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Implement EID facility services**

Key EID facility-specific patterns:
- TAT avg endpoints use `DATE_DIFF_AVG()` for all 6 hub segments
- TAT days endpoints bucket into time brackets: <7 days, 7-15 days, 16-21 days, >21 days
- Key indicators endpoint returns comprehensive metrics filtered by `lab_type`
- Gender endpoints count `HL7SexCode` F/M with positivity breakdown

- [ ] **Step 4: Implement EID facility controllers**

14 Resource classes following the EID controller pattern with `_parse_eid_common_args()`.

- [ ] **Step 5: Register facility routes**

Add to `hiv/eid/routes.py`:

```python
    # Facility Endpoints
    # Legacy: GET /eid/clinic/samples_registered_province
    api.add_resource(EidFacilityRegisteredSamples, "/hiv/eid/facilities/registered_samples/")
    # Legacy: GET /eid/clinic/samples_registered_month
    api.add_resource(EidFacilityRegisteredSamplesByMonth, "/hiv/eid/facilities/registered_samples_by_month/")
    # Legacy: GET /eid/clinic/samples_tested_province
    api.add_resource(EidFacilityTestedSamples, "/hiv/eid/facilities/tested_samples/")
    # Legacy: GET /eid/clinic/samples_tested_month
    api.add_resource(EidFacilityTestedSamplesByMonth, "/hiv/eid/facilities/tested_samples_by_month/")
    # Legacy: GET /eid/clinic/samples_tested_gender_province
    api.add_resource(EidFacilityTestedSamplesByGender, "/hiv/eid/facilities/tested_samples_by_gender/")
    # Legacy: GET /eid/clinic/samples_tested_gender_month
    api.add_resource(EidFacilityTestedSamplesByGenderByMonth, "/hiv/eid/facilities/tested_samples_by_gender_by_month/")
    # Legacy: GET /eid/clinic/samples_tat_avg_month
    api.add_resource(EidFacilityTatAvgByMonth, "/hiv/eid/facilities/tat_avg_by_month/")
    # Legacy: GET /eid/clinic/samples_tat_avg_province
    api.add_resource(EidFacilityTatAvg, "/hiv/eid/facilities/tat_avg/")
    # Legacy: GET /eid/clinic/samples_tat_days_month
    api.add_resource(EidFacilityTatDaysByMonth, "/hiv/eid/facilities/tat_days_by_month/")
    # Legacy: GET /eid/clinic/samples_tat_days_province
    api.add_resource(EidFacilityTatDays, "/hiv/eid/facilities/tat_days/")
    # Legacy: GET /eid/clinic/samples_rejected_by_month
    api.add_resource(EidFacilityRejectedSamplesByMonth, "/hiv/eid/facilities/rejected_samples_by_month/")
    # Legacy: GET /eid/clinic/samples_rejected_by_facility
    api.add_resource(EidFacilityRejectedSamples, "/hiv/eid/facilities/rejected_samples/")
    # Legacy: GET /eid/clinic/conventional/key_indicators + /eid/clinic/poc/key_indicators
    api.add_resource(EidFacilityKeyIndicators, "/hiv/eid/facilities/key_indicators/")
    # Derived from clinic data
    api.add_resource(EidFacilityTestedSamplesByAge, "/hiv/eid/facilities/tested_samples_by_age/")
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_eid_facility.py -v`

- [ ] **Step 7: Commit**

```bash
git add hiv/eid/ tests/hiv/test_eid_facility.py
git commit -m "feat: implement EID facility endpoints (14 routes) with tests"
```

---

## Task 10: EID Summary Endpoints — Services, Controllers & Tests

**Files:**
- Create: `hiv/eid/services/eid_services_summary.py`
- Create: `hiv/eid/controllers/eid_controller_summary.py`
- Create: `tests/hiv/test_eid_summary.py`
- Modify: `hiv/eid/routes.py`

- [ ] **Step 1: Write failing tests for EID summary endpoints**

Test these 10 routes:
- `/hiv/eid/summary/indicators/`
- `/hiv/eid/summary/tat/`
- `/hiv/eid/summary/tat_samples/`
- `/hiv/eid/summary/positivity/`
- `/hiv/eid/summary/number_of_samples/`
- `/hiv/eid/summary/indicators_by_province/`
- `/hiv/eid/summary/samples_positivity/`
- `/hiv/eid/summary/rejected_samples_by_month/`
- `/hiv/eid/summary/samples_by_equipment/`
- `/hiv/eid/summary/samples_by_equipment_by_month/`

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Implement EID summary services**

10 service functions. Key EID summary patterns:
- `indicators_service()` — Returns registered, tested, rejected, pending counts (filtered by `lab_type`)
- `positivity_service()` — Monthly positivity rate (positive / tested * 100)
- `indicators_by_province_service()` — Provincial breakdown with conventional/POC split
- Equipment endpoints use `EQUIPMENT_COUNT()` for each equipment type

- [ ] **Step 4: Implement EID summary controllers**

10 Resource classes following the EID controller pattern.

- [ ] **Step 5: Register summary routes**

Add to `hiv/eid/routes.py`:

```python
    # Summary/Dashboard Endpoints
    # Legacy: GET /eid/dash/pcr/indicators + /eid/dash/poc/indicators
    api.add_resource(EidSummaryIndicators, "/hiv/eid/summary/indicators/")
    # Legacy: GET /eid/dash/pcr/tat
    api.add_resource(EidSummaryTat, "/hiv/eid/summary/tat/")
    # Legacy: GET /eid/dash/pcr/tat_samples
    api.add_resource(EidSummaryTatSamples, "/hiv/eid/summary/tat_samples/")
    # Legacy: GET /eid/dash/pcr/positivity + /eid/dash/poc/positivity
    api.add_resource(EidSummaryPositivity, "/hiv/eid/summary/positivity/")
    # Legacy: GET /eid/dash/pcr/number_of_samples + /eid/dash/poc/number_of_samples
    api.add_resource(EidSummaryNumberOfSamples, "/hiv/eid/summary/number_of_samples/")
    # Legacy: GET /eid/dash/indicators_by_province
    api.add_resource(EidSummaryIndicatorsByProvince, "/hiv/eid/summary/indicators_by_province/")
    # Legacy: GET /eid/dash/samples_positivity
    api.add_resource(EidSummarySamplesPositivity, "/hiv/eid/summary/samples_positivity/")
    # Legacy: GET /eid/dash/rejected_samples_monthly
    api.add_resource(EidSummaryRejectedSamplesByMonth, "/hiv/eid/summary/rejected_samples_by_month/")
    # Legacy: GET /eid/dash/samples_by_equipment
    api.add_resource(EidSummarySamplesByEquipment, "/hiv/eid/summary/samples_by_equipment/")
    # Legacy: GET /eid/dash/samples_by_equipment_monthly
    api.add_resource(EidSummarySamplesByEquipmentByMonth, "/hiv/eid/summary/samples_by_equipment_by_month/")
```

- [ ] **Step 6: Run all EID tests**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/hiv/test_eid_*.py -v`
Expected: All PASS

- [ ] **Step 7: Commit**

```bash
git add hiv/eid/ tests/hiv/test_eid_summary.py
git commit -m "feat: implement EID summary endpoints (10 routes) with tests"
```

---

## Task 11: App Integration & Final Wiring

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Update app.py to register EID routes**

Add EID route import and registration:

```python
from hiv.eid.routes import eid_routes
```

And in the route registration section:

```python
vl_routes(api)
eid_routes(api)         # NEW
tb_gxpert_routes(api)
dict_routes(api)
authentication_routes(api)
```

- [ ] **Step 2: Run the full test suite**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/ -v --tb=short`
Expected: All tests PASS

- [ ] **Step 3: Verify app starts without errors**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -c "from app import app; print('App loaded successfully. Routes:', len([rule for rule in app.url_map.iter_rules()]))"`
Expected: App loads, prints route count (should be ~120+ including all modules)

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "feat: register EID routes in main app, complete VL/EID migration"
```

---

## Task 12: Run Full Test Suite & Coverage Report

- [ ] **Step 1: Run all tests with coverage**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -m pytest tests/ -v --cov=hiv --cov-report=term-missing`
Expected: All tests PASS, coverage report shows hiv/vl and hiv/eid modules

- [ ] **Step 2: Fix any failing tests**

If any tests fail, investigate and fix the root cause. Do not skip or disable tests.

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "test: full test suite passing with coverage for VL and EID migration"
```

---

## Task 13: Swagger/OpenAPI Documentation Update

**Files:**
- Modify: `utilities/swagger.py`

- [ ] **Step 1: Add VL and EID parameter definitions to swagger template**

In `utilities/swagger.py`, add to the `parameters` section:

```python
# VL-specific parameters
"ViralLoadResultCategory": {
    "name": "result_category",
    "in": "query",
    "type": "string",
    "enum": ["Suppressed", "Not Suppressed", "All"],
    "description": "Filter by viral load result category",
},
"ReasonForTest": {
    "name": "reason_for_test",
    "in": "query",
    "type": "string",
    "enum": ["Routine", "Suspected treatment failure", "Reason Not Specified", "All"],
    "description": "Filter by reason for test",
},
# EID-specific parameters
"LabTypeParameter": {
    "name": "lab_type",
    "in": "query",
    "type": "string",
    "enum": ["conventional", "poc", "all"],
    "default": "all",
    "description": "Filter by test type (PCR conventional vs Point of Care)",
},
"TATCategoryParameter": {
    "name": "category",
    "in": "query",
    "type": "integer",
    "enum": [0, 1, 2, 3, 4, 5],
    "description": "TAT segment: 0=Collection→HubReceive, 1=HubReceive→HubRegister, 2=HubRegister→LabReceive, 3=LabReceive→LabRegister, 4=LabRegister→Analysis, 5=Analysis→Validation",
},
"ViewportParameter": {
    "name": "viewport",
    "in": "query",
    "type": "string",
    "description": "JSON viewport for map filtering: {lat:{low,high},lng:{low,high}}",
},
```

Also add VL and EID tags to the swagger template:

```python
"tags": [
    # ... existing tags
    {"name": "HIV Viral Load/Laboratories", "description": "VL Laboratory-level analytics"},
    {"name": "HIV Viral Load/Facilities", "description": "VL Facility-level analytics"},
    {"name": "HIV Viral Load/Summary", "description": "VL Dashboard summary"},
    {"name": "HIV EID/Laboratories", "description": "EID Laboratory-level analytics"},
    {"name": "HIV EID/Facilities", "description": "EID Facility-level analytics"},
    {"name": "HIV EID/Summary", "description": "EID Dashboard summary"},
]
```

- [ ] **Step 2: Verify Swagger UI loads correctly**

Run: `cd /home/vagner/Documents/Projects/APHL/openldr/api_openldr_python && python -c "from utilities.swagger import swagger_template; print('Swagger template loaded. Tags:', len(swagger_template.get('tags', [])))"`

- [ ] **Step 3: Commit**

```bash
git add utilities/swagger.py
git commit -m "docs: add VL and EID parameter definitions to Swagger template"
```

---

## Testing Notes (applies to all test tasks)

**All test files must include these common tests:**

1. **401 Auth test**: Each test file should include a test verifying that unauthenticated requests return 401:
   ```python
   def test_unauthenticated_returns_401(self, client):
       response = client.get("/hiv/vl/laboratories/registered_samples/")
       assert response.status_code == 401
   ```

2. **200 with mock**: Each endpoint gets a test with mocked service and valid auth headers.

3. **Response structure**: At least one test per test file verifying the JSON response shape (field names and types).

**All controller classes must include `@jwt_required()` decorator** on their `get()` method. Import with:
```python
from flask_jwt_extended import jwt_required
```
