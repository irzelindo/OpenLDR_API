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
        responses:
          200:
            description: Returns a list of all facilities in JSON format.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      DistrictName:
                        type: string
                        example: "Moatize"
                      FacilityCode:
                        type: string
                        example: "25DSE"
                      FacilityName:
                        type: string
                        example: "CS 25 de Setembro (Moatize)"
                      FacilityNationalCode:
                        type: string
                        example: "01051018"
                      FacilityType:
                        type: string
                        example: "H"
                      HFStatus:
                        type: integer
                        example: 1
                      Latitude:
                        type: string
                        example: "-16.10712"
                      Longitude:
                        type: string
                        example: "33.70252"
                      ProvinceName:
                        type: string
                        example: "Tete"
        """

        id = "get all facilities"
        return jsonify(get_all_facilities())


class dict__facilities__by_province(Resource):
    def get(self, province):
        """
        Get all facilities by province.
        ---
        tags:
          - Dictionary/Facilities
        parameters:
            - $ref: '#/parameters/ProvinceParameter'
        responses:
          200:
            description: A list of all facilities in the given province
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      FacilityCode:
                        type: string
                        example: "25DSE"
                      FacilityName:
                        type: string
                        example: "CS 25 de Setembro (Moatize)"
                      FacilityNationalCode:
                        type: string
                        example: "01051018"
                      FacilityType:
                        type: string
                        example: "H"
                      HFStatus:
                        type: integer
                        example: 1
                      Latitude:
                        type: string
                        example: "-16.10712"
                      Longitude:
                        type: string
                        example: "33.70252"
                      ProvinceName:
                        type: string
                        example: "Tete"
          400:
            description: Invalid province name provided
          404:
            description: No facilities found for the given province
        """
        id = "get all facilities by province"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "province",
            # type=lambda x: x,
            type=str,
            # location="args",
            # action="append",
            location="view_args",
            help="This field cannot be blank.",
        )
        req_args = parser.parse_args()

        print(req_args)

        facilities = jsonify(get_facilities_by_province(req_args))

        return facilities


class dict__facilities__by_district(Resource):
    def get(self, district):
        """
        Get all facilities by district.
        ---
        tags:
          - Dictionary/Facilities
        parameters:
          # - $ref: '#/parameters/ProvinceParameter'
          - $ref: '#/parameters/DistrictParameter'
        responses:
          200:
            description: A list of all facilities in the given district.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      FacilityCode:
                        type: string
                        example: "25DSE"
                      FacilityName:
                        type: string
                        example: "CS 25 de Setembro (Moatize)"
                      FacilityNationalCode:
                        type: string
                        example: "01051018"
                      FacilityType:
                        type: string
                        example: "H"
                      HFStatus:
                        type: integer
                        example: 1
                      Latitude:
                        type: string
                        example: "-16.10712"
                      Longitude:
                        type: string
                        example: "33.70252"
                      ProvinceName:
                        type: string
                        example: "Tete"
                      DistrictName:
                        type: string
                        example: "Moatize"
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
            help="This field cannot be blank.",
        )
        req_args = parser.parse_args()

        # print(req_args)

        facilities = jsonify(get_facilities_by_district(req_args))

        return facilities
