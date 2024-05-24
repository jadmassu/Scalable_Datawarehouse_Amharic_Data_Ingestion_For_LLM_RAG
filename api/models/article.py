from sqlalchemy import  Column,  Integer, String
from .database import Database

db = Database()
base = db.get_base()
class Article(base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    title = Column(String)
    article_url = Column(String)
    highlight = Column(String)
    time_publish = Column(String)
    category = Column(String)
    date_published = Column(String)
    publisher_name = Column(String)
    detail_content = Column(String)
    
    
    
    

