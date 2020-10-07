"Python Avro Consumer"
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

KAFKA_TOPIC = "topic_test"

print("Starting Python Avro Consumer.")
consumer = AvroConsumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'python-consumer-avro',
    'auto.offset.reset': 'earliest',
    'schema.registry.url': 'http://localhost:8081'
})

consumer.subscribe([KAFKA_TOPIC])

try:
    while True:
        try:
            msg = consumer.poll(1.0)
        except SerializerError as ex:
            print("Message deserialization failed for {}: {}".format(msg, ex))
            break

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        print("Key:{} Value:{} [partition {}]".format(
            msg.key(),
            msg.value(),
            msg.partition()
        ))
except KeyboardInterrupt:
    pass
finally:
    print("Closing consumer.")
    consumer.close()
