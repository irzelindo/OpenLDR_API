from db.database import db


class EIDMaster(db.Model):
    __bind_key__ = "dpi"
    __tablename__ = "EIDMaster"
    __table_args__ = {"extend_existing": True}

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RequestID = db.Column(db.String(26), nullable=True)

    # Patient demographics
    SURNAME = db.Column(db.String(100), nullable=True)
    FIRSTNAME = db.Column(db.String(100), nullable=True)
    DOB = db.Column(db.DateTime, nullable=True)
    AgeInYears = db.Column(db.Integer, nullable=True)
    AgeInDays = db.Column(db.Integer, nullable=True)
    HL7SexCode = db.Column(db.String(10), nullable=True)
    NATIONALID = db.Column(db.String(50), nullable=True)
    NATIONALITY = db.Column(db.String(50), nullable=True)

    # Clinical info
    ClinicalInfo = db.Column(db.String(500), nullable=True)
    RapidHivTest = db.Column(db.String(50), nullable=True)
    PcrPreviouslyDone = db.Column(db.String(50), nullable=True)
    PtvChild = db.Column(db.String(50), nullable=True)
    PtvMother = db.Column(db.String(50), nullable=True)
    BreastfeedingInfo = db.Column(db.String(50), nullable=True)

    # Specimen
    SpecimenDatetime = db.Column(db.DateTime, nullable=True)
    LIMSSpecimenSourceCode = db.Column(db.String(20), nullable=True)
    LIMSSpecimenSourceDesc = db.Column(db.String(200), nullable=True)
    CollectionVolume = db.Column(db.String(50), nullable=True)

    # Results
    PCR_Result = db.Column(db.String(100), nullable=True)
    POC_Result = db.Column(db.String(100), nullable=True)
    Viral_Load_Result = db.Column(db.String(100), nullable=True)
    CAPCTM = db.Column(db.String(100), nullable=True)
    LogValue = db.Column(db.String(50), nullable=True)
    IsPoc = db.Column(db.String(10), nullable=True)
    HL7ResultStatusCode = db.Column(db.String(10), nullable=True)

    # Rejection
    LIMSRejectionCode = db.Column(db.String(20), nullable=True)
    LIMSRejectionDesc = db.Column(db.String(200), nullable=True)
    ResultLIMSRejectionCode = db.Column(db.String(20), nullable=True)
    ResultLIMSRejectionDesc = db.Column(db.String(200), nullable=True)

    # Requesting facility
    RequestingFacilityCode = db.Column(db.String(50), nullable=True)
    RequestingFacilityName = db.Column(db.String(200), nullable=True)
    RequestingProvinceName = db.Column(db.String(100), nullable=True)
    RequestingDistrictName = db.Column(db.String(100), nullable=True)
    RequestingLatitude = db.Column(db.String(50), nullable=True)
    RequestingLongitude = db.Column(db.String(50), nullable=True)

    # Receiving facility
    ReceivingFacilityCode = db.Column(db.String(50), nullable=True)
    ReceivingFacilityName = db.Column(db.String(200), nullable=True)
    ReceivingProvinceName = db.Column(db.String(100), nullable=True)
    ReceivingDistrictName = db.Column(db.String(100), nullable=True)

    # Testing facility
    TestingFacilityCode = db.Column(db.String(50), nullable=True)
    TestingFacilityName = db.Column(db.String(200), nullable=True)
    TestingProvinceName = db.Column(db.String(100), nullable=True)
    TestingDistrictName = db.Column(db.String(100), nullable=True)
    TestingLatitude = db.Column(db.String(50), nullable=True)
    TestingLongitude = db.Column(db.String(50), nullable=True)

    # LIMS facility
    LIMSFacilityCode = db.Column(db.String(50), nullable=True)
    LIMSFacilityName = db.Column(db.String(200), nullable=True)

    # Result-prefixed columns (used in EID queries)
    ResultRequestingFacilityName = db.Column(db.String(200), nullable=True)
    ResultRequestingProvinceName = db.Column(db.String(100), nullable=True)
    ResultRequestingDistrictName = db.Column(db.String(100), nullable=True)
    ResultRequestingFacilityCode = db.Column(db.String(50), nullable=True)
    ResultTestingFacilityCode = db.Column(db.String(50), nullable=True)
    ResultTestingFacilityName = db.Column(db.String(200), nullable=True)
    ResultTestingProvinceName = db.Column(db.String(100), nullable=True)
    ResultTestingDistrictName = db.Column(db.String(100), nullable=True)
    ResultSpecimenDatetime = db.Column(db.DateTime, nullable=True)
    ResultRegisteredDateTime = db.Column(db.DateTime, nullable=True)
    ResultReceivedDatetime = db.Column(db.DateTime, nullable=True)
    ResultAnalysisDateTime = db.Column(db.DateTime, nullable=True)
    ResultAuthorisedDateTime = db.Column(db.DateTime, nullable=True)
    ResultLIMSAnalyzerCode = db.Column(db.String(50), nullable=True)
    ResultLIMSAnalyzerName = db.Column(db.String(100), nullable=True)

    # Timeline dates
    RegisteredDateTime = db.Column(db.DateTime, nullable=True)
    ReceivedDateTime = db.Column(db.DateTime, nullable=True)
    AnalysisDateTime = db.Column(db.DateTime, nullable=True)
    AuthorisedDateTime = db.Column(db.DateTime, nullable=True)

    # Hub/Pre-registration
    LIMSPreReg_ReceivedDateTime = db.Column(db.DateTime, nullable=True)
    LIMSPreReg_RegistrationDateTime = db.Column(db.DateTime, nullable=True)
    LIMSPreReg_RegistrationFacilityCode = db.Column(db.String(50), nullable=True)
    HubLatitude = db.Column(db.String(50), nullable=True)
    HubLongitude = db.Column(db.String(50), nullable=True)

    # DISA flags
    IS_DISALINK = db.Column(db.String(10), nullable=True)
    IS_DISAPOC = db.Column(db.String(10), nullable=True)
