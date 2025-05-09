from tb.gxpert.models.tb_gx_model import TBMaster
from utilities.utils import *
from sqlalchemy import and_, or_, func, case, literal, text, extract
from sqlalchemy.sql import select


def dashboard_header_component_summary_service(req_args):
    """
    Retrieve the number of tested samples by lab
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    try:
        query = TBMaster.query.with_entities(
            func.count(
                case((TBMaster.TypeOfResult == "Ultra 6 Cores", 1), else_=None)
            ).label("Registered_Samples_Ultra_6_Cores"),
            func.count(
                case((TBMaster.TypeOfResult == "XDR 10 Cores", 1), else_=None)
            ).label("Registered_Samples_XDR_10_Cores"),
            func.count(
                case((TBMaster.TypeOfResult == "Ultra 6 Cores", 1), else_=None)
            ).label("Analyzed_Samples_Ultra_6_Cores"),
            func.count(
                case((TBMaster.TypeOfResult == "XDR 10 Cores", 1), else_=None)
            ).label("Analyzed_Samples_XDR_10_Cores"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == "Ultra 6 Cores",
                            TBMaster.FinalResult.in_(
                                FINAL_RESULT_DETECTED_VALUES),
                        ),
                        1,
                    ),
                    else_=None,
                )
            ).label("Detected_Samples_Ultra_6_Cores"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == "XDR 10 Cores",
                            TBMaster.FinalResult.in_(
                                FINAL_RESULT_DETECTED_VALUES),
                        ),
                        1,
                    ),
                    else_=None,
                )
            ).label("Detected_Samples_XDR_10_Cores"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == "Ultra 6 Cores",
                            TBMaster.FinalResult.in_(
                                FINAL_RESULT_NOT_DETECTED_VALUES),
                        ),
                        1,
                    ),
                    else_=None,
                )
            ).label("Not_Detected_Samples_Ultra_6_Cores"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == "XDR 10 Cores",
                            TBMaster.FinalResult.in_(
                                FINAL_RESULT_NOT_DETECTED_VALUES),
                        ),
                        1,
                    ),
                    else_=None,
                )
            ).label("Not_Detected_Samples_XDR_10_Cores"),
            func.avg(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == "Ultra 6 Cores",
                            TBMaster.SpecimenDatetime.isnot(None),
                        ),
                        func.datediff(
                            text("day"),
                            TBMaster.SpecimenDatetime,
                            TBMaster.AuthorisedDateTime,
                        ),
                    ),
                    else_=None,
                )
            ).label("Avg_Response_Time_Days_Ultra_6_Cores_Collection_To_Validation"),
            func.avg(
                case(
                    (and_(
                        TBMaster.TypeOfResult == "XDR 10 Cores",
                        TBMaster.SpecimenDatetime.isnot(None),
                    ),
                        func.datediff(
                            text("day"),
                            TBMaster.SpecimenDatetime,
                            TBMaster.AuthorisedDateTime,
                    ),
                    ),
                    else_=None,
                )
            ).label("Avg_Response_Time_Days_XDR_10_Cores_Collection_To_Validation"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == "Ultra 6 Cores",
                            TBMaster.FinalResult.in_(
                                FINAL_RESULT_ERROR_DETECTED_VALUES
                            ),
                        ),
                        1,
                    ),
                    else_=None,
                )
            ).label("Errors_Ultra_6_Cores"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == "XDR 10 Cores",
                            TBMaster.FinalResult.in_(
                                FINAL_RESULT_ERROR_DETECTED_VALUES
                            ),
                        ),
                        1,
                    ),
                    else_=None,
                )
            ).label("Errors_XDR_10_Cores"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == "Ultra 6 Cores",
                            TBMaster.FinalResult.in_(
                                FINAL_RESULT_INVALID_VALUES),
                        ),
                        1,
                    ),
                    else_=None,
                )
            ).label("Invalid_Ultra_6_Cores"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == "XDR 10 Cores",
                            TBMaster.FinalResult.in_(
                                FINAL_RESULT_INVALID_VALUES),
                        ),
                        1,
                    ),
                    else_=None,
                )
            ).label("Invalid_XDR_10_Cores"),
        ).filter(
            TBMaster.RegisteredDateTime.between(dates[0], dates[1])
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Registered_Samples_Ultra_6_Cores": row.Registered_Samples_Ultra_6_Cores,
                "Registered_Samples_XDR_10_Cores": row.Registered_Samples_XDR_10_Cores,
                "Analyzed_Samples_Ultra_6_Cores": row.Analyzed_Samples_Ultra_6_Cores,
                "Analyzed_Samples_XDR_10_Cores": row.Analyzed_Samples_XDR_10_Cores,
                "Detected_Samples_Ultra_6_Cores": row.Detected_Samples_Ultra_6_Cores,
                "Detected_Samples_XDR_10_Cores": row.Detected_Samples_XDR_10_Cores,
                "Not_Detected_Samples_Ultra_6_Cores": row.Not_Detected_Samples_Ultra_6_Cores,
                "Not_Detected_Samples_XDR_10_Cores": row.Not_Detected_Samples_XDR_10_Cores,
                "AVG_TRL_Days_Ultra_6_Cores": row.Avg_Response_Time_Days_Ultra_6_Cores_Collection_To_Validation,
                "AVG_TRL_Days_XDR_10_Cores": row.Avg_Response_Time_Days_XDR_10_Cores_Collection_To_Validation,
                "Errors_Ultra_6_Cores": row.Errors_Ultra_6_Cores,
                "Errors_XDR_10_Cores": row.Errors_XDR_10_Cores,
                "Invalid_Ultra_6_Cores": row.Invalid_Ultra_6_Cores,
                "Invalid_XDR_10_Cores": row.Invalid_XDR_10_Cores,
                "Start_Date": dates[0],
                "End_Date": dates[1],
            }
            for row in data
        ]

        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def dashboard_summary_positivity_by_month_service(req_args):
    """
    Retrieve the number of tested samples by lab
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    if len(facilities) == 1 and facilities[0].strip() == "":
        facilities = []

    # print(facilities)

    simple_filter = [
        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.RegisteredDateTime.is_not(None),
    ]

    if lab.lower() != "all":
        simple_filter.append(LAB_TYPE(TBMaster, lab))

    if len(facilities) > 0:
        simple_filter.append(
            or_(
                TBMaster.TestingFacilityName.in_(facilities),
                TBMaster.TestingFacilityCode.in_(facilities),
            )
        )

    try:
        query = TBMaster.query.with_entities(
            MONTH(TBMaster.RegisteredDateTime).label("Month"),
            DATE_PART("month", TBMaster.RegisteredDateTime).label(
                "Month_Name"),
            func.count(TBMaster.RegisteredDateTime).label(
                "Registered_Samples"),
            func.count(TBMaster.AnalysisDateTime).label("Analysed_Samples"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(FINAL_RESULT_DETECTED_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Detected_Samples"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(
                            FINAL_RESULT_NOT_DETECTED_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Not_Detected_Samples"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(
                            FINAL_RESULT_ERROR_DETECTED_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Errors"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(FINAL_RESULT_INVALID_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Invalid_Samples")
        ).filter(
            *simple_filter
        ).group_by(
            MONTH(
                MONTH(TBMaster.RegisteredDateTime),
                DATE_PART("month", TBMaster.RegisteredDateTime)
            )
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Month": row.Month,
                "Month_Name": row.Month_Name,
                "Registered_Samples": row.Registered_Samples,
                "Analysed_Samples": row.Analysed_Samples,
                "Detected_Samples": row.Detected_Samples,
                "Not_Detected_Samples": row.Not_Detected_Samples,
                "Errors": row.Errors,
                "Invalid_Samples": row.Invalid_Samples,
                "Start_Date": dates[0],
                "End_Date": dates[1],
            }
            for row in data
        ]

        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }


def dashboard_summary_positivity_by_lab_service(req_args):
    """
    Retrieve the number of tested samples by lab
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    if len(facilities) == 1 and facilities[0].strip() == "":
        facilities = []

    # print(facilities)

    simple_filter = [
        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.RegisteredDateTime.is_not(None),
    ]

    if lab.lower() != "all":
        simple_filter.append(LAB_TYPE(TBMaster, lab))

    if len(facilities) > 0:
        simple_filter.append(
            or_(
                TBMaster.TestingFacilityName.in_(facilities),
                TBMaster.TestingFacilityCode.in_(facilities),
            )
        )

    try:
        query = TBMaster.query.with_entities(
            TBMaster.TestingFacilityCode.label("Lab_Code"),
            TBMaster.TestingFacilityName.label("Lab_Name"),
            func.count(TBMaster.RegisteredDateTime).label(
                "Registered_Samples"),
            func.count(TBMaster.AnalysisDateTime).label("Analysed_Samples"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(FINAL_RESULT_DETECTED_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Detected_Samples"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(
                            FINAL_RESULT_NOT_DETECTED_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Not_Detected_Samples"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(
                            FINAL_RESULT_ERROR_DETECTED_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Errors"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(FINAL_RESULT_INVALID_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Invalid_Samples")
        ).filter(*simple_filter).group_by(
            TBMaster.TestingFacilityCode,
            TBMaster.TestingFacilityName
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Lab_Code": row.Lab_Code,
                "Lab_Name": row.Lab_Name,
                "Registered_Samples": row.Registered_Samples,
                "Analysed_Samples": row.Analysed_Samples,
                "Detected_Samples": row.Detected_Samples,
                "Not_Detected_Samples": row.Not_Detected_Samples,
                "Errors": row.Errors,
                "Invalid_Samples": row.Invalid_Samples,
                "Start_Date": dates[0],
                "End_Date": dates[1],
            }
            for row in data
        ]

        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def dashboard_summary_positivity_by_lab_by_age_service(req_args):
    """
    Retrieve the number of tested samples by lab by age
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    simple_filter = [
        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.RegisteredDateTime.is_not(None),
    ]

    if lab.lower() != "all":
        simple_filter.append(LAB_TYPE(TBMaster, lab))

    try:
        query = TBMaster.query.with_entities(
            case(
                (
                    TBMaster.AgeInYears.between(0, 4),
                    "0-4"
                ),
                (
                    TBMaster.AgeInYears.between(5, 9),
                    "5-9"
                ),
                (
                    TBMaster.AgeInYears.between(10, 14),
                    "10-14"
                ),
                (
                    TBMaster.AgeInYears.between(15, 19),
                    "15-19"
                ),
                (
                    TBMaster.AgeInYears.between(20, 24),
                    "20-24"
                ),
                (
                    TBMaster.AgeInYears.between(25, 29),
                    "25-29"
                ),
                (
                    TBMaster.AgeInYears.between(30, 34),
                    "30-34"
                ),
                (
                    TBMaster.AgeInYears.between(35, 39),
                    "35-39"
                ),
                (
                    TBMaster.AgeInYears.between(40, 44),
                    "40-44"
                ),
                (
                    TBMaster.AgeInYears.between(45, 49),
                    "45-49"
                ),
                (
                    TBMaster.AgeInYears.between(50, 54),
                    "50-54"
                ),
                (
                    TBMaster.AgeInYears.between(55, 59),
                    "55-59"
                ),
                (
                    TBMaster.AgeInYears.between(60, 64),
                    "60-64"
                ),
                (
                    TBMaster.AgeInYears >= 65,
                    "65+"
                ),
                else_="Not Specified"
            ).label("Faixa_Etaria"),
            func.count(TBMaster.RegisteredDateTime).label(
                "Registered_Samples"),
            func.count(TBMaster.AnalysisDateTime).label("Analysed_Samples"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(FINAL_RESULT_DETECTED_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Detected_Samples"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(
                            FINAL_RESULT_NOT_DETECTED_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Not_Detected_Samples"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(
                            FINAL_RESULT_ERROR_DETECTED_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Errors"),
            func.count(
                case(
                    (
                        TBMaster.FinalResult.in_(FINAL_RESULT_INVALID_VALUES),
                        1,
                    ),
                    else_=None,
                )
            ).label("Invalid_Samples")
        ).filter(*simple_filter).group_by(TBMaster.Age)

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Faixa_Etaria": row.Faixa_Etaria,
                "Registered_Samples": row.Registered_Samples,
                "Analysed_Samples": row.Analysed_Samples,
                "Detected_Samples": row.Detected_Samples,
                "Not_Detected_Samples": row.Not_Detected_Samples,
                "Errors": row.Errors,
                "Invalid_Samples": row.Invalid_Samples,
                "Start_Date": dates[0],
                "End_Date": dates[1],
            }
            for row in data
        ]

        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response
