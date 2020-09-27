# the kafka_listeners example code below is from https://github.com/rmoff/kafka-listeners/blob/master/python/python_kafka_test_client.py

from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer
from confluent_kafka import Producer
from datetime import datetime

bootstrap_server="localhost:9092"
topic = 'tests'

def Produce(source_data):
    print('\n<Producing>')
    p = Producer({'bootstrap.servers': bootstrap_server})

    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('❌ Message delivery failed: {}'.format(err))
        else:
            print('✅  📬  Message delivered: "{}" to {} [partition {}]'.format(msg.value().decode('utf-8'),msg.topic(), msg.partition()))

    for data in source_data:
        p.poll(0)
        p.produce(topic, data.encode('utf-8'), callback=delivery_report)

    r= p.flush(timeout=5)
    if r>0:
        print('❌ Message delivery failed ({} message(s) still remain, did we timeout sending perhaps?)\n'.format(r))

def Consume():
    print('\n<Consuming>')
    c = Consumer({
        'bootstrap.servers': bootstrap_server,
        'group.id': 'test',
        'auto.offset.reset': 'earliest'
    })

    c.subscribe([topic])
    try:
        msgs = c.consume(num_messages=1, timeout=30)

        if len(msgs)==0:
            print("❌ No message(s) consumed (maybe we timed out waiting?)\n")
        else:
            for msg in msgs:
                print('✅  💌  Message received:  "{}" from topic {}\n'.format(msg.value().decode('utf-8'),msg.topic()))
    except Exception as e:
        print("❌ Consumer error: {}\n".format(e))
    c.close()

broker = AdminClient({'bootstrap.servers': bootstrap_server})
try:         
    metadata = broker.list_topics(timeout=10)
    print("""
    ✅ Connected to bootstrap server(%s) and it returned metadata for brokers as follows:
    %s
        ---------------------
        ℹ️  This step just confirms that the bootstrap connection was successful. 
        ℹ️  For the consumer to work your client will also need to be able to resolve the broker(s) returned
            in the metadata above.
        ℹ️  If the host(s) shown are not accessible from where your client is running you need to change 
            your advertised.listener configuration on the Kafka broker(s).
    """
    % (bootstrap_server, metadata.brokers))

    try:
        Produce(['foo / ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

        Consume()
    except Exception as e:
        print(e)
        print("❌ (uncaught exception in produce/consume)")
        
except Exception as e:
    print("""
    ❌ Failed to connect to bootstrap server.
    
    👉 %s
    
    ℹ️  Check that Kafka is running, and that the bootstrap server you've provided (%s) is reachable from your client
    """
    % (e,bootstrap_server))
