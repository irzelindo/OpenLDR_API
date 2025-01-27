from tb.gxpert.models.tb_gx_model import TBMaster
from utilities.utils import *


def registered_samples_by_facility_ultra(args):
    """
    Get the total number of samples registered by facility between two dates.

    Parameters
    ----------
    request : flask.Request
        The request object.
    response : dict
        The response object.

    Returns
    -------
    list
        A list of dictionaries containing the total number of samples registered
        by facility between two dates.

    Notes
    -----
    The query parameters are as follows:

    - dates: A tuple of two dates in the format "YYYY-MM-DD". The samples
        registered between these dates will be returned.
    - facility: A list of facilities to filter by.
    - type: The type of column to retrieve. One of "province", "district", or "facility".
    """
    dates = (
        args.get("interval_dates")[0].split(",")
        if args.get("interval_dates") is not None
        else [twelve_months_ago, today]
    )

    disaggregation = True if args.get("disaggregation") == "True" else False

    # print(disaggregation)

    facility_type = (
        args.get("facility_type")
        if args.get("facility_type") is not None
        else "province"
    )

    gx_result_type = (
        args.get("genexpert_result_type")
        if args.get("genexpert_result_type")
        else "Ultra 6 Cores"
    )

    if args.get("province") is not None:
        if args.get("district") is not None:
            if args.get("health_facility") is not None:
                facilities = (
                    args["province"] + args["district"] + args["health_facility"]
                )
            else:
                facilities = args["province"] + args["district"]
        else:
            facilities = args["province"]
    else:
        facilities = []

    # print(dates)
    # print(disaggregation)
    # print(facilities)

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    # print(ColumnNames)

    try:

        query = (
            (
                TBMaster.query.with_entities(
                    ColumnNames.label("Facility"),
                    TOTAL_ALL.label("TotalSamples"),
                )
                .filter(
                    and_(
                        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
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
                        TBMaster.RegisteredDateTime.between(dates[0], dates[1]),
                        TBMaster.TypeOfResult == gx_result_type,
                        ColumnNames.isnot(None),
                    )
                )
                .group_by(ColumnNames)
            )
        )

        # print(query)

        data = query.all()

        # # print(data)

        response = [
            dict(
                Facility=row.Facility,
                RegisteredSamples=row.TotalSamples,
                StartDate=dates[0],
                EndDate=dates[1],
                Disaggregation=disaggregation,
                FacilityType=facility_type,
                TypeOfResult=gx_result_type,
            )
            for row in data
        ]

        # print(response)

        return response

    except Exception as e:
        print(e)


def tested_samples_by_facility_ultra(args):
    """
    Get the total number of samples tested by facility between two dates.

    Parameters
    ----------
    request : flask.Request
        The request object.
    response : dict
        The response object.

    Returns
    -------
    list
        A list of dictionaries containing the total number of samples tested
        by facility between two dates.

    Notes
    -----
    The query parameters are as follows:

    - dates: A tuple of two dates in the format "YYYY-MM-DD". The samples
        tested between these dates will be returned.
    - facility: A list of facilities to filter by.
    - type: The type of column to retrieve. One of "province", "district", or "facility".
    """
    dates = (
        args.get("interval_dates")[0].split(",")
        if args.get("interval_dates") is not None
        else [twelve_months_ago, today]
    )

    disaggregation = True if args.get("disaggregation") == "True" else False

    # print(disaggregation)

    facility_type = (
        args.get("facility_type")
        if args.get("facility_type") is not None
        else "province"
    )

    gx_result_type = (
        args.get("genexpert_result_type")
        if args.get("genexpert_result_type")
        else "Ultra 6 Cores"
    )

    if args.get("province") is not None:
        if args.get("district") is not None:
            if args.get("health_facility") is not None:
                facilities = (
                    args["province"] + args["district"] + args["health_facility"]
                )
            else:
                facilities = args["province"] + args["district"]
        else:
            facilities = args["province"] = args["province"]
    else:
        facilities = []

    # print(dates)
    # print(disaggregation)
    # print(facilities)

    ColumnNames = GET_COLUMN_NAME(disaggregation, facility_type, TBMaster)

    # print(ColumnNames)

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

        # print(query)

        data = query.all()

        # # print(data)

        response = [
            dict(
                Facility=row.Facility,
                TestedSamples=row.TotalSamples,
                StartDate=dates[0],
                EndDate=dates[1],
                TypeOfResult=gx_result_type,
                Disaggregation=disaggregation,
                FacilityType=facility_type,
            )
            for row in data
        ]

        # print(response)

        return response

    except Exception as e:
        print(e)
