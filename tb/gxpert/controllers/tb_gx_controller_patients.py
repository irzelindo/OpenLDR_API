from flask_restful import Resource, reqparse
from tb.gxpert.services.tb_gx_services_patients import *
from flask import jsonify, request, session
from utilities.utils import get_unverified_payload, get_token, get_user_token_info
# from configs.paths_local import *
from configs.paths import *


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
        id = "tb_gx_patients_by_name"

        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )

        session["user_info"] = get_user_token_info(token_payload)

        user_id = str(session.get("user_info").get("user_id"))

        parser = reqparse.RequestParser()


        # IntervalDates
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # GeneXpertResultType
        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # First Name
        parser.add_argument(
            "first_name",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Surname
        parser.add_argument(
            "surname",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Page
        parser.add_argument(
            "page",
            type=int,
            location="args",
            default=1,
        )

        # Per Page
        parser.add_argument(
            "per_page",
            type=int,
            location="args",
            default=50,
        )

        # Parse the request arguments
        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            response = get_patients_by_name_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
        id = "tb_gx_patients_by_facility"

        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )

        session["user_info"] = get_user_token_info(token_payload)

        user_id = str(session.get("user_info").get("user_id"))

        parser = reqparse.RequestParser()

        # Health Facility
        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # IntervalDates
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # GeneXpertResultType
        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Page
        parser.add_argument(
            "page",
            type=int,
            location="args",
            default=1,
        )

        # Per Page
        parser.add_argument(
            "per_page",
            type=int,
            location="args",
            default=50,
        )

        # Parse the request arguments
        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            response = get_patients_by_facility_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
        id = "tb_gx_patients_by_sample_type"

        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )

        session["user_info"] = get_user_token_info(token_payload)

        user_id = str(session.get("user_info").get("user_id"))

        parser = reqparse.RequestParser()

        # IntervalDates
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # GeneXpertResultType
        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Sample Type
        parser.add_argument(
            "sample_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Page
        parser.add_argument(
            "page",
            type=int,
            location="args",
            default=1,
        )

        # Per Page
        parser.add_argument(
            "per_page",
            type=int,
            location="args",
            default=50,
        )

        # Parse the request arguments
        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            response = get_patients_by_sample_type_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
        id = "tb_gx_patients_by_result_type"

        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )

        session["user_info"] = get_user_token_info(token_payload)

        user_id = str(session.get("user_info").get("user_id"))

        parser = reqparse.RequestParser()

        # IntervalDates
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # GeneXpertResultType
        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Result Type
        parser.add_argument(
            "result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Page
        parser.add_argument(
            "page",
            type=int,
            location="args",
            default=1,
        )

        # Per Page
        parser.add_argument(
            "per_page",
            type=int,
            location="args",
            default=50,
        )

        # Parse the request arguments
        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            response = get_patients_by_result_type_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
            )
