from flask_restful import Resource, reqparse
from tb.gxpert.services.tb_gx_services_summary import *
from flask import jsonify
from flask import request
from utilities.utils import get_unverified_payload, get_token
from configs.paths import *

class dashboard_header_component_summary_controller(Resource):
    def get(self):
        """
        Retrieve the summary of the number of samples from  registration to analysis on the dashboard header
        ---
        tags:
        - Tuberculosis/Summary
        parameters:
            - $ref: '#/parameters/IntervalDates'
        responses:
            200:
                description: A List of Dashboard Header Component Summary.
            400:
                description: Invalid Parameters
            404:
                description: Laboratory Not Found
            500:
                description: An Error Occured
        """
        parser = reqparse.RequestParser()

        # IntervalDates
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        # print(req_args)

        try:
            response = dashboard_header_component_summary_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )


class dashboard_summary_positivity_by_month_controller(Resource):

    def get(self):
        """
        Retrieve the number of tested samples by month
        ---
        tags:
        - Tuberculosis/Summary
        parameters:
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
            - $ref: '#/parameters/IntervalDates'
        responses:
            200:
                description: A List of Dashboard Summary Positivity by Month.
            400:
                description: Invalid Parameters
            500:
                description: An Error Occured
        """
        token = get_token(request)

        try:
            token_payload = verify_clerk_token(token)
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )
        
        user_info, token_info = get_user_token_info(token_payload)

        print(user_info)
        print(token_info)

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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
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

        # IntervalDates
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
        )

        req_args = parser.parse_args()
        req_args["user_info"] = user_info
        req_args["token_info"] = token_info

        print(req_args)

        try:
            response = dashboard_summary_positivity_by_month_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )


class dashboard_summary_positivity_by_lab_controller(Resource):
    def get(self):
        """
        Retrieve the posotivity rate by laboratory
        ---
        tags:
        - Tuberculosis/Summary
        parameters:
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
            - $ref: '#/parameters/IntervalDates'
        responses:
            200:
                description: A List of Dashboard Summary Positivity by Lab.
            400:
                description: Invalid Parameters
            500:
                description: An Error Occured
        """
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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
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

        # IntervalDates
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
        )

        req_args = parser.parse_args()

        # print(req_args)

        try:
            response = dashboard_summary_positivity_by_lab_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )


class dashboard_summary_positivity_by_lab_by_age_controller(Resource):
    def get(self):
        """
        Retrieve the positivity rate by laboratory by age
        ---
        tags:
        - Tuberculosis/Summary
        parameters:
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
            - $ref: '#/parameters/IntervalDates'
        responses:
            200:
                description: A List of Dashboard Summary Positivity by Lab by Age.
            400:
                description: Invalid Parameters
            500:
                description: An Error Occured
        """
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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
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

        # IntervalDates
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
        )

        req_args = parser.parse_args()

        # print(req_args)

        try:
            response = dashboard_summary_positivity_by_lab_by_age_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )


class dashboard_summary_sample_types_by_month_by_age_controller(Resource):
    def get(self):
        """
        Retrieve the number of registered samples by month and by specimen type
        ---
        tags:
        - Tuberculosis/Summary
        parameters:
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
            - $ref: '#/parameters/IntervalDates'
        responses:
            200:
                description: A List of Dashboard Summary Sample Types by Month.
            400:
                description: Invalid Parameters
            500:
                description: An Error Occured
        """
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

        # Disaggregation
        parser.add_argument(
            "disaggregation",
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

        # IntervalDates
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
        )

        req_args = parser.parse_args()

        # print(req_args)

        try:
            response = dashboard_summary_sample_types_by_month_by_age_service(req_args)
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )


class dashboard_summary_sample_types_by_facility_by_age_controller(Resource):
    def get(self):
        """
        Retrieve the number of registered samples by facility by specimen type by age
        ---
        tags:
        - Tuberculosis/Summary
        parameters:
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Dashboard Summary Sample Types by Facility by Age.
            400:
                description: Invalid Parameters
            500:
                description: An Error Occured
        """
        parser = reqparse.RequestParser()

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
        )

        # Province
        parser.add_argument(
            "province",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # District
        parser.add_argument(
            "district",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # FacilityType
        parser.add_argument(
            "facility_type",
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

        req_args = parser.parse_args()

        # print(req_args)

        try:
            response = dashboard_summary_sample_types_by_facility_by_age_service(
                req_args
            )
            return jsonify(response)

        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occured",
                    "error": str(e),
                }
            )
