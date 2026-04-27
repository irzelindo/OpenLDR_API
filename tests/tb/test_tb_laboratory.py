"""
Tests for TB GeneXpert Laboratory endpoints (16 routes).

Each test mocks the corresponding service function imported by
``tb.gxpert.controllers.tb_gx_controller_laboratory`` and verifies a 200
response with the expected JSON list shape.
"""
import pytest
from unittest.mock import patch


# ---------------------------------------------------------------------------
# Endpoint definitions: (url, service_function_name, mock_response)
# Names must match the symbols imported by tb_gx_controller_laboratory.py.
# ---------------------------------------------------------------------------
TB_LAB_ENDPOINTS = [
    (
        "/tb/gx/laboratories/registered_samples/",
        "registered_samples_by_lab_service",
        [{"testing_facility": "Lab A", "total": 500}],
    ),
    (
        "/tb/gx/laboratories/tested_samples/",
        "tested_samples_by_lab_service",
        [{"testing_facility": "Lab A",
          "total": 480, "positive": 70, "negative": 380}],
    ),
    (
        "/tb/gx/laboratories/registered_samples_by_month/",
        "registered_samples_by_lab_by_month_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "testing_facility": "Lab A", "total": 500}],
    ),
    (
        "/tb/gx/laboratories/tested_samples_by_month/",
        "tested_samples_by_lab_by_month_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "testing_facility": "Lab A", "total": 480}],
    ),
    (
        "/tb/gx/laboratories/tested_samples_by_sample_types/",
        "tested_samples_by_sample_types_by_laboratory_service",
        [{"testing_facility": "Lab A",
          "sputum": 350, "feces": 20, "urine": 10, "blood": 100}],
    ),
    (
        "/tb/gx/laboratories/tested_samples_by_sample_types_by_month/",
        "tested_samples_by_samples_types_by_laboratory_by_month_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "testing_facility": "Lab A", "sputum": 350}],
    ),
    (
        "/tb/gx/laboratories/rejected_samples/",
        "rejected_samples_by_lab_service",
        [{"testing_facility": "Lab A", "total": 25}],
    ),
    (
        "/tb/gx/laboratories/rejected_samples_by_month/",
        "rejected_samples_by_lab_by_month_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "testing_facility": "Lab A", "total": 25}],
    ),
    (
        "/tb/gx/laboratories/rejected_samples_by_reason/",
        "rejected_samples_by_lab_by_reason_service",
        [{"testing_facility": "Lab A",
          "reason": "Insufficient sample", "total": 10}],
    ),
    (
        "/tb/gx/laboratories/rejected_samples_by_reason_by_month/",
        "rejected_samples_by_lab_by_reason_by_month_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "testing_facility": "Lab A",
          "reason": "Insufficient sample", "total": 10}],
    ),
    (
        "/tb/gx/laboratories/tested_samples_by_drug_type/",
        "tested_samples_by_lab_by_drug_type_service",
        [{"testing_facility": "Lab A",
          "rifampicin": 70, "isoniazid": 12, "fluoroquinolona": 4}],
    ),
    (
        "/tb/gx/laboratories/tested_samples_by_drug_type_by_month/",
        "tested_samples_by_lab_by_drug_type_by_month_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "testing_facility": "Lab A", "rifampicin": 70}],
    ),
    (
        "/tb/gx/laboratories/trl_samples_by_lab_in_days/",
        "trl_samples_by_lab_by_days_service",
        [{"testing_facility": "Lab A",
          "0_2_days": 200, "3_5_days": 180, "6_10_days": 80, "above_10_days": 20}],
    ),
    (
        "/tb/gx/laboratories/trl_samples_by_lab_in_days_by_month/",
        "trl_samples_by_lab_by_days_by_month_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "testing_facility": "Lab A", "0_2_days": 200, "3_5_days": 180}],
    ),
    (
        "/tb/gx/laboratories/trl_samples_avg_by_days/",
        "trl_samples_avg_by_lab_service",
        [{"testing_facility": "Lab A", "avg_days": 3.6}],
    ),
    (
        "/tb/gx/laboratories/trl_samples_avg_by_days_by_month/",
        "trl_samples_avg_by_lab_month_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "testing_facility": "Lab A", "avg_days": 3.6}],
    ),
]


class TestTbLaboratoryEndpoints:
    """Smoke-test all 16 TB GeneXpert laboratory endpoints."""

    @pytest.mark.parametrize("url,service_name,mock_data", TB_LAB_ENDPOINTS)
    def test_endpoint_returns_200(self, client, auth_headers, url, service_name, mock_data):
        with patch(
            f"tb.gxpert.controllers.tb_gx_controller_laboratory.{service_name}",
            return_value=mock_data,
        ):
            response = client.get(url, headers=auth_headers)
            assert response.status_code == 200

    @pytest.mark.parametrize("url,service_name,mock_data", TB_LAB_ENDPOINTS)
    def test_endpoint_returns_json_list(self, client, auth_headers, url, service_name, mock_data):
        with patch(
            f"tb.gxpert.controllers.tb_gx_controller_laboratory.{service_name}",
            return_value=mock_data,
        ):
            response = client.get(url, headers=auth_headers)
            data = response.get_json()
            assert isinstance(data, list)
            assert len(data) > 0


class TestTbLabRejectedReasonResponse:
    """Test response structure for rejected_samples_by_reason endpoint."""

    def test_response_has_expected_keys(self, client, auth_headers):
        mock_data = [
            {"testing_facility": "Lab A",
             "reason": "Insufficient sample", "total": 10},
        ]
        with patch(
            "tb.gxpert.controllers.tb_gx_controller_laboratory.rejected_samples_by_lab_by_reason_service",
            return_value=mock_data,
        ):
            response = client.get(
                "/tb/gx/laboratories/rejected_samples_by_reason/",
                headers=auth_headers,
            )
            row = response.get_json()[0]
            assert {"testing_facility", "reason", "total"}.issubset(row.keys())
