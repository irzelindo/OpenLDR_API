from tb.gxpert.models.tb_gx_model import TBMaster
from utilities.utils import *
from sqlalchemy import and_, or_, func, case, literal, text


def registered_samples_by_lab_service(req_args):
    """
    Retrieve the number of registered samples by lab
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    # print(ColumnNames)

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                TBMaster.TestingFacilityName.label("laboratory"),
                TBMaster.TestingFacilityCode.label("laboratory_code"),
                TOTAL_ALL.label("total"),
            ).filter(
                and_(
                    TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.TestingFacilityName.is_not(None),
                ) if lab.lower() == "all" else and_(
                    TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
                    LAB_TYPE(TBMaster, lab),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.TestingFacilityName.is_not(None),
                )
            ).group_by(TBMaster.TestingFacilityName, TBMaster.TestingFacilityCode)
        ) if len(facilities) == 0 else (
            TBMaster.query.with_entities(
                TBMaster.TestingFacilityName.label("laboratory"),
                TBMaster.TestingFacilityCode.label("laboratory_code"),
                TOTAL_ALL.label("total"),
            ).filter(
                and_(
                    TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.TestingFacilityName.is_not(None),
                    TBMaster.TestingFacilityName.in_(facilities),

                ) if lab.lower() == "all" else and_(
                    TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
                    LAB_TYPE(TBMaster, lab),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.TestingFacilityName.is_not(None),
                    TBMaster.TestingFacilityName.in_(facilities),
                )
            ).group_by(TBMaster.TestingFacilityName, TBMaster.TestingFacilityCode)
        )

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Testing_facility": row.laboratory,
                "Testing_facility_code": row.laboratory_code,
                "Resgistered_Samples": row.total,
                "Start_date": dates[0],
                "End_date": dates[1],
                "Type_of_result": gx_result_type,
                "Lab_Type": lab,
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "status": "error",
            "data": [],
            "message": f"An error occurred: {str(e)}",
        }

        return response


def tested_samples_by_lab_service(req_args):
    """
    Retrieve the number of tested samples by lab
    """
    dates, disaggregation, facility_type, gx_result, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                TBMaster.TestingFacilityName.label("laboratory"),
                TBMaster.TestingFacilityCode.label("laboratory_code"),
                TOTAL_ALL.label("total"),
            ).filter(
                and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    TBMaster.TypeOfResult == gx_result,
                    TBMaster.TestingFacilityName.is_not(None),
                ) if lab.lower() == "all" else and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    LAB_TYPE(TBMaster, lab),
                    TBMaster.TypeOfResult == gx_result,
                    TBMaster.TestingFacilityName.is_not(None),
                )
            ).group_by(TBMaster.TestingFacilityName, TBMaster.TestingFacilityCode)
        ) if len(facilities) == 0 else (
            TBMaster.query.with_entities(
                TBMaster.TestingFacilityName.label("laboratory"),
                TBMaster.TestingFacilityCode.label("laboratory_code"),
                TOTAL_ALL.label("total"),
            ).filter(
                and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    TBMaster.TypeOfResult == gx_result,
                    TBMaster.TestingFacilityName.is_not(None),
                    TBMaster.TestingFacilityName.in_(facilities),
                ) if lab.lower() == "all" else and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    LAB_TYPE(TBMaster, lab),
                    TBMaster.TypeOfResult == gx_result,
                    TBMaster.TestingFacilityName.is_not(None),
                    TBMaster.TestingFacilityName.in_(facilities),
                )
            ).group_by(TBMaster.TestingFacilityName, TBMaster.TestingFacilityCode)
        )

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Testing_facility": row.laboratory,
                "Testing_facility_code": row.laboratory_code,
                "Tested_Samples": row.total,
                "Start_date": dates[0],
                "End_date": dates[1],
                "Type_of_result": gx_result,
                "Lab_Type": lab,
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "status": "error",
            "data": [],
            "message": f"An error occurred: {str(e)}",
        }

        return response


def registered_samples_by_lab_service_month(req_args):
    """
    Retrieve the number of registered samples by month
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    # print(ColumnNames)

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                func.MONTH(TBMaster.RegisteredDateTime).label("Month"),
                func.DATENAME(text("month"), TBMaster.RegisteredDateTime).label(
                    "Month_name"),
                # Ensure TOTAL_ALL is correctly defined
                TOTAL_ALL.label("total"),
            ).filter(
                and_(
                    TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.RegisteredDateTime.is_not(None),
                ) if lab.lower() == "all" else and_(
                    TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
                    LAB_TYPE(TBMaster, lab),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.RegisteredDateTime.is_not(None),
                )
            ).group_by(
                # Use the same column as above
                func.MONTH(TBMaster.RegisteredDateTime),
                func.DATENAME(text("month"), TBMaster.RegisteredDateTime)
            ).order_by(
                # Keep consistency with grouping
                func.MONTH(TBMaster.RegisteredDateTime)
            )
        ) if len(facilities) == 0 else (
            TBMaster.query.with_entities(
                func.MONTH(TBMaster.RegisteredDateTime).label("Month"),
                func.DATENAME(text("month"), TBMaster.RegisteredDateTime).label(
                    "Month_name"),
                # Ensure TOTAL_ALL is correctly defined
                TOTAL_ALL.label("total"),
            ).filter(
                and_(
                    TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.RegisteredDateTime.is_not(None),
                    TBMaster.TestingFacilityName.in_(facilities),
                ) if lab.lower() == "all" else and_(
                    TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
                    LAB_TYPE(TBMaster, lab),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.RegisteredDateTime.is_not(None),
                    TBMaster.TestingFacilityName.in_(facilities),
                )
            ).group_by(
                # Use the same column as above
                func.MONTH(TBMaster.RegisteredDateTime),
                func.DATENAME(text("month"), TBMaster.RegisteredDateTime)
            ).order_by(
                # Keep consistency with grouping
                func.MONTH(TBMaster.RegisteredDateTime)
            )
        )

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Month": row.Month,
                "Month_name": row.Month_name,
                "Resgistered_Samples": row.total,
                "Start_date": dates[0],
                "End_date": dates[1],
                "Type_of_result": gx_result_type,
                "Lab_Type": lab,
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "status": "error",
            "data": [],
            "message": f"An error occurred: {str(e)}",
        }

        return response


def tested_samples_by_lab_service_month(req_args):
    """
    Retrieve the number of tested samples by month
    """

    dates, disaggregation, facility_type, gx_result_type, facilities, lab = (
        PROCESS_COMMON_PARAMS_FACILITY(req_args)
    )

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    try:
        # Get the data
        query = (
            TBMaster.query.with_entities(
                func.MONTH(TBMaster.AnalysisDateTime).label("Month"),
                func.DATENAME(text("month"), TBMaster.AnalysisDateTime).label(
                    "Month_name"),
                # Ensure TOTAL_ALL is correctly defined
                TOTAL_ALL.label("total"),
            ).filter(
                and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.AnalysisDateTime.is_not(None),
                ) if lab.lower() == "all" else and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    LAB_TYPE(TBMaster, lab),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.AnalysisDateTime.is_not(None),
                )
            ).group_by(
                # Use the same column as above
                func.MONTH(TBMaster.AnalysisDateTime),
                func.DATENAME(text("month"), TBMaster.AnalysisDateTime)
            ).order_by(
                # Keep consistency with grouping
                func.MONTH(TBMaster.AnalysisDateTime)
            )
        ) if len(facilities) == 0 else (
            TBMaster.query.with_entities(
                func.MONTH(TBMaster.AnalysisDateTime).label("Month"),
                func.DATENAME(text("month"), TBMaster.AnalysisDateTime).label(
                    "Month_name"),
                # Ensure TOTAL_ALL is correctly defined
                TOTAL_ALL.label("total"),
            ).filter(
                and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.AnalysisDateTime.is_not(None),
                    TBMaster.TestingFacilityName.in_(facilities),
                ) if lab.lower() == "all" else and_(
                    TBMaster.AnalysisDateTime.between(dates[0], dates[1]),
                    LAB_TYPE(TBMaster, lab),
                    TBMaster.TypeOfResult == gx_result_type,
                    TBMaster.AnalysisDateTime.is_not(None),
                    TBMaster.TestingFacilityName.in_(facilities),
                )
            ).group_by(
                # Use the same column as above
                func.MONTH(TBMaster.AnalysisDateTime),
                func.DATENAME(text("month"), TBMaster.AnalysisDateTime)
            ).order_by(
                # Keep consistency with grouping
                func.MONTH(TBMaster.AnalysisDateTime)
            )
        )

        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Query the data
        data = query.all()

        # Serialize de data to JSON
        response = [
            {
                "Month": row.Month,
                "Month_name": row.Month_name,
                "Tested_Samples": row.total,
                "Start_date": dates[0],
                "End_date": dates[1],
                "Type_of_result": gx_result_type,
                "Lab_Type": lab,
            }
            for row in data
        ]

        # Return the response
        return response

    except Exception as e:
        # Prepare the error response
        response = {
            "status": "error",
            "data": [],
            "message": f"An error occurred: {str(e)}",
        }

        return response
