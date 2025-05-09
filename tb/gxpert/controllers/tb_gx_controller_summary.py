from flask_restful import Resource, reqparse
from tb.gxpert.services.tb_gx_services_summary import *


class dashboard_header_component_summary_controller(Resource):
    def get(self):
        """
        Retrieve the summary of the values on the dashboard header
        ---
        tags:
        - Tuberculosis/Summary
        parameters:
            - $ref: '#/parameters/GeneXpertResultType'
            - $ref: '#/parameters/TypeOfLaboratory'
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

        print(req_args)

        try:
            response = dashboard_header_component_summary_service(req_args)
            return response, 200

        except Exception as e:
            return {"message": "An Error Occured"}, 500


class dashboard_summary_positivity_by_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by month
        ---
        tags:
        - Tuberculosis/Summary
        parameters:
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A List of Dashboard Summary Positivity by Month.
            400:
                description: Invalid Parameters
            500:
                description: An Error Occured
        """
        parser = reqparse.RequestParser()

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

        print(req_args)

        try:
            response = dashboard_summary_positivity_by_month_service(req_args)
            return response, 200

        except Exception as e:
            return {"message": "An Error Occured"}, 500


class dashboard_summary_positivity_by_lab_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab
        """
        parser = reqparse.RequestParser()

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

        print(req_args)

        try:
            response = dashboard_summary_positivity_by_lab_service(req_args)
            return response, 200

        except Exception as e:
            return {"message": "An Error Occured"}, 500


class dashboard_summary_positivity_by_lab_by_age_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab by age
        """
        parser = reqparse.RequestParser()

        # GeneXpertResultType
        parser.add_argument(
            "genexpert_result_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        print(req_args)

        try:
            response = dashboard_summary_positivity_by_lab_by_age_service(
                req_args)
            return response, 200

        except Exception as e:
            return {"message": "An Error Occured"}, 500
