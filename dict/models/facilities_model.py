from db.database import db


class Facilities(db.Model):
    __bind_key__ = "dict"
    __tablename__ = "viewFacilities"
    __table_args__ = {"extend_existing": True}

    DateTimeStamp = db.Column(db.DateTime)
    VersionStamp = db.Column(db.String(30))
    FacilityCode = db.Column(db.String(15), primary_key=True)
    Description = db.Column(db.String(50))
    FacilityType = db.Column(db.String(3))
    CountryCode = db.Column(db.String(2))
    ProvinceCode = db.Column(db.String(4))
    RegionCode = db.Column(db.String(4))
    DistrictCode = db.Column(db.String(4))
    SubDistrictCode = db.Column(db.String(4))
    LattLong = db.Column(db.Text)  # Using Text to represent geography type
    HFStatus = db.Column(db.Integer)
    HealthCareID = db.Column(db.String(30))
    FacilityNationalCode = db.Column(db.String(15))
    HealthcareCountryCode = db.Column(db.String(2))
    HealthcareProvinceCode = db.Column(db.String(2052), nullable=False)
    HealthcareDistrictCode = db.Column(db.String(4104), nullable=False)
    CountryName = db.Column(db.String(50))
    CountryLattLong = db.Column(db.Text)  # Using Text to represent geography type
    ProvinceName = db.Column(db.String(50))
    ProvinceLattLong = db.Column(db.Text)  # Using Text to represent geography type
    DistrictName = db.Column(db.String(50))
    DistrictLattLong = db.Column(db.Text)  # Using Text to represent geography type
