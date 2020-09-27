# use another kafka-python library which has more parameter configs
from kafka import KafkaProducer

from time import sleep 
import os
from json import dumps

broker= "localhost:9092"
topic= "test_kafka"
DRIVER_FILE_PREFIX = "./drivers/"

config={
    'bootstrap_servers': [broker],
    "client_id":"driver.producer",
    # "key_serializer": "",
    "value_serializer":lambda x: dumps(x).encode('utf-8'),
    "acks":1,
    # "compression_type":"snappy",
    "retries":"5",
    # "batch_size":,
    # "partitioner":,
    # "connections_max_idle_ms":,
    "max_in_flight_requests_per_connection":1
    }

producer= KafkaProducer(**config)

def write():
    for i in os.listdir(DRIVER_FILE_PREFIX):
        lines= []
        with open(os.path.join(DRIVER_FILE_PREFIX, i)) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                producer.send(topic, value= f"value is {line}",)
            sleep(1)

write()

producer.close()
