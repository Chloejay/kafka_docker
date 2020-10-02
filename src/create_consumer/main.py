from confluent_kafka import Consumer, TopicPartition, KafkaError, KafkaException
from pprint import pprint
import pandas as pd 
from time import time 
from typing import Callable, Union, Any, List, Text
import json
import confluent_kafka


def count_run_time(msg_f: Callable)-> Union[int, float]:
    start = time()
    msg_f()
    cost = time()- start 
    return cost 
    
class Base_Consumer:
    def __init__(self, topic: str, bootstrap_server: str, sess_timeout: int, 
                 retries: int, group_id: str, assign: bool)-> None:
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
        self.need_assign_= assign
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_server,
            "group.id": group_id,
            "default.topic.config":{
                "auto.offset.reset": "earliest",
                "acks":1}, #EOS
            "api.version.request": True,
            "session.timeout.ms":sess_timeout,
            "enable.auto.commit": False,
            "auto.commit.interval.ms": 10000,
            "enable.auto.offset.store": True,
            'topic.metadata.refresh.interval.ms': 20000,
            "partition.assignment.strategy":"range", #default
            "retries":retries,
            "debug":"all"
            })

    def get_partitions_(self, partition_id: int)-> dict:
        part = TopicPartition(self.topic, partition_id)
        partitions = self.consumer.committed([part])
        pprint(f"Current Partition: {partition_id} - {partitions}")
        return partitions
        
    def get_topics(self)-> str:
        return self.consumer.list_topics(self.topic)

    def receive_msgs(self)-> Union[Text, pd.DataFrame]:
        running = True
        c = self.consumer
        if self.need_assign_:
            try:
                c.subscribe([self.topic], on_assign= on_assign)
            except KafkaException as e:
                pprint(e)
        c.subscribe([self.topic])
        
        message_values= list()
        offsets= list()
        keys= list() 
        partitions= list()
        try:
            while running:
                msg = c.poll(10)
                if msg is None:
                    continue
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue
                payload_= msg.value().decode("utf-8")
                key_= msg.key().decode("utf-8")
                partition_= msg.partition()
                offset_= msg.offset()
                pprint(f"Receive messages: {payload_}: {offset_}")
                
                message_values.append(payload_)
                keys.append(key_)
                partitions.append(partition_)
                offsets.append(offset_)
                
        except Exception as e:
            pprint(f"Error: {str(e)}")
        except:
            running= False
            print("Error pooling messages")
        finally:
            return pd.DataFrame({"keys": keys, 
                                 "lon_val":[v.split("\t-")[0] for v in message_values], 
                                 "lat_val":[v.split("\t-")[1] for v in message_values], 
                                 "partitions": partitions, 
                                 "offsets":offsets})
            c.close()

def on_assign(consumer:dict, partitions:List[int])-> Text:
    for p in partitions:
        p.offset= 200 # confluent_kafka.OFFSET_END
    pprint(f"Assign: {partitions}")
    consumer.assign(partitions)
    
class Consumer1(Base_Consumer):
    def __init__(self, topic, bootstrap_server, sess_timeout, retries, group, assign):
        self.partition= partition
        self.offset = offset
        self.tp_= TopicPartition(topic, partition)
        super().__init__(topic, bootstrap_server, sess_timeout, retries, group, assign)

    def is_partition_assign(self)-> bool:
        tp = self.consumer.assign([self.tp])
        if tp:
            pprint(f"Topic partition: {tp}")
            return True
        raise KafkaException(f"partition: {self.partition} at offset: {self.offset} is empty.")


def main(topic: str, bootstrap_server: str, timeout:int, group: str, retries: int, assign: bool)-> str:
    c1= Base_Consumer(topic, bootstrap_server, timeout, retries, group, assign)
    c1.receive_msgs().to_csv("tests2.csv", index= False)
    run_time = count_run_time(consumer_one.receive_msgs)
    return f"Total cost time: {run_time}"


if __name__ == "__main__":
    
    BOOTSTRAP_SERVER ="localhost:9092"
    TOPIC= "topic_"
    SESS_TIMEOUT= 20000
    GROUP_ID= "msg_offset_test2"
    RETRIES= 5
    REASSIGN = True
    pprint("Starting Python Consumer.")
    pprint(main(TOPIC, BOOTSTRAP_SERVER, SESS_TIMEOUT, GROUP_ID, RETRIES, REASSIGN))