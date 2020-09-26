from confluent_kafka import Consumer
from pprint import pprint 


def receive_msgs(topic):
    c = Consumer({
        'bootstrap.servers': bootstrap_server,
        'group.id': 'test(s)',
        'auto.offset.reset': 'earliest',
        'plugin.library.paths': 'monitoring-interceptor',
    })

    c.subscribe([topic])
    
    while True:
        try:
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
        
    c.close()



if __name__ == "__main__":
    bootstrap_server="localhost:9092"
    topic="tests"
    
    pprint("Starting Python Consumer.")
    receive_msgs(topic)