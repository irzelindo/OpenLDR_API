from hiv.vl.controllers.vl_controller_laboratory import (
    VlRegisteredSamples,
    VlRegisteredSamplesByMonth,
    VlTestedSamples,
    VlTestedSamplesByMonth,
    VlTestedSamplesByGender,
    VlTestedSamplesByGenderByLab,
    VlTestedSamplesByAge,
    VlTestedSamplesByTestReason,
    VlTestedSamplesPregnant,
    VlTestedSamplesBreastfeeding,
    VlRejectedSamples,
    VlRejectedSamplesByMonth,
    VlTatByLab,
    VlTatByMonth,
    VlSuppression,
)
from hiv.vl.controllers.vl_controller_facility import (
    VlFacilityRegisteredSamples,
    VlFacilityTestedSamplesByMonth,
    VlFacilityTestedSamplesByFacility,
    VlFacilityTestedSamplesByGender,
    VlFacilityTestedSamplesByGenderByFacility,
    VlFacilityTestedSamplesByAge,
    VlFacilityTestedSamplesByAgeByFacility,
    VlFacilityTestedSamplesByTestReason,
    VlFacilityTestedSamplesPregnant,
    VlFacilityTestedSamplesBreastfeeding,
    VlFacilityRejectedSamplesByMonth,
    VlFacilityRejectedSamplesByFacility,
    VlFacilityTatByMonth,
    VlFacilityTatByFacility,
)
from hiv.vl.controllers.vl_controller_summary import (
    VlSummaryHeaderIndicators,
    VlSummaryNumberOfSamples,
    VlSummaryViralSuppression,
    VlSummaryTat,
    VlSummarySuppressionByProvince,
    VlSummarySamplesHistory,
)


def vl_routes(api):
    """
    Registers the routes for HIV Viral Load API endpoints.
    """
    # Laboratory Endpoints
    # Legacy: GET /samples
    api.add_resource(VlRegisteredSamples, "/hiv/vl/laboratories/registered_samples/")
    # Legacy: GET /lab_samples_tested_by_month (partial - registered)
    api.add_resource(VlRegisteredSamplesByMonth, "/hiv/vl/laboratories/registered_samples_by_month/")
    # Legacy: GET /lab_samples_tested_by_lab
    api.add_resource(VlTestedSamples, "/hiv/vl/laboratories/tested_samples/")
    # Legacy: GET /lab_samples_tested_by_month
    api.add_resource(VlTestedSamplesByMonth, "/hiv/vl/laboratories/tested_samples_by_month/")
    # Legacy: GET /lab_samples_tested_by_gender
    api.add_resource(VlTestedSamplesByGender, "/hiv/vl/laboratories/tested_samples_by_gender/")
    # Legacy: GET /lab_samples_tested_by_gender_and_labs
    api.add_resource(VlTestedSamplesByGenderByLab, "/hiv/vl/laboratories/tested_samples_by_gender_by_lab/")
    # Legacy: GET /lab_samples_tested_by_age
    api.add_resource(VlTestedSamplesByAge, "/hiv/vl/laboratories/tested_samples_by_age/")
    # Legacy: GET /lab_samples_by_test_reason
    api.add_resource(VlTestedSamplesByTestReason, "/hiv/vl/laboratories/tested_samples_by_test_reason/")
    # Legacy: GET /lab_samples_tested_pregnant
    api.add_resource(VlTestedSamplesPregnant, "/hiv/vl/laboratories/tested_samples_pregnant/")
    # Legacy: GET /lab_samples_tested_breastfeeding
    api.add_resource(VlTestedSamplesBreastfeeding, "/hiv/vl/laboratories/tested_samples_breastfeeding/")
    # Legacy: GET /lab_samples_rejected
    api.add_resource(VlRejectedSamples, "/hiv/vl/laboratories/rejected_samples/")
    # Legacy: GET /lab_samples_rejected_by_month
    api.add_resource(VlRejectedSamplesByMonth, "/hiv/vl/laboratories/rejected_samples_by_month/")
    # Legacy: GET /lab_tat
    api.add_resource(VlTatByLab, "/hiv/vl/laboratories/tat_by_lab/")
    # Legacy: GET /lab_tat_by_month
    api.add_resource(VlTatByMonth, "/hiv/vl/laboratories/tat_by_month/")
    # Legacy: GET /suppression
    api.add_resource(VlSuppression, "/hiv/vl/laboratories/suppression/")

    # Facility Endpoints
    # Legacy: GET /clinic_registered_samples_by_facility
    api.add_resource(VlFacilityRegisteredSamples, "/hiv/vl/facilities/registered_samples/")
    # Legacy: GET /clinic_samples_tested_by_month
    api.add_resource(VlFacilityTestedSamplesByMonth, "/hiv/vl/facilities/tested_samples_by_month/")
    # Legacy: GET /clinic_samples_tested_by_facility
    api.add_resource(VlFacilityTestedSamplesByFacility, "/hiv/vl/facilities/tested_samples_by_facility/")
    # Legacy: GET /clinic_samples_tested_by_gender
    api.add_resource(VlFacilityTestedSamplesByGender, "/hiv/vl/facilities/tested_samples_by_gender/")
    # Legacy: GET /clinic_samples_tested_by_gender_and_facility
    api.add_resource(VlFacilityTestedSamplesByGenderByFacility, "/hiv/vl/facilities/tested_samples_by_gender_by_facility/")
    # Legacy: GET /clinic_samples_tested_by_age
    api.add_resource(VlFacilityTestedSamplesByAge, "/hiv/vl/facilities/tested_samples_by_age/")
    # Legacy: GET /clinic_samples_tested_by_age_and_facility
    api.add_resource(VlFacilityTestedSamplesByAgeByFacility, "/hiv/vl/facilities/tested_samples_by_age_by_facility/")
    # Legacy: GET /clinic_samples_by_test_reason
    api.add_resource(VlFacilityTestedSamplesByTestReason, "/hiv/vl/facilities/tested_samples_by_test_reason/")
    # Legacy: GET /clinic_tests_by_pregnancy
    api.add_resource(VlFacilityTestedSamplesPregnant, "/hiv/vl/facilities/tested_samples_pregnant/")
    # Legacy: GET /clinic_tests_by_breastfeeding
    api.add_resource(VlFacilityTestedSamplesBreastfeeding, "/hiv/vl/facilities/tested_samples_breastfeeding/")
    # Legacy: GET /clinic_samples_rejected_by_month
    api.add_resource(VlFacilityRejectedSamplesByMonth, "/hiv/vl/facilities/rejected_samples_by_month/")
    # Legacy: GET /clinic_samples_rejected_by_facility
    api.add_resource(VlFacilityRejectedSamplesByFacility, "/hiv/vl/facilities/rejected_samples_by_facility/")
    # Legacy: GET /clinic_tat
    api.add_resource(VlFacilityTatByMonth, "/hiv/vl/facilities/tat_by_month/")
    # Legacy: GET /clinic_tat_by_facility
    api.add_resource(VlFacilityTatByFacility, "/hiv/vl/facilities/tat_by_facility/")

    # Summary/Dashboard Endpoints
    # Legacy: GET /dash_indicators
    api.add_resource(VlSummaryHeaderIndicators, "/hiv/vl/summary/header_indicators/")
    # Legacy: GET /dash_number_of_samples
    api.add_resource(VlSummaryNumberOfSamples, "/hiv/vl/summary/number_of_samples/")
    # Legacy: GET /dash_viral_suppression
    api.add_resource(VlSummaryViralSuppression, "/hiv/vl/summary/viral_suppression/")
    # Legacy: GET /dash_tat
    api.add_resource(VlSummaryTat, "/hiv/vl/summary/tat/")
    # Legacy: GET /dash_map
    api.add_resource(VlSummarySuppressionByProvince, "/hiv/vl/summary/suppression_by_province/")
    # Legacy: GET /sampleshistory
    api.add_resource(VlSummarySamplesHistory, "/hiv/vl/summary/samples_history/")
