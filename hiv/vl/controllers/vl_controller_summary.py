from flask import jsonify
from flask_restful import Resource, reqparse
from hiv.vl.services.vl_services_summary import (
    header_indicators_service_by_month,
    number_of_samples_service_by_month,
    viral_suppression_service_by_month,
    tat_service_by_month,
    suppression_by_province_service_by_month,
    samples_history_service_by_month,
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


class VlSummaryHeaderIndicatorsByMonth(Resource):
    def get(self):
        """
        Retrieve header indicator counts for the summary dashboard
        ---
        tags:
            - HIV Viral Load/Summary
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Header indicator counts (registered, tested, suppressed, not_suppressed, rejected)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()

        return jsonify(header_indicators_service_by_month(req_args))


class VlSummaryNumberOfSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve monthly sample counts for the summary dashboard
        ---
        tags:
            - HIV Viral Load/Summary
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Monthly sample counts grouped by year/month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()

        return jsonify(number_of_samples_service_by_month(req_args))


class VlSummaryViralSuppressionByMonth(Resource):
    def get(self):
        """
        Retrieve monthly viral suppression trend for the summary dashboard
        ---
        tags:
            - HIV Viral Load/Summary
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Monthly suppression trend (suppressed, not_suppressed)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()

        return jsonify(viral_suppression_service_by_month(req_args))


class VlSummaryTatByMonth(Resource):
    def get(self):
        """
        Retrieve monthly turnaround time summary for the dashboard
        ---
        tags:
            - HIV Viral Load/Summary
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Monthly TAT averages (collection_reception, reception_registration, registration_analysis, analysis_validation)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()

        return jsonify(tat_service_by_month(req_args))


class VlSummarySuppressionByProvinceByMonth(Resource):

    def get(self):
        """
        Retrieve viral suppression counts grouped by province (provincial map)
        ---
        tags:
            - HIV Viral Load/Summary
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Suppression counts grouped by RequestingProvinceName
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()

        return jsonify(suppression_by_province_service_by_month(req_args))


class VlSummarySamplesHistoryByMonth(Resource):

    def get(self):
        """
        Retrieve historical sample counts by year/month
        ---
        tags:
            - HIV Viral Load/Summary
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: Historical sample counts grouped by year/month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_common_args()
        
        return jsonify(samples_history_service_by_month(req_args))
