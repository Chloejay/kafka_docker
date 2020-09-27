#/bin/bash

echo "create new topic for Producer Client"
echo "===================================="

../../confluent-5.3.0/bin/kafka-topics \
--create \
--bootstrap-server localhost:9092 \
--partitions 6 \
--replication-factor 1 \
--topic drivers 

