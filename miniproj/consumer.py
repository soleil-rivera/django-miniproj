from json import loads
from kafka import KafkaConsumer

ORDER_STORED_CONFIRM_TOPIC = "order_stored_confirm"

consumer = KafkaConsumer(
    ORDER_STORED_CONFIRM_TOPIC,
    bootstrap_servers="localhost:29092",
    api_version=(0, 10, 2),
    # value_serializer=lambda x: dumps(x).encode("utf-8"),
)
print("Listening...")
while True:
    for message in consumer:
        consumed_message = loads(message.value.decode())
        user_email = consumed_message["counter"]
        print(f"Sending email to {user_email}")
