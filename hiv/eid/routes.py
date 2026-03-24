from hiv.eid.controllers.eid_controller_laboratory import *


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
