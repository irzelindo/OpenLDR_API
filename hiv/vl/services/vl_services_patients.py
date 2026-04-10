from math import ceil
from hiv.vl.models.vl import VlData
from utilities.utils import (
    PROCESS_COMMON_PARAMS_VL,
    get_patients,
    process_patients,
)
from auth.auth_service import get_user_by_id_service


def paginate_query(query, page, per_page):
    """
    Apply pagination to a SQLAlchemy query and return paginated results with metadata.

    Parameters
    ----------
    query : sqlalchemy.orm.query.Query
        The query to paginate.
    page : int
        The page number (1-indexed).
    per_page : int
        The number of records per page.

    Returns
    -------
    tuple
        (paginated_rows, total_count, total_pages)
    """
    query = query.order_by(VlData.RequestID)
    total_count = query.count()
    total_pages = ceil(total_count / per_page) if per_page > 0 else 0
    paginated_rows = query.offset((page - 1) * per_page).limit(per_page).all()
    return paginated_rows, total_count, total_pages


def _get_user_role(req_args):
    """Extract user_id from req_args and return (user_id, user_role)."""
    user_id = req_args.get("user_id")
    if user_id is not None:
        try:
            user = get_user_by_id_service(user_id)
            user_role = user.role if user else "Unknown"
        except Exception:
            user_role = "Unknown"
    else:
        user_role = "Unknown"
    return user_id, user_role


def _check_admin_access(user_id, user_role):
    """Return error dict if user is not Admin, else None."""
    if user_role != "Admin":
        return {
            "status": "error",
            "code": 403,
            "message": f"Forbidden - User with id {user_id} and role {user_role} is not authorized to access this resource.",
        }
    return None


# ---------------------------------------------------------------------------
# VL patient entity columns used across all patient queries
# ---------------------------------------------------------------------------
VL_PATIENT_ENTITIES = [
    VlData.RequestID,
    VlData.RequestingProvinceName,
    VlData.RequestingDistrictName,
    VlData.RequestingFacilityName,
    VlData.RequestingFacilityNationalCode,
    VlData.TestingProvinceName,
    VlData.TestingDistrictName,
    VlData.TestingFacilityName,
    VlData.FIRSTNAME,
    VlData.SURNAME,
    VlData.AgeInYears,
    VlData.HL7SexCode,
    VlData.TELHOME,
    VlData.ViralLoadResultCategory,
    VlData.HIVVL_ViralLoadResult,
    VlData.HIVVL_VRLogValue,
    VlData.ReasonForTest,
    VlData.Pregnant,
    VlData.BreastFeeding,
    VlData.ARTRegimen,
    VlData.LIMSRejectionCode,
    VlData.LIMSRejectionDesc,
    VlData.LIMSSpecimenSourceCode,
    VlData.LIMSSpecimenSourceDesc,
    VlData.SpecimenDatetime,
    VlData.RegisteredDateTime,
    VlData.AnalysisDateTime,
    VlData.AuthorisedDateTime,
    VlData.FinalViralLoadResult,
]


# ---------------------------------------------------------------------------
# 1. get_patients_by_name_service
# ---------------------------------------------------------------------------
def get_patients_by_name_service(req_args):
    """
    Get list of VL patients by first name or surname between two dates.
    """
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_admin_access(user_id, user_role)
    if access_error:
        return access_error

    first_name = req_args.get("first_name")
    surname = req_args.get("surname")

    if not first_name and not surname:
        return {
            "status": "error",
            "code": 400,
            "message": "At least one of 'first_name' or 'surname' must be provided.",
        }

    filters = [
        VlData.RegisteredDateTime.between(dates[0], dates[1]),
    ]

    if first_name:
        filters.append(VlData.FIRSTNAME.ilike(f"%{first_name}%"))

    if surname:
        filters.append(VlData.SURNAME.ilike(f"%{surname}%"))

    if health_facility:
        filters.append(VlData.RequestingFacilityName == health_facility)

    page = int(req_args.get("page") or 1)
    per_page = int(req_args.get("per_page") or 50)

    try:
        query = VlData.query.with_entities(*VL_PATIENT_ENTITIES).filter(*filters)

        data, total_count, total_pages = paginate_query(query, page, per_page)

        patients = process_patients(
            data, dates, facility_type, None, "vl", None, None
        )

        return {
            "status": "success",
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "data": patients,
        }

    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"An error occurred: {str(e)}",
        }


# ---------------------------------------------------------------------------
# 2. get_patients_by_facility_service
# ---------------------------------------------------------------------------
def get_patients_by_facility_service(req_args):
    """
    Get list of VL patients registered at a specific health facility between two dates.
    """
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_admin_access(user_id, user_role)
    if access_error:
        return access_error

    if not health_facility:
        return {
            "status": "error",
            "code": 400,
            "message": "The 'health_facility' parameter is required.",
        }

    page = int(req_args.get("page") or 1)
    per_page = int(req_args.get("per_page") or 50)

    try:
        query = get_patients(
            health_facility=health_facility,
            lab=None,
            dates=dates,
            model=VlData,
            indicator=VlData.RegisteredDateTime,
            gx_result_type=None,
            test_type="vl",
            month=None,
            year=None,
        )

        data, total_count, total_pages = paginate_query(query, page, per_page)

        patients = process_patients(
            data, dates, facility_type, None, "vl", None, None
        )

        return {
            "status": "success",
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "data": patients,
        }

    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"An error occurred: {str(e)}",
        }


# ---------------------------------------------------------------------------
# 3. get_patients_by_result_type_service
# ---------------------------------------------------------------------------
def get_patients_by_result_type_service(req_args):
    """
    Get list of VL patients by viral load result category (Suppressed / Not Suppressed) between two dates.
    """
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_admin_access(user_id, user_role)
    if access_error:
        return access_error

    result_type = req_args.get("result_type")

    if not result_type:
        return {
            "status": "error",
            "code": 400,
            "message": "The 'result_type' parameter is required. Valid values: suppressed, not_suppressed.",
        }

    result_type_mapping = {
        "suppressed": "Suppressed",
        "not_suppressed": "Not Suppressed",
    }

    # result_type can be a list (action="append") or a single string
    if isinstance(result_type, list):
        result_values = []
        for rt in result_type:
            rt_lower = rt.strip().lower()
            if rt_lower not in result_type_mapping:
                return {
                    "status": "error",
                    "code": 400,
                    "message": f"Invalid 'result_type' value: '{rt}'. Valid values: {', '.join(result_type_mapping.keys())}.",
                }
            result_values.append(result_type_mapping[rt_lower])
    else:
        rt_lower = result_type.strip().lower()
        if rt_lower not in result_type_mapping:
            return {
                "status": "error",
                "code": 400,
                "message": f"Invalid 'result_type'. Valid values: {', '.join(result_type_mapping.keys())}.",
            }
        result_values = [result_type_mapping[rt_lower]]

    filters = [
        VlData.AnalysisDateTime.between(dates[0], dates[1]),
        VlData.AnalysisDateTime.is_not(None),
        VlData.ViralLoadResultCategory.in_(result_values),
    ]

    if health_facility:
        filters.append(VlData.RequestingFacilityName == health_facility)

    page = int(req_args.get("page") or 1)
    per_page = int(req_args.get("per_page") or 50)

    try:
        query = VlData.query.with_entities(*VL_PATIENT_ENTITIES).filter(*filters)

        data, total_count, total_pages = paginate_query(query, page, per_page)

        patients = process_patients(
            data, dates, facility_type, None, "vl", None, None
        )

        return {
            "status": "success",
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "data": patients,
        }

    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"An error occurred: {str(e)}",
        }


# ---------------------------------------------------------------------------
# 4. get_patients_by_test_reason_service
# ---------------------------------------------------------------------------
def get_patients_by_test_reason_service(req_args):
    """
    Get list of VL patients by reason for test between two dates.
    """
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS_VL(req_args)

    user_id, user_role = _get_user_role(req_args)
    access_error = _check_admin_access(user_id, user_role)
    if access_error:
        return access_error

    test_reason = req_args.get("test_reason")

    if not test_reason:
        return {
            "status": "error",
            "code": 400,
            "message": "The 'test_reason' parameter is required.",
        }

    if test_reason == "Reason Not Specified":
        test_reason = [
            "Não preenchido",
            "No",
            "Reason Not Specified",
            "Yes",
            ""
        ]
    elif test_reason == "Routine":
        test_reason = ["Routine"]
    elif test_reason == "Repeat":
        test_reason = ["Repeat after breastfeeding", "Repeat"]
    elif test_reason == "Suspected treatment failure":
        test_reason = ["Suspected treatment failure"]

    filters = [
        VlData.RegisteredDateTime.between(dates[0], dates[1]),
        VlData.ReasonForTest.in_(test_reason),
    ]

    if health_facility:
        filters.append(VlData.RequestingFacilityName == health_facility)

    page = int(req_args.get("page") or 1)
    per_page = int(req_args.get("per_page") or 50)

    try:
        query = VlData.query.with_entities(*VL_PATIENT_ENTITIES).filter(*filters)

        data, total_count, total_pages = paginate_query(query, page, per_page)

        patients = process_patients(
            data, dates, facility_type, None, "vl", None, None
        )

        return {
            "status": "success",
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "data": patients,
        }

    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"An error occurred: {str(e)}",
        }
