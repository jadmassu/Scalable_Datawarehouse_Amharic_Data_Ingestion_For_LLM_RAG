import os

class Config:
    KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092') # Location URL of the Broker - remote server
    FAUST_APP_ID = os.getenv('FAUST_APP_ID', 'data_stream_app') # The App name
    FAUST_STORE = os.getenv('FAUST_STORE', 'rocksdb://')

config = Config()
