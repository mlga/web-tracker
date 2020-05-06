# -*- coding:utf-8 -*-
import time

from kafka import KafkaConsumer

from kafka_tracker.config import load_config


def wait():
    config = load_config()

    while True:
        try:
            time.sleep(5)

            consumer = KafkaConsumer(
                'routepoint.created',
                bootstrap_servers=config.kafka.broker,
            )

            consumer.topics()
        except Exception as ex:
            print('Kafka connection error, retrying.', ex)
        else:
            print('Kafka connection success')
            break


if __name__ == '__main__':
    wait()
