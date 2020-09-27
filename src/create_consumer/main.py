from confluent_kafka import Consumer
from pprint import pprint
from time import time 
from typing import Callable, Union, Any, List


def count_run_time(msg_f: Callable)-> Union[int, float]:
    start= time()
    msg_f()
    cost= time()- start 
    return cost 


def receive_msgs(topic: str, bootstrap_server: str, sess_timeout: int)-> None:
    c = Consumer({
        'bootstrap.servers': bootstrap_server,
        'group.id': 'tests',
        'auto.offset.reset': 'earliest',
        "api.version.request":"true",
        # "partition.assignment.strategy":"range", #default
        "session.timeout.ms":sess_timeout,
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

def main(topic: str, bootstrap_server: str, timeout:int)-> str:
    run_time = count_run_time(receive_msgs(topic, bootstrap_server, timeout))
    return f"Total cost time: {run_time}"
    

if __name__ == "__main__":
    BOOTSTRAP_SERVER ="localhost:9092"
    TOPIC= "topic_a"
    SESS_TIMEOUT= 20000
    
    pprint("Starting Python Consumer.")
    pprint(main(TOPIC, BOOTSTRAP_SERVER, SESS_TIMEOUT))