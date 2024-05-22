from kafka import KafkaConsumer
import json

def main():
    consumer = KafkaConsumer(
        'scrapy_items',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for message in consumer:
        item = json.loads(message.value)
        # Process the item (e.g., clean and normalize text)
        print(f"Consumed item: {item}")

if __name__ == '__main__':
    main()
