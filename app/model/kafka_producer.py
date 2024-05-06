# producer.py
import datetime
import json
import typing
import logging
from flag_account import FlagAccount
from transaction import Transaction

from kafka import KafkaProducer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Producer:
    def __init__(self, bootstrap_servers: list, account_topic: str, transaction_topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.account_topic = account_topic
        self.transaction_topic = transaction_topic
        self.producer = self.create()

    def create(self):
        return KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            key_serializer=lambda v: json.dumps(v, default=self.serialize).encode("utf-8"),
            value_serializer=lambda v: json.dumps(v, default=self.serialize).encode("utf-8"),
            api_version=(2, 8, 1),
        )

    def send(self, records: typing.Union[typing.List[FlagAccount], typing.List[Transaction]]):
        for record in records:
            try:
                key = {"account_id": record.account_id}
                topic = self.account_topic
                if hasattr(record, "transaction_id"):
                    key["transaction_id"] = record.transaction_id
                    topic = self.transaction_topic
                self.producer.send(topic=topic, key=key, value=record.asdict())
            except Exception as e:
                raise RuntimeError("fails to send a message") from e
        self.producer.flush()

    def serialize(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return str(obj)
        return obj

