# -*- coding:utf-8 -*-
import pytest
from schematics.exceptions import DataError

from kafka_tracker.validators import Point


@pytest.mark.parametrize(
    'lat,lon',
    [
        (0.0, 0.0),
        (90.0, 180.0),
        (45.0, 235.0),
        (12.0, 14.5),
    ]
)
def test_point__ok(lat, lon):
    point = Point({'lat': lat, 'lon': lon})
    point.validate()

    assert point.lat == lat
    assert point.lon == lon

    point = Point({'lat': -1 * lat, 'lon': lon})
    point.validate()

    assert point.lat == -1 * lat
    assert point.lon == lon


@pytest.mark.parametrize(
    'lat,lon',
    [
        (180.0, 180.0),
        (91.0, 235.0),
        ('xxx', 12),
        (12, 'xxx'),
    ]
)
def test_point__invalid(lat, lon):
    with pytest.raises(DataError):
        point = Point({'lat': lat, 'lon': lon})
        point.validate()
