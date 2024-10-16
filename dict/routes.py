from dict.controllers.laboratories_controller import (
    dict__laboratories,
    dict__laboratories__by_province,
    dict__laboratories__by_district,
)

from dict.controllers.facilities_controller import (
    dict__facilities,
    dict__facilities__by_province,
    dict__facilities__by_district,
)


def dict_register_routes(api):

    # Get all laboratories endpoints
    api.add_resource(dict__laboratories, "/dict/laboratories")

    # Get all laboratories endpoints by province
    api.add_resource(
        dict__laboratories__by_province, "/dict/laboratories/<string:province>/"
    )

    # Get all laboratories endpoints by District
    api.add_resource(
        dict__laboratories__by_district,
        "/dict/laboratories/<string:province>/<string:district>/",
    )

    # Get all facilities endpoints
    api.add_resource(dict__facilities, "/dict/facilities/")

    # Get all facilities endpoints by province
    api.add_resource(
        dict__facilities__by_province, "/dict/facilities/<string:province>/"
    )

    # Get all facilities endpoints by District
    api.add_resource(
        dict__facilities__by_district,
        "/dict/facilities/<string:province>/<string:district>/",
    )