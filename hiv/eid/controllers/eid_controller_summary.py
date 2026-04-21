from flask import jsonify
from flask_restful import Resource
from hiv.eid.controllers.eid_controller_laboratory import (
    _execute_eid_service,
    _parse_eid_common_args,
)
from hiv.eid.services.eid_services_summary import (
    summary_indicators_service,
    summary_tat_service,
    summary_tat_samples_service,
    summary_positivity_service,
    summary_number_of_samples_service,
    summary_indicators_by_province_service,
    summary_samples_positivity_service,
    summary_rejected_samples_by_month_service,
    summary_samples_by_equipment_service,
    summary_samples_by_equipment_by_month_service,
)


class EidSummaryIndicators(Resource):
    def get(self):
        """
        Retrieve EID summary indicators (registered, tested, rejected, pending, positive, negative)
        ---
        tags:
            - HIV EID/Summary
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
                description: EID summary indicators
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_indicators_service, req_args)


class EidSummaryTat(Resource):
    def get(self):
        """
        Retrieve EID summary TAT averages by month (6 hub segments)
        ---
        tags:
            - HIV EID/Summary
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
                description: EID summary TAT by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_tat_service, req_args)


class EidSummaryTatSamples(Resource):
    def get(self):
        """
        Retrieve EID summary TAT sample distribution by time brackets
        ---
        tags:
            - HIV EID/Summary
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
                description: EID summary TAT sample distribution
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_tat_samples_service, req_args)


class EidSummaryPositivity(Resource):
    def get(self):
        """
        Retrieve EID summary monthly positivity (total, positive, negative)
        ---
        tags:
            - HIV EID/Summary
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
                description: EID summary monthly positivity
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_positivity_service, req_args)


class EidSummaryNumberOfSamples(Resource):
    def get(self):
        """
        Retrieve EID summary monthly sample counts
        ---
        tags:
            - HIV EID/Summary
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
                description: EID summary monthly sample counts
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_number_of_samples_service, req_args)


class EidSummaryIndicatorsByProvince(Resource):
    def get(self):
        """
        Retrieve EID summary indicators per province
        ---
        tags:
            - HIV EID/Summary
        parameters:
            - $ref: '#/parameters/IntervalDates'
            - $ref: '#/parameters/ProvinceParameter'
            - $ref: '#/parameters/DistrictParameter'
            - $ref: '#/parameters/HealthFacilityParameter'
            - $ref: '#/parameters/FacilityType'
            - $ref: '#/parameters/DisaggregationParameter'
        responses:
            200:
                description: EID summary indicators by province
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_indicators_by_province_service, req_args)


class EidSummarySamplesPositivity(Resource):
    def get(self):
        """
        Retrieve EID summary samples positivity with gender splits
        ---
        tags:
            - HIV EID/Summary
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
                description: EID summary samples positivity breakdown
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_samples_positivity_service, req_args)


class EidSummaryRejectedSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve EID summary rejected samples grouped by month
        ---
        tags:
            - HIV EID/Summary
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
                description: EID summary rejected samples by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_rejected_samples_by_month_service, req_args)


class EidSummarySamplesByEquipment(Resource):
    def get(self):
        """
        Retrieve EID summary samples by equipment type
        ---
        tags:
            - HIV EID/Summary
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
                description: EID summary samples by equipment
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_samples_by_equipment_service, req_args)


class EidSummarySamplesByEquipmentByMonth(Resource):
    def get(self):
        """
        Retrieve EID summary samples by equipment type by month
        ---
        tags:
            - HIV EID/Summary
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
                description: EID summary samples by equipment by month
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(summary_samples_by_equipment_by_month_service, req_args)
