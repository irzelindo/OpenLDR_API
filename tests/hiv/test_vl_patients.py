"""
Tests for VL patient endpoint query contracts.
"""

from hiv.vl.services.vl_services_patients import VL_PATIENT_ENTITIES


def test_vl_patient_entities_include_serializer_fields():
    """Selected VL patient columns must match fields used by process_patients."""
    entity_names = {entity.key for entity in VL_PATIENT_ENTITIES}

    assert "FinalViralLoadResult" in entity_names
    assert "HL7ResultStatusCode" in entity_names
