from flask_restful import Resource, reqparse
from tb.gxpert.services.tb_gx_services_laboratories import *
from flask import jsonify, request, session
from utilities.utils import get_unverified_payload, get_token
from configs.paths import *
# from configs.paths_local import *


class tb_gx_registered_samples_by_lab_controller(Resource):
    # @jwt_required()
    def get(self):
        """
        Retrieve the number of registered samples by lab agreggated by month
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
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of Registered Samples by Lab agreggated by month.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occured
        """
        id = "tb_gx_registered_samples_by_lab"

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

        # Province
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # District
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # Health Facility
        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Disaggregation
        parser.add_argument(
            "disaggregation",
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

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        # Parse the request arguments
        # This will parse the arguments from the request and return them as a dictionary
        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        # print(req_args)

        try:
            # Get the data
            response = registered_samples_by_lab_service(req_args)
            return jsonify(response)

        except Exception as e:
            # Log the error
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of Tested Samples by Lab agreggated by month.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occured
        """
        id = "tb_gx_tested_samples_by_lab"

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
        # Parse the arguments
        # Disaggregation
        parser.add_argument(
            "disaggregation",
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

        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # HealthFacility
        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # GeneXpertResultType
        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        # print(req_args)

        try:
            # Get the data
            response = tested_samples_by_lab_service(req_args)
            return jsonify(response)

        except Exception as e:
            # Log the error
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
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
                description: An Error Occured
        """
        id = "tb_gx_registered_samples_by_lab_month"

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

        # Parse the arguments
        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "disaggregation",
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

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Year
        parser.add_argument(
            "year",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Months
        parser.add_argument(
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        # print(req_args)

        try:
            # Get the data
            response = registered_samples_by_lab_by_month_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
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
                description: An Error Occured
        """

        id = "tb_gx_tested_samples_by_lab_month"

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

        # Parse the arguments
        # Disaggregation
        parser.add_argument(
            "disaggregation",
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

        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # GeneXpertResultType
        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Year
        parser.add_argument(
            "year",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Months
        parser.add_argument(
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        # print(req_args)

        try:
            # Get the data
            response = tested_samples_by_lab_by_month_service(req_args)
            return jsonify(response)

        except Exception as e:
            # Log the error
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of Rejected Samples by Lab agreggated by month.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occured
        """
        id = "tb_gx_rejected_samples_by_lab"

        parser = reqparse.RequestParser()

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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
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

        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = rejected_samples_by_lab_service(req_args)
            return jsonify(response)

        except Exception as e:
            # Log the error
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
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
                description: An Error Occured
        """
        id = "tb_gx_rejected_samples_by_lab_month"

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

        # Year Parameter
        parser.add_argument(
            "year",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Month Parameter
        parser.add_argument(
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
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

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = rejected_samples_by_lab_by_month_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of Rejected Samples by Lab by Reason.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occured
        """

        id = "tb_gx_rejected_samples_by_lab_by_reason"

        parser = reqparse.RequestParser()

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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
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

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = rejected_samples_by_lab_by_reason_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
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
                description: An Error Occured
        """

        id = "tb_gx_rejected_samples_by_lab_by_reason_month"

        parser = reqparse.RequestParser()

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

        # Parse the arguments

        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
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

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Month
        parser.add_argument(
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Year
        parser.add_argument(
            "year",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = rejected_samples_by_lab_by_reason_by_month_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of Tested Samples by Lab by Drug Type.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occured
        """
        id = "tb_gx_tested_samples_by_lab_by_drug_type"

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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
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

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = tested_samples_by_lab_by_drug_type_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
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
                description: An Error Occured
        """

        id = "tb_gx_tested_samples_by_lab_by_drug_type_month"

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
        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
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

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Year
        parser.add_argument(
            "year",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Months
        parser.add_argument(
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = tested_samples_by_lab_by_drug_type_by_month_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
        responses:
            200:
                description: A List of Tested Samples by Lab by Drug Type.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occured
        """

        id = "tb_gx_trl_samples_by_lab_by_age"

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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
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

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = trl_samples_by_lab_by_days_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
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
                description: An Error Occured
        """

        id = "tb_gx_trl_samples_by_lab_by_age_month"

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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # IntervalDates Month
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

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Year
        parser.add_argument(
            "year",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Month
        parser.add_argument(
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = trl_samples_by_lab_by_days_by_month_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory' 
        responses:
            200:
                description: A List of Average Turnaround Time of Samples by Laboratory in Days.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occured
        """
        id = "tb_gx_trl_avg_samples_by_lab_in_days"

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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        # HealthFacility
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
        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
       
        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        # print(req_args)

        try:
            # Get the data
            response = trl_samples_avg_by_lab_service(req_args)
            return jsonify(response)
        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory' 
        responses:
            200:
                description: A List of Average Turnaround Time of Samples by Facility in Days by Month.
            400:
                description: Invalid Parameters
            404:
                description: Facility Not Found
            500:
                description: An Error Occured
        """ 
        id = "tb_gx_trl_avg_samples_by_lab_in_days_by_month"

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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # HealthFacility
        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # IntervalDates Month
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # Month
        parser.add_argument(
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Year
        parser.add_argument(
            "year",
            type=int,
            location="args",
            help="This field cannot be blank.",
        )

        # GeneXpertResultType
        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = trl_samples_avg_by_lab_month_service(req_args)

            return jsonify(response)

        except Exception as e:

            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            - $ref: '#/parameters/TypeOfLaboratory'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by laboratory between two dates.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory not found
        """
        id = "tb_gx_tested_samples_types_by_laboratory"

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

        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()
        
        req_args["user_id"] = user_id

        try:
            tested_samples = (
                tested_samples_by_sample_types_by_laboratory_service(req_args)
            )

            return jsonify(tested_samples)

        except Exception as e:
            # Log the error
            return (
                jsonify(
                    {
                        "error": "An internal error occurred.",
                        "message": str(e),
                        "status": 500,
                    }
                ),
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
            - $ref: '#/parameters/TypeOfLaboratory' 
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by laboratory between two dates.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory not found
        """
        id = "tb_gx_tested_samples_by_samples_types_by_laboratory_by_month"

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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Provinces
        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # Districts
        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # HealthFacility
        parser.add_argument(
            "health_facility",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # IntervalDates Month
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        # Month
        parser.add_argument(
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # Year
        parser.add_argument(
            "year",
            type=int,
            location="args",
            help="This field cannot be blank.",
        )

        # GeneXpertResultType
        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        # TypeOfLaboratory
        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        req_args["user_id"] = user_id

        try:
            # Get the data
            response = tested_samples_by_samples_types_by_laboratory_by_month_service(req_args)

            return jsonify(response)

        except Exception as e:

            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
            )