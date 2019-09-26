import time
from kafka import TopicPartition
from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers='localhost:9092', consumer_timeout_ms=1000)
consumer.assign([TopicPartition('test', 1)])
for message in consumer:
    print(message)
    time.sleep(1)
    print("nothing in ")

print("nothing")