import pytest
from unittest.mock import patch


TB_SUMMARY_ENDPOINTS = [
    (
        "/tb/gx/summary/summary_header_component/",
        "dashboard_header_component_summary_service",
        [{"Registered_Samples_Ultra_6_Cores": 120, "Registered_Samples_XDR_10_Cores": 40}],
    ),
    (
        "/tb/gx/summary/positivity_by_month/",
        "dashboard_summary_positivity_by_month_service",
        [{"Month": 1, "Month_Name": "January", "Year": 2024, "Registered_Samples": 50}],
    ),
    (
        "/tb/gx/summary/positivity_by_lab/",
        "dashboard_summary_positivity_by_lab_service",
        [{"Lab_Name": "Lab A", "Registered_Samples": 50, "Detected_Samples": 10}],
    ),
    (
        "/tb/gx/summary/positivity_by_lab_by_age/",
        "dashboard_summary_positivity_by_lab_by_age_service",
        [{"0-4": {"Registered_Samples": 5, "Detected_Samples": 1}}],
    ),
    (
        "/tb/gx/summary/sample_types_by_month/",
        "dashboard_summary_sample_types_by_month_by_age_service",
        [{"Month": 1, "Month_Name": "January", "Year": 2024, "Specimen_Types": {}}],
    ),
    (
        "/tb/gx/summary/sample_types_by_facility_by_age/",
        "dashboard_summary_sample_types_by_facility_by_age_service",
        [{"Facility": "Clinic A", "0_4": {"sputum": 2}}],
    ),
]


class TestTbSummaryEndpoints:
    @pytest.mark.parametrize("url,service_name,mock_data", TB_SUMMARY_ENDPOINTS)
    def test_endpoint_returns_200(self, client, auth_headers, url, service_name, mock_data):
        with patch(
            f"tb.gxpert.controllers.tb_gx_controller_summary.{service_name}",
            return_value=mock_data,
        ):
            response = client.get(url, headers=auth_headers)
            assert response.status_code == 200

    @pytest.mark.parametrize("url,service_name,mock_data", TB_SUMMARY_ENDPOINTS)
    def test_endpoint_returns_401_without_auth(self, client, url, service_name, mock_data):
        response = client.get(url)
        assert response.status_code == 401
