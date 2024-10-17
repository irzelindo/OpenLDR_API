from hiv.vl.controllers.laboratory_controller import (
    RegisteredSamples,
)


def vl_routes(api):
    """
    Registers the routes for Viral Load API endpoints.

    Args:
        api: A flask_restful Api instance to which the routes are registered
    """
    # Laboratory Endpoints
    api.add_resource(RegisteredSamples, "/hiv/vl/laboratory/registered_samples/")
