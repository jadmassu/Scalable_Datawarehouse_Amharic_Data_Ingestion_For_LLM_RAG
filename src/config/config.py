import os

class Config:
    KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
    FAUST_APP_ID = os.getenv('FAUST_APP_ID', 'data_stream_app')
    FAUST_STORE = os.getenv('FAUST_STORE', 'rocksdb://')

config = Config()
