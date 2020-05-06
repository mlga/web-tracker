# -*- coding:utf-8 -*-
import environ


@environ.config(prefix="")
class AppConfig:
    # pylint: disable=too-few-public-methods

    @environ.config
    class Kafka:
        broker = environ.var(name="KAFKA_BROKER")

    kafka = environ.group(Kafka)


def load_config() -> AppConfig:
    return environ.to_config(AppConfig)
