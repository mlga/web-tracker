# -*- coding:utf-8 -*-
from kafka_tracker import records
from kafka_tracker.app import app


# topic for stream of created routes
route_created = app.topic('route.created', value_type=records.Route, partitions=1)

# topic for stream of created way points
routepoint_created = app.topic('routepoint.created', value_type=records.RoutePoint, partitions=1)
