# -*- coding:utf-8 -*-
import faust
from kafka_tracker.config import load_config


config = load_config()
app = faust.App('tracker-app', broker=config.kafka.broker)
app.conf.autodiscover = [
    'kafka_tracker.endpoints',
    'kafka_tracker.agents',
    'kafka_tracker.tables',
    'kafka_tracker.topics',
]
