from dict.models.facilities_model import Facilities
from dict.models.hf_lat_long_model import HFLatLong
from utilities.utils import *


def get_all_facilities():
    """
    Get all facilities.

    :return: all facilities in JSON format.
    """

    query = (
        Facilities.query.outerjoin(
            HFLatLong, HFLatLong.FacilityCode == Facilities.FacilityCode
        )
        .with_entities(
            Facilities.FacilityCode.label("FacilityCode"),
            Facilities.FacilityNationalCode.label("FacilityNationalCode"),
            Facilities.FacilityType.label("FacilityType"),
            Facilities.Description.label("Description"),
            Facilities.ProvinceName.label("ProvinceName"),
            Facilities.DistrictName.label("DistrictName"),
            HFLatLong.Latt.label("Latitude"),
            HFLatLong.Long.label("Longitude"),
            Facilities.HFStatus.label("HFStatus"),
        )
        .filter(and_(Facilities.HFStatus == 1, Facilities.FacilityType == "H"))
    )

    # print(query.statement)

    data = query.all()

    data_json = [
        dict(
            FacilityCode=row.FacilityCode,
            FacilityNationalCode=row.FacilityNationalCode,
            FacilityType=row.FacilityType,
            FacilityName=row.Description,
            ProvinceName=row.ProvinceName,
            DistrictName=row.DistrictName,
            Latitude=row.Latitude,
            Longitude=row.Longitude,
            HFStatus=row.HFStatus,
        )
        for row in data
    ]

    return data_json


def get_facilities_by_province(req_args):
    """
    Get all facilities by province.

    :param req_args: contains the province name as an argument.
    :return: all facilities in the given province in JSON format.
    """
    if req_args["province"] is None:
        return get_all_facilities()
    else:
        query = (
            Facilities.query.outerjoin(
                HFLatLong, HFLatLong.FacilityCode == Facilities.FacilityCode
            )
            .with_entities(
                Facilities.FacilityCode.label("FacilityCode"),
                Facilities.FacilityNationalCode.label("FacilityNationalCode"),
                Facilities.FacilityType.label("FacilityType"),
                Facilities.Description.label("Description"),
                Facilities.ProvinceName.label("ProvinceName"),
                Facilities.DistrictName.label("DistrictName"),
                HFLatLong.Latt.label("Latitude"),
                HFLatLong.Long.label("Longitude"),
                Facilities.HFStatus.label("HFStatus"),
            )
            .filter(
                and_(
                    Facilities.HFStatus == 1,
                    Facilities.FacilityType == "H",
                ),
                Facilities.ProvinceName == req_args["province"],
            )
        )

        data = query.all()

        data_json = [
            dict(
                FacilityCode=row.FacilityCode,
                FacilityNationalCode=row.FacilityNationalCode,
                FacilityType=row.FacilityType,
                FacilityName=row.Description,
                ProvinceName=row.ProvinceName,
                DistrictName=row.DistrictName,
                Latitude=row.Latitude,
                Longitude=row.Longitude,
                HFStatus=row.HFStatus,
            )
            for row in data
        ]

        return data_json


def get_facilities_by_district(req_args):
    """
    Get all facilities by district.

    :param req_args: contains the province name and district name as arguments.
    :return: all facilities in the given district in JSON format.
    """
    if req_args["province"] is not None and req_args["district"] is not None:
        query = (
            Facilities.query.outerjoin(
                HFLatLong, HFLatLong.FacilityCode == Facilities.FacilityCode
            )
            .with_entities(
                Facilities.FacilityCode.label("FacilityCode"),
                Facilities.FacilityNationalCode.label("FacilityNationalCode"),
                Facilities.FacilityType.label("FacilityType"),
                Facilities.Description.label("Description"),
                Facilities.ProvinceName.label("ProvinceName"),
                Facilities.DistrictName.label("DistrictName"),
                HFLatLong.Latt.label("Latitude"),
                HFLatLong.Long.label("Longitude"),
                Facilities.HFStatus.label("HFStatus"),
            )
            .filter(
                and_(
                    Facilities.HFStatus == 1,
                    Facilities.FacilityType == "H",
                ),
                Facilities.ProvinceName == req_args["province"],
                Facilities.DistrictName == req_args["district"],
            )
        )

        data = query.all()

        data_json = [
            dict(
                FacilityCode=row.FacilityCode,
                FacilityNationalCode=row.FacilityNationalCode,
                FacilityType=row.FacilityType,
                FacilityName=row.Description,
                ProvinceName=row.ProvinceName,
                DistrictName=row.DistrictName,
                Latitude=row.Latitude,
                Longitude=row.Longitude,
                HFStatus=row.HFStatus,
            )
            for row in data
        ]

        return data_json

    else:
        return get_all_facilities()
