from db.database import db


class TBMaster(db.Model):
    __bind_key__ = "tb"
    __tablename__ = "TBMaster"
    __table_args__ = {"extend_existing": True}

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RequestID = db.Column(db.String(26), nullable=False)
    OBRSetID = db.Column(db.Integer, nullable=True)
    LIMSPanelCode = db.Column(db.String(10), nullable=True)
    LIMSPanelDesc = db.Column(db.String(100), nullable=True)
    LIMSRejectionCode = db.Column(db.String(10), nullable=True)
    LIMSRejectionDesc = db.Column(db.String(250), nullable=True)
    TypeOfResult = db.Column(db.String(80), nullable=True)
    Gx = db.Column(db.String(80), nullable=True)
    MtbTrace = db.Column(db.String(80), nullable=True)
    Rifampicin = db.Column(db.String(80), nullable=True)
    Fluoroquinolona = db.Column(db.String(80), nullable=True)
    Isoniazid = db.Column(db.String(80), nullable=True)
    Kanamicin = db.Column(db.String(80), nullable=True)
    Amikacina = db.Column(db.String(80), nullable=True)
    Capreomicin = db.Column(db.String(80), nullable=True)
    Ethionamida = db.Column(db.String(80), nullable=True)
    FinalResult = db.Column(db.String(80), nullable=True)
    Comments = db.Column(db.String(250), nullable=True)
    RejectReason = db.Column(db.String(250), nullable=True)
    RejectRemark = db.Column(db.String(250), nullable=True)
    Remarks = db.Column(db.String(250), nullable=True)
    AgeInYears = db.Column(db.Integer, nullable=True)
    AgeInDays = db.Column(db.Integer, nullable=True)
    HL7SexCode = db.Column(db.String(1), nullable=True)
    SpecimenDatetime = db.Column(db.DateTime, nullable=True)
    RegisteredDateTime = db.Column(db.DateTime, nullable=True)
    ReceivedDateTime = db.Column(db.DateTime, nullable=True)
    AnalysisDateTime = db.Column(db.DateTime, nullable=True)
    AuthorisedDateTime = db.Column(db.DateTime, nullable=True)
    AdmitAttendDateTime = db.Column(db.DateTime, nullable=True)
    DateTimeStamp = db.Column(db.DateTime, nullable=True)
    LIMSDateTimeStamp = db.Column(db.DateTime, nullable=True)
    LIMSVersionstamp = db.Column(db.Text, nullable=True)
    GenexpertDate = db.Column(db.String(80), nullable=True)
    Versionstamp = db.Column(db.String(50), nullable=True)
    LOINCPanelCode = db.Column(db.String(10), nullable=True)
    HL7PriorityCode = db.Column(db.String(10), nullable=True)
    CollectionVolume = db.Column(db.Float, nullable=True)
    LIMSFacilityCode = db.Column(db.String(15), nullable=True)
    FacilityNationalCode = db.Column(db.String(15), nullable=True)
    LIMSFacilityName = db.Column(db.String(250), nullable=True)
    LIMSProvinceName = db.Column(db.String(50), nullable=True)
    LIMSDistrictName = db.Column(db.String(50), nullable=True)
    RequestingFacilityCode = db.Column(db.String(50), nullable=True)
    RequestingFacilityName = db.Column(db.String(250), nullable=True)
    RequestingProvinceName = db.Column(db.String(50), nullable=True)
    RequestingDistrictName = db.Column(db.String(250), nullable=True)
    ReceivingFacilityCode = db.Column(db.String(50), nullable=True)
    ReceivingFacilityName = db.Column(db.String(50), nullable=True)
    ReceivingProvinceName = db.Column(db.String(250), nullable=True)
    ReceivingDistrictName = db.Column(db.String(250), nullable=True)
    TestingFacilityCode = db.Column(db.String(50), nullable=True)
    TestingFacilityName = db.Column(db.String(250), nullable=True)
    TestingProvinceName = db.Column(db.String(50), nullable=True)
    TestingDistrictName = db.Column(db.String(250), nullable=True)
    LIMSPointOfCareDesc = db.Column(db.String(50), nullable=True)
    RequestTypeCode = db.Column(db.String(10), nullable=True)
    ICD10ClinicalInfoCodes = db.Column(db.String(50), nullable=True)
    ClinicalInfo = db.Column(db.String(250), nullable=True)
    HL7SpecimenSourceCode = db.Column(db.String(10), nullable=True)
    LIMSSpecimenSourceCode = db.Column(db.String(10), nullable=True)
    LIMSSpecimenSourceDesc = db.Column(db.String(50), nullable=True)
    HL7SpecimenSiteCode = db.Column(db.String(10), nullable=True)
    LIMSSpecimenSiteCode = db.Column(db.String(10), nullable=True)
    LIMSSpecimenSiteDesc = db.Column(db.String(50), nullable=True)
    WorkUnits = db.Column(db.Float, nullable=True)
    CostUnits = db.Column(db.Float, nullable=True)
    HL7SectionCode = db.Column(db.String(10), nullable=True)
    HL7ResultStatusCode = db.Column(db.String(10), nullable=True)
    RegisteredBy = db.Column(db.String(250), nullable=True)
    TestedBy = db.Column(db.String(250), nullable=True)
    AuthorisedBy = db.Column(db.String(250), nullable=True)
    OrderingNotes = db.Column(db.String(250), nullable=True)
    EncryptedPatientID = db.Column(db.String(250), nullable=True)
    HL7EthnicGroupCode = db.Column(db.String(10), nullable=True)
    Deceased = db.Column(db.Boolean, nullable=True)
    Newborn = db.Column(db.Boolean, nullable=True)
    HL7PatientClassCode = db.Column(db.String(10), nullable=True)
    AttendingDoctor = db.Column(db.String(250), nullable=True)
    ReferringRequestID = db.Column(db.String(26), nullable=True)
    Therapy = db.Column(db.String(250), nullable=True)
    LIMSAnalyzerCode = db.Column(db.String(10), nullable=True)
    TargetTimeDays = db.Column(db.Integer, nullable=True)
    TargetTimeMins = db.Column(db.Integer, nullable=True)
    Repeated = db.Column(db.SmallInteger, nullable=True)
    LOCATION = db.Column(db.String(10), nullable=True)
    NATIONALID = db.Column(db.String(50), nullable=True)
    SURNAME = db.Column(db.String(50), nullable=True)
    FIRSTNAME = db.Column(db.String(50), nullable=True)
    DOB = db.Column(db.DateTime, nullable=True)
    DOBType = db.Column(db.String(50), nullable=True)
    HealthcareNo = db.Column(db.String(50), nullable=True)
    TELHOME = db.Column(db.String(50), nullable=True)
    UUID = db.Column(db.String(250), nullable=True)
    EPTS = db.Column(db.String(10), nullable=True)
    EPTS_DATETIME = db.Column(db.DateTime, nullable=True)
    SMS_NOTIFICATION = db.Column(db.String(100), nullable=True)
    SMS_NOTIFICATION_DATETIME = db.Column(db.DateTime, nullable=True)
    PATIENT_NOTIFICATION = db.Column(db.String(100), nullable=True)
    FACILITY_NOTIFICATION = db.Column(db.String(100), nullable=True)
    PATIENT_NOTIFIED_AT = db.Column(db.DateTime, nullable=True)
    FACILITY_NOTIFIED_AT = db.Column(db.DateTime, nullable=True)
    PATIENT_NOTIFICATION_DELIVERY = db.Column(db.String(100), nullable=True)
    FACILITY_NOTIFICATION_DELIVERY = db.Column(db.String(100), nullable=True)
    PATIENT_NOTIFICATION_DELIVERED_AT = db.Column(db.DateTime, nullable=True)
    FACILITY_NOTIFICATION_DELIVERED_AT = db.Column(db.DateTime, nullable=True)
    SMS_ATTEMPTS_TO_FACILITY = db.Column(db.Integer, nullable=True)
    SMS_ATTEMPTS_TO_PATIENT = db.Column(db.Integer, nullable=True)
