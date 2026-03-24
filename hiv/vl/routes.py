from hiv.vl.controllers.vl_controller_laboratory import VlRegisteredSamples


def vl_routes(api):
    """
    Registers the routes for HIV Viral Load API endpoints.
    """
    # Laboratory Endpoints
    # Legacy: GET /samples
    api.add_resource(VlRegisteredSamples, "/hiv/vl/laboratories/registered_samples/")
