from tb.gxpert.models.tb_gx_model import TBMaster
from utilities.utils import *
from sqlalchemy import and_, or_, func, case, literal, text
from sqlalchemy.sql import select


def registered_samples_by_lab_service(req_args):
    """
    Retrieve the number of registered samples by lab
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
        # Get the data
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityName.is_(None),
                            func.length(TBMaster.TestingFacilityName) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityName,
                ).label("laboratory"),
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityCode.is_(None),
                            func.length(TBMaster.TestingFacilityCode) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityCode,
                ).label("laboratory_code"),
                TOTAL_ALL.label("total"),
            )
            .filter(and_(*simple_filter))
            .group_by(TBMaster.TestingFacilityName, TBMaster.TestingFacilityCode)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Testing_Facility": row.laboratory,
                "Testing_Facility_code": row.laboratory_code,
                "Resgistered_Samples": row.total,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Lab_Type": lab,
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

    # print(ColumnNames)

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.RegisteredDateTime).label("Month"),
                DATE_PART("month", TBMaster.RegisteredDateTime).label("Month_Name"),
                TOTAL_ALL.label("total"),
            )
            .filter(and_(*simple_filter))
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

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

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
                "Type_Of_Result": gx_result_type,
                "Lab_Type": lab,
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
    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    if len(facilities) == 1 and facilities[0].strip() == "":
        facilities = []

    # print(facilities)

    simple_filter = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
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
        # Get the data
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityName.is_(None),
                            func.length(TBMaster.TestingFacilityName) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityName,
                ).label("laboratory"),
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityCode.is_(None),
                            func.length(TBMaster.TestingFacilityCode) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityCode,
                ).label("laboratory_code"),
                func.count(
                    case(
                        (
                            TBMaster.FinalResult.in_(
                                [
                                    "INVALIDO",
                                    "Invalid",
                                    "Not viscous/Watery",
                                    "Very Viscous",
                                ]
                            ),
                            1,
                        )
                    ),
                ).label("invalid_results"),
                func.count(
                    case(
                        (
                            TBMaster.FinalResult.in_(
                                [
                                    "Micobacterias Não TB",
                                    "MTB not detected",
                                    "Not Detected",
                                    "NDET",
                                    "MICNO",
                                    "AMK Resistance NOT DETECTED",
                                    "CAP Resistance NOT DETECTED",
                                ]
                            ),
                            1,
                        )
                    ),
                ).label("tb_not_detected"),
                func.count(
                    case(
                        (
                            TBMaster.FinalResult.in_(
                                [
                                    "MTB complex confirmed",
                                    "MTB DETECTADO ALTO",
                                    "MTB DETECTADO BAIXISSIMO",
                                    "MTB DETECTADO BAIXO",
                                    "MTB DETECTADO MEDIO",
                                    "MTB DETECTADO MUITO BAIXO",
                                    "MTB DETECTED",
                                    "MTB Detected HI",
                                    "MTB Detected Low",
                                    "MTB Detected Medium",
                                    "MTB Detected Muito Baixo",
                                    "MTB Detected Very Low",
                                    "TRAÇOS DE MTB DETECTADOS",
                                ]
                            ),
                            1,
                        )
                    ),
                ).label("tb_detected"),
                func.count(
                    case(
                        (
                            or_(
                                TBMaster.FinalResult.in_(
                                    [
                                        "No Result",
                                        "Not Applicable",
                                        "Error",
                                        "Insufficient sample",
                                        "Instrument out of order",
                                        "INS",
                                    ]
                                ),
                                func.length(TBMaster.LIMSRejectionCode) > 0,
                                TBMaster.FinalResult.is_(None),
                            ),
                            1,
                        )
                    )
                ).label("errors"),
                TOTAL_ALL.label("total"),
            )
            .filter(and_(*simple_filter))
            .group_by(TBMaster.TestingFacilityName, TBMaster.TestingFacilityCode)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Testing_Facility": row.laboratory,
                "Testing_Facility_code": row.laboratory_code,
                "Tested_Samples": row.total,
                "Invalid_Results": row.invalid_results,
                "TB_Not_Detected": row.tb_not_detected,
                "TB_Detected": row.tb_detected,
                "Errors": row.errors,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Lab_Type": lab,
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

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    if len(facilities) == 1 and facilities[0].strip() == "":
        facilities = []

    # print(facilities)

    simple_filter = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.AnalysisDateTime.is_not(None),
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
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.AnalysisDateTime).label("Month"),
                DATE_PART("month", TBMaster.AnalysisDateTime).label("Month_Name"),
                TOTAL_ALL.label("total"),
            )
            .filter(and_(*simple_filter))
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
                "Tested_Samples": row.total,
                "Start_date": dates[0],
                "End_date": dates[1],
                "Type_of_result": gx_result_type,
                "Lab_Type": lab,
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

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    if len(facilities) == 1 and facilities[0].strip() == "":
        facilities = []

    # print(facilities)

    simple_filter = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.AnalysisDateTime.is_not(None),
        or_(
            func.length(TBMaster.LIMSRejectionCode) > 0,
            func.length(TBMaster.LIMSRejectionDesc) > 0,
        ),
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
        # Get the data
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityName.is_(None),
                            func.length(TBMaster.TestingFacilityName) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityName,
                ).label("laboratory"),
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityCode.is_(None),
                            func.length(TBMaster.TestingFacilityCode) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityCode,
                ).label("laboratory_code"),
                TOTAL_ALL.label("total"),
            )
            .filter(and_(*simple_filter))
            .group_by(TBMaster.TestingFacilityName, TBMaster.TestingFacilityCode)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Testing_Facility": row.laboratory,
                "Testing_Facility_code": row.laboratory_code,
                "Rejected_Samples": row.total,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Lab_Type": lab,
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


def rejected_samples_by_lab_service_month(req_args):
    """
    Retrieve the number of rejected samples by month
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    if len(facilities) == 1 and facilities[0].strip() == "":
        facilities = []

    # print(facilities)

    simple_filter = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.AnalysisDateTime.is_not(None),
        or_(
            func.length(TBMaster.LIMSRejectionCode) > 0,
            func.length(TBMaster.LIMSRejectionDesc) > 0,
        ),
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
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.AnalysisDateTime).label("Month"),
                DATE_PART("month", TBMaster.AnalysisDateTime).label("Month_Name"),
                TOTAL_ALL.label("total"),
            )
            .filter(and_(*simple_filter))
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
                "Type_of_result": gx_result_type,
                "Lab_Type": lab,
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

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    facilities = (
        [] if len(facilities) == 1 and facilities[0].strip() == "" else facilities
    )

    simple_filter = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.AnalysisDateTime.is_not(None),
        or_(
            func.length(TBMaster.LIMSRejectionCode) > 0,
            func.length(TBMaster.LIMSRejectionDesc) > 0,
        ),
    ]

    if lab.lower() != "all":
        simple_filter.append(LAB_TYPE(TBMaster, lab))

    if facilities:
        simple_filter.append(
            or_(
                TBMaster.TestingFacilityName.in_(facilities),
                TBMaster.TestingFacilityCode.in_(facilities),
            )
        )

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
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityName.is_(None),
                            func.length(TBMaster.TestingFacilityName) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityName,
                ).label("laboratory"),
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityCode.is_(None),
                            func.length(TBMaster.TestingFacilityCode) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityCode,
                ).label("laboratory_code"),
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
            .filter(and_(*simple_filter))
            .group_by(TBMaster.TestingFacilityName, TBMaster.TestingFacilityCode)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Testing_Facility": row.laboratory,
                "Testing_Facility_code": row.laboratory_code,
                "Rejected_Samples": row.total,
                **{key: getattr(row, key) for key in rejection_labels},
                "Other": row.Other,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Lab_Type": lab,
                "Facilities": facilities,
            }
            for row in data
        ]
        return response
    except Exception as e:
        return {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }


def rejected_samples_by_lab_by_reason_service_month(req_args):
    """
    Retrieve the number of rejected samples by lab
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    facilities = (
        [] if len(facilities) == 1 and facilities[0].strip() == "" else facilities
    )

    simple_filter = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.AnalysisDateTime.is_not(None),
        or_(
            func.length(TBMaster.LIMSRejectionCode) > 0,
            func.length(TBMaster.LIMSRejectionDesc) > 0,
        ),
    ]

    if lab.lower() != "all":
        simple_filter.append(LAB_TYPE(TBMaster, lab))

    if facilities:
        simple_filter.append(
            or_(
                TBMaster.TestingFacilityName.in_(facilities),
                TBMaster.TestingFacilityCode.in_(facilities),
            )
        )

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
            .filter(and_(*simple_filter))
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
                "Type_Of_Result": gx_result_type,
                "Lab_Type": lab,
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


def tested_samples_by_lab_by_drug_type_service(req_args):
    """
    Retrieve the number of tested samples by lab
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    facilities = (
        [] if len(facilities) == 1 and facilities[0].strip() == "" else facilities
    )

    simple_filter = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.AnalysisDateTime.is_not(None),
    ]

    if lab.lower() != "all":
        simple_filter.append(LAB_TYPE(TBMaster, lab))

    if facilities:
        simple_filter.append(
            or_(
                TBMaster.TestingFacilityName.in_(facilities),
                TBMaster.TestingFacilityCode.in_(facilities),
            )
        )
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
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityName.is_(None),
                            func.length(TBMaster.TestingFacilityName) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityName,
                ).label("laboratory"),
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityCode.is_(None),
                            func.length(TBMaster.TestingFacilityCode) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityCode,
                ).label("laboratory_code"),
                *cases,
                TOTAL_ALL.label("total"),
            )
            .filter(and_(*simple_filter))
            .group_by(
                TBMaster.TestingFacilityName,
                TBMaster.TestingFacilityCode,
            )
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # print(data)

        # Serialize de data to JSON
        response = [
            {
                "Testing_Facility": row.laboratory,
                "Testing_Facility_code": row.laboratory_code,
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
                "Type_Of_Result": gx_result_type,
                "Lab_Type": lab,
                "Facilities": facilities,
            }
            for row in data
        ]

        # print(response)

        # Return the response
        return response
    except Exception as e:
        # Prepare the error response
        response = {
            "Status": "error",
            "Data": [],
            "Message": f"An error occurred: {str(e)}",
        }


def tested_samples_by_lab_by_drug_type_service_month(req_args):
    """
    Retrieve the number of tested samples by lab
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    facilities = (
        [] if len(facilities) == 1 and facilities[0].strip() == "" else facilities
    )

    simple_filter = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.AnalysisDateTime.is_not(None),
    ]

    if lab.lower() != "all":
        simple_filter.append(LAB_TYPE(TBMaster, lab))

    if facilities:
        simple_filter.append(
            or_(
                TBMaster.TestingFacilityName.in_(facilities),
                TBMaster.TestingFacilityCode.in_(facilities),
            )
        )
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
            .filter(and_(*simple_filter))
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
                "Type_of_result": gx_result_type,
                "Lab_Type": lab,
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


def trl_samples_by_lab_by_age_service(req_args):
    """
    Retrieve the number of tested samples by lab by age
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    facilities = (
        [] if len(facilities) == 1 and facilities[0].strip() == "" else facilities
    )

    simple_filter = [
        TBMaster.AuthorisedDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.AuthorisedDateTime.is_not(None),
    ]

    if lab.lower() != "all":
        simple_filter.append(LAB_TYPE(TBMaster, lab))

    if facilities:
        simple_filter.append(
            or_(
                TBMaster.TestingFacilityName.in_(facilities),
                TBMaster.TestingFacilityCode.in_(facilities),
            )
        )

    age_not_specified = func.count(
        case(
            (
                TBMaster.AgeInYears.is_(None),
                1,
            )
        )
    ).label("age_not_specified")

    trl_functions = trl_by_lab_by_days(TBMaster)

    age_groups = [
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
        for min_age, max_age in TRL_AGES
    ]

    # print(select(*age_groups))

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityName.is_(None),
                            func.length(TBMaster.TestingFacilityName) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityName,
                ).label("laboratory"),
                case(
                    (
                        or_(
                            TBMaster.TestingFacilityCode.is_(None),
                            func.length(TBMaster.TestingFacilityCode) == 0,
                        ),
                        literal("Not Specified"),
                    ),
                    else_=TBMaster.TestingFacilityCode,
                ).label("laboratory_code"),
                *age_groups,
                age_not_specified,
                TOTAL_ALL.label("total"),
            )
            .filter(and_(*simple_filter))
            .group_by(
                # Use the same column as above
                TBMaster.TestingFacilityName,
                TBMaster.TestingFacilityCode,
            )
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Laboratory": row.laboratory,
                "Laboratory_Code": row.laboratory_code,
                "Age_Not_Specified": row.age_not_specified,
                "Total": row.total,
                **{
                    key: {
                        # Replaces the key name from the key and maintains the ages structure
                        # in the subdictionary
                        age_group.name.replace(f"{key}_", ""): getattr(
                            row, age_group.name
                        )
                        for age_group in age_groups
                        if age_group.name.startswith(f"{key}_")
                    }
                    for key, value in trl_functions.items()
                },
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
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


def trl_samples_by_lab_by_age_by_service_month(req_args):
    """
    Retrieve the number of tested samples by lab by month
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    facilities = (
        [] if len(facilities) == 1 and facilities[0].strip() == "" else facilities
    )

    simple_filter = [
        TBMaster.AuthorisedDateTime.between(dates[0], dates[1]),
        TBMaster.TypeOfResult == gx_result_type,
        TBMaster.AuthorisedDateTime.is_not(None),
    ]

    if lab.lower() != "all":
        simple_filter.append(LAB_TYPE(TBMaster, lab))

    if facilities:
        simple_filter.append(
            or_(
                TBMaster.TestingFacilityName.in_(facilities),
                TBMaster.TestingFacilityCode.in_(facilities),
            )
        )

    age_not_specified = func.count(
        case(
            (
                TBMaster.AgeInYears.is_(None),
                1,
            )
        )
    ).label("age_not_specified")

    trl_functions = trl_by_lab_by_days(TBMaster)

    age_groups = [
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
        for min_age, max_age in TRL_AGES
    ]

    # print(select(*age_groups))

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                MONTH(TBMaster.AuthorisedDateTime).label("Month"),
                DATE_PART("month", TBMaster.AuthorisedDateTime).label("Month_Name"),
                *age_groups,
                age_not_specified,
                TOTAL_ALL.label("total"),
            )
            .filter(and_(*simple_filter))
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
                "Age_Not_Specified": row.age_not_specified,
                "Total": row.total,
                **{
                    key: {
                        # Replaces the key name from the key and maintains the ages structure
                        # in the subdictionary
                        age_group.name.replace(f"{key}_", ""): getattr(
                            row, age_group.name
                        )
                        for age_group in age_groups
                        if age_group.name.startswith(f"{key}_")
                    }
                    for key, value in trl_functions.items()
                },
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
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
