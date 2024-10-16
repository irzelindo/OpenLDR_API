from db.database import db


class Laboratories(db.Model):
    __bind_key__ = "dict"
    __tablename__ = "Laboratories"
    __table_args__ = {"extend_existing": True}

    DateTimeStamp = db.Column(db.DateTime)
    VersionStamp = db.Column(db.String(30))
    LIMSVendorCode = db.Column(db.String(4))
    LabCode = db.Column(db.String(15), primary_key=True)
    FacilityCode = db.Column(db.String(15))
    LabName = db.Column(db.String(50))
    LabType = db.Column(db.String(25))
    StaffingLevel = db.Column(db.String(25))
