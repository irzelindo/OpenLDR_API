from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
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
    @jwt_required()
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
        req_args = _parse_common_args()
        return jsonify(registered_samples_service(req_args))


class VlRegisteredSamplesByMonth(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve registered samples by laboratory and month
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Registered samples by laboratory and month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(registered_samples_by_month_service(req_args))


class VlTestedSamples(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Tested samples by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tested_samples_service(req_args))


class VlTestedSamplesByMonth(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by month
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Tested samples by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tested_samples_by_month_service(req_args))


class VlTestedSamplesByGender(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by gender
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Tested samples by gender
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tested_samples_by_gender_service(req_args))


class VlTestedSamplesByGenderByLab(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by gender and laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Tested samples by gender and laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tested_samples_by_gender_by_lab_service(req_args))


class VlTestedSamplesByAge(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by age group
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Tested samples by age group
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tested_samples_by_age_service(req_args))


class VlTestedSamplesByTestReason(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by test reason
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Tested samples by test reason
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tested_samples_by_test_reason_service(req_args))


class VlTestedSamplesPregnant(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples for pregnant women
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Tested samples for pregnant women
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tested_samples_pregnant_service(req_args))


class VlTestedSamplesBreastfeeding(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples for breastfeeding women
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Tested samples for breastfeeding women
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tested_samples_breastfeeding_service(req_args))


class VlRejectedSamples(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve rejected samples by laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Rejected samples by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(rejected_samples_service(req_args))


class VlRejectedSamplesByMonth(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve rejected samples by month
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Rejected samples by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(rejected_samples_by_month_service(req_args))


class VlTatByLab(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve turnaround time by laboratory
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Turnaround time by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tat_by_lab_service(req_args))


class VlTatByMonth(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve turnaround time by month
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Turnaround time by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(tat_by_month_service(req_args))


class VlSuppression(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve suppression trend by month
        ---
        tags:
            - HIV Viral Load/Laboratories
        responses:
            200:
                description: Suppression trend by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(suppression_service(req_args))
