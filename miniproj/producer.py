from time import sleep
from json import dumps
from kafka import KafkaProducer

ORDER_STORED_TOPIC = "order_stored"

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    api_version=(0, 10, 2),
    # value_serializer=lambda x: dumps(x).encode("utf-8"),
)
for j in range(1, 10):
    print("Iteration", j)
    data = {"counter": j}
    # producer.send("topictest", value=data)
    producer.send(ORDER_STORED_TOPIC, dumps(data).encode("utf-8"))
    print("Done...", j)
    sleep(1)
