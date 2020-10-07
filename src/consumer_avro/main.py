from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

KAFKA_TOPIC = "topic_test"
consumer = AvroConsumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'python-consumer-avro',
    'auto.offset.reset': 'earliest',
    'schema.registry.url': 'http://localhost:8081'
})

consumer.subscribe([KAFKA_TOPIC])

def consume():
    while True:
        try:
            msg = consumer.poll(100)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            return ("Key:{} Value:{} [partition {}]".format(
                msg.key(),
                msg.value(),
                msg.partition()
            ))
        except KeyboardInterrupt:
            pass
        except SerializerError as ex:
            print("Message deserialization failed for {}: {}".format(msg, ex))
            break

    print("Closing consumer.")
    consumer.close()

if __name__== "__main__":
    print("Starting Python Avro Consumer.")
    print(consume())