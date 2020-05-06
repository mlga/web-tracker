# -*- coding:utf-8 -*-
from geopy import Point as GeoPoint
from schematics import Model
from schematics.exceptions import ValidationError
from schematics.types import FloatType


def validate_latitude(value):
    try:
        GeoPoint(latitude=value)
    except ValueError as ex:
        raise ValidationError(str(ex))

    return value


def validate_longitude(value):
    try:
        GeoPoint(longitude=value)
    except ValueError as ex:
        raise ValidationError(str(ex))

    return value


class Point(Model):
    """
    Point models way point geolocation information. It provides validation
    of data structure and correctness.
    """
    lat = FloatType(required=True, validators=[validate_latitude])
    lon = FloatType(required=True, validators=[validate_longitude])
