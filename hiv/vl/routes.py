from hiv.vl.controllers.laboratory_controller import (
    RegisteredSamples,
)

from dict.controllers.laboratories_controller import (
    dict__laboratories,
    dict__laboratories__by_district,
    dict__laboratories__by_province,
)

from dict.controllers.facilities_controller import (
    dict__facilities,
    dict__facilities__by_district,
    dict__facilities__by_province,
)


def dict_routes(api):
    """
    Registers the routes for Dictionary API endpoints.

    Args:
        api: A flask_restful Api instance to which the routes are registered
    """
    # Dictionary Endpoints
    api.add_resource(dict__laboratories, "/dict/laboratories/")
    api.add_resource(
        dict__laboratories__by_province, "/dict/laboratories/<string:province>/"
    )
    api.add_resource(
        dict__laboratories__by_district,
        "/dict/laboratories/<string:province>/<string:district>/",
    )
    api.add_resource(dict__facilities, "/dict/facilities/")
    api.add_resource(
        dict__facilities__by_province, "/dict/facilities/<string:province>/"
    )
    api.add_resource(
        dict__facilities__by_district,
        "/dict/facilities/<string:province>/<string:district>/",
    )


def vl_routes(api):
    """
    Registers the routes for Viral Load API endpoints.

    Args:
        api: A flask_restful Api instance to which the routes are registered
    """
    # Laboratory Endpoints
    api.add_resource(RegisteredSamples, "/hiv/vl/laboratory/registered_samples/")
