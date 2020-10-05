from time import sleep
import os
import atexit
import random
from multiprocessing import Process 

from confluent_kafka import Producer
from create_topic import Topics

BROKER= "localhost:9092"
DRIVER_FILE_PREFIX = "src/create_producer/drivers/"
DRIVER_ID = os.getenv("DRIVER_ID", f"driver-{random.randint(1,3)}")

# ==== https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md ====
config= {
'bootstrap.servers': BROKER,
"client.id":"driver.producer",
# "statistics.interval.ms":1000,
"api.version.request": True,
"retries":5,  #only relevant if acks !=0
'partitioner': 'random',
'debug': "all",
}

producer = Producer(**config)

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: %s: %s' %(str(msg), str(err)))
    else:
        print('Sent Key:%s Value: %s' %(msg.key().decode(), msg.value().decode()))

def exit_handler():
    print("Flushing producer and exiting.")
    producer.flush()

# ==== https://docs.python.org/3/library/atexit.html====
atexit.register(exit_handler)

def produce_(topic):
    with open(os.path.join(DRIVER_FILE_PREFIX, DRIVER_ID + ".csv")) as f:
        lines = f.readlines()
    try:
        pos = 0
        while True:
            line = lines[pos].strip()
            producer.poll(0) # metadata
            producer.produce(
                topic,
                key= DRIVER_ID,
                value= line,
                callback= delivery_report)
            sleep(1)
            pos = (pos + 1) % len(lines)
            
    except Exception as e:
        print(str(e))
    producer.close()


def main(topic: str, partition: int, replica: int):
    KAFKA_TOPIC = topic
    topic= Topics(BROKER, [KAFKA_TOPIC], partition, replica)
    topic.create_topic()
    print(f"Create topics {KAFKA_TOPIC}")
    print(f"Starting Python producer. {KAFKA_TOPIC}")
    produce_(KAFKA_TOPIC)