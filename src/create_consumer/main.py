from confluent_kafka import Consumer, TopicPartition, KafkaError, KafkaException
from pprint import pprint
import pandas as pd 
from time import time 
from typing import Callable, Union, Any, List
import json


def count_run_time(msg_f: Callable)-> Union[int, float]:
    start= time()
    msg_f()
    cost= time()- start 
    return cost 

class Base_Consumer:
    def __init__(self, topic: str, bootstrap_server: str, sess_timeout: int, retries: int, 
                 group: str, partition: int=0, offset: int= 0)-> None:
        """
        Config Consumer properties, 
        Args:
            topic (str): topic of meassage
            bootstrap_server (str): broker connection host:port
            sess_timeout (int): detect failures when using Kafka’s group management facilities
            retries (int): retry for error and exception
            group (str): consumer group id 
            partition (int, optional): Defaults to 0.
            offset (int, optional): message next ready to read position. Defaults to 0.
        """
        self.topic= topic
        self.tp= TopicPartition(topic, partition, offset)
        self.consumer = Consumer({
        "bootstrap.servers": bootstrap_server,
        "group.id": group,
        "default.topic.config":{"auto.offset.reset": "earliest"},
        "api.version.request": True,
        "session.timeout.ms":sess_timeout,
        "enable.auto.commit": True,
        "enable.auto.offset.store": True,
        # "partition.assignment.strategy":"range", #default
        "retries":retries,
        "debug":"all"
        })

    def receive_msgs(self):
        c = self.consumer
        c.subscribe([self.topic])
        # c.consume(num_messages=1, timeout=30)
        try:
            running = True
            message_values= list()
            while running:
                msg = c.poll(0.1)
                if msg is None:
                    continue
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue
                # value_= json.load(msg.value.decode("utf-8"))
                msg= msg.value().decode("utf-8")
                message_values.append(msg)
        except Exception as e:
            pprint(f"Error: {str(e)}")
        finally:
            df = pd.DataFrame([sub.split("\t-") for sub in message_values], columns=["lon", "lat"])
            return df
            c.close()
            
    # reassign partition
    def partition_assign(self):
        pass

class Consumer1(Base_Consumer):
    def __init__(self, topic, bootstrap_server, sess_timeout, retries, group, partition, offset):
        self.partition= partition
        self.offset = offset
        self.tp_= TopicPartition(topic, partition)
        super().__init__(topic, bootstrap_server, sess_timeout, retries, group)
        
    def get_topics(self):
        topics= self.consumer.list_topics(topic= self.topic) 
        return topics

        # partitions = []
        # for name, meta  in topics.topics.items():
            # for partition_id in meta.partitions.keys():
                # part = TopicPartition(name, partition_id)
                # partitions.append(part)
                
        # partitions = self.consumer.committed(partitions)
        # print(partitions)
        
    def get_pos(self, timeout= None):
        low, high = self.consumer.get_watermark_offsets(self.tp, timeout)
        print(low, high)

    def is_partition_assign(self)-> bool:
        tp = self.consumer.assign([self.tp])
        if tp:
            pprint(f"Topic partition: {tp}")
            return True
        raise KafkaException(f"partition: {self.partition} at offset: {self.offset} is empty.")

    def _more_config(self):
        pass


def main(topic: str, bootstrap_server: str, timeout:int, group: str, retries: int, partition: int, offset: int)-> str:
    consumer_one= Base_Consumer(topic, bootstrap_server, timeout, retries, group)
    (consumer_one.receive_msgs()).to_csv("tests.csv", index= False)
    run_time = count_run_time(consumer_one.receive_msgs)
    return f"Total cost time: {run_time}"
    



if __name__ == "__main__":
    BOOTSTRAP_SERVER ="localhost:9092"
    TOPIC= "topic_b"
    SESS_TIMEOUT= 10000
    GROUP= "messages"
    RETRIES= 1
    PARTITION=0
    OFFSET =0
    pprint("Starting Python Consumer.")
    pprint(main(TOPIC, BOOTSTRAP_SERVER, SESS_TIMEOUT, GROUP, RETRIES, PARTITION, OFFSET))