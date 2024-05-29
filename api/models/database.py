from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os,sys

from dotenv import load_dotenv

load_dotenv()
rpath = os.path.abspath('../api')



# username = os.getenv("POSTGRES_USER")
# password = os.getenv("POSTGRES_PASSWORD")
# host = os.getenv("POSTGRES_HOST")
# port = os.getenv("POSTGRES_PORT")
# database = os.getenv("POSTGRES_DB")

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")


# SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@db:{port}/{database}"
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}/{database}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

def get_base():
        return Base

def create_all_tables():
   return Base.metadata.create_all(bind=engine)
 
