from flask import jsonify
from flask_restful import Resource, reqparse
from dict.services.facilities_services import (
    get_all_facilities,
    get_facilities_by_province,
    get_facilities_by_district,
)


class dict__facilities(Resource):
    def get(self):
        """
        Get all facilities.
        ---
        tags:
            - Dictionary/Facilities
        responses:
            200:
                description: A list of all facilities.
            400:
                description: Invalid facility type provided.
            404:
                description: No facilities found.
        """

        try:

            reponse = get_all_facilities()

            return jsonify(reponse)

        except Exception as e:

            return jsonify(
                {
                    "status": "error",
                    "error": "Failed to retrieve facilities",
                    "message": str(e),
                }
            )


class dict__facilities__by_province(Resource):
    def get(self):
        """
        Get all facilities by province.
        ---
        tags:
            - Dictionary/Facilities
        parameters:
            - $ref: '#/parameters/ProvinceParameter'
        responses:
            200:
                description: A list of all facilities.
            400:
                description: Invalid facility type provided.
            404:
                description: No facilities found.
        """
        parser = reqparse.RequestParser()

        parser.add_argument(
            "province",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )
        req_args = parser.parse_args()

        try:

            facilities = get_facilities_by_province(req_args)

            return jsonify(facilities)

        except Exception as e:

            return jsonify(
                {
                    "status": "error",
                    "error": "Failed to retrieve facilities by province",
                    "message": str(e),
                }
            )


class dict__facilities__by_district(Resource):
    def get(self):
        """
        Get all facilities by district.
        ---
        tags:
            - Dictionary/Facilities
        parameters:
            - $ref: '#/parameters/DistrictParameter'
        responses:
            200:
                description: A list of all facilities.
            400:
                description: Invalid facility type provided.
            404:
                description: No facilities found.
        """

        parser = reqparse.RequestParser()

        parser.add_argument(
            "district",
            type=lambda x: x,
            location="args",
            action="append",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        try:

            facilities = get_facilities_by_district(req_args)

            return jsonify(facilities)

        except Exception as e:

            return jsonify(
                {
                    "message": str(e),
                    "status": "error",
                    "error": "Failed to retrieve facilities by district",
                }
            )
