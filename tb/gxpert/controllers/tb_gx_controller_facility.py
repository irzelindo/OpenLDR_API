from flask_restful import Resource, reqparse
from tb.gxpert.services.tb_gx_services_facilities import *
from flask import jsonify


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

            registered_samples = registered_samples_by_facility_service(req_args)

            return jsonify(registered_samples)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
        id = "tb_gx_registered_samples_by_month_by_facility"

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
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "year",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        print(req_args)

        try:
            registered_samples = registered_samples_by_month_by_facility_service(
                req_args
            )

            return jsonify(registered_samples)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
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
            tested_samples = tested_samples_by_facility_service(req_args)
            return jsonify(tested_samples)
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An internal error occurred."}), 500


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
        id = "tb_gx_tested_samples_by_month_by_facility"

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
            "month",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "year",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        print(req_args)

        try:
            tested_samples = tested_samples_by_month_by_facility_service(req_args)
            return jsonify(tested_samples)
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return (
                jsonify(
                    {
                        "error": "An internal error occurred.",
                        "message": str(e),
                        "status": 500,
                    }
                ),
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
            tested_samples = tested_samples_by_facility_disaggregated_service(req_args)
            return jsonify(tested_samples)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An internal error occurred."}), 500


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
            tested_samples = tested_samples_by_facility_disaggregated_by_gender_service(
                req_args
            )
            return jsonify(tested_samples)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An internal error occurred."}), 500


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
            tested_samples = tested_samples_by_facility_disaggregated_by_age_service(
                req_args
            )
            return jsonify(tested_samples)
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An internal error occurred."}), 500


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
            tested_samples = (
                tested_samples_types_by_facility_disaggregated_by_age_service(req_args)
            )
            return jsonify(tested_samples)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An internal error occurred."}), 500


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
            tested_samples = (
                tested_samples_by_facility_disaggregated_by_drug_type_service(req_args)
            )
            return jsonify(tested_samples)
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An internal error occurred."}), 500


class tb_gx_tested_samples_by_facility_disaggregated_by_drug_type_by_age_controller(
    Resource
):
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
        id = "tb_gx_tested_samples_by_disaggregated_by_drug_type_by_age"

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
                tested_samples_by_facility_disaggregated_by_drug_type_by_age_service(
                    req_args
                )
            )
            return jsonify(tested_samples)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return {"error": "An internal error occurred."}, 500


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
                description: An Error Occured
        """
        id = "tb_gx_rejected_samples_by_facility"

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

        # print(req_args)

        try:
            # Get the data
            response = rejected_samples_by_facility_service(req_args)
            return jsonify(response)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"status": 400, "error": "Bad Request", "message": str(e)})


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
                description: An Error Occured
        """
        id = "tb_gx_rejected_samples_by_facility_month"

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

        print(req_args)

        try:
            # Get the data
            response = rejected_samples_by_facility_by_month_service(req_args)
            return jsonify(response)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"status": 400, "error": "Bad Request", "message": str(e)})


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
                description: An Error Occured
        """

        id = "tb_gx_rejected_samples_by_facility_by_reason"

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

        # print(req_args)

        try:
            # Get the data
            response = rejected_samples_by_facility_by_reason_service(req_args)
            return jsonify(response)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"status": 400, "error": "Bad Request", "message": str(e)})


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
                description: An Error Occured
        """

        id = "tb_gx_rejected_samples_by_facility_by_reason_month"

        parser = reqparse.RequestParser()

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

        # print(req_args)

        try:
            # Get the data
            response = rejected_samples_by_facility_by_reason_by_month_service(req_args)
            return jsonify(response)

        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            return jsonify({"status": 400, "error": "Bad Request", "message": str(e)})
