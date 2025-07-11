from sqlalchemy import and_, or_, func, case, literal, text
from datetime import datetime, timedelta
from flask import jsonify

# Get the current date and time
getdate = datetime.now()

# Format the current date as a string in the format "YYYY-MM-DD"
today = getdate.strftime("%Y-%m-%d")

# Calculate the date 366 days ago from the current date and format it as a string
twelve_months_ago = (getdate - timedelta(days=365)).strftime("%Y-%m-%d")


# Lambda function to extract the year from a date and label it as "year"
def YEAR(date_and_time):
    """
    Extract the year from a date and label it as "year"

    Parameters
    ----------
    date_and_time : datetime
        The date and time to extract the year from

    Returns
    -------
    year : int
        The extracted year
    """

    return func.year(date_and_time).label("year")


# Lambda function to extract the month from a date and label it as "month"
def MONTH(date_and_time):
    """
    Extract the month from a date and label it as "month"

    Parameters
    ----------
    date_and_time : datetime
        The date and time to extract the month from

    Returns
    -------
    month : int
        The extracted month
    """

    return func.month(date_and_time)


# Lambda function to extract a specific date part from a date and label it with the given name
def DATE_PART(date_name, date_and_time):
    """
    Extracts a specific date part from a date and labels it with the given name.

    Parameters
    ----------
    date_name : str
        The name of the date part to extract, e.g., "year", "month", "day", "dayofweek", "quarter", etc.
    date_and_time : datetime
        The date from which to extract the part.

    Returns
    -------
    sqlalchemy.sql.expression.Function
        A SQLAlchemy Function object that extracts the given date part from the given date and labels it with the given name.
    """
    return func.datename(text(date_name), date_and_time)


# Lambda function to extract the quarter from a date and label it as "quarter"


def QUARTER(date_and_time):
    """
    Extract the quarter from a date and label it as "quarter"

    Parameters
    ----------
    date_and_time : datetime
        The date and time to extract the quarter from

    Returns
    -------
    quarter : int
        The extracted quarter
    """
    return func.quarter(date_and_time)


# Lambda function to extract the day of the week from a date and label it as "week"


def WEEK(date_and_time):
    """
    Extract the day of the week from a date and label it as "week"

    Parameters
    ----------
    date_and_time : datetime
        The date and time to extract the day of the week from

    Returns
    -------
    week : int
        The extracted day of the week
    """
    return func.dayofweek(date_and_time)


# Lambda function to extract the day from a date and label it as "day"


def DAY(date_and_time):
    """
    Extract the day from a date and label it as "day"

    Parameters
    ----------
    date_and_time : datetime
        The date and time to extract the day from

    Returns
    -------
    day : int
        The extracted day
    """

    return func.day(date_and_time)


# Lambda function to return a statment for Conventional or POC type of laboratory


def LAB_TYPE(TBMaster, lab_type):
    """
    A lambda function to return a statment for Conventional or POC type of laboratory
    based on the RequestID in TBMaster table.

    Parameters
    ----------
    TBMaster : sqlalchemy.ext.declarative.DeclarativeMeta
        The TBMaster table
    lab_type : str
        The type of laboratory to return a statment for

    Returns
    -------
    sqlalchemy.sql.elements.BinaryExpression
        A statement for Conventional or POC type of laboratory
    """
    if lab_type == "Point_Of_Care":
        return func.isnumeric(func.substring(TBMaster.RequestID, 7, 3)) == 1
    elif lab_type == "Conventional":
        return func.isnumeric(func.substring(TBMaster.RequestID, 7, 3)) == 0


# Lambda function to count the total number of rows and label it as "total"
TOTAL_ALL = func.count().label("total")

# Lambda function to count the number of non-null values in a field and label it as "total_not_null"


def TOTAL_NOT_NULL(field):
    """
    A lambda function to count the number of non-null values in a field and label it as "total_not_null"

    Parameters
    ----------
    field : sqlalchemy.sql.elements.ColumnClause
        The field to count the number of non-null values

    Returns
    -------
    sqlalchemy.sql.elements.Label
        A statement with the label "total_not_null"
    """

    return func.count(
        case(
            (
                (
                    or_(
                        field.isnot(None),
                        func.length(field) > 0,
                    ),
                    1,
                )
            ),
            else_=None,
        )
    )


# Lambda function to count the number of null values in a field and label it as "total_null"


def TOTAL_NULL(field):
    """
    A lambda function to count the number of null values in a field and label it as "total_null"

    Parameters
    ----------
    field : sqlalchemy.sql.elements.ColumnClause
        The field to count the number of null values

    Returns
    -------
    sqlalchemy.sql.elements.Label
        A statement with the label "total_null"
    """

    return func.count(
        case(
            (
                (
                    or_(
                        field.is_(None),
                        func.length(field) == 0,
                    ),
                    1,
                )
            ),
            else_=None,
        )
    )


# Lambda function to count the number of values in a field that are in a given list of values and label it as "total_in"


def TOTAL_IN(field, values):
    """
    A lambda function to count the number of values in a field that are in a given list of values and label it as "total_in"

    Parameters
    ----------
    field : sqlalchemy.sql.elements.ColumnClause
        The field to count the number of values
    values : list
        The list of values to count

    Returns
    -------
    sqlalchemy.sql.elements.Label
        A statement with the label "total_in"
    """
    return func.count(
        case(
            (
                (
                    field.in_(values),
                    1,
                )
            ),
            else_=None,
        )
    )


# Lambda function to calculate the average difference in days between two date fields and label it as "date_diff_avg_{field1}_to_{field2}"


def DATE_DIFF_AVG(fields):
    """
    A lambda function to calculate the average difference in days between two date fields and label it as "date_diff_avg_{field1}_to_{field2}"

    Parameters
    ----------
    field1 : sqlalchemy.sql.elements.ColumnClause
        The first date field
    field2 : sqlalchemy.sql.elements.ColumnClause
        The second date field

    Returns
    -------
    sqlalchemy.sql.elements.Label
        A statement with the label "date_diff_avg_{field1}_to_{field2}"
    """

    return func.avg(func.datediff(text("day"), fields[0], fields[1])).label(
        f"date_diff_avg_{fields[0]}_to_{fields[1]}"
    )


# Lambda function to calculate the minimum difference in days between two date fields and label it as "date_diff_min_{field1}_to_{field2}"


def DATE_DIFF_MIN(fields):
    """
    A lambda function to calculate the minimum difference in days between two date fields and label it as "date_diff_min_{field1}_to_{field2}"

    Parameters
    ----------
    field1 : sqlalchemy.sql.elements.ColumnClause
        The first date field
    field2 : sqlalchemy.sql.elements.ColumnClause
        The second date field

    Returns
    -------
    sqlalchemy.sql.elements.Label
        A statement with the label "date_diff_min_{field1}_to_{field2}"
    """
    return func.min(func.datediff(text("day"), fields[0], fields[1])).label(
        f"date_diff_min_{fields[0]}_to_{fields[1]}"
    )


# Lambda function to calculate the maximum difference in days between two date fields and label it as "date_diff_max_{field1}_to_{field2}"


def DATE_DIFF_MAX(fields):
    """
    A lambda function to calculate the maximum difference in days between two date fields and label it as "date_diff_max_{field1}_to_{field2}"

    Parameters
    ----------
    field1 : sqlalchemy.sql.elements.ColumnClause
        The first date field
    field2 : sqlalchemy.sql.elements.ColumnClause
        The second date field

    Returns
    -------
    sqlalchemy.sql.elements.Label
        A statement with the label "date_diff_max_{field1}_to_{field2}"
    """
    return func.max(func.datediff(text("day"), fields[0], fields[1])).label(
        f"date_diff_max_{fields[0]}_to_{fields[1]}"
    )


# Lambda function to count the number of rows where a field matches a given value and label it as "suppression"


def SUPPRESSION(field, value):
    """
    A lambda function to count the number of rows where a field matches a given value and label it as "suppression"

    Parameters
    ----------
    field : sqlalchemy.sql.elements.ColumnClause
        The field to count the number of values
    value : str
        The value to count

    Returns
    -------
    sqlalchemy.sql.elements.Label
        A statement with the label "suppression"
    """
    return func.count(case((field == f"{value}", 1), else_=None))


# Lambda function to count the number of rows where two fields match given values and label it as "gender_suppression"


def GENDER_SUPPRESSION(fields, values):
    """
    A lambda function to count the number of rows where two fields match given values and label it as "gender_suppression"

    Parameters
    ----------
    fields : list
        A list of two sqlalchemy.sql.elements.ColumnClause, the first for the patient's gender and the second for the patient's age
    values : list
        A list of two values to count, the first for the patient's gender and the second for the patient's age

    Returns
    -------
    sqlalchemy.sql.elements.Label
        A statement with the label "gender_suppression"
    """
    return func.count(
        case(((and_(fields[0] == values[0], fields[1] == values[1]), 1)), else_=None)
    )


# List of possible values for the final result that indicate detection
FINAL_RESULT_DETECTED_VALUES = [
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
    "DETECTED",
]


def trl_by_lab_by_days(TBMaster):
    """
    Function to calculate the turnaround time (TAT) by laboratory in days

    Parameters
    ----------
    TBMaster : sqlalchemy.ext.declarative.DeclarativeMeta
        The TBMaster model

    Returns
    -------
    dict
        A dictionary with the following keys and values:
        - colheita_us__recepcao_lab: The turnaround time from specimen collection to reception in the laboratory
        - recepcao_lab__registo_no_lab: The turnaround time from reception in the laboratory to registration
        - registo_no_lab__analise_no_lab: The turnaround time from registration to analysis in the laboratory
        - analise_no_lab__validacao_no_lab: The turnaround time from analysis in the laboratory to validation
    """
    return {
        "colheita_us__recepcao_lab": func.datediff(
            text("DAY"), TBMaster.SpecimenDatetime, TBMaster.ReceivedDateTime
        ),
        "recepcao_lab__registo_no_lab": func.datediff(
            text("DAY"), TBMaster.ReceivedDateTime, TBMaster.RegisteredDateTime
        ),
        "registo_no_lab__analise_no_lab": func.datediff(
            text("DAY"), TBMaster.RegisteredDateTime, TBMaster.AnalysisDateTime
        ),
        "analise_no_lab__validacao_no_lab": func.datediff(
            text("DAY"), TBMaster.AnalysisDateTime, TBMaster.AuthorisedDateTime
        ),
    }


# List of possible values for the final result that indicate non-detection
FINAL_RESULT_NOT_DETECTED_VALUES = [
    "NDET",
    "MTB not detected",
    "Not Detected",
    "Micobacterias Não TB",
]

FINAL_RESULT_INDETERMINATE_VALUES = [
    "MTB Indeterminate",
    "Resistance Indeterminate",
    "RIF Resistance Indeterminate",
]

FINAL_RESULT_ERROR_DETECTED_VALUES = [
    "No Result",
    "Not Applicable",
    "Error",
    "Insufficient sample",
    "Instrument out of order",
    "INS",
]

FINAL_RESULT_INVALID_VALUES = [
    "INVALIDO",
    "Invalid",
    "Not viscous/Watery",
    "Very Viscous",
]

# List of possible values for rifampicin result that indicate non-detection
NOT_DETECTED_VALUES = [
    "MTB not detected",
    "NDET",
    "No Result",
    "NORES",
    "Resistance Not Detected",
    "RIF Resistance Not Detected",
]

# List of possible values for rifampicin result that indicate detection
DETECTED_VALUES = [
    "DET",
    "MTB Detected Medium",
    "Resistance Detected",
    "RIF Resistance Detected",
]

INDETERMINATED_VALUES = [
    "Indeterminate",
    "Resistance Indeterminate",
]

# List of possible values for the sputum specimen source code that indicate TB specimens
TB_SPUTUM_SPECIMEN_SOURCE_CODES = [
    "SPTX",
    "SPTX-L",
    "SPTX-M",
    "SPTX-S",
    "EXP",
    "ESCAR",
    "SAL",
]

# List of possible values for the feces specimen source code that indicate TB specimens
TB_FECES_SPECIMEN_SOURCE_CODES = ["FEC", "FEC-L", "FEC-M", "FEC-S", "FZ", "FF"]

# List of possible values for the urine specimen source code that indicate TB specimens
TB_URINE_SPECIMEN_SOURCE_CODES = ["UR", "UR-L", "UR-M", "UR-S", "U", "SUF", "US"]

# List of possible values for the blood specimen source code that indicate TB specimens
TB_BLOOD_SPECIMEN_SOURCE_CODES = ["BLO", "BLO-L", "BLO-M", "BLO-S", "SA", "SAT"]


# Define age ranges
TB_AGE_RANGES = [
    (0, 4),
    (5, 9),
    (10, 14),
    (15, 19),
    (20, 24),
    (25, 29),
    (30, 34),
    (35, 39),
    (40, 44),
    (45, 49),
    (50, 54),
    (55, 59),
    (60, 64),
    (65, None),
    (None, None),
]

TRL_DAYS = [
    (None, 7),
    (7, 15),
    (16, 21),
    (21, None),
]

# Define resistance states
TB_RESISTANCE_STATES = {
    "Detected": DETECTED_VALUES,
    "Not_Detected": NOT_DETECTED_VALUES,
    "Indeterminate": INDETERMINATED_VALUES,
}

# Define rejection reasons
SPECIMEN_REJECTION_CODES = {
    "INSUFICIENT_SPECIMEN": ["INS"],
    "SPECIMEN_NOT_RECEIVED": ["NSRP", "RSA", "SDBSA", "EMPT"],
    "SPECIMEN_UNSUITABLE_FOR_TESTING": [
        "UNS",
        "DRY",
        "AMCON",
        "SOIL",
        "RECDE",
    ],
    "EQUIPMENT_FAILURE": ["MACH"],
    "REPEAT_SPECIMEN_COLLECTION": ["REPIT", "REJOL", "SPUN2"],
    "SPECIMEN_NOT_LABELED": ["AMONR", "INLS"],
    "LABORATORY_ACIDENT": ["ACC", "PROBT"],
    "MISSING_REAGENT": ["FDR"],
    "DOUBLE_REGISTRATION": ["DUPRG"],
    "TECHNICAL_ERROR": ["ERRTC"],
}

SPECIMEN_REJECTION_CODES_VALUES = {
    "INSUFICIENT_SPECIMEN": ["Insufficient Sample"],
    "SPECIMEN_NOT_RECEIVED": [
        "Unsuitable for testing",
        "Dry Specimen",
        "DBS sem amostra",
        "Empty container received",
    ],
    "SPECIMEN_UNSUITABLE_FOR_TESTING": [
        "Unsuitable Specimen",
        "Dry Specimen",
        "Amostra contaminada com Produt",
        "Soiled Containers",
        "Overfilled container",
    ],
    "EQUIPMENT_FAILURE": ["Machine Breakdown"],
    "REPEAT_SPECIMEN_COLLECTION": [
        "Repeat Collection",
        "Repeat sample collection",
        "please repeat",
    ],
    "SPECIMEN_NOT_LABELED": ["Specimen Not Labelled", "Inadequately labeled samples"],
    "LABORATORY_ACIDENT": ["Laboratory Accident", "Problemas tecnicos no laborato"],
    "MISSING_REAGENT": ["Falts de reagente"],
    "DOUBLE_REGISTRATION": ["Double registration"],
    "TECHNICAL_ERROR": ["Error tecnico"],
}


def generate_drug_cases(TBMaster, drug, gx_result_type):
    """
    Generate SQLAlchemy count expressions for drug resistance cases.

    This function creates three count expressions for a given drug and result type:
    1. Resistance Detected
    2. Resistance Not Detected
    3. Resistance Indeterminate

    Each expression counts the number of records in the TBMaster table where:
    - The TypeOfResult matches the given `gx_result_type`.
    - The specified drug attribute is not None and matches one of the detection values
    (DETECTED_VALUES, NOT_DETECTED_VALUES, or INDETERMINATED_VALUES).

    Args:
        TBMaster: The SQLAlchemy model representing the master table of TB data.
        drug (str): The name of the drug column in the TBMaster table.
        gx_result_type (str): The type of GeneXpert result to filter by.

    Returns:
        list: A list of SQLAlchemy count expressions labeled for each resistance state.
    """

    return [
        func.count(
            case(
                (
                    and_(
                        getattr(TBMaster, drug).isnot(None),
                        getattr(TBMaster, drug).in_(DETECTED_VALUES),
                    ),
                    1,
                )
            )
        ).label(f"{drug}_Resistance_Detected"),
        func.count(
            case(
                (
                    and_(
                        getattr(TBMaster, drug).isnot(None),
                        getattr(TBMaster, drug).in_(NOT_DETECTED_VALUES),
                    ),
                    1,
                )
            )
        ).label(f"{drug}_Resistance_Not_Detected"),
        func.count(
            case(
                (
                    and_(
                        getattr(TBMaster, drug).isnot(None),
                        getattr(TBMaster, drug).in_(INDETERMINATED_VALUES),
                    ),
                    1,
                )
            )
        ).label(f"{drug}_Resistance_Indeterminate"),
    ]


def create_count_column(
    age_start, age_end, state, values, TBMaster, drug_column, gx_result_type
):
    """
    Create a SQLAlchemy column that counts the number of records in a TBMaster query
    that match a given condition.

    Parameters
    ----------
    age_start : int
        The start of the age range to filter by.
    age_end : int or None
        The end of the age range to filter by. If None, the filter is for 65+.
    state : str
        The state of the TB test result (e.g. 'Detected', 'Not_Detected', 'Indeterminate').
    values : list of str
        The values that the drug column should be in.
    TBMaster : sqlalchemy declarative base
        The TBMaster table.
    drug_column : sqlalchemy column
        The column of the drug to filter by.
    gx_result_type : str
        The type of result to filter by (e.g. 'Xpert', 'Ultra').

    Returns
    -------
    sqlalchemy.sql.expression.Function
        A column that can be added to a query that counts the number of records that
        match the condition.
    """

    if age_start is None and age_end is None:
        age_condition = TBMaster.AgeInYears.is_(None)
        label_suffix = "Not_Specified"
    else:
        age_condition = (
            TBMaster.AgeInYears >= age_start
            if age_end is None
            else TBMaster.AgeInYears.between(age_start, age_end)
        )

        label_suffix = (
            f"{age_start}_{age_end}" if age_end is not None else f"{age_start}_plus"
        )

    condition = (
        and_(
            drug_column.in_(values),
            age_condition,
        )
        if drug_column is not None
        else (and_(age_condition))
    )

    return func.count(case({condition: 1}, else_=None)).label(
        f"Resistance_{state}_{label_suffix}"
    )


def GET_COLUMN_NAME(disaggregation, facility_type, Model):
    """
    Get the appropriate column name based on the disaggregation and facility type.

    Parameters
    ----------
    disaggregation : bool
        Whether to disaggregate the data or not.
    facility_type : str
        The type of facility (province, district, or health facility).
    TbMaster : object
        The TbMaster object containing the column names.

    Returns
    -------
    str
        The appropriate column name based on the given parameters.
    """
    if disaggregation is True:
        if facility_type == "province":
            return Model.RequestingDistrictName
        elif facility_type == "district":
            return Model.RequestingFacilityName
        elif facility_type == "health_facility":
            return Model.RequestingFacilityName  # Criar uma query que traz pacientes
        else:
            return Model.RequestingProvinceName
    else:
        if facility_type == "province":
            return Model.RequestingProvinceName
        elif facility_type == "district":
            return Model.RequestingDistrictName
        elif facility_type == "health_facility":
            return Model.RequestingFacilityName
        else:
            return Model.RequestingProvinceName


def PROCESS_COMMON_PARAMS_FACILITY(args):
    """
    Process common parameters used across multiple functions.

    Parameters
    ----------
    args : dict
        The input arguments.

    Returns
    -------
    tuple
        A tuple containing the processed parameters:
        (dates, disaggregation, facility_type, gx_result_type, facilities)
    """
    # Get the interval dates from the input arguments, defaulting to the last 12 months if not provided
    dates = (
        args.get("interval_dates")[0].split(",")
        if args.get("interval_dates") is not None
        else [twelve_months_ago, today]
    )

    # Get the disaggregation value from the input arguments, defaulting to False if not provided
    disaggregation = True if args.get("disaggregation") == "True" else False

    # Get the facility type from the input arguments, defaulting to "province" if not provided
    facility_type = (
        "province"
        if args.get("province")
        and not (args.get("district") or args.get("health_facility"))
        # and not disaggregation
        else (
            "district"
            if args.get("district") and not args.get("health_facility")
            # and not disaggregation
            else (
                "health_facility"
                if args.get("health_facility")
                else args.get("facility_type")
            )
        )
    )

    # Get the health facility from the input arguments, defaulting to None if not provided
    health_facility = (
        args.get("health_facility") if args.get("health_facility") is not None else None
    )
    # Get the GeneXpert result type from the input arguments, defaulting to "Ultra 6 Cores" if not provided
    gx_result_type = (
        args.get("genexpert_result_type") if args.get("genexpert_result_type") else None
    )

    # Get the type of laboratory from the input arguments, defaulting to "Conventional" if not provided
    type_of_laboratory = (
        args.get("type_of_laboratory") if args.get("type_of_laboratory") else "all"
    )

    if args.get("conventional_laboratories") is not None:
        facilities = args["conventional_laboratories"]
    elif args.get("point_of_care_laboratories") is not None:
        facilities = args["point_of_care_laboratories"]
    # Get the facilities based on the input arguments
    elif args.get("province") is not None:
        if args.get("district") is not None:
            # if args.get("health_facility") is not None:
            #     facilities = args["health_facility"]
            # else:
            facilities = args["district"]
        else:
            facilities = args["province"]
    else:
        facilities = []

    return (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        type_of_laboratory,
        health_facility,
    )


def get_patients(
    health_facility, lab, dates, model, indicator, gx_result_type, test_type
):
    """
    Get patients based on the health_facility, lab, and dates.

    Parameters
    ----------
    health_facility : str
        The health_facility to filter by.
    lab : str
        The type of laboratory.
    dates : list
        The list of dates to filter by.
    Model : sqlalchemy.ext.declarative.DeclarativeMeta
        The TBMaster model.

    Returns
    -------
    sqlalchemy.sql.elements.BinaryExpression
        A SQLAlchemy expression to filter patients based on the given parameters.
    """
    filters = [
        model.RequestingFacilityName == health_facility,
        indicator.between(dates[0], dates[1]),
    ]

    if gx_result_type != "All" and gx_result_type is not None:
        filters.append(model.TypeOfResult == gx_result_type)

    patiens = model.query.with_entities(
        model.RequestID,
        model.RequestingProvinceName,
        model.RequestingDistrictName,
        model.RequestingFacilityName,
        model.FacilityNationalCode,
        model.FIRSTNAME,
        model.SURNAME,
        model.AgeInYears,
        model.HL7SexCode,
        model.TELHOME,
        model.FinalResult,
        model.MtbTrace,
        model.Rifampicin,
        model.Fluoroquinolona,
        model.Isoniazid,
        model.Kanamicin,
        model.Amikacina,
        model.Capreomicin,
        model.Ethionamida,
        model.RejectReason,
        model.RejectRemark,
        model.Remarks,
        model.SpecimenDatetime,
        model.RegisteredDateTime,
        model.AnalysisDateTime,
        model.AuthorisedDateTime,
        model.LIMSSpecimenSourceCode,
        model.LIMSSpecimenSourceDesc,
        model.LIMSAnalyzerCode,
        model.TypeOfResult,
    ).filter(*filters)

    return patiens


def process_patients(patiens, dates, facility_type, gx_result_type, test_type):
    """Process the list of patients and return a structured response."""

    response = [
        {
            "request_id": patient.RequestID.strip() if patient.RequestID else None,
            "province": (
                patient.RequestingProvinceName.strip()
                if patient.RequestingProvinceName
                else None
            ),
            "district": (
                patient.RequestingDistrictName.strip()
                if patient.RequestingDistrictName
                else None
            ),
            "health_facility": (
                patient.RequestingFacilityName.strip()
                if patient.RequestingFacilityName
                else None
            ),
            "facility_national_code": patient.FacilityNationalCode,
            "first_name": patient.FIRSTNAME.strip() if patient.FIRSTNAME else None,
            "last_name": patient.SURNAME.strip() if patient.SURNAME else None,
            "age_in_years": patient.AgeInYears,
            "sex_code": patient.HL7SexCode.strip() if patient.HL7SexCode else None,
            "telephone": patient.TELHOME.strip() if patient.TELHOME else None,
            "final_result": patient.FinalResult,
            "mtb_trace": patient.MtbTrace,
            "rifampicin": patient.Rifampicin,
            "fluoroquinolona": patient.Fluoroquinolona,
            "isoniazid": patient.Isoniazid,
            "kanamicin": patient.Kanamicin,
            "amikacina": patient.Amikacina,
            "capreomicin": patient.Capreomicin,
            "ethionamida": patient.Ethionamida,
            "reject_reason": (
                patient.RejectReason.strip() if patient.RejectReason else None
            ),
            "reject_remark": (
                patient.RejectRemark.strip() if patient.RejectRemark else None
            ),
            "remarks": patient.Remarks.strip() if patient.Remarks else None,
            "specimen_datetime": (
                patient.SpecimenDatetime.isoformat()
                if patient.SpecimenDatetime
                else None
            ),
            "registered_datetime": (
                patient.RegisteredDateTime.isoformat()
                if patient.RegisteredDateTime
                else None
            ),
            "analysis_datetime": (
                patient.AnalysisDateTime.isoformat()
                if patient.AnalysisDateTime
                else None
            ),
            "authorised_datetime": (
                patient.AuthorisedDateTime.isoformat()
                if patient.AuthorisedDateTime
                else None
            ),
            "specimen_source_code": (
                patient.LIMSSpecimenSourceCode.strip()
                if patient.LIMSSpecimenSourceCode
                else None
            ),
            "specimen_source_desc": (
                patient.LIMSSpecimenSourceDesc.strip()
                if patient.LIMSSpecimenSourceDesc
                else None
            ),
            "analyzer_code": (
                patient.LIMSAnalyzerCode.strip() if patient.LIMSAnalyzerCode else None
            ),
            "Start_Date": dates[0],
            "End_Date": dates[1],
            "Facility_Type": facility_type,
            "Type_Of_Result": (
                gx_result_type if gx_result_type is not None else patient.TypeOfResult
            ),
        }
        for patient in patiens
    ]

    return response
