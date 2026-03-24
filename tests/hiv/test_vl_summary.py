"""
Tests for VL Summary/Dashboard endpoints (6 routes).
Each test mocks the corresponding service function at the controller layer
and verifies a 200 response with expected data structure.
"""
import pytest
from unittest.mock import patch


# ---------------------------------------------------------------------------
# Endpoint definitions: (url, service_function_name, mock_response)
# ---------------------------------------------------------------------------
VL_SUMMARY_ENDPOINTS = [
    (
        "/hiv/vl/summary/header_indicators/",
        "header_indicators_service",
        {"registered": 5000, "tested": 4500, "suppressed": 3800,
         "not_suppressed": 700, "rejected": 120},
    ),
    (
        "/hiv/vl/summary/number_of_samples/",
        "number_of_samples_service",
        [{"year": 2024, "month": 1, "month_name": "January", "total": 450}],
    ),
    (
        "/hiv/vl/summary/viral_suppression/",
        "viral_suppression_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "suppressed": 360, "not_suppressed": 60}],
    ),
    (
        "/hiv/vl/summary/tat/",
        "tat_service",
        [{"year": 2024, "month": 1, "month_name": "January",
          "collection_reception": 2.5, "reception_registration": 1.0,
          "registration_analysis": 0.5, "analysis_validation": 0.3}],
    ),
    (
        "/hiv/vl/summary/suppression_by_province/",
        "suppression_by_province_service",
        [{"province": "Maputo", "suppressed": 1200, "not_suppressed": 200}],
    ),
    (
        "/hiv/vl/summary/samples_history/",
        "samples_history_service",
        [{"year": 2023, "month": 6, "month_name": "June", "total": 380}],
    ),
]


class TestVlSummaryEndpoints:
    """Test all 6 VL summary endpoints return 200 with mocked service."""

    @pytest.mark.parametrize("url,service_name,mock_data", VL_SUMMARY_ENDPOINTS)
    def test_endpoint_returns_200(self, client, auth_headers, url, service_name, mock_data):
        """Each endpoint should return 200 when authenticated and service returns data."""
        with patch(
            f"hiv.vl.controllers.vl_controller_summary.{service_name}",
            return_value=mock_data,
        ):
            response = client.get(url, headers=auth_headers)
            assert response.status_code == 200

    @pytest.mark.parametrize("url,service_name,mock_data", VL_SUMMARY_ENDPOINTS)
    def test_endpoint_returns_401_without_auth(self, client, url, service_name, mock_data):
        """Each endpoint should return 401 when no JWT token is provided."""
        response = client.get(url)
        assert response.status_code == 401


class TestVlSummaryHeaderIndicatorsResponse:
    """Test response structure for header_indicators endpoint."""

    def test_response_is_dict_with_expected_keys(self, client, auth_headers):
        mock_data = {
            "registered": 5000,
            "tested": 4500,
            "suppressed": 3800,
            "not_suppressed": 700,
            "rejected": 120,
        }
        with patch(
            "hiv.vl.controllers.vl_controller_summary.header_indicators_service",
            return_value=mock_data,
        ):
            response = client.get(
                "/hiv/vl/summary/header_indicators/",
                headers=auth_headers,
            )
            data = response.get_json()
            assert isinstance(data, dict)
            expected_keys = {"registered", "tested", "suppressed", "not_suppressed", "rejected"}
            assert expected_keys == set(data.keys())


class TestVlSummaryNumberOfSamplesResponse:
    """Test response structure for number_of_samples endpoint."""

    def test_response_is_list_with_expected_keys(self, client, auth_headers):
        mock_data = [{"year": 2024, "month": 1, "month_name": "January", "total": 450}]
        with patch(
            "hiv.vl.controllers.vl_controller_summary.number_of_samples_service",
            return_value=mock_data,
        ):
            response = client.get(
                "/hiv/vl/summary/number_of_samples/",
                headers=auth_headers,
            )
            data = response.get_json()
            assert isinstance(data, list)
            assert len(data) > 0
            row = data[0]
            expected_keys = {"year", "month", "month_name", "total"}
            assert expected_keys == set(row.keys())


class TestVlSummaryViralSuppressionResponse:
    """Test response structure for viral_suppression endpoint."""

    def test_response_is_list_with_expected_keys(self, client, auth_headers):
        mock_data = [
            {"year": 2024, "month": 1, "month_name": "January",
             "suppressed": 360, "not_suppressed": 60}
        ]
        with patch(
            "hiv.vl.controllers.vl_controller_summary.viral_suppression_service",
            return_value=mock_data,
        ):
            response = client.get(
                "/hiv/vl/summary/viral_suppression/",
                headers=auth_headers,
            )
            data = response.get_json()
            assert isinstance(data, list)
            assert len(data) > 0
            row = data[0]
            expected_keys = {"year", "month", "month_name", "suppressed", "not_suppressed"}
            assert expected_keys == set(row.keys())


class TestVlSummaryTatResponse:
    """Test response structure for tat endpoint."""

    def test_response_is_list_with_expected_keys(self, client, auth_headers):
        mock_data = [
            {"year": 2024, "month": 1, "month_name": "January",
             "collection_reception": 2.5, "reception_registration": 1.0,
             "registration_analysis": 0.5, "analysis_validation": 0.3}
        ]
        with patch(
            "hiv.vl.controllers.vl_controller_summary.tat_service",
            return_value=mock_data,
        ):
            response = client.get(
                "/hiv/vl/summary/tat/",
                headers=auth_headers,
            )
            data = response.get_json()
            assert isinstance(data, list)
            assert len(data) > 0
            row = data[0]
            expected_keys = {
                "year", "month", "month_name",
                "collection_reception", "reception_registration",
                "registration_analysis", "analysis_validation",
            }
            assert expected_keys == set(row.keys())


class TestVlSummarySuppressionByProvinceResponse:
    """Test response structure for suppression_by_province endpoint."""

    def test_response_is_list_with_expected_keys(self, client, auth_headers):
        mock_data = [{"province": "Maputo", "suppressed": 1200, "not_suppressed": 200}]
        with patch(
            "hiv.vl.controllers.vl_controller_summary.suppression_by_province_service",
            return_value=mock_data,
        ):
            response = client.get(
                "/hiv/vl/summary/suppression_by_province/",
                headers=auth_headers,
            )
            data = response.get_json()
            assert isinstance(data, list)
            assert len(data) > 0
            row = data[0]
            expected_keys = {"province", "suppressed", "not_suppressed"}
            assert expected_keys == set(row.keys())


class TestVlSummarySamplesHistoryResponse:
    """Test response structure for samples_history endpoint."""

    def test_response_is_list_with_expected_keys(self, client, auth_headers):
        mock_data = [{"year": 2023, "month": 6, "month_name": "June", "total": 380}]
        with patch(
            "hiv.vl.controllers.vl_controller_summary.samples_history_service",
            return_value=mock_data,
        ):
            response = client.get(
                "/hiv/vl/summary/samples_history/",
                headers=auth_headers,
            )
            data = response.get_json()
            assert isinstance(data, list)
            assert len(data) > 0
            row = data[0]
            expected_keys = {"year", "month", "month_name", "total"}
            assert expected_keys == set(row.keys())
