from tb.gxpert.controllers.tb_gx_controller_facility import *
from tb.gxpert.controllers.tb_gx_controller_laboratory import *
from tb.gxpert.controllers.tb_gx_controller_summary import *


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
        tb_gx_tested_samples_by_facility_disaggregated_by_drug_type_by_age,
        "/tb/gx/facilities/tested_samples_disaggregated_by_drug_type_by_age/",
    )

    # Labortory Endpoints
    api.add_resource(
        registered_samples_by_lab_controller,
        "/tb/gx/laboratories/registered_samples/",
    )

    api.add_resource(
        tested_samples_by_lab_controller,
        "/tb/gx/laboratories/tested_samples/",
    )

    api.add_resource(
        registered_samples_by_lab_month_controller,
        "/tb/gx/laboratories/registered_samples_by_month/",
    )

    api.add_resource(
        tested_samples_by_lab_month_controller,
        "/tb/gx/laboratories/tested_samples_by_month/",
    )

    api.add_resource(
        rejected_samples_by_lab_controller,
        "/tb/gx/laboratories/rejected_samples/",
    )

    api.add_resource(
        rejected_samples_by_lab_month_controller,
        "/tb/gx/laboratories/rejected_samples_by_month/",
    )

    api.add_resource(
        rejected_samples_by_lab_by_reason_controller,
        "/tb/gx/laboratories/rejected_samples_by_reason/",
    )

    api.add_resource(
        rejected_samples_by_lab_by_reason_month_controller,
        "/tb/gx/laboratories/rejected_samples_by_reason_by_month/",
    )

    api.add_resource(
        tested_samples_by_lab_by_drug_type_controller,
        "/tb/gx/laboratories/tested_samples_by_drug_type/",
    )

    api.add_resource(
        tested_samples_by_lab_by_drug_type_month_controller,
        "/tb/gx/laboratories/tested_samples_by_drug_type_by_month/",
    )

    api.add_resource(
        trl_samples_by_lab_by_age_controller,
        "/tb/gx/laboratories/trl_samples_by_lab_by_age/",
    )

    api.add_resource(
        trl_samples_by_lab_by_age_month_controller,
        "/tb/gx/laboratories/trl_samples_by_lab_by_age_month/",
    )

    # SummaryLaboratory Endpoints
    api.add_resource(
        dashboard_header_component_summary_controller,
        "/tb/gx/laboratories/summary/registered_samples/",
    )
