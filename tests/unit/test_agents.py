# -*- coding:utf-8 -*-
import pytest
from unittest.mock import patch

from kafka_tracker import agents, records, tables


@pytest.mark.asyncio
async def test_process_route():
    """
    Test that new route is correctly stored in table.
    """
    async with agents.create_route.test_context() as agent:
        order = records.Route(routeid='aaa1', creationtime=12)
        await agent.put(order)

        assert tables.route_created_at['aaa1'] == 12


@pytest.mark.asyncio
async def test_process_routepoint():
    """
    Test that way points are correctly stored in route last point table and
    in route length.
    """
    async with agents.create_route_point.test_context() as agent:
        for point in [
            records.RoutePoint(routeid='aaa2', tracktime=12, lat=-25.4025905, lon=-49.3124416),
            records.RoutePoint(routeid='aaa2', tracktime=13, lat=-23.559798, lon=-46.634971),
            records.RoutePoint(routeid='aaa2', tracktime=14, lat=59.3258414, lon=17.70188),
            records.RoutePoint(routeid='aaa2', tracktime=15, lat=54.273901, lon=18.591889),
        ]:
            await agent.put(point)

        assert tables.route_latest_point['aaa2'] == (54.273901, 18.591889)
        assert 11750 < tables.route_length['aaa2'] < 11900


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'route_created_at,point_tracked_at',
    [
        (1577793345, 1577879745),  # track point from the future
        (1577879745, 1577793345),  # track point from the past
    ]
)
async def test_process_routepoint__too_old(route_created_at, point_tracked_at):
    """
    Test that way points are not tracked when too old.
    """
    with patch('kafka_tracker.agents.tables.route_created_at') as mocked_table:
        mocked_table.__getitem__.return_value = route_created_at

        async with agents.create_route_point.test_context() as agent:
            for point in [
                records.RoutePoint(routeid='aaa3', tracktime=point_tracked_at, lat=-25.4025905, lon=-49.3124416),
            ]:
                await agent.put(point)

            assert tables.route_latest_point['aaa3'] is None
            assert tables.route_length['aaa3'] is None
