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
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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

        parser = reqparse.RequestParser()

        # Parse the arguments
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        print(req_args)

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
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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

        parser = reqparse.RequestParser()
        # Parse the arguments
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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
        id = "tb_gx_registered_samples_by_lab_month"

        parser = reqparse.RequestParser()

        # Parse the arguments

        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
          - $ref: '#/parameters/GeneXpertResultType'
          - $ref: '#/parameters/TypeOfLaboratory'
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
        # ConventionalLaboratories
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        print(req_args)

        try:
            # Get the data
            response = tested_samples_by_lab_service_month(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class rejected_samples_by_lab_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by lab agreggated by month
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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

        # Parse the arguments
        # ConventionalLaboratories
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        print(req_args)

        try:
            # Get the data
            response = rejected_samples_by_lab_service(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class rejected_samples_by_lab_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by lab agreggated by month
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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
        id = "tb_gx_rejected_samples_by_lab_month"

        parser = reqparse.RequestParser()

        # Parse the arguments
        # ConventionalLaboratories
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        print(req_args)

        try:
            # Get the data
            response = rejected_samples_by_lab_service_month(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class rejected_samples_by_lab_by_reason_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by lab by reason
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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

        # Parse the arguments
        # ConventionalLaboratories
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        print(req_args)

        try:
            # Get the data
            response = rejected_samples_by_lab_by_reason_service(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class rejected_samples_by_lab_by_reason_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of rejected samples by lab by reason
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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

        id = "tb_gx_rejected_samples_by_lab_by_reason_month"

        parser = reqparse.RequestParser()

        # Parse the arguments
        # ConventionalLaboratories
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        print(req_args)

        try:
            # Get the data
            response = rejected_samples_by_lab_by_reason_service_month(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class tested_samples_by_lab_by_drug_type_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab by drug type
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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

        parser = reqparse.RequestParser()

        # Parse the arguments
        # ConventionalLaboratories
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        print(req_args)

        try:
            # Get the data
            response = tested_samples_by_lab_by_drug_type_service(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class tested_samples_by_lab_by_drug_type_month_controller(Resource):
    def get(self):
        """
        Retrieve the number of tested samples by lab by drug type"
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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

        id = "tb_gx_tested_samples_by_lab_by_drug_type_month"

        parser = reqparse.RequestParser()

        # Parse the arguments
        # ConventionalLaboratories
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        print(req_args)

        try:
            # Get the data
            response = tested_samples_by_lab_by_drug_type_service_month(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class trl_samples_by_lab_in_days_controller(Resource):
    def get(self):
        """
        Retrieve the turnaround time samples tested in days
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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

        parser = reqparse.RequestParser()

        # Parse the arguments
        # ConventionalLaboratories
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        print(req_args)

        try:
            # Get the data
            response = trl_samples_by_lab_by_days_service(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400


class trl_samples_by_lab_in_days_month_controller(Resource):
    def get(self):
        """
        Retrieve the turnaround time samples tested in days by month
        ---
        tags:
          - Tuberculosis/Laboratories
        parameters:
          - $ref: '#/parameters/ConventionalLaboratories'
          - $ref: '#/parameters/PointOfCareLaboratories'
          - $ref: '#/parameters/IntervalDates'
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

        id = "tb_gx_trl_samples_by_lab_by_age_month"

        parser = reqparse.RequestParser()

        # Parse the arguments
        # ConventionalLaboratories
        parser.add_argument(
            "conventional_laboratories",
            type=lambda x: x,
            action="append",
            location="args",
            help="This field cannot be blank.",
        )

        # PointOfCareLaboratories
        parser.add_argument(
            "point_of_care_laboratories",
            type=lambda x: x,
            action="append",
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

        req_args = parser.parse_args()

        print(req_args)

        try:
            # Get the data
            response = trl_samples_by_lab_by_days_by_service_month(req_args)
            return response, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"message": str(e)}, 400
