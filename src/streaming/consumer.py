import faust
from config.config import config
from utils.common import setup_logging

setup_logging()

app = faust.App(config.FAUST_APP_ID, broker=config.KAFKA_BROKER, store=config.FAUST_STORE)

class Data(faust.Record, serializer='json'):
    id: int
    value: str

topic = app.topic('data-topic', value_type=Data)

@app.agent(topic)
async def consume_data(stream):
    async for event in stream:
        print(f'Processed: {event}')
        # Add data processing logic here

if __name__ == '__main__':
    app.main()
