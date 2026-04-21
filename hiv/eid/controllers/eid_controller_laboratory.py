from flask import jsonify, request, session
from flask_restful import Resource, reqparse
from utilities.utils import get_unverified_payload, get_token, get_user_token_info
from hiv.eid.services.eid_services_laboratory import (
    tested_samples_by_month_service,
    registered_samples_by_month_service,
    tested_samples_service,
    tat_service,
    tat_samples_service,
    rejected_samples_service,
    rejected_samples_by_month_service,
    samples_by_equipment_service,
    samples_by_equipment_by_month_service,
    sample_routes_service,
    sample_routes_viewport_service,
)


def _parse_eid_common_args():
    """Parse standardized query parameters for EID endpoints."""
    parser = reqparse.RequestParser()
    parser.add_argument("interval_dates", type=lambda x: x, location="args", action="append")
    parser.add_argument("province", type=lambda x: x, location="args", action="append")
    parser.add_argument("district", type=lambda x: x, location="args", action="append")
    parser.add_argument("health_facility", type=str, location="args")
    parser.add_argument("facility_type", type=str, location="args")
    parser.add_argument("disaggregation", type=str, location="args")
    parser.add_argument("lab_type", type=str, location="args", default="all")
    parser.add_argument("category", type=int, location="args")
    parser.add_argument("viewport", type=str, location="args")
    return parser.parse_args()


def _execute_eid_service(service, req_args):
    """Execute an EID service with token validation and normalized error responses."""
    token = get_token(request) or "Unknown"

    try:
        token_payload = get_unverified_payload(token)
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occurred",
                    "error": str(e),
                }
            ),
            500,
        )

    session["user_info"] = get_user_token_info(token_payload)
    user_id = str(session.get("user_info").get("user_id"))
    req_args["user_id"] = user_id

    try:
        return jsonify(service(req_args))
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "code": 500,
                    "message": "An Error Occurred",
                    "error": str(e),
                }
            ),
            500,
        )


class EidTestedSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve EID tested samples by month
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
        responses:
            200:
                description: EID tested samples by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(tested_samples_by_month_service, req_args)


class EidRegisteredSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve EID registered samples by month
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
        responses:
            200:
                description: EID registered samples by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(registered_samples_by_month_service, req_args)


class EidTestedSamples(Resource):
    def get(self):
        """
        Retrieve EID tested samples by laboratory
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
        responses:
            200:
                description: EID tested samples by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(tested_samples_service, req_args)


class EidTat(Resource):
    def get(self):
        """
        Retrieve EID turnaround time by laboratory
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
        responses:
            200:
                description: EID turnaround time by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(tat_service, req_args)


class EidTatSamples(Resource):
    def get(self):
        """
        Retrieve EID TAT sample distribution by time brackets
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
            - $ref: '#/parameters/TATCategoryParameter'
        responses:
            200:
                description: EID TAT sample distribution
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(tat_samples_service, req_args)


class EidRejectedSamples(Resource):
    def get(self):
        """
        Retrieve EID rejected samples by laboratory
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
        responses:
            200:
                description: EID rejected samples by laboratory
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(rejected_samples_service, req_args)


class EidRejectedSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve EID rejected samples by month
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
        responses:
            200:
                description: EID rejected samples by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(rejected_samples_by_month_service, req_args)


class EidSamplesByEquipment(Resource):
    def get(self):
        """
        Retrieve EID samples by equipment type
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
        responses:
            200:
                description: EID samples by equipment type
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(samples_by_equipment_service, req_args)


class EidSamplesByEquipmentByMonth(Resource):
    def get(self):
        """
        Retrieve EID samples by equipment type by month
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
        responses:
            200:
                description: EID samples by equipment type by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(samples_by_equipment_by_month_service, req_args)


class EidSampleRoutes(Resource):
    def get(self):
        """
        Retrieve EID sample routes between facilities
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
        responses:
            200:
                description: EID sample routes
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(sample_routes_service, req_args)


class EidSampleRoutesViewport(Resource):
    def get(self):
        """
        Retrieve EID sample routes filtered by viewport
        ---
        tags:
            - HIV EID/Laboratories
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
            - $ref: '#/parameters/LabTypeParameter'
            - $ref: '#/parameters/ViewportParameter'
        responses:
            200:
                description: EID sample routes within viewport
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(sample_routes_viewport_service, req_args)
