from tb.gxpert.models.tb_gx_model import TBMaster
from utilities.utils import *
from sqlalchemy import and_, or_, func, case, literal
from sqlalchemy.sql import select


def registered_samples_by_lab_service(req_args):
    """
    Retrieve the number of registered samples by lab
    """
    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                None,  # No facility is required here
                health_facility,
                dates,
                TBMaster,
                TBMaster.RegisteredDateTime,
                gx_result_type,
                "tb",
            )

            data = query.all()

            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )

            return response

        # Get the data
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            ColumnNames.is_(None),
                            func.length(ColumnNames) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=ColumnNames,
                ).label("laboratory"),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(ColumnNames)
            .order_by(ColumnNames)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Testing_Facility": row.laboratory,
                "Resgistered_Samples": row.total,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type or "All",
                "Lab_Type": lab_type,
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def registered_samples_by_lab_service_month(req_args):
    """
    Retrieve the number of registered samples by month
    """

    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    # Retrieve the column names based on the disaggregation and facility type
    # This function should be defined in your utilities or models
    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    filters = [
        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
        TBMaster.RegisteredDateTime.is_not(None),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))
    # print(ColumnNames)

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                None,  # No facility is required here
                health_facility,
                dates,
                TBMaster,
                TBMaster.RegisteredDateTime,
                gx_result_type,
                "tb",
            )

            data = query.all()

            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )

            return response
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.RegisteredDateTime).label("Month"),
                DATE_PART("month", TBMaster.RegisteredDateTime).label("Month_Name"),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(
                # Use the same column as above
                MONTH(TBMaster.RegisteredDateTime),
                DATE_PART("month", TBMaster.RegisteredDateTime),
            )
            .order_by(
                # Keep consistency with grouping
                MONTH(TBMaster.RegisteredDateTime),
            )
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Month": row.Month,
                "Month_Name": row.Month_Name,
                "Resgistered_Samples": row.total,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type or "All",
                "Lab_Type": lab_type,
                "Facilities": facilities,
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def tested_samples_by_lab_service(req_args):
    """
    Retrieve the number of tested samples by lab
    """
    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.AnalysisDateTime.is_not(None),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                None,  # No facility is required here
                health_facility,
                dates,
                TBMaster,
                TBMaster.AnalysisDateTime,
                gx_result_type,
                "tb",
            )

            data = query.all()

            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )

            return response
        # Get the data
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            ColumnNames.is_(None),
                            func.length(ColumnNames) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=ColumnNames,
                ).label("laboratory"),
                func.count(
                    case(
                        (
                            TBMaster.FinalResult.in_(FINAL_RESULT_INVALID_VALUES),
                            1,
                        )
                    ),
                ).label("invalid_results"),
                func.count(
                    case(
                        (
                            TBMaster.FinalResult.in_(FINAL_RESULT_NOT_DETECTED_VALUES),
                            1,
                        )
                    ),
                ).label("tb_not_detected"),
                func.count(
                    case(
                        (
                            TBMaster.FinalResult.in_(FINAL_RESULT_DETECTED_VALUES),
                            1,
                        )
                    ),
                ).label("tb_detected"),
                func.count(
                    case(
                        (
                            TBMaster.FinalResult.in_(
                                FINAL_RESULT_ERROR_DETECTED_VALUES
                            ),
                            1,
                        )
                    )
                ).label("errors"),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(ColumnNames)
            .order_by(ColumnNames)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Testing_Facility": row.laboratory,
                "Tested_Samples": row.total,
                "Invalid_Results": row.invalid_results,
                "TB_Not_Detected": row.tb_not_detected,
                "TB_Detected": row.tb_detected,
                "Errors": row.errors,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type or "All",
                "Lab_Type": lab_type,
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def tested_samples_by_lab_service_month(req_args):
    """
    Retrieve the number of tested samples by month
    """

    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.AnalysisDateTime.is_not(None),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                None,  # No facility is required here
                health_facility,
                dates,
                TBMaster,
                TBMaster.AnalysisDateTime,
                gx_result_type,
                "tb",
            )

            data = query.all()

            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )

            return response
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.AnalysisDateTime).label("Month"),
                DATE_PART("month", TBMaster.AnalysisDateTime).label("Month_Name"),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(
                # Use the same column as above
                MONTH(TBMaster.AnalysisDateTime),
                DATE_PART("month", TBMaster.AnalysisDateTime),
            )
            .order_by(
                # Keep consistency with grouping
                MONTH(TBMaster.AnalysisDateTime)
            )
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Month": row.Month,
                "Month_Name": row.Month_Name,
                "Tested_Samples": row.total,
                "Start_date": dates[0],
                "End_date": dates[1],
                "Type_of_result": gx_result_type or "All",
                "Lab_Type": lab_type,
                "Facilities": facilities,
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def rejected_samples_by_lab_service(req_args):
    """
    Retrieve the number of rejected samples by lab
    """

    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    # Retrieve the column names based on the disaggregation and facility type
    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.AnalysisDateTime.is_not(None),
        or_(
            func.length(TBMaster.LIMSRejectionCode) > 0,
            func.length(TBMaster.LIMSRejectionDesc) > 0,
        ),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                None,  # No facility is required here
                health_facility,
                dates,
                TBMaster,
                TBMaster.AnalysisDateTime,
                gx_result_type,
                "tb",
            )

            data = query.all()

            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )

            return response
        # Get the data
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            ColumnNames.is_(None),
                            func.length(ColumnNames) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=ColumnNames,
                ).label("laboratory"),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(ColumnNames)
            .order_by(ColumnNames)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Testing_Facility": row.laboratory,
                "Rejected_Samples": row.total,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type or "All",
                "Lab_Type": lab_type,
                "Facilities": facilities,
            }
            for row in data
        ]
        # Return the response
        return response
    except Exception as e:
        # Prepare the error response
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def rejected_samples_by_lab_service_month(req_args):
    """
    Retrieve the number of rejected samples by month
    """

    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.AnalysisDateTime.is_not(None),
        or_(
            func.length(TBMaster.LIMSRejectionCode) > 0,
            func.length(TBMaster.LIMSRejectionDesc) > 0,
        ),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                None,  # No facility is required here
                health_facility,
                dates,
                TBMaster,
                TBMaster.AnalysisDateTime,
                gx_result_type,
                "tb",
            )

            data = query.all()

            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )

            return response
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.AnalysisDateTime).label("Month"),
                DATE_PART("month", TBMaster.AnalysisDateTime).label("Month_Name"),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(
                # Use the same column as above
                MONTH(TBMaster.AnalysisDateTime),
                DATE_PART("month", TBMaster.AnalysisDateTime),
            )
            .order_by(
                # Keep consistency with grouping
                MONTH(TBMaster.AnalysisDateTime)
            )
        )

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Month": row.Month,
                "Month_Name": row.Month_Name,
                "Rejected_Samples": row.total,
                "Start_date": dates[0],
                "End_date": dates[1],
                "Type_of_result": gx_result_type or "All",
                "Lab_Type": lab_type,
                "Facilities": facilities,
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def rejected_samples_by_lab_by_reason_service(req_args):
    """
    Retrieve the number of rejected samples by lab
    """

    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    # Retrieve the column names based on the disaggregation and facility type
    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.AnalysisDateTime.is_not(None),
        or_(
            func.length(TBMaster.LIMSRejectionCode) > 0,
            func.length(TBMaster.LIMSRejectionDesc) > 0,
        ),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    rejection_labels = {
        "Isuficient_Specimen": "INSUFICIENT_SPECIMEN",
        "Specimen_Not_Received": "SPECIMEN_NOT_RECEIVED",
        "Specimen_Unsuitable_For_Testing": "SPECIMEN_UNSUITABLE_FOR_TESTING",
        "Equipment_Failure": "EQUIPMENT_FAILURE",
        "Repeat_Specimen_Collection": "REPEAT_SPECIMEN_COLLECTION",
        "Specimen_Not_Labeled": "SPECIMEN_NOT_LABELED",
        "Laboratory_Acident": "LABORATORY_ACIDENT",
        "Missing_Reagent": "MISSING_REAGENT",
        "Double_Registration": "DOUBLE_REGISTRATION",
        "Technical_Error": "TECHNICAL_ERROR",
    }

    try:

        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                None,  # No facility is required here
                health_facility,
                dates,
                TBMaster,
                TBMaster.AnalysisDateTime,
                gx_result_type,
                "tb",
            )

            data = query.all()

            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )

            return response

        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            ColumnNames.is_(None),
                            func.length(ColumnNames) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=ColumnNames,
                ).label("laboratory"),
                *[
                    func.count(
                        case(
                            (
                                TBMaster.LIMSRejectionCode.in_(
                                    SPECIMEN_REJECTION_CODES[value]
                                ),
                                1,
                            )
                        )
                    ).label(key)
                    for key, value in rejection_labels.items()
                ],
                func.count(
                    case(
                        (
                            TBMaster.LIMSRejectionCode.notin_(
                                sum(
                                    (
                                        SPECIMEN_REJECTION_CODES[v]
                                        for v in rejection_labels.values()
                                    ),
                                    [],
                                )
                            ),
                            1,
                        )
                    )
                ).label("Other"),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(ColumnNames)
            .order_by(ColumnNames)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Testing_Facility": row.laboratory,
                "Rejected_Samples": row.total,
                **{key: getattr(row, key) for key in rejection_labels},
                "Other": row.Other,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type or "All",
                "Lab_Type": lab_type,
                "Facilities": facilities,
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


def rejected_samples_by_lab_by_reason_service_month(req_args):
    """
    Retrieve the number of rejected samples by lab
    """
    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    # Retrieve the column names based on the disaggregation and facility type
    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.AnalysisDateTime.is_not(None),
        or_(
            func.length(TBMaster.LIMSRejectionCode) > 0,
            func.length(TBMaster.LIMSRejectionDesc) > 0,
        ),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    rejection_labels = {
        "Isuficient_Specimen": "INSUFICIENT_SPECIMEN",
        "Specimen_Not_Received": "SPECIMEN_NOT_RECEIVED",
        "Specimen_Unsuitable_For_Testing": "SPECIMEN_UNSUITABLE_FOR_TESTING",
        "Equipment_Failure": "EQUIPMENT_FAILURE",
        "Repeat_Specimen_Collection": "REPEAT_SPECIMEN_COLLECTION",
        "Specimen_Not_Labeled": "SPECIMEN_NOT_LABELED",
        "Laboratory_Acident": "LABORATORY_ACIDENT",
        "Missing_Reagent": "MISSING_REAGENT",
        "Double_Registration": "DOUBLE_REGISTRATION",
        "Technical_Error": "TECHNICAL_ERROR",
    }

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.AnalysisDateTime).label("Month"),
                DATE_PART("month", TBMaster.AnalysisDateTime).label("Month_Name"),
                *[
                    func.count(
                        case(
                            (
                                TBMaster.LIMSRejectionCode.in_(
                                    SPECIMEN_REJECTION_CODES[value]
                                ),
                                1,
                            )
                        )
                    ).label(key)
                    for key, value in rejection_labels.items()
                ],
                func.count(
                    case(
                        (
                            TBMaster.LIMSRejectionCode.notin_(
                                sum(
                                    (
                                        SPECIMEN_REJECTION_CODES[v]
                                        for v in rejection_labels.values()
                                    ),
                                    [],
                                )
                            ),
                            1,
                        )
                    )
                ).label("Other"),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(
                # Use the same column as above
                MONTH(TBMaster.AnalysisDateTime),
                DATE_PART("month", TBMaster.AnalysisDateTime),
            )
            .order_by(
                # Keep consistency with grouping
                MONTH(TBMaster.AnalysisDateTime)
            )
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Month": row.Month,
                "Month_Name": row.Month_Name,
                "Rejected_Samples": row.total,
                **{key: getattr(row, key) for key in rejection_labels},
                "Other": row.Other,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type or "All",
                "Lab_Type": lab_type,
                "Facilities": facilities,
            }
            for row in data
        ]
        # Return the response
        return response
    except Exception as e:
        # Prepare the error response
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def tested_samples_by_lab_by_drug_type_service(req_args):
    """
    Retrieve the number of tested samples by lab
    """

    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.AnalysisDateTime.is_not(None),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    # Define the drugs and their cases
    drugs = [
        "Rifampicin",
        "Isoniazid",
        "Fluoroquinolona",
        "Kanamicin",
        "Amikacina",
        "Capreomicin",
        "Ethionamida",
    ]

    cases = [
        func.count(
            case(
                (
                    and_(
                        TBMaster.Rifampicin.is_(None),
                        TBMaster.Isoniazid.isnot(None),
                        TBMaster.Fluoroquinolona.isnot(None),
                        TBMaster.Kanamicin.isnot(None),
                        TBMaster.Amikacina.isnot(None),
                        TBMaster.Capreomicin.isnot(None),
                        TBMaster.Ethionamida.isnot(None),
                    ),
                    1,
                )
            )
        ).label("Rifampicin_Null")
    ]

    for drug in drugs:
        cases.extend(generate_drug_cases(TBMaster, drug, gx_result_type))

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                None,  # No facility is required here
                health_facility,
                dates,
                TBMaster,
                TBMaster.AnalysisDateTime,
                gx_result_type,
                "tb",
            )

            data = query.all()

            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )

            return response
        # Get the data
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            ColumnNames.is_(None),
                            func.length(ColumnNames) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=ColumnNames,
                ).label("laboratory"),
                *cases,
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(ColumnNames)
            .order_by(ColumnNames)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Testing_Facility": row.laboratory,
                "Tested_Samples": row.total,
                "Rifampicin_Null": row.Rifampicin_Null,
                **{
                    drug: {
                        "Resistance_Detected": getattr(
                            row, f"{drug}_Resistance_Detected"
                        ),
                        "Resistance_Not_Detected": getattr(
                            row, f"{drug}_Resistance_Not_Detected"
                        ),
                        "Resistance_Indeterminate": getattr(
                            row, f"{drug}_Resistance_Indeterminate"
                        ),
                    }
                    for drug in drugs
                },
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type or "All",
                "Lab_Type": lab_type,
                "Facilities": facilities,
            }
            for row in data
        ]
        # Return the response
        return response
    except Exception as e:
        # Prepare the error response
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def tested_samples_by_lab_by_drug_type_service_month(req_args):
    """
    Retrieve the number of tested samples by lab
    """

    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.AnalysisDateTime.is_not(None),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    drugs = [
        "Rifampicin",
        "Isoniazid",
        "Fluoroquinolona",
        "Kanamicin",
        "Amikacina",
        "Capreomicin",
        "Ethionamida",
    ]

    cases = [
        func.count(
            case(
                (
                    and_(
                        TBMaster.Rifampicin.is_(None),
                        TBMaster.Isoniazid.isnot(None),
                        TBMaster.Fluoroquinolona.isnot(None),
                        TBMaster.Kanamicin.isnot(None),
                        TBMaster.Amikacina.isnot(None),
                        TBMaster.Capreomicin.isnot(None),
                        TBMaster.Ethionamida.isnot(None),
                    ),
                    1,
                )
            )
        ).label("Rifampicin_Null")
    ]

    for drug in drugs:
        cases.extend(generate_drug_cases(TBMaster, drug, gx_result_type))

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.AnalysisDateTime).label("Month"),
                DATE_PART("month", TBMaster.AnalysisDateTime).label("Month_Name"),
                *cases,
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(
                # Use the same column as above
                MONTH(TBMaster.AnalysisDateTime),
                DATE_PART("month", TBMaster.AnalysisDateTime),
            )
            .order_by(
                # Keep consistency with grouping
                MONTH(TBMaster.AnalysisDateTime)
            )
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Month": row.Month,
                "Month_Name": row.Month_Name,
                "Tested_Samples": row.total,
                "Rifampicin_Null": row.Rifampicin_Null,
                **{
                    drug: {
                        "Resistance_Detected": getattr(
                            row, f"{drug}_Resistance_Detected"
                        ),
                        "Resistance_Not_Detected": getattr(
                            row, f"{drug}_Resistance_Not_Detected"
                        ),
                        "Resistance_Indeterminate": getattr(
                            row, f"{drug}_Resistance_Indeterminate"
                        ),
                    }
                    for drug in drugs
                },
                "Start_date": dates[0],
                "End_date": dates[1],
                "Type_of_result": gx_result_type or "All",
                "Lab_Type": lab_type,
                "Facilities": facilities,
            }
            for row in data
        ]
        # Return the response
        return response
    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def trl_samples_by_lab_by_days_service(req_args):
    """
    Retrieve the turnaround time samples tested in days
    """

    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AuthorisedDateTime.between(dates[0], dates[1]),
        TBMaster.AuthorisedDateTime.is_not(None),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    trl_functions = trl_by_lab_by_days(TBMaster)

    days_groups = [
        (
            func.count(case(((value.between(min_age, max_age), 1)))).label(
                f"{key}_between_{min_age}_{max_age}"
            )
            if min_age is not None and max_age is not None
            else (
                func.count(case(((value < max_age), 1))).label(
                    f"{key}_less_than_{max_age}"
                )
                if min_age is None
                else (
                    func.count(case(((value > min_age), 1))).label(
                        f"{key}_greater_than_{min_age}"
                    )
                )
            )
        )
        for key, value in trl_functions.items()
        for min_age, max_age in TRL_DAYS
    ]

    # print(select(*age_groups))

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                None,  # No facility is required here
                health_facility,
                dates,
                TBMaster,
                TBMaster.AuthorisedDateTime,
                gx_result_type,
                "tb",
            )

            data = query.all()

            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )

            return response
        # Get the data
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            ColumnNames.is_(None),
                            func.length(ColumnNames) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=ColumnNames,
                ).label("laboratory"),
                *days_groups,
                func.count(case(((TBMaster.SpecimenDatetime.is_(None), 1)))).label(
                    "specimen_datetime_null"
                ),
                func.count(case(((TBMaster.ReceivedDateTime.is_(None), 1)))).label(
                    "received_datetime_null"
                ),
                func.count(case(((TBMaster.RegisteredDateTime.is_(None), 1)))).label(
                    "registered_datetime_null"
                ),
                func.count(case(((TBMaster.AnalysisDateTime.is_(None), 1)))).label(
                    "analysis_datetime_null"
                ),
                func.count(case(((TBMaster.AuthorisedDateTime.is_(None), 1)))).label(
                    "authorised_datetime_null"
                ),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(ColumnNames)
            .order_by(ColumnNames)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Laboratory": row.laboratory,
                "Total": row.total,
                "Specimen_Datetime_Null": row.specimen_datetime_null,
                "Received_Datetime_Null": row.received_datetime_null,
                "Registered_Datetime_Null": row.registered_datetime_null,
                "Analysis_Datetime_Null": row.analysis_datetime_null,
                "Authorised_Datetime_Null": row.authorised_datetime_null,
                **{
                    key: {
                        # Replaces the key name from the key and maintains the ages structure
                        # in the subdictionary
                        age_group.name.replace(f"{key}_", ""): getattr(
                            row, age_group.name
                        )
                        for age_group in days_groups
                        if age_group.name.startswith(f"{key}_")
                    }
                    for key, value in trl_functions.items()
                },
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type or "All",
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response


def trl_samples_by_lab_by_days_by_service_month(req_args):
    """
    Retrieve the turnaround time tested samples in days by month
    """

    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab_type,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(req_args)

    ColumnNames = GET_COLUMN_NAME(
        disaggregation, facility_type, TBMaster, "laboratories"
    )

    # Remove any empty or whitespace-only entries from facilities
    facilities = [f.strip() for f in facilities if f.strip()]

    filters = [
        TBMaster.AuthorisedDateTime.between(dates[0], dates[1]),
        TBMaster.AuthorisedDateTime.is_not(None),
    ]

    # If after cleaning it's empty, reset it to an empty list
    if not facilities:
        facilities = []

    if facilities:
        if facility_type == "province":
            filters.append(TBMaster.TestingProvinceName.in_(facilities))
        elif facility_type == "district":
            filters.append(TBMaster.TestingDistrictName.in_(facilities))
        elif facility_type == "health_facility":
            filters.append(TBMaster.TestingFacilityName.in_(facilities))

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    if lab_type.lower() != "all":
        filters.append(LAB_TYPE(TBMaster, lab_type))

    trl_functions = trl_by_lab_by_days(TBMaster)

    days_groups = [
        (
            func.count(case(((value.between(min_age, max_age), 1)))).label(
                f"{key}_between_{min_age}_{max_age}"
            )
            if min_age is not None and max_age is not None
            else (
                func.count(case(((value < max_age), 1))).label(
                    f"{key}_less_than_{max_age}"
                )
                if min_age is None
                else (
                    func.count(case(((value > min_age), 1))).label(
                        f"{key}_greater_than_{min_age}"
                    )
                )
            )
        )
        for key, value in trl_functions.items()
        for min_age, max_age in TRL_DAYS
    ]

    # print(select(*age_groups))

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.AuthorisedDateTime).label("Month"),
                DATE_PART("month", TBMaster.AuthorisedDateTime).label("Month_Name"),
                *days_groups,
                func.count(case(((TBMaster.SpecimenDatetime.is_(None), 1)))).label(
                    "specimen_datetime_null"
                ),
                func.count(case(((TBMaster.ReceivedDateTime.is_(None), 1)))).label(
                    "received_datetime_null"
                ),
                func.count(case(((TBMaster.RegisteredDateTime.is_(None), 1)))).label(
                    "registered_datetime_null"
                ),
                func.count(case(((TBMaster.AnalysisDateTime.is_(None), 1)))).label(
                    "analysis_datetime_null"
                ),
                func.count(case(((TBMaster.AuthorisedDateTime.is_(None), 1)))).label(
                    "authorised_datetime_null"
                ),
                TOTAL_ALL.label("total"),
            )
            .filter(*filters)
            .group_by(
                MONTH(TBMaster.AuthorisedDateTime),
                DATE_PART("month", TBMaster.AuthorisedDateTime),
            )
            .order_by(MONTH(TBMaster.AuthorisedDateTime))
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Month": row.Month,
                "Month_Name": row.Month_Name,
                "Total": row.total,
                "Specimen_Datetime_Null": row.specimen_datetime_null,
                "Received_Datetime_Null": row.received_datetime_null,
                "Registered_Datetime_Null": row.registered_datetime_null,
                "Analysis_Datetime_Null": row.analysis_datetime_null,
                "Authorised_Datetime_Null": row.authorised_datetime_null,
                **{
                    key: {
                        # Replaces the key name from the key and maintains the ages structure
                        # in the subdictionary
                        age_group.name.replace(f"{key}_", ""): getattr(
                            row, age_group.name
                        )
                        for age_group in days_groups
                        if age_group.name.startswith(f"{key}_")
                    }
                    for key, value in trl_functions.items()
                },
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type or "All",
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }

        return response
