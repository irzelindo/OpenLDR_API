from db.database import db


class HFLatLong(db.Model):
    __bind_key__ = "dict"
    __tablename__ = "HFLattLong"
    __table_args__ = {"extend_existing": True}

    FacilityCode = db.Column(db.String(20), primary_key=True)
    FacilityNationalCode = db.Column(db.Integer)
    LattLong = db.Column(db.String(255))
    Latt = db.Column(db.String(255))
    Long = db.Column(db.String(255))
