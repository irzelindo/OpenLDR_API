from flask import jsonify
from flask_restful import Resource
from hiv.eid.services.eid_services_facilities import (
    facility_registered_samples_service,
    facility_registered_samples_by_month_service,
    facility_tested_samples_service,
    facility_tested_samples_by_month_service,
    facility_tested_samples_by_gender_service,
    facility_tested_samples_by_gender_by_month_service,
    facility_tat_avg_by_month_service,
    facility_tat_avg_service,
    facility_tat_days_by_month_service,
    facility_tat_days_service,
    facility_rejected_samples_by_month_service,
    facility_rejected_samples_service,
    facility_key_indicators_service,
    facility_tested_samples_by_age_service,
)
from hiv.eid.controllers.eid_controller_laboratory import (
    _execute_eid_service,
    _parse_eid_common_args,
)


class EidFacilityRegisteredSamples(Resource):
    def get(self):
        """
        Retrieve EID registered samples by requesting facility
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID registered samples by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_registered_samples_service, req_args)


class EidFacilityRegisteredSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve EID registered samples by month (facility)
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID registered samples by month (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_registered_samples_by_month_service, req_args)


class EidFacilityTestedSamples(Resource):
    def get(self):
        """
        Retrieve EID tested samples by requesting facility
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID tested samples by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_tested_samples_service, req_args)


class EidFacilityTestedSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve EID tested samples by month (facility)
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID tested samples by month (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_tested_samples_by_month_service, req_args)


class EidFacilityTestedSamplesByGender(Resource):
    def get(self):
        """
        Retrieve EID tested samples by gender and requesting facility
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID tested samples by gender and requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_tested_samples_by_gender_service, req_args)


class EidFacilityTestedSamplesByGenderByMonth(Resource):
    def get(self):
        """
        Retrieve EID tested samples by gender by month (facility)
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID tested samples by gender by month (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_tested_samples_by_gender_by_month_service, req_args)


class EidFacilityTatAvgByMonth(Resource):
    def get(self):
        """
        Retrieve EID average TAT by month (facility)
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID average TAT by month (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_tat_avg_by_month_service, req_args)


class EidFacilityTatAvg(Resource):
    def get(self):
        """
        Retrieve EID average TAT by requesting facility
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID average TAT by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_tat_avg_service, req_args)


class EidFacilityTatDaysByMonth(Resource):
    def get(self):
        """
        Retrieve EID TAT day brackets by month (facility)
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID TAT day brackets by month (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_tat_days_by_month_service, req_args)


class EidFacilityTatDays(Resource):
    def get(self):
        """
        Retrieve EID TAT day brackets by requesting facility
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID TAT day brackets by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_tat_days_service, req_args)


class EidFacilityRejectedSamplesByMonth(Resource):
    def get(self):
        """
        Retrieve EID rejected samples by month (facility)
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID rejected samples by month (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_rejected_samples_by_month_service, req_args)


class EidFacilityRejectedSamples(Resource):
    def get(self):
        """
        Retrieve EID rejected samples by requesting facility
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID rejected samples by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_rejected_samples_service, req_args)


class EidFacilityKeyIndicators(Resource):
    def get(self):
        """
        Retrieve EID key indicators by requesting facility
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID key indicators by requesting facility
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_key_indicators_service, req_args)


class EidFacilityTestedSamplesByAge(Resource):
    def get(self):
        """
        Retrieve EID tested samples by age group (facility)
        ---
        tags:
            - HIV EID/Facilities
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
                description: EID tested samples by age group (facility)
            401:
                description: Missing or invalid JWT token
            500:
                description: An Error Occurred
        """
        req_args = _parse_eid_common_args()
        return _execute_eid_service(facility_tested_samples_by_age_service, req_args)
