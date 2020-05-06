# -*- coding:utf-8 -*-
from datetime import datetime

import faust
from geopy.distance import great_circle

from kafka_tracker import tables, topics, records
from kafka_tracker.app import app


@app.agent(topics.route_created)
async def create_route(
        routes: faust.StreamT[records.Route],
):
    """
    Worker processing `route.created` kafka topic messages.

    It's sole job is to create mapping route -> creation time.
    """
    async for route in routes:
        print(f'Route created. ID: {route.routeid}, creation time: {route.creationtime}')

        tables.route_created_at[route.routeid] = route.creationtime

        yield route.creationtime


async def filter_today(
        points: faust.StreamT[records.RoutePoint],
):
    """
    Filter out points tracked not within the same day as route was created.
    """
    async for point in points:
        route_create_at = tables.route_created_at[point.routeid]

        if route_create_at is None:
            # no information about a route, just accept it
            yield point
            continue

        route_create_at = datetime.fromtimestamp(route_create_at).date()
        point_track_at = point.track_datetime.date()

        if route_create_at != point_track_at:
            print(f'Point tracked at {point_track_at} but route was created at {route_create_at}. Discarding.')
            yield None
            continue

        yield point


@app.agent(topics.routepoint_created)
async def create_route_point(
        points: faust.StreamT[records.RoutePoint],
):
    """
    Worker processing `routepoint.created` kafka topic messages.

    It's job is to calculate route length by consuming consequent route way points.
    Additionally, it maintains the table of longest route per day.
    """
    async for point in filter_today(points):
        if point is None:
            yield None
            continue

        # use current date, not route creation time, this is debatable
        today: str = datetime.utcnow().date().isoformat()

        print(f'Point ({point.lat}, {point.lon}) added to route {point.routeid}')

        # calculate length of a route
        previous_point = tables.route_latest_point[point.routeid]
        current_point = (point.lat, point.lon)

        if previous_point is None:
            tables.route_length[point.routeid] = 0
        else:
            tables.route_length[point.routeid] += great_circle(
                previous_point,
                current_point,
            ).kilometers

        tables.route_latest_point[point.routeid] = current_point

        yield current_point

        # select the longest route today
        current_longest = tables.today_longest_route[today]
        if current_longest is None:
            tables.today_longest_route[today] = point.routeid
        else:
            current_longest_len = tables.route_length[current_longest]
            this_len = tables.route_length[point.routeid]

            if this_len > current_longest_len:
                tables.today_longest_route[today] = point.routeid

        print(f'Current length of route {point.routeid} = {tables.route_length[point.routeid]}')
        print(f'Route {tables.today_longest_route[today]} is currently the longest one for today.')

        yield tables.today_longest_route[today]
