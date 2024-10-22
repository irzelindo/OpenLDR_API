from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
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
        parameters:
          - $ref: '#/parameters/ProvinceParameter'
        responses:
          200:
            description: Returns a list of all facilities in JSON format.
            schema:
              $ref: '#/components/schemas/Facilities'
          400:
            description: Invalid district name provided
          404:
            description: District not found
        """
        id = "get all facilities"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "province",
            type=lambda x: x,
            # type=str,
            location="args",
            action="append",
            # location="view_args",
            help="This field cannot be blank.",
        )
        req_args = parser.parse_args()

        if req_args["province"] is None:
            return jsonify(get_all_facilities())
        else:
            return jsonify(get_facilities_by_province(req_args))


class dict__facilities__by_district(Resource):
    def get(self, district):
        """
        Get all facilities by district.
        ---
        tags:
          - Dictionary/Facilities
        parameters:
          - $ref: '#/parameters/DistrictParameter'
        responses:
          200:
            description: A list of all facilities in the given district.
            schema:
              $ref: '#/components/schemas/Facilities'
          400:
            description: Invalid district name provided
          404:
            description: District not found
        """
        id = "get all facilities by district"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "district",
            # type=lambda x: x,
            type=str,
            # location="args",
            location="view_args",
            # action="append",
            help="This field cannot be blank.",
        )
        req_args = parser.parse_args()

        print(req_args)

        facilities = jsonify(get_facilities_by_district(req_args))

        return facilities
