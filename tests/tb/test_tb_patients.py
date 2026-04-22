import pytest
from unittest.mock import patch


TB_PATIENT_ENDPOINTS = [
    (
        "/tb/gx/patients/by_name/",
        "get_patients_by_name_service",
        {"status": "success", "data": [{"request_id": "REQ-1"}]},
    ),
    (
        "/tb/gx/patients/by_facility/",
        "get_patients_by_facility_service",
        {"status": "success", "data": [{"request_id": "REQ-2"}]},
    ),
    (
        "/tb/gx/patients/by_sample_type/?sample_type=sputum",
        "get_patients_by_sample_type_service",
        {"status": "success", "data": [{"request_id": "REQ-3"}]},
    ),
    (
        "/tb/gx/patients/by_result_type/?result_type=detected",
        "get_patients_by_result_type_service",
        {"status": "success", "data": [{"request_id": "REQ-4"}]},
    ),
]


class TestTbPatientEndpoints:
    @pytest.mark.parametrize("url,service_name,mock_data", TB_PATIENT_ENDPOINTS)
    def test_endpoint_returns_200(self, client, auth_headers, url, service_name, mock_data):
        with patch(
            f"tb.gxpert.controllers.tb_gx_controller_patients.{service_name}",
            return_value=mock_data,
        ):
            response = client.get(url, headers=auth_headers)
            assert response.status_code == 200

    @pytest.mark.parametrize("url,service_name,mock_data", TB_PATIENT_ENDPOINTS)
    def test_endpoint_returns_401_without_auth(self, client, url, service_name, mock_data):
        response = client.get(url)
        assert response.status_code == 401
