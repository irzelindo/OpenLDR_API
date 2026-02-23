from math import ceil
from tb.gxpert.models.tb_gx_model import TBMaster
from utilities.utils import *
from sqlalchemy import and_, or_, func, case, literal
from datetime import datetime
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
    # Order the query by RegisteredDateTime in descending order
    query = query.order_by(TBMaster.RequestID)
    total_count = query.count()
    total_pages = ceil(total_count / per_page) if per_page > 0 else 0
    paginated_rows = query.offset((page - 1) * per_page).limit(per_page).all()
    return paginated_rows, total_count, total_pages


def get_patients_by_name_service(req_args):
    """
    Get list of patients by first name or surname between two dates.
    """
    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    user_id = req_args.get("user_id")
    first_name = req_args.get("first_name")
    surname = req_args.get("surname")

    if user_id is not None:
        try:
            user = get_user_by_id_service(user_id)
        except Exception as e:
            return {
                "status": "error",
                "code": 500,
                "message": "An Error Occured",
                "error": str(e),
            }
        user_role = user.role if user else "Unknown"
    else:
        user_role = "Unknown"

    if user_role != "Admin":
        return {
            "status": "error",
            "code": 403,
            "message": f"Forbidden - User with id {user_id} and role {user_role} is not authorized to access this resource.",
        }

    if not first_name and not surname:
        return {
            "status": "error",
            "code": 400,
            "message": "At least one of 'first_name' or 'surname' must be provided.",
        }

    filters = [
        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
    ]

    if first_name:
        filters.append(TBMaster.FIRSTNAME.ilike(f"%{first_name}%"))

    if surname:
        filters.append(TBMaster.SURNAME.ilike(f"%{surname}%"))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    page = int(req_args.get("page") or 1)
    per_page = int(req_args.get("per_page") or 50)

    try:
        query = TBMaster.query.with_entities(
            TBMaster.RequestID,
            TBMaster.RequestingProvinceName,
            TBMaster.RequestingDistrictName,
            TBMaster.RequestingFacilityName,
            TBMaster.FacilityNationalCode,
            TBMaster.TestingProvinceName,
            TBMaster.TestingDistrictName,
            TBMaster.TestingFacilityName,
            TBMaster.FIRSTNAME,
            TBMaster.SURNAME,
            TBMaster.AgeInYears,
            TBMaster.HL7SexCode,
            TBMaster.TELHOME,
            TBMaster.FinalResult,
            TBMaster.MtbTrace,
            TBMaster.Rifampicin,
            TBMaster.Fluoroquinolona,
            TBMaster.Isoniazid,
            TBMaster.Kanamicin,
            TBMaster.Amikacina,
            TBMaster.Capreomicin,
            TBMaster.Ethionamida,
            TBMaster.RejectReason,
            TBMaster.RejectRemark,
            TBMaster.Remarks,
            TBMaster.SpecimenDatetime,
            TBMaster.RegisteredDateTime,
            TBMaster.AnalysisDateTime,
            TBMaster.AuthorisedDateTime,
            TBMaster.LIMSSpecimenSourceCode,
            TBMaster.LIMSSpecimenSourceDesc,
            TBMaster.LIMSAnalyzerCode,
            TBMaster.TypeOfResult,
        ).filter(*filters)

        data, total_count, total_pages = paginate_query(query, page, per_page)

        patients = process_patients(
            data, dates, facility_type, gx_result_type, "tb", None, None
        )

        response = {
            "status": "success",
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "data": patients,
        }

        return response

    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"An error occurred: {str(e)}",
        }


def get_patients_by_facility_service(req_args):
    """
    Get list of patients registered by facility between two dates.
    """
    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    user_id = req_args.get("user_id")

    if user_id is not None:
        try:
            user = get_user_by_id_service(user_id)
        except Exception as e:
            return {
                "status": "error",
                "code": 500,
                "message": "An Error Occured",
                "error": str(e),
            }
        user_role = user.role if user else "Unknown"
    else:
        user_role = "Unknown"

    if user_role != "Admin":
        return {
            "status": "error",
            "code": 403,
            "message": f"Forbidden - User with id {user_id} and role {user_role} is not authorized to access this resource.",
        }

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
            model=TBMaster,
            indicator=TBMaster.RegisteredDateTime,
            gx_result_type=gx_result_type,
            test_type="tb",
            month=None,
            year=None,
        )

        data, total_count, total_pages = paginate_query(query, page, per_page)

        patients = process_patients(
            data, dates, facility_type, gx_result_type, "tb", None, None
        )

        response = {
            "status": "success",
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "data": patients,
        }

        return response

    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"An error occurred: {str(e)}",
        }


def get_patients_by_sample_type_service(req_args):
    """
    Get list of patients by sample type (specimen source) between two dates.
    """
    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    user_id = req_args.get("user_id")
    sample_type = req_args.get("sample_type")

    if user_id is not None:
        try:
            user = get_user_by_id_service(user_id)
        except Exception as e:
            return {
                "status": "error",
                "code": 500,
                "message": "An Error Occured",
                "error": str(e),
            }
        user_role = user.role if user else "Unknown"
    else:
        user_role = "Unknown"

    if user_role != "Admin":
        return {
            "status": "error",
            "code": 403,
            "message": f"Forbidden - User with id {user_id} and role {user_role} is not authorized to access this resource.",
        }

    if not sample_type:
        return {
            "status": "error",
            "code": 400,
            "message": "The 'sample_type' parameter is required. Valid values: sputum, feces, urine, blood.",
        }

    sample_type_mapping = {
        "sputum": TB_SPUTUM_SPECIMEN_SOURCE_CODES,
        "feces": TB_FECES_SPECIMEN_SOURCE_CODES,
        "urine": TB_URINE_SPECIMEN_SOURCE_CODES,
        "blood": TB_BLOOD_SPECIMEN_SOURCE_CODES,
    }

    sample_type_lower = sample_type.lower()
    if sample_type_lower not in sample_type_mapping:
        return {
            "status": "error",
            "code": 400,
            "message": f"Invalid 'sample_type'. Valid values: {', '.join(sample_type_mapping.keys())}.",
        }

    specimen_codes = sample_type_mapping[sample_type_lower]

    filters = [
        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
        TBMaster.LIMSSpecimenSourceCode.in_(specimen_codes),
    ]

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if health_facility:
        filters.append(TBMaster.RequestingFacilityName == health_facility)

    page = int(req_args.get("page") or 1)
    per_page = int(req_args.get("per_page") or 50)

    try:
        query = TBMaster.query.with_entities(
            TBMaster.RequestID,
            TBMaster.RequestingProvinceName,
            TBMaster.RequestingDistrictName,
            TBMaster.RequestingFacilityName,
            TBMaster.FacilityNationalCode,
            TBMaster.TestingProvinceName,
            TBMaster.TestingDistrictName,
            TBMaster.TestingFacilityName,
            TBMaster.FIRSTNAME,
            TBMaster.SURNAME,
            TBMaster.AgeInYears,
            TBMaster.HL7SexCode,
            TBMaster.TELHOME,
            TBMaster.FinalResult,
            TBMaster.MtbTrace,
            TBMaster.Rifampicin,
            TBMaster.Fluoroquinolona,
            TBMaster.Isoniazid,
            TBMaster.Kanamicin,
            TBMaster.Amikacina,
            TBMaster.Capreomicin,
            TBMaster.Ethionamida,
            TBMaster.RejectReason,
            TBMaster.RejectRemark,
            TBMaster.Remarks,
            TBMaster.SpecimenDatetime,
            TBMaster.RegisteredDateTime,
            TBMaster.AnalysisDateTime,
            TBMaster.AuthorisedDateTime,
            TBMaster.LIMSSpecimenSourceCode,
            TBMaster.LIMSSpecimenSourceDesc,
            TBMaster.LIMSAnalyzerCode,
            TBMaster.TypeOfResult,
        ).filter(*filters)

        data, total_count, total_pages = paginate_query(query, page, per_page)

        patients = process_patients(
            data, dates, facility_type, gx_result_type, "tb", None, None
        )

        response = {
            "status": "success",
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "data": patients,
        }

        return response

    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"An error occurred: {str(e)}",
        }


def get_patients_by_result_type_service(req_args):
    """
    Get list of patients by result type (detected, not detected, indeterminate, etc.) between two dates.
    """
    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    user_id = req_args.get("user_id")
    result_type = req_args.get("result_type")

    if user_id is not None:
        try:
            user = get_user_by_id_service(user_id)
        except Exception as e:
            return {
                "status": "error",
                "code": 500,
                "message": "An Error Occured",
                "error": str(e),
            }
        user_role = user.role if user else "Unknown"
    else:
        user_role = "Unknown"

    if user_role != "Admin":
        return {
            "status": "error",
            "code": 403,
            "message": f"Forbidden - User with id {user_id} and role {user_role} is not authorized to access this resource.",
        }

    if not result_type:
        return {
            "status": "error",
            "code": 400,
            "message": "The 'result_type' parameter is required. Valid values: detected, not_detected, indeterminate, error, invalid.",
        }

    result_type_mapping = {
        "detected": FINAL_RESULT_DETECTED_VALUES,
        "not_detected": FINAL_RESULT_NOT_DETECTED_VALUES,
        "indeterminate": FINAL_RESULT_INDETERMINATE_VALUES,
        "error": FINAL_RESULT_ERROR_DETECTED_VALUES,
        "invalid": FINAL_RESULT_INVALID_VALUES,
    }

    result_type_lower = result_type.lower()
    if result_type_lower not in result_type_mapping:
        return {
            "status": "error",
            "code": 400,
            "message": f"Invalid 'result_type'. Valid values: {', '.join(result_type_mapping.keys())}.",
        }

    result_values = result_type_mapping[result_type_lower]

    filters = [
        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
        TBMaster.FinalResult.in_(result_values),
    ]

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if health_facility:
        filters.append(TBMaster.RequestingFacilityName == health_facility)

    page = int(req_args.get("page") or 1)
    per_page = int(req_args.get("per_page") or 50)

    try:
        query = TBMaster.query.with_entities(
            TBMaster.RequestID,
            TBMaster.RequestingProvinceName,
            TBMaster.RequestingDistrictName,
            TBMaster.RequestingFacilityName,
            TBMaster.FacilityNationalCode,
            TBMaster.TestingProvinceName,
            TBMaster.TestingDistrictName,
            TBMaster.TestingFacilityName,
            TBMaster.FIRSTNAME,
            TBMaster.SURNAME,
            TBMaster.AgeInYears,
            TBMaster.HL7SexCode,
            TBMaster.TELHOME,
            TBMaster.FinalResult,
            TBMaster.MtbTrace,
            TBMaster.Rifampicin,
            TBMaster.Fluoroquinolona,
            TBMaster.Isoniazid,
            TBMaster.Kanamicin,
            TBMaster.Amikacina,
            TBMaster.Capreomicin,
            TBMaster.Ethionamida,
            TBMaster.RejectReason,
            TBMaster.RejectRemark,
            TBMaster.Remarks,
            TBMaster.SpecimenDatetime,
            TBMaster.RegisteredDateTime,
            TBMaster.AnalysisDateTime,
            TBMaster.AuthorisedDateTime,
            TBMaster.LIMSSpecimenSourceCode,
            TBMaster.LIMSSpecimenSourceDesc,
            TBMaster.LIMSAnalyzerCode,
            TBMaster.TypeOfResult,
        ).filter(*filters)

        data, total_count, total_pages = paginate_query(query, page, per_page)

        patients = process_patients(
            data, dates, facility_type, gx_result_type, "tb", None, None
        )

        response = {
            "status": "success",
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "data": patients,
        }

        return response

    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"An error occurred: {str(e)}",
        }