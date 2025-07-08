from tb.gxpert.models.tb_gx_model import TBMaster
from utilities.utils import *
from sqlalchemy import and_, or_, func, case, literal, text


def registered_samples_by_facility(args):
    """
    Get the total number of samples registered by facility between two dates.
    """
    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(args)

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    filters = [
        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
        ColumnNames.isnot(None),
    ]

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                health_facility,
                lab,
                dates,
                TBMaster,
                TBMaster.RegisteredDateTime,
                gx_result_type,
                "tb",
            )
        elif not facilities:
            # If no facilities are provided, query all facilities
            query = (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    TOTAL_ALL.label("TotalSamples"),
                )
                .filter(
                    *filters,
                )
                .group_by(ColumnNames)
            )
        else:
            # If facilities are provided, filter by the selected facility type
            query = (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    TOTAL_ALL.label("TotalSamples"),
                )
                .filter(
                    *filters,
                    GET_COLUMN_NAME(False, facility_type, TBMaster).in_(facilities),
                )
                .group_by(ColumnNames)
            )

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        if facility_type == "health_facility":
            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )
            return response
        else:
            response = [
                {
                    "Facility": row.Facility,
                    "Registered_Samples": row.TotalSamples,
                    "Start_Date": dates[0],
                    "End_Date": dates[1],
                    "Disaggregation": disaggregation,
                    "Facility_Type": facility_type,
                    "Type_Of_Result": gx_result_type if gx_result_type else "All",
                }
                for row in data
            ]
            return response

    except Exception as e:
        print(f"An error occurred in registered_samples_by_facility: {str(e)}")
        raise


def tested_samples_by_facility(args):
    """
    Get the total number of samples tested by facility between two dates.
    """
    (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        lab,
        health_facility,
    ) = PROCESS_COMMON_PARAMS_FACILITY(args)

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    filters = [
        TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
        TBMaster.HL7ResultStatusCode == "F",
        ColumnNames.isnot(None),
    ]

    if gx_result_type not in ("All", None):
        filters.append(TBMaster.TypeOfResult == gx_result_type)

    try:
        if facility_type == "health_facility":
            # Call get_patients if facility_type is equal to health_facility
            # And disaggregation is true
            query = get_patients(
                health_facility,
                lab,
                dates,
                TBMaster,
                TBMaster.AnalysisDateTime,
                gx_result_type,
                "tb",
            )
        elif not facilities:
            # If no facilities are provided, query all facilities
            query = (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
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
                                TBMaster.FinalResult.in_(
                                    FINAL_RESULT_NOT_DETECTED_VALUES
                                ),
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
                                or_(
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_ERROR_DETECTED_VALUES
                                    ),
                                    func.length(TBMaster.LIMSRejectionCode) > 0,
                                    TBMaster.FinalResult.is_(None),
                                ),
                                1,
                            )
                        )
                    ).label("errors"),
                    TOTAL_ALL.label("TotalSamples"),
                )
                .filter(
                    *filters,
                )
                .group_by(ColumnNames)
            )
        else:
            # If facilities are provided, filter by the selected facility type
            query = (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
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
                                TBMaster.FinalResult.in_(
                                    FINAL_RESULT_NOT_DETECTED_VALUES
                                ),
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
                                or_(
                                    TBMaster.FinalResult.in_(
                                        FINAL_RESULT_ERROR_DETECTED_VALUES
                                    ),
                                    func.length(TBMaster.LIMSRejectionCode) > 0,
                                ),
                                1,
                            )
                        )
                    ).label("errors"),
                    TOTAL_ALL.label("TotalSamples"),
                )
                .filter(
                    *filters,
                    GET_COLUMN_NAME(False, facility_type, TBMaster).in_(facilities),
                )
                .group_by(ColumnNames)
            )
        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        if facility_type == "health_facility":
            response = process_patients(
                data, dates, facility_type, gx_result_type, "tb"
            )
            return response
        else:
            response = [
                {
                    "Facility": row.Facility,
                    "Tested_Samples": row.TotalSamples,
                    "Detected": row.tb_detected,
                    "Not_Detected": row.tb_not_detected,
                    "Invalid": row.invalid_results,
                    "Errors": row.errors,
                    "Start_Date": dates[0],
                    "End_Date": dates[1],
                    "Disaggregation": disaggregation,
                    "Facility_Type": facility_type if facility_type else None,
                    "Type_Of_Result": gx_result_type if gx_result_type else "All",
                }
                for row in data
            ]

        return response

    except Exception as e:
        print(f"An error occurred in tested_samples_by_facility: {str(e)}")
        raise


def tested_samples_by_facility_disaggregated(args):
    """
    Get the total number of samples tested by facility between two dates,
    disaggregated by mtb trace, detected, invalid, without result and errors.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:

        common_entities = [
            ColumnNames.label("Facility"),
            TOTAL_ALL.label("TotalSamples"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == gx_result_type,
                            or_(
                                TBMaster.FinalResult.in_(FINAL_RESULT_DETECTED_VALUES),
                                TBMaster.MtbTrace.in_(FINAL_RESULT_DETECTED_VALUES),
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
                                TBMaster.MtbTrace.in_(FINAL_RESULT_NOT_DETECTED_VALUES),
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
                            TBMaster.Rifampicin.in_(NOT_DETECTED_VALUES),
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
                                TBMaster.Rifampicin.in_(["invalid", "invalido", "inv"]),
                            ),
                        ),
                        1,
                    )
                )
            ).label("Invalid"),
            func.count(
                case(
                    (
                        and_(
                            TBMaster.TypeOfResult == gx_result_type,
                            or_(
                                TBMaster.FinalResult == None,
                                TBMaster.FinalResult.in_(["NORES", "No Result"]),
                                TBMaster.MtbTrace.in_(["NORES", "No Result"]),
                            ),
                        ),
                        1,
                    )
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
                                func.length(TBMaster.LIMSRejectionCode) > 0,
                                TBMaster.LIMSRejectionDesc.isnot(None),
                                func.length(TBMaster.LIMSRejectionDesc) > 0,
                            ),
                        ),
                        1,
                    )
                )
            ).label("RejectedSamples"),
        ]

        common_filter = [
            TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
            ColumnNames.isnot(None),
        ]

        if len(facilities) > 0:
            facility_filter = (
                TBMaster.RequestingProvinceName.in_(facilities)
                if facility_type == "province"
                else (
                    TBMaster.RequestingDistrictName.in_(facilities)
                    if facility_type == "district"
                    else TBMaster.RequestingFacilityName.in_(facilities)
                )
            )
            common_filter.append(facility_filter)

        query = (
            TBMaster.query.with_entities(*common_entities)
            .filter(and_(*common_filter))
            .group_by(ColumnNames)
        )

        data = query.all()

        # print(query.statement)

        response = [
            {
                "Facility": row.Facility,
                "Tested_Samples": row.TotalSamples,
                "Detected": row.Detected,
                "Not_Detected": row.NotDetected,
                "Rifampicin_Detected": row.RifampicinDetected,
                "Rifampicin_Not_Detected": row.RifampicinNotDetected,
                "Invalid": row.Invalid,
                "Without_Result": row.WithoutResult,
                "Rejected_Samples": row.RejectedSamples,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Disaggregation": disaggregation,
                "Facility_Type": facility_type,
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
    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        sex_codes = {"M": "Male", "F": "Female", "I": "Indet"}

        result_types = {
            "Det": DETECTED_VALUES,
            "NotDet": NOT_DETECTED_VALUES,
            "Null": None,
        }

        counts = [ColumnNames.label("Facility")]

        for result_prefix, values in result_types.items():
            for sex_code, sex_label in sex_codes.items():
                counts.append(
                    func.count(
                        case(
                            (
                                and_(
                                    TBMaster.TypeOfResult == gx_result_type,
                                    TBMaster.Rifampicin.in_(values),
                                    TBMaster.HL7SexCode == sex_code,
                                ),
                                1,
                            )
                        )
                    ).label(f"Rif{result_prefix}{sex_label}")
                    if result_prefix in ("Det", "NotDet")
                    else (
                        func.count(
                            case(
                                (
                                    and_(
                                        TBMaster.TypeOfResult == gx_result_type,
                                        TBMaster.Rifampicin.is_(None),
                                        TBMaster.HL7SexCode == sex_label,
                                    ),
                                    1,
                                )
                            )
                        )
                    ).label(f"RifNull{sex_label}")
                )

        query = TBMaster.query.with_entities(*counts).filter(
            and_(
                TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                ColumnNames.isnot(None),
            )
        )

        if facilities:
            if facility_type == "province":
                query = query.filter(TBMaster.RequestingProvinceName.in_(facilities))
            elif facility_type == "district":
                query = query.filter(TBMaster.RequestingDistrictName.in_(facilities))
            else:
                query = query.filter(TBMaster.RequestingFacilityName.in_(facilities))

        query = query.group_by(ColumnNames)

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "Rif_Det_Male": row.RifDetMale,
                "Rif_Det_Female": row.RifDetFemale,
                "Rif_Det_Indet": row.RifDetIndet,
                "Rif_NotDet_Male": row.RifNotDetMale,
                "Rif_NotDet_Female": row.RifNotDetFemale,
                "Rif_NotDet_Indet": row.RifNotDetIndet,
                "Rif_Null_Male": row.RifNullMale,
                "Rif_Null_Female": row.RifNullFemale,
                "Rif_Null_Indet": row.RifNullIndet,
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Disaggregation": disaggregation,
                "Facility_Type": facility_type,
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

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        RESULT_CATEGORIES = {
            "Detected": lambda: TBMaster.FinalResult.in_(FINAL_RESULT_DETECTED_VALUES),
            "Not_Detected": lambda: TBMaster.FinalResult.in_(
                FINAL_RESULT_NOT_DETECTED_VALUES
            ),
            "Invalid": lambda: or_(
                TBMaster.FinalResult.in_(["invalid", "invalido", "inv"]),
                TBMaster.Rifampicin.in_(["invalid", "invalido", "inv"]),
            ),
            "WithoutResult": lambda: or_(
                TBMaster.FinalResult.in_(["NORES", "No Result"]),
                TBMaster.MtbTrace.in_(["NORES", "No Result"]),
            ),
            "RejectedSamples": lambda: and_(
                TBMaster.HL7ResultStatusCode == "X",
                or_(
                    TBMaster.LIMSRejectionCode.isnot(None),
                    func.length(TBMaster.LIMSRejectionCode) > 0,
                    TBMaster.LIMSRejectionDesc.isnot(None),
                    func.length(TBMaster.LIMSRejectionDesc) > 0,
                ),
            ),
        }

        # Generate columns dynamically
        count_columns = [ColumnNames.label("Facility")]

        for age_min, age_max in TB_AGE_RANGES:
            age_suffix = (
                f"{age_min}_to_{age_max}"
                if age_max
                else ("65_plus" if age_min == 65 else "Not_Specified")
            )

            age_condition = (
                TBMaster.AgeInYears.between(age_min, age_max)
                if age_max
                else (
                    TBMaster.AgeInYears >= age_min
                    if age_min == 65
                    else TBMaster.AgeInYears.is_(None)
                )
            )

            for category, condition_func in RESULT_CATEGORIES.items():
                conditions = [
                    TBMaster.TypeOfResult == gx_result_type,
                    condition_func(),
                    TBMaster.AgeInYears.isnot(None),
                    age_condition,
                ]
                count_columns.append(
                    func.count(case((and_(*conditions), 1))).label(
                        f"{category}_{age_suffix}"
                    )
                )

        # Build the base query
        base_query = TBMaster.query.with_entities(*count_columns).group_by(ColumnNames)

        # Apply filters based on facilities
        if len(facilities) > 0:
            facility_filter = {
                "province": TBMaster.RequestingProvinceName.in_(facilities),
                "district": TBMaster.RequestingDistrictName.in_(facilities),
                "facility": TBMaster.RequestingFacilityName.in_(facilities),
            }.get(facility_type, TBMaster.RequestingFacilityName.in_(facilities))
            filters = and_(
                TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                facility_filter,
                ColumnNames.isnot(None),
            )
        else:
            filters = and_(
                TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                ColumnNames.isnot(None),
            )

        # Final query
        query = base_query.filter(filters)

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "0_4": {
                    "detected": row.Detected_0_to_4,
                    "not_detected": row.Not_Detected_0_to_4,
                    "invalid": row.Invalid_0_to_4,
                    "without_result": row.WithoutResult_0_to_4,
                    "rejected_samples": row.RejectedSamples_0_to_4,
                },
                "5_9": {
                    "detected": row.Detected_5_to_9,
                    "not_detected": row.Not_Detected_5_to_9,
                    "invalid": row.Invalid_5_to_9,
                    "without_result": row.WithoutResult_5_to_9,
                    "rejected_samples": row.RejectedSamples_5_to_9,
                },
                "10_14": {
                    "detected": row.Detected_10_to_14,
                    "not_detected": row.Not_Detected_10_to_14,
                    "invalid": row.Invalid_10_to_14,
                    "without_result": row.WithoutResult_10_to_14,
                    "rejected_samples": row.RejectedSamples_10_to_14,
                },
                "15_19": {
                    "detected": row.Detected_15_to_19,
                    "not_detected": row.Not_Detected_15_to_19,
                    "invalid": row.Invalid_15_to_19,
                    "without_result": row.WithoutResult_15_to_19,
                    "rejected_samples": row.RejectedSamples_15_to_19,
                },
                "20_24": {
                    "detected": row.Detected_20_to_24,
                    "not_detected": row.Not_Detected_20_to_24,
                    "invalid": row.Invalid_20_to_24,
                    "without_result": row.WithoutResult_20_to_24,
                    "rejected_samples": row.RejectedSamples_20_to_24,
                },
                "25_29": {
                    "detected": row.Detected_25_to_29,
                    "not_detected": row.Not_Detected_25_to_29,
                    "invalid": row.Invalid_25_to_29,
                    "without_result": row.WithoutResult_25_to_29,
                    "rejected_samples": row.RejectedSamples_25_to_29,
                },
                "30_34": {
                    "detected": row.Detected_30_to_34,
                    "not_detected": row.Not_Detected_30_to_34,
                    "invalid": row.Invalid_30_to_34,
                    "without_result": row.WithoutResult_30_to_34,
                    "rejected_samples": row.RejectedSamples_30_to_34,
                },
                "35_39": {
                    "detected": row.Detected_35_to_39,
                    "not_detected": row.Not_Detected_35_to_39,
                    "invalid": row.Invalid_35_to_39,
                    "without_result": row.WithoutResult_35_to_39,
                    "rejected_samples": row.RejectedSamples_35_to_39,
                },
                "40_44": {
                    "detected": row.Detected_40_to_44,
                    "not_detected": row.Not_Detected_40_to_44,
                    "invalid": row.Invalid_40_to_44,
                    "without_result": row.WithoutResult_40_to_44,
                    "rejected_samples": row.RejectedSamples_40_to_44,
                },
                "45_49": {
                    "detected": row.Detected_45_to_49,
                    "not_detected": row.Not_Detected_45_to_49,
                    "invalid": row.Invalid_45_to_49,
                    "without_result": row.WithoutResult_45_to_49,
                    "rejected_samples": row.RejectedSamples_45_to_49,
                },
                "50_54": {
                    "detected": row.Detected_50_to_54,
                    "not_detected": row.Not_Detected_50_to_54,
                    "invalid": row.Invalid_50_to_54,
                    "without_result": row.WithoutResult_50_to_54,
                    "rejected_samples": row.RejectedSamples_50_to_54,
                },
                "55_59": {
                    "detected": row.Detected_55_to_59,
                    "not_detected": row.Not_Detected_55_to_59,
                    "invalid": row.Invalid_55_to_59,
                    "without_result": row.WithoutResult_55_to_59,
                    "rejected_samples": row.RejectedSamples_55_to_59,
                },
                "60_64": {
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
                "Age_Not_Specified": {
                    "detected": row.Detected_Not_Specified,
                    "not_detected": row.Not_Detected_Not_Specified,
                    "invalid": row.Invalid_Not_Specified,
                    "without_result": row.WithoutResult_Not_Specified,
                    "rejected_samples": row.RejectedSamples_Not_Specified,
                },
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Disaggregation": disaggregation,
                "Facility_Type": facility_type,
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
    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:

        SPECIMEN_TYPES = {
            "Sputum": TB_SPUTUM_SPECIMEN_SOURCE_CODES,
            "Feces": TB_FECES_SPECIMEN_SOURCE_CODES,
            "Urine": TB_URINE_SPECIMEN_SOURCE_CODES,
            "Blood": TB_BLOOD_SPECIMEN_SOURCE_CODES,
        }

        ALL_SPECIMEN_CODES = (
            TB_SPUTUM_SPECIMEN_SOURCE_CODES
            + TB_FECES_SPECIMEN_SOURCE_CODES
            + TB_URINE_SPECIMEN_SOURCE_CODES
            + TB_BLOOD_SPECIMEN_SOURCE_CODES
        )

        # Generate count columns dynamically
        count_columns = [ColumnNames.label("Facility")]

        for age_min, age_max in TB_AGE_RANGES:
            age_suffix = (
                f"{age_min}_to_{age_max}"
                if age_min is not None and age_max is not None
                else (
                    "65_plus"
                    if age_min == 65 and age_max is None
                    else "Age_Not_Specified"
                )
            )

            for spec_name, spec_codes in SPECIMEN_TYPES.items():
                conditions = [
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.AgeInYears.is_not(None),
                    TBMaster.LIMSSpecimenSourceCode.in_(spec_codes),
                ]

                if age_min is not None and age_max is not None:
                    conditions.append(TBMaster.AgeInYears.between(age_min, age_max))
                elif age_min == 65 and age_max is None:
                    conditions.append(TBMaster.AgeInYears >= age_min)
                else:
                    conditions = [
                        TBMaster.TypeOfResult == gx_result_type,
                        TBMaster.AgeInYears.is_(None),
                        TBMaster.LIMSSpecimenSourceCode.in_(spec_codes),
                    ]

                count_columns.append(
                    func.count(case(((and_(*conditions), 1)))).label(
                        f"{spec_name}_{age_suffix}"
                    )
                )

            # Add Other category
            other_conditions = [
                TBMaster.TypeOfResult == gx_result_type,
                TBMaster.AgeInYears.is_not(None),
                TBMaster.LIMSSpecimenSourceCode.notin_(ALL_SPECIMEN_CODES),
            ]

            count_columns.append(
                func.count(case(((and_(*other_conditions), 1)))).label(
                    f"Other_{age_suffix}"
                )
            )

            # Main query
            base_filters = [
                TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                ColumnNames.is_not(None),
            ]

            if len(facilities) > 0:
                facility_filter = {
                    "province": TBMaster.RequestingProvinceName.in_(facilities),
                    "district": TBMaster.RequestingDistrictName.in_(facilities),
                    "facility": TBMaster.RequestingFacilityName.in_(facilities),
                }.get(facility_type, TBMaster.RequestingFacilityName.in_(facilities))
                filters = base_filters + [facility_filter]
            else:
                filters = base_filters

            query = (
                TBMaster.query.with_entities(*count_columns)
                .filter(and_(*filters))
                .group_by(ColumnNames)
            )

        data = query.all()

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        response = [
            {
                "Facility": row.Facility,
                "0_4": {
                    "sputum": row.Sputum_0_to_4,
                    "feces": row.Feces_0_to_4,
                    "urine": row.Urine_0_to_4,
                    "blood": row.Blood_0_to_4,
                    "other": row.Other_0_to_4,
                },
                "5_9": {
                    "sputum": row.Sputum_5_to_9,
                    "feces": row.Feces_5_to_9,
                    "urine": row.Urine_5_to_9,
                    "blood": row.Blood_5_to_9,
                    "other": row.Other_5_to_9,
                },
                "10_14": {
                    "sputum": row.Sputum_10_to_14,
                    "feces": row.Feces_10_to_14,
                    "urine": row.Urine_10_to_14,
                    "blood": row.Blood_10_to_14,
                    "other": row.Other_10_to_14,
                },
                "15_19": {
                    "sputum": row.Sputum_15_to_19,
                    "feces": row.Feces_15_to_19,
                    "urine": row.Urine_15_to_19,
                    "blood": row.Blood_15_to_19,
                    "other": row.Other_15_to_19,
                },
                "20_24": {
                    "sputum": row.Sputum_20_to_24,
                    "feces": row.Feces_20_to_24,
                    "urine": row.Urine_20_to_24,
                    "blood": row.Blood_20_to_24,
                    "other": row.Other_20_to_24,
                },
                "25_29": {
                    "sputum": row.Sputum_25_to_29,
                    "feces": row.Feces_25_to_29,
                    "urine": row.Urine_25_to_29,
                    "blood": row.Blood_25_to_29,
                    "other": row.Other_25_to_29,
                },
                "30_34": {
                    "sputum": row.Sputum_30_to_34,
                    "feces": row.Feces_30_to_34,
                    "urine": row.Urine_30_to_34,
                    "blood": row.Blood_30_to_34,
                    "other": row.Other_30_to_34,
                },
                "35_39": {
                    "sputum": row.Sputum_35_to_39,
                    "feces": row.Feces_35_to_39,
                    "urine": row.Urine_35_to_39,
                    "blood": row.Blood_35_to_39,
                    "other": row.Other_35_to_39,
                },
                "40_44": {
                    "sputum": row.Sputum_40_to_44,
                    "feces": row.Feces_40_to_44,
                    "urine": row.Urine_40_to_44,
                    "blood": row.Blood_40_to_44,
                    "other": row.Other_40_to_44,
                },
                "45_49": {
                    "sputum": row.Sputum_45_to_49,
                    "feces": row.Feces_45_to_49,
                    "urine": row.Urine_45_to_49,
                    "blood": row.Blood_45_to_49,
                    "other": row.Other_45_to_49,
                },
                "50_54": {
                    "sputum": row.Sputum_50_to_54,
                    "feces": row.Feces_50_to_54,
                    "urine": row.Urine_50_to_54,
                    "blood": row.Blood_50_to_54,
                    "other": row.Other_50_to_54,
                },
                "55_59": {
                    "sputum": row.Sputum_55_to_59,
                    "feces": row.Feces_55_to_59,
                    "urine": row.Urine_55_to_59,
                    "blood": row.Blood_55_to_59,
                    "other": row.Other_55_to_59,
                },
                "60_64": {
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
                "Age_Not_Specified": {
                    "sputum": row.Sputum_Age_Not_Specified,
                    "feces": row.Feces_Age_Not_Specified,
                    "urine": row.Urine_Age_Not_Specified,
                    "blood": row.Blood_Age_Not_Specified,
                    "other": row.Other_Age_Not_Specified,
                },
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Disaggregation": disaggregation,
                "Facility_Type": facility_type,
            }
            for row in data
        ]
        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_types_by_facility_disaggregated_by_age: {str(e)}"
        )


def tested_samples_by_facility_disaggregated_by_drug_type(
    req_args,
):
    """
    This function returns the number of tested samples by facility, disaggregated by drug type.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

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
        base_query = (
            TBMaster.query.with_entities(ColumnNames.label("Facility"), *cases)
            .filter(
                and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    TBMaster.FinalResult.isnot(None),
                    ColumnNames.isnot(None),
                )
            )
            .group_by(ColumnNames)
        )

        query = (
            base_query.filter(
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
            ).group_by(ColumnNames)
            if len(facilities) > 0
            else base_query
        )

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
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Disaggregation": disaggregation,
                "Facility_Type": facility_type,
            }
            for row in data
        ]
        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_by_facility_rifampicin_disaggregated_by_drug_type: {str(e)}"
        )


def tested_samples_by_facility_disaggregated_by_drug_type_by_age(
    req_args,
):
    """
    This function returns the number of tested samples by facility, disaggregated by drug type and age.
    """
    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    drug = req_args.get("drug")

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        drug_column = getattr(TBMaster, drug)

        # Generate all count columns dynamically
        count_columns = [
            create_count_column(
                start, end, state, values, TBMaster, drug_column, gx_result_type
            )
            for (start, end) in TB_AGE_RANGES
            for state, values in TB_RESISTANCE_STATES.items()
        ]

        # Build the base query
        base_query = (
            TBMaster.query.with_entities(ColumnNames.label("Facility"), *count_columns)
            .filter(
                and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    TBMaster.FinalResult.isnot(None),
                    ColumnNames.isnot(None),
                )
            )
            .group_by(ColumnNames)
        )

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
            )
            if len(facilities) > 0
            else base_query
        )

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = query.all()

        response = [
            {
                "Facility": row.Facility,
                "0_4": {
                    "Resistance_Detected": row.Resistance_Detected_0_4,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_0_4,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_0_4,
                },
                "5_9": {
                    "Resistance_Detected": row.Resistance_Detected_5_9,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_5_9,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_5_9,
                },
                "10_14": {
                    "Resistance_Detected": row.Resistance_Detected_10_14,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_10_14,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_10_14,
                },
                "15_19": {
                    "Resistance_Detected": row.Resistance_Detected_15_19,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_15_19,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_15_19,
                },
                "20_24": {
                    "Resistance_Detected": row.Resistance_Detected_20_24,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_20_24,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_20_24,
                },
                "25_29": {
                    "Resistance_Detected": row.Resistance_Detected_25_29,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_25_29,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_25_29,
                },
                "30_34": {
                    "Resistance_Detected": row.Resistance_Detected_30_34,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_30_34,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_30_34,
                },
                "35_39": {
                    "Resistance_Detected": row.Resistance_Detected_35_39,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_35_39,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_35_39,
                },
                "40_44": {
                    "Resistance_Detected": row.Resistance_Detected_40_44,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_40_44,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_40_44,
                },
                "45_49": {
                    "Resistance_Detected": row.Resistance_Detected_45_49,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_45_49,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_45_49,
                },
                "50_54": {
                    "Resistance_Detected": row.Resistance_Detected_50_54,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_50_54,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_50_54,
                },
                "55_59": {
                    "Resistance_Detected": row.Resistance_Detected_55_59,
                    "Resistance_Not_Detected": row.Resistance_Not_Detected_55_59,
                    "Resistance_Indeterminate": row.Resistance_Indeterminate_55_59,
                },
                "60_64": {
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
                "Start_Date": dates[0],
                "End_Date": dates[1],
                "Type_Of_Result": gx_result_type,
                "Disaggregation": disaggregation,
                "Facility_Type": facility_type,
                "Drug": drug,
            }
            for row in data
        ]

        return response

    except Exception as e:
        print(
            f"An error occurred in tested_samples_by_facility_rifampicin_resistance_disaggregated_by_drug_type_by_age: {str(e)}"
        )
