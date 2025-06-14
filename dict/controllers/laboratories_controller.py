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
                $ref: '#/components/schemas/Facilities'
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
    def get(self):
        """
        Get all laboratories by province.
        ---
        tags:
          - Dictionary/Laboratories
        parameters:
          - $ref: '#/parameters/ProvinceParameter'
          - $ref: '#/parameters/LabTypeParameter'
        responses:
          200:
            description: A list of all laboratories in the given province.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Facilities'
          404:
            description: No laboratories found for the specified province.
        """
        id = "get all laboratories by province"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "province",
            # type=str,
            # location="view_args",
            type=lambda x: x,
            action="append",
            # location="view_args",
            location="args",
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
    def get(self):
        """
        Get all laboratories by district.
        ---
        tags:
          - Dictionary/Laboratories
        parameters:
          - $ref: '#/parameters/DistrictParameter'
          - $ref: '#/parameters/LabTypeParameter'
        responses:
          200:
            description: A list of all laboratories in the given district.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Facilities'
          404:
            description: No laboratories found for the specified district.
        """
        id = "get all laboratories by district"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "district",
            # type=str,
            type=lambda x: x,
            action="append",
            # location="view_args",
            location="args",
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
