from confluent_kafka.admin import AdminClient, NewTopic
from typing import List


class Topics:
    def __init__(self, kafka_: str, topic_list:List[str], partition: int, replica: int):
        self.kafka_= AdminClient({'bootstrap.servers': kafka_})
        self.topic_list= topic_list
        self.new_topic= [NewTopic(topic, num_partitions= partition, replication_factor= replica) for topic in topic_list]


    def create_topic(self):
        fs = self.kafka_.create_topics(self.new_topic)
        for topic, f in fs.items():
            try:
                f.result()
                print("Topic {} created".format(topic))

            except Exception as e:
                print("Failed to create topic {}: {}".format(topic, e))



if __name__== "__main__":
    topic= Topics("localhost:9092", ["drivers"], 6, 1)
    topic.create_topic()

