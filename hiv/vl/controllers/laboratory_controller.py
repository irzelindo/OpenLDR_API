from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
from hiv.vl.services.laboratory_services import get_registered_samples_service


class RegisteredSamples(Resource):
    # Define a function to retrieve tested samples per laboratory
    def get(self):
        id = "laboratory_get_registered_samples"
        parser = reqparse.RequestParser()
        parser.add_argument(
            "provinces",
            type=lambda x: x,
            location="args",
            action="append",
            # default=[*provinces],
            help="This field cannot be blank.",
        )
        parser.add_argument(
            "dates",
            type=lambda x: x,
            location="args",
            action="append",
            # default=[*dates],
            help="This field cannot be blank.",
        )
        parser.add_argument("filter_by", type=str, location="args")

        req_args = parser.parse_args()

        registered_samples = jsonify(get_registered_samples_service(req_args))

        return registered_samples
