from sqlalchemy import and_, or_, func, case, literal, text
from datetime import datetime, timedelta

# Get the current date and time
getdate = datetime.now()

# Format the current date as a string in the format "YYYY-MM-DD"
today = getdate.strftime("%Y-%m-%d")

# Calculate the date 366 days ago from the current date and format it as a string
twelve_months_ago = (getdate - timedelta(days=365)).strftime("%Y-%m-%d")

# Lambda function to extract the year from a date and label it as "year"


def YEAR(date_and_time):
    return func.year(date_and_time).label("year")


# Lambda function to extract the month from a date and label it as "month"


def MONTH(date_and_time):
    return func.month(date_and_time)


# Lambda function to extract a specific date part from a date and label it with the given name


def DATE_PART(date_name, date_and_time):
    return func.datename(text(date_name), date_and_time)


# Lambda function to extract the quarter from a date and label it as "quarter"


def QUARTER(date_and_time):
    return func.quarter(date_and_time)


# Lambda function to extract the day of the week from a date and label it as "week"


def WEEK(date_and_time):
    return func.dayofweek(date_and_time)


# Lambda function to extract the day from a date and label it as "day"


def DAY(date_and_time):
    return func.day(date_and_time)


# Lambda function to return a statment for Conventional or POC type of laboratory


def LAB_TYPE(TBMaster, lab_type):
    if lab_type == "Point_Of_Care":
        return func.isnumeric(func.substring(TBMaster.RequestID, 7, 3)) == 1
    elif lab_type == "Conventional":
        return func.isnumeric(func.substring(TBMaster.RequestID, 7, 3)) == 0


# Lambda function to count the total number of rows and label it as "total"
TOTAL_ALL = func.count().label("total")

# Lambda function to count the number of non-null values in a field and label it as "total_not_null"


def TOTAL_NOT_NULL(field):
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
    return func.avg(func.datediff(text("day"), fields[0], fields[1])).label(
        f"date_diff_avg_{fields[0]}_to_{fields[1]}"
    )


# Lambda function to calculate the minimum difference in days between two date fields and label it as "date_diff_min_{field1}_to_{field2}"


def DATE_DIFF_MIN(fields):
    return func.min(func.datediff(text("day"), fields[0], fields[1])).label(
        f"date_diff_min_{fields[0]}_to_{fields[1]}"
    )


# Lambda function to calculate the maximum difference in days between two date fields and label it as "date_diff_max_{field1}_to_{field2}"


def DATE_DIFF_MAX(fields):
    return func.max(func.datediff(text("day"), fields[0], fields[1])).label(
        f"date_diff_max_{fields[0]}_to_{fields[1]}"
    )


# Lambda function to count the number of rows where a field matches a given value and label it as "suppression"


def SUPPRESSION(field, value):
    return func.count(case((field == f"{value}", 1), else_=None))


# Lambda function to count the number of rows where two fields match given values and label it as "gender_suppression"


def GENDER_SUPPRESSION(fields, values):
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
    "Error",
    "No Result",
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
    return [
        func.count(
            case(
                (
                    and_(
                        TBMaster.TypeOfResult == gx_result_type,
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
                        TBMaster.TypeOfResult == gx_result_type,
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
                        TBMaster.TypeOfResult == gx_result_type,
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

    condition = and_(
        TBMaster.TypeOfResult == gx_result_type,
        drug_column.isnot(None),
        drug_column.in_(values),
        age_condition,
    )
    return func.count(case({condition: 1}, else_=None)).label(
        f"Resistance_{state}_{label_suffix}"
    )


def GET_COLUMN_NAME(disaggregation, facility_type, TbMaster):
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
            return TbMaster.RequestingDistrictName
        elif facility_type == "district":
            return TbMaster.RequestingFacilityName
        elif facility_type == "health_facility":
            return TbMaster.RequestingFacilityName # Criar ume query que traz pacientes
        else:
            return TbMaster.RequestingProvinceName
    else:
        if facility_type == "province":
            return TbMaster.RequestingProvinceName
        elif facility_type == "district":
            return TbMaster.RequestingDistrictName
        elif facility_type == "health_facility":
            return TbMaster.RequestingFacilityName
        else:
            return TbMaster.RequestingProvinceName


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
        args.get("facility_type")
        if args.get("facility_type") is not None
        else "province"
    )

    # Get the GeneXpert result type from the input arguments, defaulting to "Ultra 6 Cores" if not provided
    gx_result_type = (
        args.get("genexpert_result_type")
        if args.get("genexpert_result_type")
        else "Ultra 6 Cores"
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

    return (
        dates,
        disaggregation,
        facility_type,
        gx_result_type,
        facilities,
        type_of_laboratory,
    )
