import time

from app.model.stock import Stock
from confluent_kafka import Producer
from app.utils.kafka_config import KAFKA_CONFIG
import json
import time


# init producer
producer = Producer({
    'bootstrap.servers': KAFKA_CONFIG['bootstrap_servers']
})

index = 1
while True:
    # generate data
    stocks = Stock.create()
    for stock in stocks:
        message = json.dumps(stock.asdict()).encode('utf-8')
        producer.produce('stock', message)
    producer.flush()
    print("Complete batch: " + index.__str__())
    index += 1
    time.sleep(0.1)