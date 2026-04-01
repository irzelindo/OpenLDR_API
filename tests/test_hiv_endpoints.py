"""
Integration test script for HIV VL and EID endpoints.
Tests database connectivity and endpoint responses against the live databases.
"""
import os
import sys
import json
import time

# Set environment variables BEFORE importing the app
os.environ["FLASK_SECRET_KEY"] = "test-secret-key-for-testing"
os.environ["CDR_DOMAIN"] = "disamoz.org.mz"
os.environ["LOCAL_DOMAIN"] = "disamoz.org.mz"
os.environ["DB_USER"] = "sa"
os.environ["DB_PASSWORD"] = "disalab"
os.environ["DB_VL_DATA"] = "viralloaddata"
os.environ["DB_VL_SMS"] = "viralloaddata"  # VlData model uses vlSMS bind
os.environ["DB_DPI"] = "eiddata"
# Placeholder values for unused databases (won't be queried)
os.environ["DB_HIV_AD"] = "hivad_placeholder"
os.environ["DB_TB_DATA"] = "tbdata_placeholder"
os.environ["DB_DICT"] = "dict_placeholder"
os.environ["DB_USERS"] = "users_placeholder"

# Add the project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


def get_test_token():
    """Generate a test JWT token for accessing protected endpoints."""
    from flask_jwt_extended import create_access_token
    with app.app_context():
        return create_access_token(
            identity="test_user",
            additional_claims={
                "user_id": 1,
                "user_name": "test_user",
                "first_name": "Test",
                "last_name": "User",
                "email_address": "test@test.com",
                "role": "Admin",
            }
        )


def test_endpoint(client, token, url, params=None, label=None):
    """Test a single endpoint and report results."""
    label = label or url
    headers = {"Authorization": f"Bearer {token}"}
    query_string = params or {}

    try:
        start = time.time()
        response = client.get(url, query_string=query_string, headers=headers)
        elapsed = round(time.time() - start, 2)

        status = response.status_code
        try:
            data = response.get_json()
        except Exception:
            data = response.data.decode("utf-8")[:200]

        # Determine result
        if status == 200:
            if isinstance(data, list):
                result = f"OK - {len(data)} records ({elapsed}s)"
            elif isinstance(data, dict) and "error" in data:
                result = f"ERROR (in response) - {data.get('error', '')[:100]} ({elapsed}s)"
            elif isinstance(data, dict):
                result = f"OK - dict with {len(data)} keys ({elapsed}s)"
            else:
                result = f"OK - {type(data).__name__} ({elapsed}s)"
        else:
            error_msg = ""
            if isinstance(data, dict):
                error_msg = data.get("message", data.get("msg", str(data)))[:100]
            result = f"FAIL ({status}) - {error_msg} ({elapsed}s)"

        print(f"  {'PASS' if status == 200 and not (isinstance(data, dict) and 'error' in data) else 'FAIL'} | {label} => {result}")
        return status == 200 and not (isinstance(data, dict) and "error" in data)
    except Exception as e:
        print(f"  FAIL | {label} => EXCEPTION: {str(e)[:150]}")
        return False


def main():
    # Default date range: last 12 months
    default_params = {
        "interval_dates": json.dumps(["2025-01-01", "2026-03-25"]),
    }

    client = app.test_client()
    token = get_test_token()

    passed = 0
    failed = 0
    total = 0

    # =========================================================================
    # TEST 1: Database Connectivity
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST: Database Connectivity")
    print("=" * 70)

    with app.app_context():
        from db.database import db

        # Test VL database (vlSMS bind)
        try:
            result = db.session.execute(
                db.text("SELECT 1"),
                bind_arguments={"bind_key": "vlSMS" if "vlSMS" in app.config.get("SQLALCHEMY_BINDS", {}) else "vl"}
            )
            print("  PASS | VL Database (vlSMS) - Connection successful")
            passed += 1
        except Exception as e:
            print(f"  FAIL | VL Database (vlSMS) - {str(e)[:150]}")
            failed += 1
        total += 1

        # Test EID database (dpi bind)
        try:
            result = db.session.execute(
                db.text("SELECT 1"),
                bind_arguments={"bind_key": "dpi"}
            )
            print("  PASS | EID Database (dpi) - Connection successful")
            passed += 1
        except Exception as e:
            print(f"  FAIL | EID Database (dpi) - {str(e)[:150]}")
            failed += 1
        total += 1

        # Test VL table exists
        try:
            result = db.session.execute(
                db.text("SELECT TOP 1 * FROM VlData"),
                bind_arguments={"bind_key": "vlSMS" if "vlSMS" in app.config.get("SQLALCHEMY_BINDS", {}) else "vl"}
            )
            print("  PASS | VlData table - Exists and accessible")
            passed += 1
        except Exception as e:
            print(f"  FAIL | VlData table - {str(e)[:150]}")
            failed += 1
        total += 1

        # Test EID table exists
        try:
            result = db.session.execute(
                db.text("SELECT TOP 1 * FROM EIDMaster"),
                bind_arguments={"bind_key": "dpi"}
            )
            print("  PASS | EIDMaster table - Exists and accessible")
            passed += 1
        except Exception as e:
            print(f"  FAIL | EIDMaster table - {str(e)[:150]}")
            failed += 1
        total += 1

    # =========================================================================
    # TEST 2: HIV VL Laboratory Endpoints
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST: HIV VL Laboratory Endpoints")
    print("=" * 70)

    vl_lab_endpoints = [
        "/hiv/vl/laboratories/registered_samples/",
        "/hiv/vl/laboratories/registered_samples_by_month/",
        "/hiv/vl/laboratories/tested_samples/",
        "/hiv/vl/laboratories/tested_samples_by_month/",
        "/hiv/vl/laboratories/tested_samples_by_gender/",
        "/hiv/vl/laboratories/tested_samples_by_gender_by_lab/",
        "/hiv/vl/laboratories/tested_samples_by_age/",
        "/hiv/vl/laboratories/tested_samples_by_test_reason/",
        "/hiv/vl/laboratories/tested_samples_pregnant/",
        "/hiv/vl/laboratories/tested_samples_breastfeeding/",
        "/hiv/vl/laboratories/rejected_samples/",
        "/hiv/vl/laboratories/rejected_samples_by_month/",
        "/hiv/vl/laboratories/tat_by_lab/",
        "/hiv/vl/laboratories/tat_by_month/",
        "/hiv/vl/laboratories/suppression/",
    ]

    for ep in vl_lab_endpoints:
        total += 1
        if test_endpoint(client, token, ep, default_params):
            passed += 1
        else:
            failed += 1

    # =========================================================================
    # TEST 3: HIV VL Facility Endpoints
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST: HIV VL Facility Endpoints")
    print("=" * 70)

    vl_fac_endpoints = [
        "/hiv/vl/facilities/registered_samples/",
        "/hiv/vl/facilities/tested_samples_by_month/",
        "/hiv/vl/facilities/tested_samples_by_facility/",
        "/hiv/vl/facilities/tested_samples_by_gender/",
        "/hiv/vl/facilities/tested_samples_by_gender_by_facility/",
        "/hiv/vl/facilities/tested_samples_by_age/",
        "/hiv/vl/facilities/tested_samples_by_age_by_facility/",
        "/hiv/vl/facilities/tested_samples_by_test_reason/",
        "/hiv/vl/facilities/tested_samples_pregnant/",
        "/hiv/vl/facilities/tested_samples_breastfeeding/",
        "/hiv/vl/facilities/rejected_samples_by_month/",
        "/hiv/vl/facilities/rejected_samples_by_facility/",
        "/hiv/vl/facilities/tat_by_month/",
        "/hiv/vl/facilities/tat_by_facility/",
    ]

    for ep in vl_fac_endpoints:
        total += 1
        if test_endpoint(client, token, ep, default_params):
            passed += 1
        else:
            failed += 1

    # =========================================================================
    # TEST 4: HIV VL Summary Endpoints
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST: HIV VL Summary Endpoints")
    print("=" * 70)

    vl_summary_endpoints = [
        "/hiv/vl/summary/header_indicators/",
        "/hiv/vl/summary/number_of_samples/",
        "/hiv/vl/summary/viral_suppression/",
        "/hiv/vl/summary/tat/",
        "/hiv/vl/summary/suppression_by_province/",
        "/hiv/vl/summary/samples_history/",
    ]

    for ep in vl_summary_endpoints:
        total += 1
        if test_endpoint(client, token, ep, default_params):
            passed += 1
        else:
            failed += 1

    # =========================================================================
    # TEST 5: HIV EID Laboratory Endpoints
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST: HIV EID Laboratory Endpoints")
    print("=" * 70)

    eid_lab_endpoints = [
        "/hiv/eid/laboratories/tested_samples_by_month/",
        "/hiv/eid/laboratories/registered_samples_by_month/",
        "/hiv/eid/laboratories/tested_samples/",
        "/hiv/eid/laboratories/tat/",
        "/hiv/eid/laboratories/tat_samples/",
        "/hiv/eid/laboratories/rejected_samples/",
        "/hiv/eid/laboratories/rejected_samples_by_month/",
        "/hiv/eid/laboratories/samples_by_equipment/",
        "/hiv/eid/laboratories/samples_by_equipment_by_month/",
        "/hiv/eid/laboratories/sample_routes/",
        "/hiv/eid/laboratories/sample_routes_viewport/",
    ]

    for ep in eid_lab_endpoints:
        total += 1
        if test_endpoint(client, token, ep, default_params):
            passed += 1
        else:
            failed += 1

    # =========================================================================
    # TEST 6: HIV EID Facility Endpoints
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST: HIV EID Facility Endpoints")
    print("=" * 70)

    eid_fac_endpoints = [
        "/hiv/eid/facilities/registered_samples/",
        "/hiv/eid/facilities/registered_samples_by_month/",
        "/hiv/eid/facilities/tested_samples/",
        "/hiv/eid/facilities/tested_samples_by_month/",
        "/hiv/eid/facilities/tested_samples_by_gender/",
        "/hiv/eid/facilities/tested_samples_by_gender_by_month/",
        "/hiv/eid/facilities/tat_avg_by_month/",
        "/hiv/eid/facilities/tat_avg/",
        "/hiv/eid/facilities/tat_days_by_month/",
        "/hiv/eid/facilities/tat_days/",
        "/hiv/eid/facilities/rejected_samples_by_month/",
        "/hiv/eid/facilities/rejected_samples/",
        "/hiv/eid/facilities/key_indicators/",
        "/hiv/eid/facilities/tested_samples_by_age/",
    ]

    for ep in eid_fac_endpoints:
        total += 1
        if test_endpoint(client, token, ep, default_params):
            passed += 1
        else:
            failed += 1

    # =========================================================================
    # TEST 7: HIV EID Summary Endpoints
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST: HIV EID Summary Endpoints")
    print("=" * 70)

    eid_summary_endpoints = [
        "/hiv/eid/summary/indicators/",
        "/hiv/eid/summary/tat/",
        "/hiv/eid/summary/tat_samples/",
        "/hiv/eid/summary/positivity/",
        "/hiv/eid/summary/number_of_samples/",
        "/hiv/eid/summary/indicators_by_province/",
        "/hiv/eid/summary/samples_positivity/",
        "/hiv/eid/summary/rejected_samples_by_month/",
        "/hiv/eid/summary/samples_by_equipment/",
        "/hiv/eid/summary/samples_by_equipment_by_month/",
    ]

    for ep in eid_summary_endpoints:
        total += 1
        if test_endpoint(client, token, ep, default_params):
            passed += 1
        else:
            failed += 1

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{total} passed, {failed}/{total} failed")
    print("=" * 70)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
