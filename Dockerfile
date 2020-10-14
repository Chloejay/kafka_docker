FROM confluentinc/cp-kafka-connect-base:5.3.0
RUN  confluent-hub install --no-prompt confluentinc/kafka-connect-mqtt:1.2.3
RUN  confluent-hub install --no-prompt jcustenborder/kafka-connect-redis:0.0.2.9