from utilities.utils import (
    PROCESS_COMMON_PARAMS_VL,
    YEAR, MONTH, DATE_PART, TOTAL_ALL, TOTAL_NOT_NULL, TOTAL_NULL,
    SUPPRESSION, DATE_DIFF_AVG,
    and_, func, case,
)
from hiv.vl.models.vl import VlData


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


# ---------------------------------------------------------------------------
# 1. header_indicators_service
# ---------------------------------------------------------------------------
def header_indicators_service(req_args):
    """Single-row summary: registered, tested, suppressed, not_suppressed, rejected."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    base_filters = [VlData.RegisteredDateTime.between(dates[0], dates[1])]
    base_filters.extend(_build_facility_filters(facilities, facility_type))

    try:
        query = (
            VlData.query.with_entities(
                TOTAL_ALL,
                TOTAL_NOT_NULL(VlData.AnalysisDateTime).label("tested"),
                SUPPRESSION(VlData.ViralLoadResultCategory, "Suppressed").label("suppressed"),
                SUPPRESSION(VlData.ViralLoadResultCategory, "Not Suppressed").label("not_suppressed"),
                func.count(
                    case(
                        (
                            and_(
                                VlData.LIMSRejectionCode.is_not(None),
                                VlData.LIMSRejectionCode != "",
                            ),
                            1,
                        )
                    )
                ).label("rejected"),
            )
            .filter(and_(*base_filters))
        )
        row = query.one()
        return dict(
            registered=row.total,
            tested=row.tested,
            suppressed=row.suppressed,
            not_suppressed=row.not_suppressed,
            rejected=row.rejected,
            facilities=facilities,
            start_date=dates[0],
            end_date=dates[1],
        )
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 2. number_of_samples_service
# ---------------------------------------------------------------------------
def number_of_samples_service(req_args):
    """Monthly sample count grouped by year/month."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    filters = [VlData.RegisteredDateTime.between(dates[0], dates[1])]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.RegisteredDateTime)

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
            dict(
                    year=row.year, 
                    month=row[1], 
                    month_name=row[2], 
                    total=row.total,
                    start_date=dates[0],
                    end_date=dates[1],
                    facilities=facilities,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 3. viral_suppression_service
# ---------------------------------------------------------------------------
def viral_suppression_service(req_args):
    """Monthly suppression trend with suppressed/not_suppressed counts."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

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
            )
            .filter(and_(*filters))
            .group_by(*group_cols)
            .order_by(*order_cols)
        )
        data = query.all()
        return [
            dict(
                year=row.year, month=row[1], month_name=row[2],
                suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
                start_date=dates[0],
                end_date=dates[1],
                facilities=facilities,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 4. tat_service
# ---------------------------------------------------------------------------
def tat_service(req_args):
    """TAT summary with 4 segments grouped by year/month."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

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
# 5. suppression_by_province_service
# ---------------------------------------------------------------------------
def suppression_by_province_service(req_args):
    """Suppression counts grouped by RequestingProvinceName (provincial map)."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
    ]
    filters.extend(_build_facility_filters(facilities, facility_type))

    try:
        query = (
            VlData.query.with_entities(
                VlData.RequestingProvinceName.label("province"),
                *_suppression_entities(),
            )
            .filter(and_(*filters))
            .group_by(VlData.RequestingProvinceName)
            .order_by(VlData.RequestingProvinceName)
        )
        data = query.all()
        return [
            dict(
                province=row.province,
                suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
                start_date=dates[0],
                end_date=dates[1],
                facilities=facilities,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}


# ---------------------------------------------------------------------------
# 6. samples_history_service
# ---------------------------------------------------------------------------
def samples_history_service(req_args):
    """Historical sample counts grouped by year/month (broader date range)."""
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)
    
    filters = [VlData.RegisteredDateTime.between(dates[0], dates[1])]
    filters.extend(_build_facility_filters(facilities, facility_type))

    group_cols, order_cols = _year_month_group_order(VlData.RegisteredDateTime)

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
            dict(
                year=row.year, 
                month=row[1], 
                month_name=row[2], 
                total=row.total,
                start_date=dates[0],
                end_date=dates[1],
                facilities=facilities,
            )
            for row in data
        ]
    except Exception as e:
        return {"status": "error", "code": 500, "message": "An Error Occurred", "error": str(e)}
