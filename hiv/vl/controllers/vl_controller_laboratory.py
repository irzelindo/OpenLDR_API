from flask import jsonify, request, session
from flask_restful import Resource, reqparse
from utilities.utils import get_unverified_payload, get_token, get_user_token_info
from hiv.vl.services.vl_services_laboratory import (
    registered_samples_service,
    registered_samples_by_month_service,
    tested_samples_service,
    tested_samples_by_month_service,
    tested_samples_by_gender_service,
    tested_samples_by_gender_by_lab_service,
    tested_samples_by_age_service,
    tested_samples_by_test_reason_service,
    tested_samples_pregnant_service,
    tested_samples_breastfeeding_service,
    rejected_samples_service,
    rejected_samples_by_month_service,
    tat_by_lab_service,
    tat_by_month_service,
    suppression_service,
)


def _parse_common_args():
    """Parse standardized query parameters."""
    parser = reqparse.RequestParser()
    parser.add_argument("interval_dates", type=lambda x: x, location="args", action="append")
    parser.add_argument("province", type=lambda x: x, location="args", action="append")
    parser.add_argument("district", type=lambda x: x, location="args", action="append")
    parser.add_argument("health_facility", type=str, location="args")
    parser.add_argument("facility_type", type=str, location="args")
    parser.add_argument("disaggregation", type=str, location="args")
    return parser.parse_args()


class VlRegisteredSamples(Resource):
    def get(self):
        """
        Retrieve registered samples by laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Registered samples by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(registered_samples_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlRegisteredSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve registered samples by laboratory and month
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Registered samples by laboratory and month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(registered_samples_by_month_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTestedSamples(Resource):
    def get(self):
        """
        Retrieve tested samples by laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tested_samples_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTestedSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve tested samples by month
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tested_samples_by_month_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTestedSamplesByGender(Resource):
    def get(self):
        """
        Retrieve tested samples by gender
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by gender
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tested_samples_by_gender_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTestedSamplesByGenderByLab(Resource):
    def get(self):
        """
        Retrieve tested samples by gender and laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by gender and laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tested_samples_by_gender_by_lab_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTestedSamplesByAge(Resource):
    def get(self):
        """
        Retrieve tested samples by age group
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by age group
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tested_samples_by_age_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTestedSamplesByTestReason(Resource):
    def get(self):
        """
        Retrieve tested samples by test reason
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by test reason
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tested_samples_by_test_reason_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTestedSamplesPregnant(Resource):
    def get(self):
        """
        Retrieve tested samples for pregnant women
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples for pregnant women
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tested_samples_pregnant_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTestedSamplesBreastfeeding(Resource):
    def get(self):
        """
        Retrieve tested samples for breastfeeding women
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples for breastfeeding women
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tested_samples_breastfeeding_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlRejectedSamples(Resource):
    def get(self):
        """
        Retrieve rejected samples by laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Rejected samples by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(rejected_samples_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlRejectedSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve rejected samples by month
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Rejected samples by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(rejected_samples_by_month_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTatByLab(Resource):
    def get(self):
        """
        Retrieve turnaround time by laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Turnaround time by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tat_by_lab_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlTatByMonth(Resource):
    def get(self):
        """
        Retrieve turnaround time by month
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Turnaround time by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(tat_by_month_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlSuppression(Resource):
    def get(self):
        """
        Retrieve suppression trend by month
        ---
        tags:
            - HIV Viral Load/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Suppression trend by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        token = get_token(request) or "Unknown"

        try:
            token_payload = get_unverified_payload(token)
        except Exception as e:
            return jsonify({"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)})

        session["user_info"] = get_user_token_info(token_payload)
        user_id = str(session.get("user_info").get("user_id"))

        req_args = _parse_common_args()
        req_args["user_id"] = user_id

        try:
            return jsonify(suppression_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})
