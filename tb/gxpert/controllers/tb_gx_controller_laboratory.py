from flask_restful import Resource, reqparse
from tb.gxpert.services.tb_gx_services_laboratories import *


class registered_samples_by_lab_controller(Resource):
    def get(self):
        """
        Retrieve the number of registered samples by lab agreggated by month
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/IntervalDates'
          - $ref: '#/parameters/GeneXpertResultType'
          - $ref: '#/parameters/TypeOfFacility'
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

        parser = reqparse.RequestParser()

        # Parse the arguments
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "genexpert_result_type",
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

        req_args = parser.parse_args()

        # print(req_args)

        try:
            # Get the data
            response = registered_samples_by_lab_service(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class tested_samples_by_lab_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab agreggated by month
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/IntervalDates'
          - $ref: '#/parameters/GeneXpertResultType'
          - $ref: '#/parameters/TypeOfFacility'
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

        parser = reqparse.RequestParser()
        # Parse the arguments
        parser.add_argument(
            "interval_dates",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "genexpert_result_type",
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

        req_args = parser.parse_args()

        print(req_args)

        try:
            # Get the data
            response = tested_samples_by_lab_service(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class registered_samples_by_lab_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of registered samples by lab agreggated by month.
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/IntervalDates'
          - $ref: '#/parameters/GeneXpertResultType'
          - $ref: '#/parameters/TypeOfFacility'
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

        parser = reqparse.RequestParser()

        # Parse the arguments
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

        parser.add_argument(
            "type_of_laboratory",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        print(req_args)

        try:
            # Get the data
            response = registered_samples_by_lab_service_month(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class tested_samples_by_lab_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab by agreggated by month
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/IntervalDates'
          - $ref: '#/parameters/GeneXpertResultType'
          - $ref: '#/parameters/TypeOfFacility'
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

        parser = reqparse.RequestParser()

        # Parse the arguments
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

        print(req_args)

        try:
            # Get the data
            response = tested_samples_by_lab_service_month(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400
