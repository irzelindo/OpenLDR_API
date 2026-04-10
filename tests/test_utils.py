import pytest
from unittest.mock import MagicMock
from sqlalchemy import Column, String, DateTime, Integer


def test_positivity_returns_case_expression():
    """POSITIVITY should return a CASE WHEN expression for counting positive results."""
    from utilities.utils import POSITIVITY

    mock_field = Column("PCR_Result", String)
    result = POSITIVITY(mock_field, "Positive")
    assert result is not None


def test_process_common_params_extracts_standard_params():
    """PROCESS_COMMON_PARAMS should extract interval_dates, province, facility_type, disaggregation."""
    from utilities.utils import PROCESS_COMMON_PARAMS_VL

    req_args = {
        "interval_dates": ["2024-01-01", "2024-12-31"],
        "province": ["Maputo", "Sofala"],
        "district": None,
        "health_facility": None,
        "facility_type": "province",
        "disaggregation": "True",
    }
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)
    assert dates == ["2024-01-01", "2024-12-31"]
    assert facilities == ["Maputo", "Sofala"]
    assert facility_type == "province"
    assert disaggregation is True
    assert health_facility is None


def test_process_common_params_defaults():
    """PROCESS_COMMON_PARAMS should handle missing/None parameters gracefully."""
    from utilities.utils import PROCESS_COMMON_PARAMS_VL

    req_args = {
        "interval_dates": None,
        "province": None,
        "district": None,
        "health_facility": None,
        "facility_type": None,
        "disaggregation": None,
    }
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)
    assert len(dates) == 2
    assert facility_type == "province"
    assert disaggregation is False
    assert facilities == []


def test_process_common_params_district():
    """PROCESS_COMMON_PARAMS should extract district facilities when facility_type is district."""
    from utilities.utils import PROCESS_COMMON_PARAMS_VL

    req_args = {
        "interval_dates": ["2024-01-01", "2024-12-31"],
        "province": None,
        "district": ["Beira", "Dondo"],
        "health_facility": None,
        "facility_type": "district",
        "disaggregation": "False",
    }
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)
    assert facilities == ["Beira", "Dondo"]
    assert facility_type == "district"


def test_lab_type_eid_poc():
    """LAB_TYPE_EID should filter for POC when lab_type is 'poc'."""
    from utilities.utils import LAB_TYPE_EID

    class MockModel:
        IsPoc = Column("IsPoc", String)

    result = LAB_TYPE_EID(MockModel, "poc")
    assert result is not None


def test_lab_type_eid_all():
    """LAB_TYPE_EID should return None when lab_type is 'all'."""
    from utilities.utils import LAB_TYPE_EID

    class MockModel:
        IsPoc = Column("IsPoc", String)

    result = LAB_TYPE_EID(MockModel, "all")
    assert result is None
