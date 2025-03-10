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

    api.add_resource(
        tb_gx_tested_samples_by_facility_disaggregated,
        "/tb/gx/facilities/tested_samples_disaggregated/",
    )

    api.add_resource(
        tb_gx_tested_samples_by_facility_disaggregated_by_gender,
        "/tb/gx/facilities/tested_samples_disaggregated_by_gender/",
    )

    api.add_resource(
        tb_gx_tested_samples_by_facility_disaggregated_by_age,
        "/tb/gx/facilities/tested_samples_disaggregated_by_age/",
    )

    api.add_resource(
        tb_gx_tested_samples_types_by_facility_disaggregated_by_age,
        "/tb/gx/facilities/tested_samples_types_disaggregated_by_age/",
    )

    api.add_resource(
        tb_gx_tested_samples_by_facility_disaggregated_by_drug_type,
        "/tb/gx/facilities/tested_samples_disaggregated_by_drug_type/",
    )

    api.add_resource(
        tb_gx_tested_samples_by_facility_rifampicin_resistance_disaggregated_by_drug_type_by_age,
        "/tb/gx/facilities/tested_samples_rifampicin_resistance_disaggregated_by_drug_type_by_age/",
    )
