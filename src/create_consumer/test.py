import confluent_kafka
import pandas as pd 

c = confluent_kafka.Consumer({"bootstrap.servers": "localhost:9092", "group.id":"msg+"})

def on_assign (consumer, partitions):
    for p in partitions:
        p.offset = 100
    print('assign', partitions)
    consumer.assign(partitions)

def test():
    c.subscribe(["topic_"], on_assign=on_assign)
    try:
        payload_= list()
        partitions_= list()
        offsets_= list()
        while True:
            m = c.poll(1)
            if m is None:
                continue
            if m.error() is None:
                print('Received message', m.value(), m.offset(), m.partition())
                payload_.append(m.value())
                partitions_.append(m.partition())
                offsets_.append(m.offset())
                

    except Exception as e:
        print(str(e))
    finally:
        return pd.DataFrame({"payload":payload_, "partition": partitions_, "offsets": offsets_})
        c.close()

test().to_csv("test.csv", index= False)