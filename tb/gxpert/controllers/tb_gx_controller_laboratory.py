from flask_restful import Resource

from tb.gxpert.services.tb_gx_services_laboratories import (
    registered_samples_by_lab_service,
    registered_samples_by_lab_by_month_service,
    tested_samples_by_lab_service,
    tested_samples_by_lab_by_month_service,
    tested_samples_by_sample_types_by_laboratory_service,
    tested_samples_by_samples_types_by_laboratory_by_month_service,
    rejected_samples_by_lab_service,
    rejected_samples_by_lab_by_month_service,
    rejected_samples_by_lab_by_reason_service,
    rejected_samples_by_lab_by_reason_by_month_service,
    tested_samples_by_lab_by_drug_type_service,
    tested_samples_by_lab_by_drug_type_by_month_service,
    trl_samples_by_lab_by_days_service,
    trl_samples_by_lab_by_days_by_month_service,
    trl_samples_avg_by_lab_service,
    trl_samples_avg_by_lab_month_service,
)
from utilities.controller_helpers import (
    STR_ARG,
    build_common_parser,
    run_reporting_endpoint,
)


# Shared parser for all TB GeneXpert laboratory endpoints.
_parser = build_common_parser(
    extra_args=[
        ("genexpert_result_type", STR_ARG),
        ("type_of_laboratory", STR_ARG),
        ("month", STR_ARG),
        ("year", STR_ARG),
        ("drug", STR_ARG),
    ]
)


class tb_gx_registered_samples_by_lab_controller(Resource):
    def get(self):
        """
        Retrieve the number of registered samples by lab aggregated by month
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Registered Samples by Lab aggregated by month.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, registered_samples_by_lab_service
        )


class tb_gx_tested_samples_by_lab_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab agreggated by month
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Tested Samples by Lab agreggated by month.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_lab_service
        )


class tb_gx_registered_samples_by_lab_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of registered samples by lab agreggated by month.
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/MonthsParameter'
        responses:
            200:
                description: A List of Registered Samples by Lab agreggated by month.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, registered_samples_by_lab_by_month_service
        )


class tb_gx_tested_samples_by_lab_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab by agreggated by month
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/MonthsParameter'
        responses:
            200:
                description: A List of Tested  Samples by Lab agreggated by month.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_lab_by_month_service
        )


class tb_gx_rejected_samples_by_lab_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by lab agreggated by month
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Rejected Samples by Lab agreggated by month.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, rejected_samples_by_lab_service
        )


class tb_gx_rejected_samples_by_lab_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by lab agreggated by month
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/MonthsParameter'
        responses:
            200:
                description: A List of Rejected Samples by Lab agreggated by month.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, rejected_samples_by_lab_by_month_service
        )


class tb_gx_rejected_samples_by_lab_by_reason_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by lab by reason
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Rejected Samples by Lab by Reason.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, rejected_samples_by_lab_by_reason_service
        )


class tb_gx_rejected_samples_by_lab_by_reason_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by lab by reason
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/MonthsParameter'
        responses:
            200:
                description: A List of Rejected Samples by Lab by Reason.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, rejected_samples_by_lab_by_reason_by_month_service
        )


class tb_gx_tested_samples_by_lab_by_drug_type_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab by drug type
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Tested Samples by Lab by Drug Type.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_lab_by_drug_type_service
        )


class tb_gx_tested_samples_by_lab_by_drug_type_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab by drug type"
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/MonthsParameter'
        responses:
            200:
                description: A List of Tested Samples by Lab by Drug Type.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_lab_by_drug_type_by_month_service
        )


class tb_gx_trl_samples_by_lab_in_days_controller(Resource):
    def get(self):
        """
        Retrieve the turnaround time samples tested in days
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Tested Samples by Lab by Drug Type.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, trl_samples_by_lab_by_days_service
        )


class tb_gx_trl_samples_by_lab_in_days_month_controller(Resource):
    def get(self):
        """
        Retrieve the turnaround time samples tested in days by month
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/MonthsParameter'
        responses:
            200:
                description: A List of Tested Samples by Lab by Drug Type.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, trl_samples_by_lab_by_days_by_month_service
        )


class tb_gx_trl_avg_samples_by_lab_in_days_controller(Resource):
    def get(self):
        """
        Retrieve the average turnaround time of samples tested in days by laboratory
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Average Turnaround Time of Samples by Laboratory in Days.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, trl_samples_avg_by_lab_service
        )


class tb_gx_trl_avg_samples_by_lab_in_days_by_month_controller(Resource):
    def get(self):
        """
        Retrieve the average turnaround time of samples tested in days by laboratory by month
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/MonthsParameter'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Average Turnaround Time of Samples by Facility in Days by Month.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, trl_samples_avg_by_lab_month_service
        )


class tb_gx_tested_samples_by_sample_types_by_laboratory_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by sample type by laboratory between two dates.
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by laboratory between two dates.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory not found
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_sample_types_by_laboratory_service
        )


class tb_gx_tested_samples_by_sample_types_by_laboratory_by_month_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by sample type by laboratory by month.
        ---
        tags:
            - Tuberculosis/Laboratories
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/MonthsParameter'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by laboratory between two dates.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory not found
        """
        return run_reporting_endpoint(
            _parser.parse_args,
            tested_samples_by_samples_types_by_laboratory_by_month_service,
        )
