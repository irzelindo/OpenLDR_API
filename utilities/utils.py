from sqlalchemy import and_, or_, func, case, literal, text
from datetime import datetime, timedelta

getdate = datetime.now()

today = getdate.strftime("%Y-%m-%d")

twelve_months_ago = (getdate - timedelta(days=366)).strftime("%Y-%m-%d")

YEAR = lambda date_and_time: func.year(date_and_time).label("year")

MONTH = lambda date_and_time: func.month(date_and_time).label("month")

DATE_PART = lambda date_name, date_and_time: func.datename(
    text(date_name), date_and_time
).label(f"{date_name}")

QUARTER = lambda date_and_time: func.quarter(date_and_time).label("quarter")

WEEK = lambda date_and_time: func.dayofweek(date_and_time).label("week")

DAY = lambda date_and_time: func.day(date_and_time).label("day")

TOTAL_ALL = func.count().label("total")

TOTAL_NOT_NULL = lambda field: func.count(
    case(
        (
            (
                or_(
                    field.isnot(None),
                    func.length(field) > 0,
                ),
                1,
            )
        ),
        else_=None,
    )
)

TOTAL_NULL = lambda field: func.count(
    case(
        (
            (
                or_(
                    field.is_(None),
                    func.length(field) == 0,
                ),
                1,
            )
        ),
        else_=None,
    )
)

TOTAL_IN = lambda field, values: func.count(
    case(
        (
            (
                field.in_(values),
                1,
            )
        ),
        else_=None,
    )
)

DATE_DIFF_AVG = lambda fields: func.avg(
    func.datediff(text("day"), fields[0], fields[1])
).label(f"date_diff_avg_{fields[0]}_to_{fields[1]}")


DATE_DIFF_MIN = lambda fields: func.min(
    func.datediff(text("day"), fields[0], fields[1])
).label(f"date_diff_min_{fields[0]}_to_{fields[1]}")


DATE_DIFF_MAX = lambda fields: func.max(
    func.datediff(text("day"), fields[0], fields[1])
).label(f"date_diff_max_{fields[0]}_to_{fields[1]}")


SUPPRESSION = lambda field, value: func.count(
    case((field == f"{value}", 1), else_=None)
)


GENDER_SUPPRESSION = lambda fields, values: func.count(
    case(((and_(fields[0] == values[0], fields[1] == values[1]), 1)), else_=None)
)


def GET_COLUMN_NAME(disaggregation, facility_type, TbMaster):
    if disaggregation is True:
        if facility_type == "province":
            return TbMaster.RequestingDistrictName
        elif facility_type == "district":
            return TbMaster.RequestingFacilityName
        elif facility_type == "health_facility":
            return TbMaster.RequestingFacilityName
        else:
            return TbMaster.RequestingProvinceName
    else:
        if facility_type == "province":
            return TbMaster.RequestingProvinceName
        elif facility_type == "district":
            return TbMaster.RequestingDistrictName
        elif facility_type == "health_facility":
            return TbMaster.RequestingFacilityName
        else:
            return TbMaster.RequestingProvinceName
