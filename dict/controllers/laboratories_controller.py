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

        :param lab_type: laboratory type.
        :return: all laboratories in JSON format.
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

        :param province: province name.
        :return: all laboratories in the given province in JSON format.
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
    def get(self, province, district):
        """
        Get all laboratories by district.

        :param province: province name.
        :param district: district name.
        :return: all laboratories in the given district in JSON format.
        """
        id = "get all laboratories by district"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "province",
            type=str,
            location="view_args",
            help="This field cannot be blank.",
        )
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
