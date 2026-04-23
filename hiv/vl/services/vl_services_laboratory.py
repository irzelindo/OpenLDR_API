from utilities.utils import (
    PROCESS_COMMON_PARAMS_VL,
    YEAR, MONTH, DATE_PART, TOTAL_ALL, TOTAL_NOT_NULL, TOTAL_NULL,
    SUPPRESSION, GENDER_SUPPRESSION, DATE_DIFF_AVG,
    and_, or_, func, case, text,
)
from db.database import db
from hiv.vl.models.vl import VlData
from utilities.auth_helpers import get_user_role as _get_user_role


def _check_health_facility_access(user_id, user_role, facility_type):
    """Return error dict if non-Admin tries to access health_facility level, else None."""
    if facility_type == "health_facility" and user_role != "Admin":
        return {
            "status": "error",
            "code": 403,
            "message": f"Forbidden - User with id {user_id} and role {user_role} is not authorized to access this resource.",
        }
    return None


def _build_facility_filters(facilities, facility_type):
    """Build facility filter conditions based on facility_type."""
    if not facilities:
        return []
    if facility_type == "province":
        return [VlData.TestingProvinceName.in_(facilities)]
    elif facility_type == "district":
        return [VlData.TestingDistrictName.in_(facilities)]
    elif facility_type == "health_facility":
        return [VlData.TestingFacilityName.in_(facilities)]
    return []


def _year_month_group_order(date_field):
    """Return (group_by, order_by) tuples for year/month grouping."""
    cols = [YEAR(date_field), MONTH(date_field), DATE_PART("month", date_field)]
    return cols, cols


def _suppression_entities():
    """Standard suppression with_entities columns."""
    return [
        SUPPRESSION(VlData.ViralLoadResultCategory, "Suppressed").label("suppressed"),
        SUPPRESSION(VlData.ViralLoadResultCategory, "Not Suppressed").label("not_suppressed"),
    ]


def _gender_suppression_entities():
    """Standard gender-stratified suppression columns."""
    return [
        GENDER_SUPPRESSION(
            [VlData.ViralLoadResultCategory, VlData.HL7SexCode],
            ["Suppressed", "M"],
        ).label("male_suppressed"),
        GENDER_SUPPRESSION(
            [VlData.ViralLoadResultCategory, VlData.HL7SexCode],
            ["Not Suppressed", "M"],
        ).label("male_not_suppressed"),
        GENDER_SUPPRESSION(
            [VlData.ViralLoadResultCategory, VlData.HL7SexCode],
            ["Suppressed", "F"],
        ).label("female_suppressed"),
        GENDER_SUPPRESSION(
            [VlData.ViralLoadResultCategory, VlData.HL7SexCode],
            ["Not Suppressed", "F"],
        ).label("female_not_suppressed"),
    ]


def _totals_entities():
    """Standard total/not_null/null columns."""
    return [
        TOTAL_ALL,
        TOTAL_NOT_NULL(VlData.ViralLoadResultCategory).label("total_not_null"),
        TOTAL_NULL(VlData.ViralLoadResultCategory).label("total_null"),
    ]


# ---------------------------------------------------------------------------
# 1. registered_samples_service
# ---------------------------------------------------------------------------
def registered_samples_service(req_args):
    """Registered samples grouped by year/month with suppression and gender splits."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [VlData.RegisteredDateTime.between(dates[0], dates[1])]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                *_suppression_entities(),
                *_gender_suppression_entities(),
                *_totals_entities(),
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                total=row.total, total_not_null=row.total_not_null,
                total_null=row.total_null, suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
                male_suppressed=row.male_suppressed,
                male_not_suppressed=row.male_not_suppressed,
                female_suppressed=row.female_suppressed,
                female_not_suppressed=row.female_not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 2. registered_samples_by_month_service
# ---------------------------------------------------------------------------
def registered_samples_by_month_service(req_args):
    """Registered samples grouped by year/month AND TestingFacilityName."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [VlData.RegisteredDateTime.between(dates[0], dates[1])]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                VlData.TestingFacilityName.label("testing_facility"),
                *_suppression_entities(),
                *_gender_suppression_entities(),
                *_totals_entities(),
            )
            .filter(and_(*filters))
            .group_by(*group_cols, VlData.TestingFacilityName)
            .order_by(*order_cols, VlData.TestingFacilityName)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                testing_facility=row.testing_facility,
                total=row.total, total_not_null=row.total_not_null,
                total_null=row.total_null, suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
                male_suppressed=row.male_suppressed,
                male_not_suppressed=row.male_not_suppressed,
                female_suppressed=row.female_suppressed,
                female_not_suppressed=row.female_not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 3. tested_samples_service
# ---------------------------------------------------------------------------
def tested_samples_service(req_args):
    """Tested samples grouped by TestingFacilityName."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    try:
        query = (
            VlData.query.with_entities(
                VlData.TestingFacilityName.label("testing_facility"),
                *_suppression_entities(),
                *_totals_entities(),
            )
            .filter(and_(*filters))
            .group_by(VlData.TestingFacilityName)
            .order_by(VlData.TestingFacilityName)
        )
        data = query.all()
        return [
            dict(
                testing_facility=row.testing_facility,
                total=row.total, total_not_null=row.total_not_null,
                total_null=row.total_null, suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 4. tested_samples_by_month_service
# ---------------------------------------------------------------------------
def tested_samples_by_month_service(req_args):
    """Tested samples grouped by year/month with suppression and gender splits."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                *_suppression_entities(),
                *_gender_suppression_entities(),
                *_totals_entities(),
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                total=row.total, total_not_null=row.total_not_null,
                total_null=row.total_null, suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
                male_suppressed=row.male_suppressed,
                male_not_suppressed=row.male_not_suppressed,
                female_suppressed=row.female_suppressed,
                female_not_suppressed=row.female_not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 5. tested_samples_by_gender_service
# ---------------------------------------------------------------------------
def tested_samples_by_gender_service(req_args):
    """Tested samples grouped by year/month with gender-stratified suppression."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                *_gender_suppression_entities(),
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                male_suppressed=row.male_suppressed,
                male_not_suppressed=row.male_not_suppressed,
                female_suppressed=row.female_suppressed,
                female_not_suppressed=row.female_not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 6. tested_samples_by_gender_by_lab_service
# ---------------------------------------------------------------------------
def tested_samples_by_gender_by_lab_service(req_args):
    """Tested samples grouped by year/month and TestingFacilityName with gender splits."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                VlData.TestingFacilityName.label("testing_facility"),
                *_gender_suppression_entities(),
            )
            .filter(and_(*filters))
            .group_by(*group_cols, VlData.TestingFacilityName)
            .order_by(*order_cols, VlData.TestingFacilityName)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                testing_facility=row.testing_facility,
                male_suppressed=row.male_suppressed,
                male_not_suppressed=row.male_not_suppressed,
                female_suppressed=row.female_suppressed,
                female_not_suppressed=row.female_not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 7. tested_samples_by_age_service
# ---------------------------------------------------------------------------
def tested_samples_by_age_service(req_args):
    """Tested samples grouped by year/month with age group classification."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    age_case = case(
        (VlData.AgeInYears.between(0, 14), "0-14"),
        (VlData.AgeInYears.between(15, 19), "15-19"),
        (VlData.AgeInYears.between(20, 24), "20-24"),
        (VlData.AgeInYears.between(25, 29), "25-29"),
        (VlData.AgeInYears.between(30, 34), "30-34"),
        (VlData.AgeInYears.between(35, 39), "35-39"),
        (VlData.AgeInYears.between(40, 44), "40-44"),
        (VlData.AgeInYears.between(45, 49), "45-49"),
        (VlData.AgeInYears >= 50, "50+"),
        else_="Unknown",
    ).label("age_group")

    try:
        # Use subquery to work around SQL Server parameterized CASE in GROUP BY
        subq = (
            db.session.query(
                VlData.AnalysisDateTime,
                age_case,
            )
            .filter(and_(*filters))
            .subquery()
        )
        query = (
            db.session.query(
                func.year(subq.c.AnalysisDateTime).label("year"),
                func.month(subq.c.AnalysisDateTime),
                func.datename(text("month"), subq.c.AnalysisDateTime),
                subq.c.age_group,
                func.count().label("total"),
            )
            .group_by(
                func.year(subq.c.AnalysisDateTime),
                func.month(subq.c.AnalysisDateTime),
                func.datename(text("month"), subq.c.AnalysisDateTime),
                subq.c.age_group,
            )
            .order_by(
                func.year(subq.c.AnalysisDateTime),
                func.month(subq.c.AnalysisDateTime),
                subq.c.age_group,
            )
        )
        data = query.all()
        return [
            dict(
                year=row[0], month=row[1], month_name=row[2],
                age_group=row.age_group, total=row.total,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 8. tested_samples_by_test_reason_service
# ---------------------------------------------------------------------------
def tested_samples_by_test_reason_service(req_args):
    """Tested samples grouped by year/month with test reason counts."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                func.count(case((VlData.ReasonForTest == "Routine", 1))).label("routine"),
                func.count(case((
                    VlData.ReasonForTest.in_([
                        "Suspected treatment failure",
                        "Suspeita de falha terapêutica",
                    ]), 1
                ))).label("treatment_failure"),
                func.count(case((
                    VlData.ReasonForTest.in_([
                        "Não preenchido",
                        "Reason Not Specified",
                    ]), 1
                ))).label("reason_not_specified"),
                TOTAL_ALL,
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                routine=row.routine, treatment_failure=row.treatment_failure,
                reason_not_specified=row.reason_not_specified, total=row.total,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 9. tested_samples_pregnant_service
# ---------------------------------------------------------------------------
def tested_samples_pregnant_service(req_args):
    """Tested samples for pregnant women grouped by year/month."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
        VlData.Pregnant == "Yes",
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                *_suppression_entities(),
                TOTAL_ALL,
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                total=row.total, suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 10. tested_samples_breastfeeding_service
# ---------------------------------------------------------------------------
def tested_samples_breastfeeding_service(req_args):
    """Tested samples for breastfeeding women grouped by year/month."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
        VlData.BreastFeeding == "Yes",
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                *_suppression_entities(),
                TOTAL_ALL,
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                total=row.total, suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 11. rejected_samples_service
# ---------------------------------------------------------------------------
def rejected_samples_service(req_args):
    """Rejected samples grouped by TestingFacilityName."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.LIMSRejectionCode.is_not(None),
        VlData.LIMSRejectionCode != "",
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    try:
        query = (
            VlData.query.with_entities(
                VlData.TestingFacilityName.label("testing_facility"),
                TOTAL_ALL,
            )
            .filter(and_(*filters))
            .group_by(VlData.TestingFacilityName)
            .order_by(VlData.TestingFacilityName)
        )
        data = query.all()
        return [
            dict(testing_facility=row.testing_facility, total=row.total)
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 12. rejected_samples_by_month_service
# ---------------------------------------------------------------------------
def rejected_samples_by_month_service(req_args):
    """Rejected samples grouped by year/month."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.LIMSRejectionCode.is_not(None),
        VlData.LIMSRejectionCode != "",
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                TOTAL_ALL,
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(year=row.year, month=row[1], month_name=row[2], total=row.total)
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 13. tat_by_lab_service
# ---------------------------------------------------------------------------
def tat_by_lab_service(req_args):
    """Turnaround time averages grouped by TestingFacilityName."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    try:
        query = (
            VlData.query.with_entities(
                VlData.TestingFacilityName.label("testing_facility"),
                DATE_DIFF_AVG([VlData.SpecimenDatetime, VlData.ReceivedDateTime]).label("collection_reception"),
                DATE_DIFF_AVG([VlData.ReceivedDateTime, VlData.RegisteredDateTime]).label("reception_registration"),
                DATE_DIFF_AVG([VlData.RegisteredDateTime, VlData.AnalysisDateTime]).label("registration_analysis"),
                DATE_DIFF_AVG([VlData.AnalysisDateTime, VlData.AuthorisedDateTime]).label("analysis_validation"),
            )
            .filter(and_(*filters))
            .group_by(VlData.TestingFacilityName)
            .order_by(VlData.TestingFacilityName)
        )
        data = query.all()
        return [
            dict(
                testing_facility=row.testing_facility,
                collection_reception=row.collection_reception,
                reception_registration=row.reception_registration,
                registration_analysis=row.registration_analysis,
                analysis_validation=row.analysis_validation,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 14. tat_by_month_service
# ---------------------------------------------------------------------------
def tat_by_month_service(req_args):
    """Turnaround time averages grouped by year/month."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                DATE_DIFF_AVG([VlData.SpecimenDatetime, VlData.ReceivedDateTime]).label("collection_reception"),
                DATE_DIFF_AVG([VlData.ReceivedDateTime, VlData.RegisteredDateTime]).label("reception_registration"),
                DATE_DIFF_AVG([VlData.RegisteredDateTime, VlData.AnalysisDateTime]).label("registration_analysis"),
                DATE_DIFF_AVG([VlData.AnalysisDateTime, VlData.AuthorisedDateTime]).label("analysis_validation"),
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                collection_reception=row.collection_reception,
                reception_registration=row.reception_registration,
                registration_analysis=row.registration_analysis,
                analysis_validation=row.analysis_validation,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 15. suppression_service
# ---------------------------------------------------------------------------
def suppression_service(req_args):
    """Monthly suppression trend (suppressed, not_suppressed, total)."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_health_facility_access(user_id, user_role, facility_type)
    if access_error:
        return access_error

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.AnalysisDateTime)

    try:
        query = (
            VlData.query.with_entities(
                *group_cols,
                *_suppression_entities(),
                TOTAL_ALL,
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                total=row.total, suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}
