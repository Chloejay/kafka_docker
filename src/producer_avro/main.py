from time import sleep
import os
import atexit
import random 

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer


DRIVER_FILE_PREFIX = "./drivers/"
KAFKA_TOPIC = "topic_test"
DRIVER_ID = os.getenv("DRIVER_ID", f"driver-{random.randint(1,3)}")
print("Starting Python Avro producer.")

value_schema = avro.load("position_value.avsc")
key_schema = avro.load("position_key.avsc")

producer = AvroProducer(
    {'bootstrap.servers': 'localhost:9092',
    'partitioner': 'murmur2_random',
    "api.version.request": True,
    'schema.registry.url': 'http://localhost:8081',
    # "debug":"all"
    }, 
    default_key_schema=key_schema, 
    default_value_schema=value_schema)

def exit_handler():
    print("Flushing producer and exiting.")
    producer.flush()

atexit.register(exit_handler)

with open(os.path.join(DRIVER_FILE_PREFIX, DRIVER_ID + ".csv")) as f:
    lines = f.readlines()

pos = 0
while True:
    line = lines[pos]
    producer.poll(0)
    key = {"key" : DRIVER_ID}
    latitude = line.split(",")[0].strip()
    longitude = line.split(",")[1].strip()
    value = {"latitude" : float(latitude), "longitude" : float(longitude)}
    try:
        producer.produce(
            topic=KAFKA_TOPIC,
            value=value,
            key=key,
            callback= lambda err, msg: print("Sent Key:{} Value:{}".format(key, value) if err is None else err),
            )
        sleep(1)
        pos = (pos + 1) % len(lines)
    except Exception as e:
        print(f"Failed to produce message. Error: {e}")
        break


# kafka-avro-console-consumer --bootstrap-server localhost:9092 \
#  --property schema.registry.url=http://localhost:8081 \
#  --topic driver-test --property print.key=true \
#  --from-beginning
