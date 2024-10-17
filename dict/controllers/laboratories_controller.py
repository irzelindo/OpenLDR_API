from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
from dict.services.laboratories_services import (
    get_all_laboratories,
    get_laboratories_by_province,
    get_laboratories_by_district,
)


class dict__laboratories(Resource):
    def get(self):
        """
        Get all laboratories.
        ---
        tags:
          - Dictionary/Laboratories
        parameters:
            - $ref: '#/parameters/LabTypeParameter'
        responses:
          200:
            description: A list of all laboratories.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      LabCode:
                        type: string
                        example: "LAB001"
                      LabName:
                        type: string
                        example: "Central Research Laboratory"
                      LabType:
                        type: string
                        example: "public"
                      StaffingLevel:
                        type: string
                        example: "High"
                      FacilityCode:
                        type: string
                        example: "FAC123"
                      DateTimeStamp:
                        type: string
                        format: date-time
                        example: "2024-03-12T08:55:23Z"
          400:
            description: Invalid lab type provided.
          404:
            description: No laboratories found.
        """
        id = "get all laboratories"
        parser = reqparse.RequestParser()

        parser.add_argument(
            "lab_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        print(req_args)

        return jsonify(get_all_laboratories(req_args))


class dict__laboratories__by_province(Resource):
    def get(self, province):
        """
        Get all laboratories by province.
        ---
        tags:
          - Dictionary/Laboratories
        parameters:
          - $ref: '#/parameters/ProvinceParameter'
        responses:
          200:
            description: A list of all laboratories in the given province.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      LabCode:
                        type: string
                        example: "LAB001"
                      LabName:
                        type: string
                        example: "Central Research Laboratory"
                      LabType:
                        type: string
                        example: "public"
                      StaffingLevel:
                        type: string
                        example: "High"
                      FacilityCode:
                        type: string
                        example: "FAC123"
                      DateTimeStamp:
                        type: string
                        format: date-time
                        example: "2024-03-12T08:55:23Z"
          404:
            description: No laboratories found for the specified province.
        """
        id = "get all laboratories by province"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "province",
            type=str,
            location="view_args",
            help="This field cannot be blank.",
        )

        parser.add_argument(
            "lab_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )
        req_args = parser.parse_args()

        print(req_args)

        return jsonify(get_laboratories_by_province(req_args))


class dict__laboratories__by_district(Resource):
    def get(self, district):
        """
        Get all laboratories by district.
        ---
        tags:
          - Dictionary/Laboratories
        parameters:
          - $ref: '#/parameters/DistrictParameter'
        responses:
          200:
            description: A list of all laboratories in the given district.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      LabCode:
                        type: string
                        example: "LAB001"
                      LabName:
                        type: string
                        example: "Central Research Laboratory"
                      LabType:
                        type: string
                        example: "public"
                      StaffingLevel:
                        type: string
                        example: "High"
                      FacilityCode:
                        type: string
                        example: "FAC123"
                      DateTimeStamp:
                        type: string
                        format: date-time
                        example: "2024-03-12T08:55:23Z"
          404:
            description: No laboratories found for the specified district.
        """
        id = "get all laboratories by district"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "district",
            type=str,
            location="view_args",
            help="This field cannot be blank.",
        )
        parser.add_argument(
            "lab_type",
            type=str,
            location="args",
            help="This field cannot be blank.",
        )

        req_args = parser.parse_args()

        print(req_args)

        return jsonify(get_laboratories_by_district(req_args))
