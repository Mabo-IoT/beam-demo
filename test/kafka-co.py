from pykafka import KafkaClient


client = KafkaClient(hosts="192.168.0.110:9092")
topic = client.topics["test"]


consumer = topic.get_simple_consumer()

for message in consumer:
    if message is not None:
        print(message.value)

