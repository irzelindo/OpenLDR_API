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

        :return: all facilities in JSON format.
        """
        id = "get all facilities"
        return jsonify(get_all_facilities())


class dict__facilities__by_province(Resource):
    def get(self, province):
        """
        Get all facilities by province.

        :param province: province name.
        :return: all facilities in the given province in JSON format.
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
    def get(self, province, district):
        """
        Get all facilities by district.

        :param province: province name.
        :param district: district name.
        :return: all facilities in the given district in JSON format.
        """
        id = "get all facilities by district"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "province",
            # type=lambda x: x,
            type=str,
            # location="args",
            location="view_args",
            help="This field cannot be blank.",
        )
        parser.add_argument(
            "district",
            # type=lambda x: x,
            type=str,
            # location="args",
            location="view_args",
            help="This field cannot be blank.",
        )
        req_args = parser.parse_args()

        facilities = jsonify(get_facilities_by_district(req_args))

        return facilities
