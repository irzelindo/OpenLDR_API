from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from hiv.vl.services.vl_services_facilities import (
    facility_registered_samples_service,
    facility_tested_samples_by_month_service,
    facility_tested_samples_by_facility_service,
    facility_tested_samples_by_gender_service,
    facility_tested_samples_by_gender_by_facility_service,
    facility_tested_samples_by_age_service,
    facility_tested_samples_by_age_by_facility_service,
    facility_tested_samples_by_test_reason_service,
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
    @jwt_required()
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
            - $ref: '#/parameters/FacilityTypeParameter'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Registered samples by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_registered_samples_service(req_args))


class VlFacilityTestedSamplesByMonth(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by month (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Tested samples by month (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tested_samples_by_month_service(req_args))


class VlFacilityTestedSamplesByFacility(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples grouped by requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Tested samples by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tested_samples_by_facility_service(req_args))


class VlFacilityTestedSamplesByGender(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by gender (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Tested samples by gender (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tested_samples_by_gender_service(req_args))


class VlFacilityTestedSamplesByGenderByFacility(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by gender and requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Tested samples by gender and requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tested_samples_by_gender_by_facility_service(req_args))


class VlFacilityTestedSamplesByAge(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by age group (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Tested samples by age group (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tested_samples_by_age_service(req_args))


class VlFacilityTestedSamplesByAgeByFacility(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by age group and requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Tested samples by age group and requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tested_samples_by_age_by_facility_service(req_args))


class VlFacilityTestedSamplesByTestReason(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples by test reason (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Tested samples by test reason (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tested_samples_by_test_reason_service(req_args))


class VlFacilityTestedSamplesPregnant(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples for pregnant women (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Tested samples for pregnant women (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tested_samples_pregnant_service(req_args))


class VlFacilityTestedSamplesBreastfeeding(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve tested samples for breastfeeding women (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Tested samples for breastfeeding women (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tested_samples_breastfeeding_service(req_args))


class VlFacilityRejectedSamplesByMonth(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve rejected samples by month (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Rejected samples by month (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_rejected_samples_by_month_service(req_args))


class VlFacilityRejectedSamplesByFacility(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve rejected samples grouped by requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Rejected samples by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_rejected_samples_by_facility_service(req_args))


class VlFacilityTatByMonth(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve turnaround time by month (facility)
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Turnaround time by month (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tat_by_month_service(req_args))


class VlFacilityTatByFacility(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve turnaround time grouped by requesting facility
        ---
        tags:
            - HIV Viral Load/Facilities
        responses:
            200:
                description: Turnaround time by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        return jsonify(facility_tat_by_facility_service(req_args))
