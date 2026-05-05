from flask_restful import Resource

from tb.gxpert.services.tb_gx_services_patients import (
    get_patients_by_name_service,
    get_patients_by_facility_service,
    get_patients_by_sample_type_service,
    get_patients_by_result_type_service,
)
from utilities.controller_helpers import (
    LIST_ARG,
    STR_ARG,
    build_common_parser,
    run_reporting_endpoint,
)


# Shared parser for all TB GeneXpert patient endpoints.
_parser = build_common_parser(
    extra_args=[
        ("genexpert_result_type", STR_ARG),
        ("first_name", STR_ARG),
        ("surname", STR_ARG),
        ("result_type", LIST_ARG),
        ("sample_type", LIST_ARG),
        ("page", {"type": int, "location": "args", "default": 1}),
        ("per_page", {"type": int, "location": "args", "default": 50}),
    ]
)


class tb_gx_patients_by_name_controller(Resource):
    def get(self):
        """
        Retrieve patients by first name or surname between two dates
        ---
        tags:
            - Tuberculosis/Patients
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/GeneXpertResultType'
            - name: first_name
              in: query
              type: string
              required: false
              description: The patient's first name (partial match)
            - name: surname
              in: query
              type: string
              required: false
              description: The patient's surname (partial match)
            - $ref: '#/parameters/HealthFacilityParameter'
            - name: page
              in: query
              type: integer
              required: false
              default: 1
              description: Page number (1-indexed)
            - name: per_page
              in: query
              type: integer
              required: false
              default: 50
              description: Number of records per page
        responses:
            200:
                description: A List of Patients matching the name criteria.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, get_patients_by_name_service
        )


class tb_gx_patients_by_facility_controller(Resource):
    def get(self):
        """
        Retrieve patients registered at a specific health facility between two dates
        ---
        tags:
            - Tuberculosis/Patients
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/HealthFacilityParameter'
            - name: page
              in: query
              type: integer
              required: false
              default: 1
              description: Page number (1-indexed)
            - name: per_page
              in: query
              type: integer
              required: false
              default: 50
              description: Number of records per page
        responses:
            200:
                description: A List of Patients registered at the facility.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, get_patients_by_facility_service
        )


class tb_gx_patients_by_sample_type_controller(Resource):
    def get(self):
        """
        Retrieve patients by sample type (specimen source) between two dates
        ---
        tags:
            - Tuberculosis/Patients
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/GeneXpertResultType'
            - name: sample_type
              in: query
              type: array
              required: true
              items:
                type: string
                enum: ["sputum", "feces", "urine", "blood"]
              description: The sample type to filter by (sputum, feces, urine, blood)
            - name: page
              in: query
              type: integer
              required: false
              default: 1
              description: Page number (1-indexed)
            - name: per_page
              in: query
              type: integer
              required: false
              default: 50
              description: Number of records per page
        responses:
            200:
                description: A List of Patients filtered by sample type.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, get_patients_by_sample_type_service
        )


class tb_gx_patients_by_result_type_controller(Resource):
    def get(self):
        """
        Retrieve patients by result type (detected, not_detected, indeterminate, error, invalid) between two dates
        ---
        tags:
            - Tuberculosis/Patients
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/GeneXpertResultType'
            - name: result_type
              in: query
              type: array
              required: true
              items:
                type: string
                enum: ["detected", "not_detected", "indeterminate", "error", "invalid"]
              description: The result type to filter by (detected, not_detected, indeterminate, error, invalid)
            - name: page
              in: query
              type: integer
              required: false
              default: 1
              description: Page number (1-indexed)
            - name: per_page
              in: query
              type: integer
              required: false
              default: 50
              description: Number of records per page
        responses:
            200:
                description: A List of Patients filtered by result type.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        return run_reporting_endpoint(
            _parser.parse_args, get_patients_by_result_type_service
        )
