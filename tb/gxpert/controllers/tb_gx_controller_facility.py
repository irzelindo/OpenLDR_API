from flask_restful import Resource

from tb.gxpert.services.tb_gx_services_facilities import (
    registered_samples_by_facility_service,
    registered_samples_by_month_by_facility_service,
    tested_samples_by_facility_service,
    tested_samples_by_month_by_facility_service,
    tested_samples_by_facility_disaggregated_service,
    tested_samples_by_facility_disaggregated_by_gender_service,
    tested_samples_by_facility_disaggregated_by_age_service,
    tested_samples_by_sample_types_by_facility_service,
    tested_samples_types_by_facility_disaggregated_by_age_service,
    tested_samples_by_facility_disaggregated_by_drug_type_service,
    tested_samples_by_facility_disaggregated_by_drug_type_by_age_service,
    rejected_samples_by_facility_service,
    rejected_samples_by_facility_by_month_service,
    rejected_samples_by_facility_by_reason_service,
    rejected_samples_by_facility_by_reason_by_month_service,
    trl_samples_by_facility_by_days_service,
    trl_samples_by_facility_by_days_tb_service,
    trl_samples_by_facility_by_days_by_month_service,
    trl_samples_avg_by_facility_service,
    trl_samples_avg_by_facility_month_service,
)
from utilities.controller_helpers import (
    STR_ARG,
    build_common_parser,
    run_reporting_endpoint,
)


# Shared parser for all TB GeneXpert facility endpoints.
_parser = build_common_parser(
    extra_args=[
        ("gene_xpert_result_type", STR_ARG),
        ("month", STR_ARG),
        ("year", STR_ARG),
        ("type_of_laboratory", STR_ARG),
        ("drug", STR_ARG),
    ]
)


class tb_gx_registered_samples_by_facility_controller(Resource):
    def get(self):
        """
        Get the total number of samples registered by facility between two dates.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples registered by facility between two dates.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
        """
        return run_reporting_endpoint(
            _parser.parse_args, registered_samples_by_facility_service
        )


class tb_gx_registered_samples_by_month_by_facility_controller(Resource):
    def get(self):
        """
        Get the total number of samples registered by facility between two dates, grouped by month.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/MonthsParameter'
            - $ref: '#/parameters/YearParameter'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples registered by facility between two dates, grouped by month.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
        """
        return run_reporting_endpoint(
            _parser.parse_args, registered_samples_by_month_by_facility_service
        )


class tb_gx_tested_samples_by_facility_controller(Resource):
    def get(self):
        """
        Get the total number of samples tested by facility between two dates.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by facility between two dates.
            400:
                description: Invalid Parameters
            404:
                description: Facility not found
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_facility_service
        )


class tb_gx_tested_samples_by_month_by_facility_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by month by facility between two dates.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/MonthsParameter'
            - $ref: '#/parameters/YearParameter'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by month by facility between two dates.
            400:
                description: Invalid Parameters
            404:
                description: Facility not found
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_month_by_facility_service
        )


class tb_gx_tested_samples_by_facility_disaggregated_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by facility between two dates, disaggregated.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by facility between two dates, disaggregated by mtb trace, detected, invalid, without result and errors.
            400:
                description: Invalid Parameters
            404:
                description: Facility not found
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_facility_disaggregated_service
        )


class tb_gx_tested_samples_by_facility_disaggregated_by_gender_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by facility between two dates, disaggregated by gender.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by facility between two dates, disaggregated by gender.
            400:
                description: Invalid Parameters
            404:
                description: Facility not found
        """
        return run_reporting_endpoint(
            _parser.parse_args,
            tested_samples_by_facility_disaggregated_by_gender_service,
        )


class tb_gx_tested_samples_by_facility_disaggregated_by_age_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by facility between two dates, disaggregated by age.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by facility between two dates, disaggregated by age.
            400:
                description: Invalid Parameters
            404:
                description: Facility not found
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_facility_disaggregated_by_age_service
        )


class tb_gx_tested_samples_by_sample_types_by_facility_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by sample type by facility between two dates.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by facility between two dates.
            400:
                description: Invalid Parameters
            404:
                description: Facility not found
        """
        return run_reporting_endpoint(
            _parser.parse_args, tested_samples_by_sample_types_by_facility_service
        )


class tb_gx_tested_samples_types_by_facility_disaggregated_by_age_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by sample type by facility between two dates, disaggregated by age.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by facility between two dates, disaggregated by age.
            400:
                description: Invalid Parameters
            404:
                description: Facility not found
        """
        return run_reporting_endpoint(
            _parser.parse_args,
            tested_samples_types_by_facility_disaggregated_by_age_service,
        )


class tb_gx_tested_samples_by_facility_disaggregated_by_drug_type_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by facility between two dates, disaggregated by drug type.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by facility between two dates, disaggregated by drug type.
            400:
                description: Invalid Parameters
        """
        return run_reporting_endpoint(
            _parser.parse_args,
            tested_samples_by_facility_disaggregated_by_drug_type_service,
        )


class tb_gx_tested_samples_by_facility_disaggregated_by_drug_type_by_age_controller(Resource):
    def get(self):
        """
        Get the number of samples tested by facility between two dates, disaggregated by drug type and age.
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/DrugTypeParameter'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by facility between two dates, disaggregated by drug type and age.
            400:
                description: Invalid Parameters
            404:
                description: Facility not found
        """
        return run_reporting_endpoint(
            _parser.parse_args,
            tested_samples_by_facility_disaggregated_by_drug_type_by_age_service,
        )


class tb_gx_rejected_samples_by_facility_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by facility agreggated by facility
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of Rejected Samples by Facility agreggated by facility.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, rejected_samples_by_facility_service
        )


class tb_gx_rejected_samples_by_facility_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by facility agreggated by month
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/MonthsParameter'
        responses:
            200:
                description: A List of Rejected Samples by facility agreggated by month.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, rejected_samples_by_facility_by_month_service
        )


class tb_gx_rejected_samples_by_facility_by_reason_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by facility by reason
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of Rejected Samples by facility by Reason.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, rejected_samples_by_facility_by_reason_service
        )


class tb_gx_rejected_samples_by_facility_by_reason_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by facility by reason by month
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/MonthsParameter'
        responses:
            200:
                description: A List of Rejected Samples by Facility by Reason.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, rejected_samples_by_facility_by_reason_by_month_service
        )


class tb_gx_trl_samples_by_facility_in_days_controller(Resource):
    def get(self):
        """
        Retrieve the number of TR samples by facility in days
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of TR Samples by Facility in Days.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, trl_samples_by_facility_by_days_service
        )


class tb_gx_trl_samples_by_facility_in_days_tb_controller(Resource):
    def get(self):
        """
        Retrieve the turnaround time samples tested in days tuberculoses
        ranges by facility
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: Turnaround time samples tested in days by facility
            400:
                description: Invalid request parameters
            500:
                description: Internal server error
        """
        return run_reporting_endpoint(
            _parser.parse_args, trl_samples_by_facility_by_days_tb_service
        )


class tb_gx_trl_samples_by_facility_in_days_by_month_controller(Resource):
    def get(self):
        """
        Retrieve the turnaround time samples tested in days by month
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
            - $ref: '#/parameters/MonthsParameter'
            - $ref: '#/parameters/YearParameter'
        responses:
            200:
                description: A List of TR Samples by Facility in Days by Month.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, trl_samples_by_facility_by_days_by_month_service
        )


class tb_gx_trl_avg_samples_by_facility_in_days_controller(Resource):
    def get(self):
        """
        Retrieve the average turnaround time of samples tested in days by facility
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of Average Turnaround Time of Samples by Facility in Days.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, trl_samples_avg_by_facility_service
        )


class tb_gx_trl_avg_samples_by_facility_in_days_by_month_controller(Resource):
    def get(self):
        """
        Retrieve the average turnaround time of samples tested in days by facility by month
        ---
        tags:
            - Tuberculosis/Facilities
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/MonthsParameter'
            - $ref: '#/parameters/YearParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
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
            _parser.parse_args, trl_samples_avg_by_facility_month_service
        )
