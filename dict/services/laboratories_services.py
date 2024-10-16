from dict.models.laboratories_model import Laboratories
from dict.models.facilities_model import Facilities
from dict.models.hf_lat_long_model import HFLatLong
from utilities.utils import *


def get_all_laboratories(req_args):
    """
    Get all laboratories.

    :param req_args: contains the laboratory type as an argument.
    :return: all laboratories in JSON format.
    """

    if req_args["lab_type"] is not None:
        query = (
            Laboratories.query.outerjoin(
                HFLatLong, HFLatLong.FacilityCode == Laboratories.LabCode
            )
            .join(Facilities, Laboratories.LabCode == Facilities.FacilityCode)
            .with_entities(
                Laboratories.LabCode.label("LabCode"),
                Laboratories.LabName.label("LabName"),
                Laboratories.LabType.label("LabType"),
                HFLatLong.Latt.label("Latitude"),
                HFLatLong.Long.label("Longitude"),
            )
            .filter(
                Laboratories.LabType == req_args["lab_type"], Facilities.HFStatus == 1
            )
        )
    else:
        query = (
            Laboratories.query.outerjoin(
                HFLatLong, HFLatLong.FacilityCode == Laboratories.LabCode
            )
            .join(Facilities, Laboratories.LabCode == Facilities.FacilityCode)
            .with_entities(
                Laboratories.LabCode.label("LabCode"),
                Laboratories.LabName.label("LabName"),
                Laboratories.LabType.label("LabType"),
                HFLatLong.Latt.label("Latitude"),
                HFLatLong.Long.label("Longitude"),
            )
            .filter(Facilities.HFStatus == 1)
        )

    data = query.all()

    data_json = [
        dict(
            LabCode=row.LabCode,
            LabName=row.LabName,
            LabType=row.LabType,
            Latitude=row.Latitude,
            Longitude=row.Longitude,
        )
        for row in data
    ]

    return data_json


def get_laboratories_by_province(req_args):
    """
    Get all laboratories by province.

    :param req_args: contains the province name and the laboratory type as arguments.
    :return: all laboratories in the given province in JSON format.
    """

    if req_args["province"] is not None and req_args["lab_type"] is not None:
        query = (
            Laboratories.query.join(
                Facilities, Laboratories.LabCode == Facilities.FacilityCode
            )
            .outerjoin(HFLatLong, HFLatLong.FacilityCode == Laboratories.LabCode)
            .with_entities(
                Laboratories.LabCode.label("LabCode"),
                Laboratories.LabName.label("LabName"),
                Laboratories.LabType.label("LabType"),
                Facilities.CountryName.label("CountryName"),
                Facilities.ProvinceName.label("ProvinceName"),
                Facilities.DistrictName.label("DistrictName"),
                HFLatLong.Latt.label("Latitude"),
                HFLatLong.Long.label("Longitude"),
                Facilities.FacilityType.label("FacilityType"),
                Facilities.HFStatus.label("HFStatus"),
            )
            .filter(
                Facilities.ProvinceName == req_args["province"],
                Facilities.HFStatus == 1,
                Laboratories.LabType == req_args["lab_type"],
            )
        )
        data = query.all()
        data_json = [
            dict(
                LabCode=row.LabCode,
                LabName=row.LabName,
                LabType=row.LabType,
                CountryName=row.CountryName,
                ProvinceName=row.ProvinceName,
                DistrictName=row.DistrictName,
                Latitude=row.Latitude,
                Longitude=row.Longitude,
                FacilityType=row.FacilityType,
                HFStatus=row.HFStatus,
            )
            for row in data
        ]

        return data_json
    elif req_args["lab_type"] is None:
        query = (
            Laboratories.query.join(
                Facilities, Laboratories.LabCode == Facilities.FacilityCode
            )
            .outerjoin(HFLatLong, HFLatLong.FacilityCode == Laboratories.LabCode)
            .with_entities(
                Laboratories.LabCode.label("LabCode"),
                Laboratories.LabName.label("LabName"),
                Laboratories.LabType.label("LabType"),
                Facilities.CountryName.label("CountryName"),
                Facilities.ProvinceName.label("ProvinceName"),
                HFLatLong.Latt.label("Latitude"),
                HFLatLong.Long.label("Longitude"),
                Facilities.DistrictName.label("DistrictName"),
                Facilities.FacilityType.label("FacilityType"),
                Facilities.HFStatus.label("HFStatus"),
            )
            .filter(
                Facilities.ProvinceName == req_args["province"],
                Facilities.HFStatus == 1,
            )
        )
        data = query.all()
        data_json = [
            dict(
                LabCode=row.LabCode,
                LabName=row.LabName,
                LabType=row.LabType,
                CountryName=row.CountryName,
                ProvinceName=row.ProvinceName,
                DistrictName=row.DistrictName,
                Latitude=row.Latitude,
                Longitude=row.Longitude,
                FacilityType=row.FacilityType,
                HFStatus=row.HFStatus,
            )
            for row in data
        ]

        return data_json
    else:
        return get_all_laboratories(req_args)


def get_laboratories_by_district(req_args):
    """
    Get all laboratories by district.

    :param req_args: a dictionary containing the query parameters. The following
        keys are expected:
        - province: province name.
        - district: district name.
        - lab_type: laboratory type.
    :return: a list of dictionaries representing the laboratories in the given
        district in JSON format.
    """
    if (
        req_args["province"] is not None
        and req_args["district"] is not None
        and req_args["lab_type"] is not None
    ):
        query = (
            Laboratories.query.join(
                Facilities, Laboratories.LabCode == Facilities.FacilityCode
            )
            .outerjoin(HFLatLong, HFLatLong.FacilityCode == Laboratories.LabCode)
            .with_entities(
                Laboratories.LabCode.label("LabCode"),
                Laboratories.LabName.label("LabName"),
                Laboratories.LabType.label("LabType"),
                Facilities.CountryName.label("CountryName"),
                Facilities.ProvinceName.label("ProvinceName"),
                Facilities.DistrictName.label("DistrictName"),
                HFLatLong.Latt.label("Latitude"),
                HFLatLong.Long.label("Longitude"),
                Facilities.FacilityType.label("FacilityType"),
                Facilities.HFStatus.label("HFStatus"),
            )
            .filter(
                Facilities.ProvinceName == req_args["province"],
                Facilities.DistrictName == req_args["district"],
                Facilities.HFStatus == 1,
                Laboratories.LabType == req_args["lab_type"],
            )
        )
        data = query.all()

        data_json = [
            dict(
                LabCode=row.LabCode,
                LabName=row.LabName,
                LabType=row.LabType,
                CountryName=row.CountryName,
                ProvinceName=row.ProvinceName,
                DistrictName=row.DistrictName,
                Latitude=row.Latitude,
                Longitude=row.Longitude,
                FacilityType=row.FacilityType,
                HFStatus=row.HFStatus,
            )
            for row in data
        ]

        return data_json

    elif req_args["lab_type"] is None:
        query = (
            Laboratories.query.join(
                Facilities, Laboratories.LabCode == Facilities.FacilityCode
            )
            .outerjoin(HFLatLong, HFLatLong.FacilityCode == Laboratories.LabCode)
            .with_entities(
                Laboratories.LabCode.label("LabCode"),
                Laboratories.LabName.label("LabName"),
                Laboratories.LabType.label("LabType"),
                Facilities.CountryName.label("CountryName"),
                Facilities.ProvinceName.label("ProvinceName"),
                Facilities.DistrictName.label("DistrictName"),
                HFLatLong.Latt.label("Latitude"),
                HFLatLong.Long.label("Longitude"),
                Facilities.FacilityType.label("FacilityType"),
                Facilities.HFStatus.label("HFStatus"),
            )
            .filter(
                Facilities.ProvinceName == req_args["province"],
                Facilities.DistrictName == req_args["district"],
                Facilities.HFStatus == 1,
            )
        )
        data = query.all()

        data_json = [
            dict(
                LabCode=row.LabCode,
                LabName=row.LabName,
                LabType=row.LabType,
                CountryName=row.CountryName,
                ProvinceName=row.ProvinceName,
                DistrictName=row.DistrictName,
                Latitude=row.Latitude,
                Longitude=row.Longitude,
                FacilityType=row.FacilityType,
                HFStatus=row.HFStatus,
            )
            for row in data
        ]

        return data_json
    else:
        return get_all_laboratories(req_args)
