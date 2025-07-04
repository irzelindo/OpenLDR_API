from flask_restful import Resource, reqparse
from tb.gxpert.services.tb_gx_services_facilities import *


class tb_gx_registered_samples_by_facility(Resource):
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
        id = "tb_gx_registered_samples_by_facility"

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
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "facility_type",
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

        # print(req_args)

        try:

            registered_samples = registered_samples_by_facility(req_args)

            return registered_samples, 200

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"error": "An internal error occurred."}, 500


class tb_gx_tested_samples_by_facility(Resource):
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
        id = "tb_gx_tested_samples_by_facility"

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
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "facility_type",
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

        try:
            tested_samples = tested_samples_by_facility(req_args)
            return tested_samples, 200
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"error": "An internal error occurred."}, 500


class tb_gx_tested_samples_by_facility_disaggregated(Resource):
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
        id = "tb_gx_tested_samples_by_facility_disaggregated"

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
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "facility_type",
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
        # print(req_args)

        try:
            tested_samples = tested_samples_by_facility_disaggregated(req_args)
            return tested_samples, 200
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"error": "An internal error occurred."}, 500


class tb_gx_tested_samples_by_facility_disaggregated_by_gender(Resource):
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
        id = "tb_gx_tested_samples_by_facility_disaggregated_by_gender"

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
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "facility_type",
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
        # print(req_args)

        try:
            tested_samples = tested_samples_by_facility_disaggregated_by_gender(
                req_args
            )
            return tested_samples, 200
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"error": "An internal error occurred."}, 500


class tb_gx_tested_samples_by_facility_disaggregated_by_age(Resource):
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
        id = "tb_gx_tested_samples_by_facility_disaggregated_by_age"

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
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "facility_type",
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
        # print(req_args)

        try:
            tested_samples = tested_samples_by_facility_disaggregated_by_age(req_args)
            return tested_samples, 200
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"error": "An internal error occurred."}, 500


class tb_gx_tested_samples_types_by_facility_disaggregated_by_age(Resource):
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
        id = "tb_gx_tested_samples_types_by_facility_disaggregated_by_age"

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
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "facility_type",
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
        # print(req_args)

        try:
            tested_samples = tested_samples_types_by_facility_disaggregated_by_age(
                req_args
            )
            return tested_samples, 200
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"error": "An internal error occurred."}, 500


class tb_gx_tested_samples_by_facility_disaggregated_by_drug_type(Resource):
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
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/GeneXpertResultType'
        responses:
            200:
                description: A list of dictionaries containing the total number of samples tested by facility between two dates, disaggregated by drug type.
            400:
                description: Invalid Parameters
        """
        id = "tb_gx_tested_samples_by_facility_disaggregated_by_drug_type"

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
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "facility_type",
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
        # print(req_args)

        try:
            tested_samples = tested_samples_by_facility_disaggregated_by_drug_type(
                req_args
            )
            return tested_samples, 200
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"error": "An internal error occurred."}, 500


class tb_gx_tested_samples_by_facility_disaggregated_by_drug_type_by_age(Resource):
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
        id = "tb_gx_tested_samples_by_facility_rifampicin_resistance_disaggregated_by_drug_type_by_age"

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
            "disaggregation",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "facility_type",
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

        parser.add_argument(
            "drug",
            type=str,
            location="args",
            help="This field cannot be blank.",
            required=True,
        )
        req_args = parser.parse_args()

        # print(req_args)

        try:
            tested_samples = (
                tested_samples_by_facility_disaggregated_by_drug_type_by_age(req_args)
            )
            return tested_samples, 200
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"error": "An internal error occurred."}, 500
