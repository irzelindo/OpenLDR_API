"""
Tests for TB GeneXpert Patients endpoints (4 routes).

Each test mocks the corresponding service function imported by
``tb.gxpert.controllers.tb_gx_controller_patients`` and verifies a 200
response. The patient endpoints return a paginated payload of the form::

    {
        "status": "success",
        "page": 1,
        "per_page": 50,
        "total_count": N,
        "total_pages": M,
        "data": [...]
    }
"""
import pytest
from unittest.mock import patch


def _paginated(rows, page=1, per_page=50):
    """Build the standard paginated envelope returned by patient services."""
    return {
        "status": "success",
        "page": page,
        "per_page": per_page,
        "total_count": len(rows),
        "total_pages": 1,
        "data": rows,
    }


SAMPLE_PATIENT = {
    "RequestID": "REQ-001",
    "FIRSTNAME": "John",
    "SURNAME": "Doe",
    "AgeInYears": 35,
    "HL7SexCode": "M",
    "RequestingFacilityName": "Health Center A",
    "FinalResult": "MTB Detected",
}


# ---------------------------------------------------------------------------
# Endpoint definitions: (url, service_function_name, query_string, mock_response)
# Each patient endpoint requires a different mandatory parameter so we send
# valid query strings to avoid validation 400s.
# ---------------------------------------------------------------------------
TB_PATIENT_ENDPOINTS = [
    (
        "/tb/gx/patients/by_name/",
        "get_patients_by_name_service",
        {"first_name": "John"},
        _paginated([SAMPLE_PATIENT]),
    ),
    (
        "/tb/gx/patients/by_facility/",
        "get_patients_by_facility_service",
        {"health_facility": "Health Center A"},
        _paginated([SAMPLE_PATIENT]),
    ),
    (
        "/tb/gx/patients/by_sample_type/",
        "get_patients_by_sample_type_service",
        {"sample_type": "sputum"},
        _paginated([SAMPLE_PATIENT]),
    ),
    (
        "/tb/gx/patients/by_result_type/",
        "get_patients_by_result_type_service",
        {"result_type": "detected"},
        _paginated([SAMPLE_PATIENT]),
    ),
]


class TestTbPatientsEndpoints:
    """Smoke-test the 4 TB GeneXpert patient endpoints."""

    @pytest.mark.parametrize(
        "url,service_name,query_string,mock_data", TB_PATIENT_ENDPOINTS
    )
    def test_endpoint_returns_200(
        self, client, auth_headers, url, service_name, query_string, mock_data
    ):
        with patch(
            f"tb.gxpert.controllers.tb_gx_controller_patients.{service_name}",
            return_value=mock_data,
        ):
            response = client.get(
                url, headers=auth_headers, query_string=query_string
            )
            assert response.status_code == 200

    @pytest.mark.parametrize(
        "url,service_name,query_string,mock_data", TB_PATIENT_ENDPOINTS
    )
    def test_endpoint_returns_paginated_envelope(
        self, client, auth_headers, url, service_name, query_string, mock_data
    ):
        with patch(
            f"tb.gxpert.controllers.tb_gx_controller_patients.{service_name}",
            return_value=mock_data,
        ):
            response = client.get(
                url, headers=auth_headers, query_string=query_string
            )
            data = response.get_json()
            assert isinstance(data, dict)
            assert {"status", "page", "per_page", "total_count", "total_pages", "data"}.issubset(
                data.keys()
            )
            assert isinstance(data["data"], list)


class TestTbPatientsQueryParameters:
    """Verify pagination + filter parameters are forwarded into the service."""

    def test_service_receives_pagination_and_filters(self, client, auth_headers):
        captured = {}

        def fake_service(req_args):
            captured.update(req_args)
            return _paginated([])

        with patch(
            "tb.gxpert.controllers.tb_gx_controller_patients.get_patients_by_name_service",
            side_effect=fake_service,
        ):
            client.get(
                "/tb/gx/patients/by_name/",
                headers=auth_headers,
                query_string={
                    "first_name": "John",
                    "surname": "Doe",
                    "page": "2",
                    "per_page": "25",
                },
            )

        assert captured.get("first_name") == "John"
        assert captured.get("surname") == "Doe"
        assert captured.get("page") == 2
        assert captured.get("per_page") == 25
