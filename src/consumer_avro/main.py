from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
import pandas as pd
import os 


KAFKA_TOPIC = "topic_test"
consumer = AvroConsumer({
    "bootstrap.servers": "localhost:29092",
    "group.id": "consumer-avro_test",
    "auto.offset.reset": "earliest",
    "schema.registry.url": "http://localhost:8081",
    "api.version.request": True,
    "debug":"all"
})

consumer.subscribe([KAFKA_TOPIC])

def consume():
    try:
        keys_= list() 
        values_lat= list()
        values_lon= list()
        partitions_= list()
        while True:
            try:
                msg = consumer.poll(10)
                if msg is None:
                    continue
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue
                keys_.append(msg.key().get("key"))
                values_lat.append(msg.value().get("latitude"))
                values_lon.append(msg.value().get("longitude"))
                partitions_.append(msg.partition())
            except SerializerError as e:
                print("Message deserialization failed for {}: {}".format(msg, e))
                break
            
    except Exception as e:
        print("Error", e)
    finally:
        return pd.DataFrame({"avro_consumer_keys":keys_, 
                             "avro_consumer_lat":values_lat, 
                             "avro_consumer_lon":values_lon,
                             "avro_consumer_partitions":partitions_})
        print("Closing consumer.")
        consumer.close()


if __name__== "__main__":
    print("Starting Python Avro Consumer.")
    consume().to_csv(os.path.join("src/consumer_avro", "avro_consumer1.csv"), index= False)