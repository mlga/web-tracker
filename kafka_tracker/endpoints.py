# -*- coding:utf-8 -*-
import uuid
from datetime import datetime, date
from json import JSONDecodeError

from faust.web import View, Request
from schematics.exceptions import ValidationError, DataError

from kafka_tracker import tables, records, topics, validators
from kafka_tracker.app import app


@app.page('/route/')
class RouteView(View):

    async def post(self, request: Request):  # pylint: disable=arguments-differ
        route_id = str(uuid.uuid4())
        route_creation_time = datetime.utcnow().timestamp()

        await topics.route_created.send(
            key=route_id,
            value=records.Route(route_id, route_creation_time),
        )

        return self.json({'route_id': route_id}, status=201)


@app.page('/route/{route_id}/way_point/')
class RoutePointView(View):

    async def post(self, request: Request, route_id: str):  # pylint: disable=arguments-differ
        now = datetime.utcnow().timestamp()

        try:
            point = validators.Point(await request.json())
            point.validate()
        except JSONDecodeError as ex:
            return self.json({'json_decode_error': str(ex)}, status=400)
        except (ValidationError, DataError) as ex:
            return self.json(ex.to_primitive(), status=400)
        except:  # pylint: disable=bare-except
            return self.text('', status=500)

        await topics.routepoint_created.send(
            key=route_id,
            value=records.RoutePoint(
                route_id,
                now,
                point.lat,
                point.lon,
            )
        )

        return self.text('', status=201)


@app.page('/route/{route_id}/length/')
class RouteLengthView(View):

    @app.table_route(table=tables.route_length, match_info='route_id')
    async def get(self, request, route_id):  # pylint: disable=arguments-differ
        length = tables.route_length[route_id]

        if length is None:
            raise self.NotFound()

        return self.json({'km': length})


@app.page('/longest_route_of_day/{for_date}/')
class LongestRoute(View):

    @app.table_route(table=tables.today_longest_route, match_info='for_date')
    async def get(self, request, for_date):  # pylint: disable=arguments-differ
        print(f'requesting longest route for {for_date} date')

        try:
            day = date.fromisoformat(for_date)
        except ValueError as ex:
            return self.json({'date_parse_error': str(ex)}, status=400)
        except:  # pylint: disable=bare-except
            return self.text('', status=500)

        today = datetime.utcnow().date()
        if day == today:
            return self.json({'error': 'Cannot request longest route for today.'}, status=400)
        if day > today:
            return self.json({'error': 'Cannot request longest route from the future.'}, status=400)

        route_id = tables.today_longest_route[for_date]

        return self.json({'route_id': route_id})
