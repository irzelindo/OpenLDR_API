from flask_restful import Resource, reqparse
from hiv.vl.services.vl_services_patients import (
    get_patients_by_name_service,
    get_patients_by_facility_service,
    get_patients_by_result_type_service,
    get_patients_by_test_reason_service,
)
from flask import jsonify, request, session
from utilities.utils import get_unverified_payload, get_token, get_user_token_info


def _parse_common_args():
    """Parse standardized query parameters."""
    parser = reqparse.RequestParser()
    parser.add_argument("interval_dates", type=lambda x: x, location="args", action="append")
    parser.add_argument("province", type=lambda x: x, location="args", action="append")
    parser.add_argument("district", type=lambda x: x, location="args", action="append")
    parser.add_argument("test_reason", type=lambda x: x, location="args", action="append")
    parser.add_argument("health_facility", type=str, location="args")
    parser.add_argument("facility_type", type=str, location="args")
    parser.add_argument("disaggregation", type=str, location="args")
    parser.add_argument("first_name", type=str, location="args")
    parser.add_argument("surname", type=str, location="args")
    parser.add_argument("result_type", type=lambda x: x, location="args", action="append")
    parser.add_argument("test_reason", type=str, location="args")
    parser.add_argument("page", type=int, location="args", default=1)
    parser.add_argument("per_page", type=int, location="args", default=50)
    return parser.parse_args()


class VlPatientsByName(Resource):
    def get(self):
        """
        Retrieve VL patients by first name or surname between two dates
        ---
        tags:
            - HIV Viral Load/Patients
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - name: first_name
              in: query
              type: string
              required: false
              description: The patient's first name (partial match)
            - name: surname
              in: query
              type: string
              required: false
              description: The patient's surname (partial match)
            - $ref: '#/parameters/HealthFacilityParameter'
            - name: page
              in: query
              type: integer
              required: false
              default: 1
              description: Page number (1-indexed)
            - name: per_page
              in: query
              type: integer
              required: false
              default: 50
              description: Number of records per page
        responses:
            200:
                description: A List of VL Patients matching the name criteria.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occurred",
                    "error": str(e),
                }
            )

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            response = get_patients_by_name_service(req_args)
            return jsonify(response)
        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
            )


class VlPatientsByFacility(Resource):
    def get(self):
        """
        Retrieve VL patients registered at a specific health facility between two dates
        ---
        tags:
            - HIV Viral Load/Patients
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/HealthFacilityParameter'
            - name: page
              in: query
              type: integer
              required: false
              default: 1
              description: Page number (1-indexed)
            - name: per_page
              in: query
              type: integer
              required: false
              default: 50
              description: Number of records per page
        responses:
            200:
                description: A List of VL Patients registered at the facility.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occurred",
                    "error": str(e),
                }
            )

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            response = get_patients_by_facility_service(req_args)
            return jsonify(response)
        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
            )


class VlPatientsByResultType(Resource):
    def get(self):
        """
        Retrieve VL patients by viral load result category (suppressed / not_suppressed) between two dates
        ---
        tags:
            - HIV Viral Load/Patients
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - name: result_type
              in: query
              type: array
              required: true
              items:
                type: string
                enum: ["suppressed", "not_suppressed"]
              description: The viral load result category to filter by
            - $ref: '#/parameters/HealthFacilityParameter'
            - name: page
              in: query
              type: integer
              required: false
              default: 1
              description: Page number (1-indexed)
            - name: per_page
              in: query
              type: integer
              required: false
              default: 50
              description: Number of records per page
        responses:
            200:
                description: A List of VL Patients filtered by result type.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occurred",
                    "error": str(e),
                }
            )

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            response = get_patients_by_result_type_service(req_args)
            return jsonify(response)
        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
            )


class VlPatientsByTestReason(Resource):
    def get(self):
        """
        Retrieve VL patients by reason for test between two dates
        ---
        tags:
            - HIV Viral Load/Patients
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/TestReasonParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - name: page
              in: query
              type: integer
              required: false
              default: 1
              description: Page number (1-indexed)
            - name: per_page
              in: query
              type: integer
              required: false
              default: 50
              description: Number of records per page
        responses:
            200:
                description: A List of VL Patients filtered by test reason.
            400:
                description: Invalid Parameters
            403:
                description: Forbidden
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occurred",
                    "error": str(e),
                }
            )

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            response = get_patients_by_test_reason_service(req_args)
            return jsonify(response)
        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
            )
