from utilities.utils import *
from utilities.utils import PROCESS_COMMON_PARAMS
from hiv.vl.models.vl import VlData


def get_registered_samples_service(req_args):
    """
    Function to get registered samples from the Viral Load database.

    Parameters
    ----------
    req_args : dict
        A dictionary containing the query parameters. The following keys are
        expected:
        - interval_dates: A list of two dates in the format "YYYY-MM-DD". The
          samples registered between these dates will be returned.
        - province: A list of province names to filter by.
        - district: A list of district names to filter by.
        - health_facility: A specific facility name to filter by.
        - facility_type: The type of facility filter. One of "province",
          "district", "health_facility".
        - disaggregation: Whether to disaggregate results.

    Returns
    -------
    list
        A list of dictionaries containing the total number of samples registered
        by month and year, the total number of samples with results, the total
        number of samples without results, the number of samples with suppressed
        viral load, the number of samples with not suppressed viral load, the
        number of male and female samples with and without suppressed viral load.
    """
    dates, facilities, facility_type, disaggregation, health_facility = PROCESS_COMMON_PARAMS(req_args)

    conditions = []
    if facilities:
        if facility_type == "province":
            conditions.append(VlData.RequestingProvinceName.in_(facilities))
        elif facility_type == "district":
            conditions.append(VlData.RequestingDistrictName.in_(facilities))
        else:
            conditions.append(VlData.RequestingFacilityName.in_(facilities))

        # AnalysisDateTime filter condition
        if dates:
            conditions.append(
                VlData.AnalysisDateTime.between(
                    dates[0], dates[1]
                )
            )

        # Query to fetch the data
        query = (
            VlData.query.with_entities(
                YEAR(VlData.AnalysisDateTime),
                MONTH(VlData.AnalysisDateTime),
                DATE_PART("month", VlData.AnalysisDateTime),
                SUPPRESSION(VlData.ViralLoadResultCategory, "Suppressed").label(
                    "suppressed"
                ),
                SUPPRESSION(VlData.ViralLoadResultCategory, "Not Suppressed").label(
                    "not_suppressed"
                ),
                GENDER_SUPPRESSION(
                    [VlData.ViralLoadResultCategory, VlData.HL7SexCode],
                    ["Suppressed", "M"],
                ).label("male_suppressed"),
                GENDER_SUPPRESSION(
                    [VlData.ViralLoadResultCategory, VlData.HL7SexCode],
                    ["Not Suppressed", "M"],
                ).label("male_not_suppressed"),
                GENDER_SUPPRESSION(
                    [VlData.ViralLoadResultCategory, VlData.HL7SexCode],
                    ["Suppressed", "F"],
                ).label("female_suppressed"),
                GENDER_SUPPRESSION(
                    [VlData.ViralLoadResultCategory, VlData.HL7SexCode],
                    ["Not Suppressed", "F"],
                ).label("female_not_suppressed"),
                TOTAL_ALL,
                TOTAL_NOT_NULL(VlData.ViralLoadResultCategory).label("total_not_null"),
                TOTAL_NULL(VlData.ViralLoadResultCategory).label("total_null"),
            )
            .filter(and_(*conditions))
            .group_by(
                YEAR(VlData.AnalysisDateTime),
                MONTH(VlData.AnalysisDateTime),
                DATE_PART("month", VlData.AnalysisDateTime),
            )
            .order_by(
                YEAR(VlData.AnalysisDateTime),
                MONTH(VlData.AnalysisDateTime),
                DATE_PART("month", VlData.AnalysisDateTime),
            )
        )

        # print the data sql statement
        print(query.statement)

        # Execute the query
        data = query.all()

        # Convert the result to JSON format
        data_json = [
            dict(
                year=row.year,
                month=row.month,
                month_name=row.month_name,
                total=row.total,
                total_not_null=row.total_not_null,
                total_null=row.total_null,
                suppressed=row.suppressed,
                not_suppressed=row.not_suppressed,
                male_suppressed=row.male_suppressed,
                male_not_suppressed=row.male_not_suppressed,
                female_suppressed=row.female_suppressed,
                female_not_suppressed=row.female_not_suppressed,
            )
            for row in data
        ]

        return data_json
