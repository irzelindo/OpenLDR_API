"""
Tests for TB GeneXpert Summary/Dashboard endpoints (6 routes).

Each test mocks the corresponding service function imported by
``tb.gxpert.controllers.tb_gx_controller_summary`` and verifies a 200
response.
"""
import pytest
from unittest.mock import patch


# ---------------------------------------------------------------------------
# Endpoint definitions: (url, service_function_name, mock_response)
# Names must match the symbols imported by tb_gx_controller_summary.py.
# ---------------------------------------------------------------------------
TB_SUMMARY_ENDPOINTS = [
    (
        "/tb/gx/summary/summary_header_component/",
        "dashboard_header_component_summary_service",
        [{"registered": 5000, "tested": 4500,
          "positive": 700, "rejected": 120}],
    ),
    (
        "/tb/gx/summary/positivity_by_month/",
        "dashboard_summary_positivity_by_month_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "total": 450, "positive": 70, "positivity": 0.155}],
    ),
    (
        "/tb/gx/summary/positivity_by_lab/",
        "dashboard_summary_positivity_by_lab_service",
        [{"testing_facility": "Lab A",
          "total": 480, "positive": 70, "positivity": 0.145}],
    ),
    (
        "/tb/gx/summary/positivity_by_lab_by_age/",
        "dashboard_summary_positivity_by_lab_by_age_service",
        [{"testing_facility": "Lab A", "age_group": "15-19",
          "positive": 5, "total": 25}],
    ),
    (
        "/tb/gx/summary/sample_types_by_month/",
        "dashboard_summary_sample_types_by_month_by_age_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "age_group": "15-19", "sputum": 20, "blood": 5}],
    ),
    (
        "/tb/gx/summary/sample_types_by_facility_by_age/",
        "dashboard_summary_sample_types_by_facility_by_age_service",
        [{"requesting_facility": "Health Center A",
          "age_group": "15-19", "sputum": 20, "blood": 5}],
    ),
]


class TestTbSummaryEndpoints:
    """Smoke-test all 6 TB GeneXpert summary endpoints."""

    @pytest.mark.parametrize("url,service_name,mock_data", TB_SUMMARY_ENDPOINTS)
    def test_endpoint_returns_200(self, client, auth_headers, url, service_name, mock_data):
        with patch(
            f"tb.gxpert.controllers.tb_gx_controller_summary.{service_name}",
            return_value=mock_data,
        ):
            response = client.get(url, headers=auth_headers)
            assert response.status_code == 200

    @pytest.mark.parametrize("url,service_name,mock_data", TB_SUMMARY_ENDPOINTS)
    def test_endpoint_returns_json(self, client, auth_headers, url, service_name, mock_data):
        with patch(
            f"tb.gxpert.controllers.tb_gx_controller_summary.{service_name}",
            return_value=mock_data,
        ):
            response = client.get(url, headers=auth_headers)
            assert response.get_json() is not None


class TestTbSummaryPositivityByMonthResponse:
    """Test response structure for positivity_by_month endpoint."""

    def test_response_has_expected_keys(self, client, auth_headers):
        mock_data = [
            {"year": 2024, "month": 1, "month_name": "January",
             "total": 450, "positive": 70, "positivity": 0.155},
        ]
        with patch(
            "tb.gxpert.controllers.tb_gx_controller_summary.dashboard_summary_positivity_by_month_service",
            return_value=mock_data,
        ):
            response = client.get(
                "/tb/gx/summary/positivity_by_month/",
                headers=auth_headers,
            )
            row = response.get_json()[0]
            assert {"year", "month", "positive", "total"}.issubset(row.keys())
