# -*- coding:utf-8 -*-
from typing import Tuple

from faust.types import TableT

from kafka_tracker.app import app


# map route ID to its creation time
route_created_at: TableT[str, int] = app.Table(
    'route_created_at',
    default=lambda: None,
    partitions=1,
)

# map route ID to its latest way point
route_latest_point: TableT[str, Tuple[int, int]] = app.Table(
    'route_latest_point',
    default=lambda: None,
    partitions=1,
)

# map route ID to its current length
route_length: TableT[str, int] = app.Table(
    'route_length',
    default=lambda: None,
    partitions=1,
)

# map date in ISO format (2020-01-01) to ID of longest route that day
today_longest_route: TableT[str, str] = app.Table(
    'today_longest_route',
    default=lambda: None,
    partitions=1,
)
