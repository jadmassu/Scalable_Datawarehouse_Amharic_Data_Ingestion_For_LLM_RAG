import faust
from config.config import config
from utils.common import setup_logging

setup_logging()

app = faust.App(config.FAUST_APP_ID, broker=config.KAFKA_BROKER)

class Data(faust.Record, serializer='json'):
    id: int
    value: str

topic = app.topic('data-topic', value_type=Data)

@app.agent(topic)
async def process(stream):
    async for event in stream:
        print(f'Received: {event}')

if __name__ == '__main__':
    app.main()
