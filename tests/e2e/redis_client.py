import json
import typing
from typing import Dict

import redis

from allocation import config

r = redis.Redis(**config.get_redis_host_and_port())


def subscribe_to(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    confirmation = pubsub.get_message(timeout=3)
    confirmation = typing.cast(Dict[str, str], confirmation)
    assert confirmation["type"] == "subscribe"
    return pubsub


def publish_message(channel, message):
    r.publish(channel, json.dumps(message))
