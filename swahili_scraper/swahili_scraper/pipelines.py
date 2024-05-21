# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import motor.motor_asyncio
from kafka import KafkaProducer
import json
import asyncio
from scrapy.utils.project import get_project_settings

class MongoDBPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.mongo_uri = settings.get('MONGO_URI')
        self.mongo_db = settings.get('MONGO_DATABASE', 'items')
        self.collection_name = 'scraped_items'
        self.client = None
        self.db = None

    async def open_spider(self, spider):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    async def close_spider(self, spider):
        self.client.close()

    async def process_item(self, item, spider):
        await self.db[self.collection_name].insert_one(dict(item))
        return item

class KafkaPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.kafka_server = settings.get('KAFKA_SERVER')
        self.topic = settings.get('KAFKA_TOPIC')
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    async def process_item(self, item, spider):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.producer.send,
            self.topic,
            item
        )
        return item

    def close_spider(self, spider):
        self.producer.flush()
        self.producer.close()
