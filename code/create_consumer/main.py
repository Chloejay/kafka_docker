from confluent_kafka import Consumer
from pprint import pprint 


def receive_msgs(topic, bootstrap_server):
    c = Consumer({
        'bootstrap.servers': bootstrap_server,
        'group.id': 'tests',
        'auto.offset.reset': 'earliest',
        "api.version.request":"true",
        # "partition.assignment.strategy":"range",
        "session.timeout.ms":20000,
        "enable.auto.commit": "true",
        "enable.auto.offset.store": "true",
        "retries":5,
        "debug":"all"
        # 'plugin.library.paths': 'monitoring-interceptor',
    })

    c.subscribe([topic])
    try:
        while True:
            msg = c.poll(1.0)
            # c.consume(num_messages=1, timeout=30)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            print(msg.key().decode('utf-8'), 
                  msg.value().decode('utf-8'), 
                  msg.partition())
    
    except Exception as e:
        pprint(str(e))
    finally:
        c.close()



if __name__ == "__main__":
    bootstrap_server="localhost:9092"
    topic= "topic_a"
    
    pprint("Starting Python Consumer.")
    receive_msgs(topic, bootstrap_server)