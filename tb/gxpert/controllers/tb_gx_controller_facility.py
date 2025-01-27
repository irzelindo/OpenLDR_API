from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
from tb.gxpert.services.tb_gx_services_facilities import (
    registered_samples_by_facility_ultra,
    tested_samples_by_facility_ultra,
)


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
                description: Facility not found

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

        registered_samples = jsonify(registered_samples_by_facility_ultra(req_args))

        return registered_samples


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

        # print(req_args)

        tested_samples = jsonify(tested_samples_by_facility_ultra(req_args))

        return tested_samples
