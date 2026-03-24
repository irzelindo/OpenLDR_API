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
