from time import sleep
import os
import atexit

from confluent_kafka import Producer
from create_topic import Topics


if __name__ == "__main__":
    BROKER= "localhost:9092"
    DRIVER_FILE_PREFIX = "./drivers/"
    KAFKA_TOPIC = "topic_b"

    topic= Topics(BROKER, [KAFKA_TOPIC], 6, 1)
    topic.create_topic()
    print(f"Create topics {KAFKA_TOPIC}")

    DRIVER_ID = os.getenv("DRIVER_ID", "driver-3")
    print("Starting Python producer.")

    # https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config= {
    'bootstrap.servers': BROKER,
    "client.id":"driver.producer",
    # 'plugin.library.paths': 'monitoring-interceptor',
    # "statistics.interval.ms":1000,
    "api.version.request": True,
    "retries":5, #only relevant if acks !=0
    'partitioner': 'random',
    'debug': 'admin,broker, metadata', #all
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

    # https://docs.python.org/3/library/atexit.html
    atexit.register(exit_handler)

    with open(os.path.join(DRIVER_FILE_PREFIX, DRIVER_ID + ".csv")) as f:
        lines = f.readlines()
    try:
        pos = 0
        while True:
            line = lines[pos].strip()
            producer.poll(0) #receive metadata from broker

            #asynchronous
            producer.produce(
                KAFKA_TOPIC,
                key= DRIVER_ID,
                value= line,
                callback= delivery_report)
            sleep(1)
            pos = (pos + 1) % len(lines)
    except Exception as e:
        print(str(e))
    finally:
        producer.close()