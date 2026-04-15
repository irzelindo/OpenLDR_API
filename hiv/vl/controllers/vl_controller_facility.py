from flask import jsonify, request, session
from flask_restful import Resource, reqparse
from utilities.utils import get_unverified_payload, get_token, get_user_token_info
from hiv.vl.services.vl_services_facilities import (
    facility_registered_samples_service,
    facility_tested_samples_by_month_service,
    facility_tested_samples_by_facility_service,
    facility_tested_samples_by_month_by_gender_service,
    facility_tested_samples_by_gender_by_facility_service,
    facility_tested_samples_by_age_by_month_service,
    facility_tested_samples_by_age_by_facility_service,
    facility_tested_samples_by_test_reason_by_month_service,
    facility_tested_samples_by_test_reason_by_facility_service,
    facility_tested_samples_pregnant_service,
    facility_tested_samples_breastfeeding_service,
    facility_rejected_samples_by_month_service,
    facility_rejected_samples_by_facility_service,
    facility_tat_by_month_service,
    facility_tat_by_facility_service,
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


class VlFacilityRegisteredSamples(Resource):
    def get(self):
        """
        Retrieve registered samples by requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Registered samples by requesting facility
            401:
                description: Missing or invalid JWT token
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
            return jsonify(facility_registered_samples_service(req_args))
        except Exception as e:
            return jsonify(
                {
                    "error": "An internal error occurred.",
                    "message": str(e),
                    "status": 500,
                }
            )


class VlFacilityTestedSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve tested samples by month (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by month (facility)
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
            return jsonify(facility_tested_samples_by_month_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTestedSamplesByFacility(Resource):
    def get(self):
        """
        Retrieve tested samples grouped by requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by requesting facility
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
            return jsonify(facility_tested_samples_by_facility_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTestedSamplesByGenderByMonth(Resource):
    def get(self):
        """
        Retrieve tested samples by gender (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by gender (facility)
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
            return jsonify(facility_tested_samples_by_month_by_gender_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTestedSamplesByGenderByFacility(Resource):
    def get(self):
        """
        Retrieve tested samples by gender and requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by gender and requesting facility
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
            return jsonify(facility_tested_samples_by_gender_by_facility_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTestedSamplesByAgeByMonth(Resource):
    def get(self):
        """
        Retrieve tested samples by age group (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by age group (facility)
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
            return jsonify(facility_tested_samples_by_age_by_month_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTestedSamplesByAgeByFacility(Resource):
    def get(self):
        """
        Retrieve tested samples by age group and requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by age group and requesting facility
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
            return jsonify(facility_tested_samples_by_age_by_facility_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTestedSamplesByTestReasonByMonth(Resource):
    def get(self):
        """
        Retrieve tested samples by test reason (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by test reason (facility)
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
            return jsonify(facility_tested_samples_by_test_reason_by_month_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTestedSamplesByTestReasonByFacility(Resource):
    def get(self):
        """
        Retrieve tested samples by test reason (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples by test reason (facility)
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
            return jsonify(facility_tested_samples_by_test_reason_by_facility_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTestedSamplesPregnant(Resource):
    def get(self):
        """
        Retrieve tested samples for pregnant women (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples for pregnant women (facility)
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
            return jsonify(facility_tested_samples_pregnant_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTestedSamplesBreastfeeding(Resource):
    def get(self):
        """
        Retrieve tested samples for breastfeeding women (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Tested samples for breastfeeding women (facility)
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
            return jsonify(facility_tested_samples_breastfeeding_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityRejectedSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve rejected samples by month (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Rejected samples by month (facility)
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
            return jsonify(facility_rejected_samples_by_month_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityRejectedSamplesByFacility(Resource):
    def get(self):
        """
        Retrieve rejected samples grouped by requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Rejected samples by requesting facility
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
            return jsonify(facility_rejected_samples_by_facility_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTatByMonth(Resource):
    def get(self):
        """
        Retrieve turnaround time by month (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Turnaround time by month (facility)
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
            return jsonify(facility_tat_by_month_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})


class VlFacilityTatByFacility(Resource):
    def get(self):
        """
        Retrieve turnaround time grouped by requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Turnaround time by requesting facility
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
            return jsonify(facility_tat_by_facility_service(req_args))
        except Exception as e:
            return jsonify({"error": "An internal error occurred.", "message": str(e), "status": 500})
