from tb.gxpert.controllers.tb_gx_controller_facility import *


def tb_gxpert_routes(api):

    # Facilities Endpoints
    api.add_resource(
        tb_gx_registered_samples_by_facility,
        "/tb/gx/facilities/registered_samples/",
    )

    api.add_resource(
        tb_gx_tested_samples_by_facility,
        "/tb/gx/facilities/tested_samples/",
    )
