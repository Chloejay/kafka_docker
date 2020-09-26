from time import sleep
import os
import atexit

from confluent_kafka import Producer
from create_topic import Topics 
# set docker for running, what the logic here?

if __name__ == "__main__":
    
    BROKER= "localhost:9092"
    DRIVER_FILE_PREFIX = "./drivers/"
    KAFKA_TOPIC = "tests_001"

    topic= Topics(BROKER, [KAFKA_TOPIC], 6, 1)
    topic.create_topic()
    print(f"Create topics {KAFKA_TOPIC}")

    DRIVER_ID = os.getenv("DRIVER_ID", "driver-3")
    print("Starting Python producer.")

    # https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config= {
    'bootstrap.servers': BROKER,
    "client.id":"driver.producer",
    # "key.serializer": "",
    # "value.serializer":"",
    'plugin.library.paths': 'monitoring-interceptor',
    'partitioner': 'murmur2_random'}

    producer = Producer(**config)

    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: %s: %s' %(str(msg), str(err)))
        else:
            print('Sent Key:%s Value: %s' %(msg.key().decode(), msg.value().decode()))
    
    def exit_handler():
        """Run this on exit"""
        print("Flushing producer and exiting.")
        producer.flush()

    # https://docs.python.org/3/library/atexit.html
    atexit.register(exit_handler)

    with open(os.path.join(DRIVER_FILE_PREFIX, DRIVER_ID + ".csv")) as f:
        lines = f.readlines()

    pos = 0
    while True:
        line = lines[pos].strip()
        producer.poll(0)

        #asynchronous write 
        producer.produce(
            KAFKA_TOPIC,
            key= DRIVER_ID,
            value= line,
            callback= delivery_report)

        sleep(1)
        pos = (pos + 1) % len(lines)

    producer.close()