from hiv.eid.controllers.eid_controller_laboratory import *
from hiv.eid.controllers.eid_controller_facility import *


def eid_routes(api):
    """Registers the routes for HIV EID API endpoints."""
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
