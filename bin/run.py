# -*- coding:utf-8 -*-
from kafka_tracker.app import app


if __name__ == '__main__':
    app.conf.autodiscover = [
        'kafka_tracker.endpoints',
        'kafka_tracker.agents',
        'kafka_tracker.tables',
        'kafka_tracker.topics',
    ]

    app.main()
