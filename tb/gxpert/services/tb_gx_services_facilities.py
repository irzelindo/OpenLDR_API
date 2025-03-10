from tb.gxpert.models.tb_gx_model import TBMaster
from utilities.utils import *
from sqlalchemy import and_, or_, func, case, literal, text


def registered_samples_by_facility_ultra(args):
    """
    Get the total number of samples registered by facility between two dates.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities = (
        PROCESS_COMMON_PARAMS(args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        query = (
            (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    TOTAL_ALL.label("TotalSamples"),
                )
                .filter(
                    and_(
                        TBMaster.RegisteredDateTime.between(
                            dates[0], dates[1]),
                        TBMaster.TypeOfResult == gx_result_type,
                        (
                            TBMaster.RequestingProvinceName.in_(facilities)
                            if facility_type == "province"
                            else (
                                TBMaster.RequestingDistrictName.in_(facilities)
                                if facility_type == "district"
                                else TBMaster.RequestingFacilityName.in_(facilities)
                            )
                        ),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
            if len(facilities) > 0
            else (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    TOTAL_ALL.label("TotalSamples"),
                )
                .filter(
                    and_(
                        TBMaster.RegisteredDateTime.between(
                            dates[0], dates[1]),
                        TBMaster.TypeOfResult == gx_result_type,
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
        )

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "RegisteredSamples": row.TotalSamples,
                "StartDate": dates[0],
                "EndDate": dates[1],
                "Disaggregation": disaggregation,
                "FacilityType": facility_type,
                "TypeOfResult": gx_result_type,
            }
            for row in data
        ]

        return response

    except Exception as e:
        print(
            f"An error occurred in registered_samples_by_facility_ultra: {str(e)}")
        raise


def tested_samples_by_facility_ultra(args):
    """
    Get the total number of samples tested by facility between two dates.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities = (
        PROCESS_COMMON_PARAMS(args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:

        query = (
            (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    TOTAL_ALL.label("TotalSamples"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        TBMaster.HL7ResultStatusCode == "F",
                        TBMaster.TypeOfResult == gx_result_type,
                        (
                            TBMaster.RequestingProvinceName.in_(facilities)
                            if facility_type == "province"
                            else (
                                TBMaster.RequestingDistrictName.in_(facilities)
                                if facility_type == "district"
                                else TBMaster.RequestingFacilityName.in_(facilities)
                            )
                        ),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
            if len(facilities) > 0
            else (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    TOTAL_ALL.label("TotalSamples"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        TBMaster.TypeOfResult == gx_result_type,
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
        )

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "TestedSamples": row.TotalSamples,
                "StartDate": dates[0],
                "EndDate": dates[1],
                "TypeOfResult": gx_result_type,
                "Disaggregation": disaggregation,
                "FacilityType": facility_type,
            }
            for row in data
        ]

        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_by_facility_ultra: {str(e)}")
        raise


def tested_samples_by_facility_disaggregated(args):
    """
    Get the total number of samples tested by facility between two dates,
    disaggregated by mtb trace, detected, invalid, without result and errors.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities = (
        PROCESS_COMMON_PARAMS(args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        query = (
            (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    TOTAL_ALL.label("TotalSamples"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            FINAL_RESULT_DETECTED_VALUES
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            FINAL_RESULT_DETECTED_VALUES
                                        ),
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Detected"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            FINAL_RESULT_NOT_DETECTED_VALUES
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            FINAL_RESULT_NOT_DETECTED_VALUES
                                        ),
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("NotDetected"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(DETECTED_VALUES),
                                ),
                                1,
                            )
                        )
                    ).label("RifampicinDetected"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(
                                        NOT_DETECTED_VALUES),
                                ),
                                1,
                            ),
                        )
                    ).label("RifampicinNotDetected"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult == None,
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        (
                            TBMaster.RequestingProvinceName.in_(facilities)
                            if facility_type == "province"
                            else (
                                TBMaster.RequestingDistrictName.in_(facilities)
                                if facility_type == "district"
                                else TBMaster.RequestingFacilityName.in_(facilities)
                            )
                        ),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
            if len(facilities) > 0
            else (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    TOTAL_ALL.label("TotalSamples"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            FINAL_RESULT_DETECTED_VALUES
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            FINAL_RESULT_DETECTED_VALUES
                                        ),
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Detected"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            FINAL_RESULT_NOT_DETECTED_VALUES
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            FINAL_RESULT_NOT_DETECTED_VALUES
                                        ),
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("NotDetected"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(DETECTED_VALUES),
                                ),
                                1,
                            )
                        )
                    ).label("RifampicinDetected"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(
                                        NOT_DETECTED_VALUES),
                                ),
                                1,
                            )
                        )
                    ).label("RifampicinNotDetected"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult == None,
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
        )

        data = query.all()

        # print(query.statement)

        response = [
            {
                "Facility": row.Facility,
                "TotalSamples": row.TotalSamples,
                "Detected": row.Detected,
                "NotDetected": row.NotDetected,
                "RifampicinDetected": row.RifampicinDetected,
                "RifampicinNotDetected": row.RifampicinNotDetected,
                "Invalid": row.Invalid,
                "WithoutResult": row.WithoutResult,
                "RejectedSamples": row.RejectedSamples,
                "StartDate": dates[0],
                "EndDate": dates[1],
                "TypeOfResult": gx_result_type,
                "Disaggregation": disaggregation,
                "FacilityType": facility_type,
            }
            for row in data
        ]

        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_by_facility_ultra_disaggregated: {str(e)}"
        )
        raise


def tested_samples_by_facility_disaggregated_by_gender(args):
    """
    Get the total number of samples tested by facility between two dates,
    disaggregated by Gender.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities = (
        PROCESS_COMMON_PARAMS(args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        query = (
            (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "M",
                                ),
                                1,
                            ),
                        )
                    ).label("RifDetMale"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "F",
                                ),
                                1,
                            ),
                        )
                    ).label("RifDetFemale"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "I",
                                ),
                                1,
                            ),
                        )
                    ).label("RifDetIndet"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(
                                        NOT_DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "M",
                                ),
                                1,
                            ),
                        )
                    ).label("RifNotDetMale"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(
                                        NOT_DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "F",
                                ),
                                1,
                            ),
                        )
                    ).label("RifNotDetFemale"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(
                                        NOT_DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "I",
                                ),
                                1,
                            ),
                        )
                    ).label("RifNotDetIndet"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        (
                            TBMaster.RequestingProvinceName.in_(facilities)
                            if facility_type == "province"
                            else (
                                TBMaster.RequestingDistrictName.in_(facilities)
                                if facility_type == "district"
                                else TBMaster.RequestingFacilityName.in_(facilities)
                            )
                        ),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
            if len(facilities) > 0
            else (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(
                                        NOT_DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "M",
                                ),
                                1,
                            ),
                        )
                    ).label("RifDetMale"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "F",
                                ),
                                1,
                            ),
                        )
                    ).label("RifDetFemale"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "I",
                                ),
                                1,
                            ),
                        )
                    ).label("RifDetIndet"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(
                                        NOT_DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "M",
                                ),
                                1,
                            ),
                        )
                    ).label("RifNotDetMale"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(
                                        NOT_DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "F",
                                ),
                                1,
                            ),
                        )
                    ).label("RifNotDetFemale"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(
                                        NOT_DETECTED_VALUES),
                                    TBMaster.HL7SexCode == "I",
                                ),
                                1,
                            ),
                        )
                    ).label("RifNotDetIndet"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        (
                            TBMaster.RequestingProvinceName.in_(facilities)
                            if facility_type == "province"
                            else (
                                TBMaster.RequestingDistrictName.in_(facilities)
                                if facility_type == "district"
                                else TBMaster.RequestingFacilityName.in_(facilities)
                            )
                        ),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
        )

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "RifDetMale": row.RifDetMale,
                "RifDetFemale": row.RifDetFemale,
                "RifDetIndet": row.RifDetIndet,
                "RifNotDetMale": row.RifNotDetMale,
                "RifNotDetFemale": row.RifNotDetFemale,
                "RifNotDetIndet": row.RifNotDetIndet,
                "StartDate": dates[0],
                "EndDate": dates[1],
                "TypeOfResult": gx_result_type,
                "Disaggregation": disaggregation,
                "FacilityType": facility_type,
            }
            for row in data
        ]

        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_by_facility_ultra_disaggregated_by_gender: {str(e)}"
        )


def tested_samples_by_facility_disaggregated_by_age(args):
    """
    Get the total number of samples tested by facility between two dates,
    disaggregated by Age.
    """

    dates, disaggregation, facility_type, gx_result_type, facilities = (
        PROCESS_COMMON_PARAMS(args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        query = (
            (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears > 65,
                                ),
                                1,
                            )
                        )
                    ).label("Detected_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears > 65,
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears > 65,
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears > 65,
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_65_plus"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        (
                            TBMaster.RequestingProvinceName.in_(facilities)
                            if facility_type == "province"
                            else (
                                TBMaster.RequestingDistrictName.in_(facilities)
                                if facility_type == "district"
                                else TBMaster.RequestingFacilityName.in_(facilities)
                            )
                        ),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
            if len(facilities) > 0
            else (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                ),
                                1,
                            )
                        )
                    ).label("Detected_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears > 65,
                                ),
                                1,
                            )
                        )
                    ).label("Detected_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_NOT_DETECTED_VALUES
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears > 65,
                                ),
                                1,
                            )
                        )
                    ).label("Not_Detected_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                        TBMaster.Rifampicin.in_(
                                            ["invalid", "invalido", "inv"]
                                        ),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears > 65,
                                ),
                                1,
                            ),
                        )
                    ).label("Invalid_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    or_(
                                        TBMaster.FinalResult.in_(
                                            ["NORES", "No Result"]
                                        ),
                                        TBMaster.MtbTrace.in_(
                                            ["NORES", "No Result"]),
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears > 65,
                                ),
                                1,
                            ),
                        )
                    ).label("WithoutResult_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.HL7ResultStatusCode == "X",
                                    or_(
                                        TBMaster.LIMSRejectionCode.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionCode) > 0,
                                        TBMaster.LIMSRejectionDesc.isnot(None),
                                        func.length(
                                            TBMaster.LIMSRejectionDesc) > 0,
                                    ),
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                ),
                                1,
                            )
                        )
                    ).label("RejectedSamples_65_plus"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
        )

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "0-4": {
                    "detected": row.Detected_0_to_4,
                    "not_detected": row.Not_Detected_0_to_4,
                    "invalid": row.Invalid_0_to_4,
                    "without_result": row.WithoutResult_0_to_4,
                    "rejected_samples": row.RejectedSamples_0_to_4,
                },
                "5-9": {
                    "detected": row.Detected_5_to_9,
                    "not_detected": row.Not_Detected_5_to_9,
                    "invalid": row.Invalid_5_to_9,
                    "without_result": row.WithoutResult_5_to_9,
                    "rejected_samples": row.RejectedSamples_5_to_9,
                },
                "10-14": {
                    "detected": row.Detected_10_to_14,
                    "not_detected": row.Not_Detected_10_to_14,
                    "invalid": row.Invalid_10_to_14,
                    "without_result": row.WithoutResult_10_to_14,
                    "rejected_samples": row.RejectedSamples_10_to_14,
                },
                "15-19": {
                    "detected": row.Detected_15_to_19,
                    "not_detected": row.Not_Detected_15_to_19,
                    "invalid": row.Invalid_15_to_19,
                    "without_result": row.WithoutResult_15_to_19,
                    "rejected_samples": row.RejectedSamples_15_to_19,
                },
                "20-24": {
                    "detected": row.Detected_20_to_24,
                    "not_detected": row.Not_Detected_20_to_24,
                    "invalid": row.Invalid_20_to_24,
                    "without_result": row.WithoutResult_20_to_24,
                    "rejected_samples": row.RejectedSamples_20_to_24,
                },
                "25-29": {
                    "detected": row.Detected_25_to_29,
                    "not_detected": row.Not_Detected_25_to_29,
                    "invalid": row.Invalid_25_to_29,
                    "without_result": row.WithoutResult_25_to_29,
                    "rejected_samples": row.RejectedSamples_25_to_29,
                },
                "30-34": {
                    "detected": row.Detected_30_to_34,
                    "not_detected": row.Not_Detected_30_to_34,
                    "invalid": row.Invalid_30_to_34,
                    "without_result": row.WithoutResult_30_to_34,
                    "rejected_samples": row.RejectedSamples_30_to_34,
                },
                "35-39": {
                    "detected": row.Detected_35_to_39,
                    "not_detected": row.Not_Detected_35_to_39,
                    "invalid": row.Invalid_35_to_39,
                    "without_result": row.WithoutResult_35_to_39,
                    "rejected_samples": row.RejectedSamples_35_to_39,
                },
                "40-44": {
                    "detected": row.Detected_40_to_44,
                    "not_detected": row.Not_Detected_40_to_44,
                    "invalid": row.Invalid_40_to_44,
                    "without_result": row.WithoutResult_40_to_44,
                    "rejected_samples": row.RejectedSamples_40_to_44,
                },
                "45-49": {
                    "detected": row.Detected_45_to_49,
                    "not_detected": row.Not_Detected_45_to_49,
                    "invalid": row.Invalid_45_to_49,
                    "without_result": row.WithoutResult_45_to_49,
                    "rejected_samples": row.RejectedSamples_45_to_49,
                },
                "50-54": {
                    "detected": row.Detected_50_to_54,
                    "not_detected": row.Not_Detected_50_to_54,
                    "invalid": row.Invalid_50_to_54,
                    "without_result": row.WithoutResult_50_to_54,
                    "rejected_samples": row.RejectedSamples_50_to_54,
                },
                "55-59": {
                    "detected": row.Detected_55_to_59,
                    "not_detected": row.Not_Detected_55_to_59,
                    "invalid": row.Invalid_55_to_59,
                    "without_result": row.WithoutResult_55_to_59,
                    "rejected_samples": row.RejectedSamples_55_to_59,
                },
                "60-64": {
                    "detected": row.Detected_60_to_64,
                    "not_detected": row.Not_Detected_60_to_64,
                    "invalid": row.Invalid_60_to_64,
                    "without_result": row.WithoutResult_60_to_64,
                    "rejected_samples": row.RejectedSamples_60_to_64,
                },
                "65+": {
                    "detected": row.Detected_65_plus,
                    "not_detected": row.Not_Detected_65_plus,
                    "invalid": row.Invalid_65_plus,
                    "without_result": row.WithoutResult_65_plus,
                    "rejected_samples": row.RejectedSamples_65_plus,
                },
                "StartDate": dates[0],
                "EndDate": dates[1],
                "TypeOfResult": gx_result_type,
                "Disaggregation": disaggregation,
                "FacilityType": facility_type,
            }
            for row in data
        ]

        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_by_facility_disaggregated_by_age: {str(e)}"
        )


def tested_samples_types_by_facility_disaggregated_by_age(req_args):
    """
    Get the number of samples tested by facility between two dates, disaggregated by age.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities = (
        PROCESS_COMMON_PARAMS(req_args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        query = (
            (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_65_plus"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        (
                            TBMaster.RequestingProvinceName.in_(facilities)
                            if facility_type == "province"
                            else (
                                TBMaster.RequestingDistrictName.in_(facilities)
                                if facility_type == "district"
                                else TBMaster.RequestingFacilityName.in_(facilities)
                            )
                        ),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
            if len(facilities) > 0 else (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_0_to_4"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(5, 9),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_5_to_9"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(10, 14),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_10_to_14"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(15, 19),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(0, 4),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_15_to_19"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(20, 24),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_20_to_24"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(25, 29),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_25_to_29"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(30, 34),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_30_to_34"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(35, 39),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_35_to_39"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(40, 44),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_40_to_44"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(45, 49),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_45_to_49"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(50, 54),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_50_to_54"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(55, 59),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_55_to_59"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears.between(60, 64),
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_60_to_64"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Sputum_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_FECES_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Feces_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_URINE_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Urine_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.in_(
                                        TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Blood_65_plus"),
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.AgeInYears.isnot(None),
                                    TBMaster.AgeInYears >= 65,
                                    TBMaster.LIMSSpecimenSourceCode.notin_(
                                        TB_SPUTUM_SPECIMEN_SOURCE_CODES
                                        + TB_FECES_SPECIMEN_SOURCE_CODES
                                        + TB_URINE_SPECIMEN_SOURCE_CODES
                                        + TB_BLOOD_SPECIMEN_SOURCE_CODES
                                    ),
                                ),
                                1,
                            )
                        )
                    ).label("Other_65_plus"),
                )
                .filter(
                    and_(
                        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
        )

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "0-4": {
                    "sputum": row.Sputum_0_to_4,
                    "feces": row.Feces_0_to_4,
                    "urine": row.Urine_0_to_4,
                    "blood": row.Blood_0_to_4,
                    "other": row.Other_0_to_4,
                },
                "5-9": {
                    "sputum": row.Sputum_5_to_9,
                    "feces": row.Feces_5_to_9,
                    "urine": row.Urine_5_to_9,
                    "blood": row.Blood_5_to_9,
                    "other": row.Other_5_to_9,
                },
                "10-14": {
                    "sputum": row.Sputum_10_to_14,
                    "feces": row.Feces_10_to_14,
                    "urine": row.Urine_10_to_14,
                    "blood": row.Blood_10_to_14,
                    "other": row.Other_10_to_14,
                },
                "15-19": {
                    "sputum": row.Sputum_15_to_19,
                    "feces": row.Feces_15_to_19,
                    "urine": row.Urine_15_to_19,
                    "blood": row.Blood_15_to_19,
                    "other": row.Other_15_to_19,
                },
                "20-24": {
                    "sputum": row.Sputum_20_to_24,
                    "feces": row.Feces_20_to_24,
                    "urine": row.Urine_20_to_24,
                    "blood": row.Blood_20_to_24,
                    "other": row.Other_20_to_24,
                },
                "25-29": {
                    "sputum": row.Sputum_25_to_29,
                    "feces": row.Feces_25_to_29,
                    "urine": row.Urine_25_to_29,
                    "blood": row.Blood_25_to_29,
                    "other": row.Other_25_to_29,
                },
                "30-34": {
                    "sputum": row.Sputum_30_to_34,
                    "feces": row.Feces_30_to_34,
                    "urine": row.Urine_30_to_34,
                    "blood": row.Blood_30_to_34,
                    "other": row.Other_30_to_34,
                },
                "35-39": {
                    "sputum": row.Sputum_35_to_39,
                    "feces": row.Feces_35_to_39,
                    "urine": row.Urine_35_to_39,
                    "blood": row.Blood_35_to_39,
                    "other": row.Other_35_to_39,
                },
                "40-44": {
                    "sputum": row.Sputum_40_to_44,
                    "feces": row.Feces_40_to_44,
                    "urine": row.Urine_40_to_44,
                    "blood": row.Blood_40_to_44,
                    "other": row.Other_40_to_44,
                },
                "45-49": {
                    "sputum": row.Sputum_45_to_49,
                    "feces": row.Feces_45_to_49,
                    "urine": row.Urine_45_to_49,
                    "blood": row.Blood_45_to_49,
                    "other": row.Other_45_to_49,
                },
                "50-54": {
                    "sputum": row.Sputum_50_to_54,
                    "feces": row.Feces_50_to_54,
                    "urine": row.Urine_50_to_54,
                    "blood": row.Blood_50_to_54,
                    "other": row.Other_50_to_54,
                },
                "55-59": {
                    "sputum": row.Sputum_55_to_59,
                    "feces": row.Feces_55_to_59,
                    "urine": row.Urine_55_to_59,
                    "blood": row.Blood_55_to_59,
                    "other": row.Other_55_to_59,
                },
                "60-64": {
                    "sputum": row.Sputum_60_to_64,
                    "feces": row.Feces_60_to_64,
                    "urine": row.Urine_60_to_64,
                    "blood": row.Blood_60_to_64,
                    "other": row.Other_60_to_64,
                },
                "65+": {
                    "sputum": row.Sputum_65_plus,
                    "feces": row.Feces_65_plus,
                    "urine": row.Urine_65_plus,
                    "blood": row.Blood_65_plus,
                    "other": row.Other_65_plus,
                },
                "StartDate": dates[0],
                "EndDate": dates[1],
                "TypeOfResult": gx_result_type,
                "Disaggregation": disaggregation,
                "FacilityType": facility_type,
            }
            for row in data
        ]
        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_types_by_facility_disaggregated_by_age: {str(e)}"
        )


def tested_samples_by_facility_rifampicin_resistance_disaggregated_by_drug_type(
    req_args,
):
    """
    This function returns the number of tested samples by facility, disaggregated by drug type.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities = (
        PROCESS_COMMON_PARAMS(req_args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    drugs = [
        "Rifampicin", "Isoniazid", "Fluoroquinolona", "Kanamicin",
        "Amikacina", "Capreomicin", "Ethionamida"
    ]

    cases = [
        func.count(
            case(
                (
                    and_(
                        TBMaster.TypeOfResult == gx_result_type,
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
        # print(ColumnNames)
        base_query = TBMaster.query.with_entities(
            ColumnNames.label("Facility"),
            *cases
        ).filter(
            and_(
                TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                TBMaster.FinalResult.isnot(None),
                ColumnNames.isnot(None),
            )
        ).group_by(ColumnNames)

        query = base_query.filter(
            and_(
                TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                (
                    TBMaster.RequestingProvinceName.in_(facilities)
                    if facility_type == "province"
                    else (
                        TBMaster.RequestingDistrictName.in_(facilities)
                        if facility_type == "district"
                        else TBMaster.RequestingFacilityName.in_(facilities)
                    )
                ),
            )
        ).group_by(ColumnNames) if len(facilities) > 0 else base_query

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "Rifampicin_Null": row.Rifampicin_Null,
                "Rifampicin": {
                    "Resistance_Detected": row.Rifampicin_Resistance_Detected,
                    "Resistance_Not_Detected": row.Rifampicin_Resistance_Not_Detected,
                    "Resistance_Indeterminate": row.Rifampicin_Resistance_Indeterminate,
                },
                "Isoniazid": {
                    "Resistance_Detected": row.Isoniazid_Resistance_Detected,
                    "Resistance_Not_Detected": row.Isoniazid_Resistance_Not_Detected,
                    "Resistance_Indeterminate": row.Isoniazid_Resistance_Indeterminate,
                },
                "Fluoroquinolona": {
                    "Resistance_Detected": row.Fluoroquinolona_Resistance_Detected,
                    "Resistance_Not_Detected": row.Fluoroquinolona_Resistance_Not_Detected,
                    "Resistance_Indeterminate": row.Fluoroquinolona_Resistance_Indeterminate,
                },
                "Kanamicin": {
                    "Resistance_Detected": row.Kanamicin_Resistance_Detected,
                    "Resistance_Not_Detected": row.Kanamicin_Resistance_Not_Detected,
                    "Resistance_Indeterminate": row.Kanamicin_Resistance_Indeterminate,
                },
                "Amikacin": {
                    "Resistance_Detected": row.Amikacina_Resistance_Detected,
                    "Resistance_Not_Detected": row.Amikacina_Resistance_Not_Detected,
                    "Resistance_Indeterminate": row.Amikacina_Resistance_Indeterminate,
                },
                "Capreomicin": {
                    "Resistance_Detected": row.Capreomicin_Resistance_Detected,
                    "Resistance_Not_Detected": row.Capreomicin_Resistance_Not_Detected,
                    "Resistance_Indeterminate": row.Capreomicin_Resistance_Indeterminate,
                },
                "Ethionamide": {
                    "Resistance_Detected": row.Ethionamida_Resistance_Detected,
                    "Resistance_Not_Detected": row.Ethionamida_Resistance_Not_Detected,
                    "Resistance_Indeterminate": row.Ethionamida_Resistance_Indeterminate,
                },
                "StartDate": dates[0],
                "EndDate": dates[1],
                "TypeOfResult": gx_result_type,
                "Disaggregation": disaggregation,
                "FacilityType": facility_type,
            }
            for row in data
        ]
        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_by_facility_rifampicin_disaggregated_by_drug_type: {str(e)}"
        )


def tested_samples_by_facility_rifampicin_resistance_disaggregated_by_drug_type_by_age(
    req_args,
):
    """
    This function returns the number of tested samples by facility, disaggregated by drug type and age.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities = (
        PROCESS_COMMON_PARAMS(req_args)
    )

    drug = req_args.get("drug")

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        drug_column = getattr(TBMaster, drug)

        # Generate all count columns dynamically
        count_columns = [
            create_count_column(start, end, state, values,
                TBMaster, drug_column, gx_result_type)
            for (start, end) in TB_AGE_RANGES
            for state, values in TB_RESISTANCE_STATES.items()
        ]

        # Build the base query
        base_query = TBMaster.query.with_entities(
            ColumnNames.label("Facility"),
            *count_columns
        ).filter(
            and_(
                TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                TBMaster.FinalResult.isnot(None),
                ColumnNames.isnot(None),
            )
        ).group_by(ColumnNames)

        # Apply facility filter if needed
        query = (
            base_query.filter(
                (
                    TBMaster.RequestingProvinceName.in_(facilities)
                    if facility_type == "province"
                    else (
                        TBMaster.RequestingDistrictName.in_(facilities)
                        if facility_type == "district"
                        else TBMaster.RequestingFacilityName.in_(facilities)
                    )
                )
            ) if len(facilities) > 0 else base_query
        )

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "0-4": {
                    "Resistance_Detected": row.Resistance_Detected_0_4,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_0_4,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_0_4,
                },
                "5-9": {
                    "Resistance_Detected": row.Resistance_Detected_5_9,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_5_9,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_5_9,
                },
                "10-14": {
                    "Resistance_Detected": row.Resistance_Detected_10_14,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_10_14,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_10_14,
                },
                "15-19": {
                    "Resistance_Detected": row.Resistance_Detected_15_19,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_15_19,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_15_19,
                },
                "20-24": {
                    "Resistance_Detected": row.Resistance_Detected_20_24,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_20_24,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_20_24,
                },
                "25-29": {
                    "Resistance_Detected": row.Resistance_Detected_25_29,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_25_29,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_25_29,
                },
                "30-34": {
                    "Resistance_Detected": row.Resistance_Detected_30_34,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_30_34,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_30_34,
                },
                "35-39": {
                    "Resistance_Detected": row.Resistance_Detected_35_39,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_35_39,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_35_39,
                },
                "40-44": {
                    "Resistance_Detected": row.Resistance_Detected_40_44,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_40_44,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_40_44,
                },
                "45-49": {
                    "Resistance_Detected": row.Resistance_Detected_45_49,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_45_49,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_45_49,
                },
                "50-54": {
                    "Resistance_Detected": row.Resistance_Detected_50_54,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_50_54,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_50_54,
                },
                "55-59": {
                    "Resistance_Detected": row.Resistance_Detected_55_59,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_55_59,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_55_59,
                },
                "60-64": {
                    "Resistance_Detected": row.Resistance_Detected_60_64,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_60_64,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_60_64,
                },
                "65+": {
                    "Resistance_Detected": row.Resistance_Detected_65_plus,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_65_plus,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_65_plus,
                },
                "Not_Specified": {
                    "Resistance_Detected": row.Resistance_Detected_Not_Specified,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_Not_Specified,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_Not_Specified,
                },
                "StartDate": dates[0],
                "EndDate": dates[1],
                "TypeOfResult": gx_result_type,
                "Disaggregation": disaggregation,
                "FacilityType": facility_type,
                "Drug": drug,
            }
            for row in data
        ]

        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_by_facility_rifampicin_resistance_disaggregated_by_drug_type_by_age: {str(e)}"
        )
