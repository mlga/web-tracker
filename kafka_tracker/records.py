# -*- coding:utf-8 -*-
from datetime import datetime

import faust


class Route(faust.Record):
    # pylint: disable=abstract-method

    routeid: str
    creationtime: int

    @property
    def creation_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.creationtime)


class RoutePoint(faust.Record):
    # pylint: disable=abstract-method

    routeid: str
    tracktime: int
    lat: float
    lon: float

    @property
    def track_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.tracktime)
