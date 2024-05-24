from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import String,  inspect, or_
from sqlalchemy.orm import Session


from models.article import Article
from view_model.article_vm import ArticleCreateVM, ArticleFilterVM 




def create_data( db: Session, data:ArticleCreateVM):
        db_data = Article( 
                        image_url = data.image_url,
                        title = data.title,
                        article_url = data.article_url,
                        highlight = data.highlight,
                        time_publish = data.time_publish,
                        category = data.category,
                        date_published = data.date_published,
                        publisher_name = data.publisher_name,
                        detail_content = data.detail_content
    )
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data

def get_data (db: Session):
        return  db.query(Article)
def search_data(db: Session, query: str):
    search_term = f"%{query}%"
    columns = [column.name for column in inspect(Article).columns]
    filters = []
    for column in columns:
        col_attr = getattr(Article, column)
        
        if isinstance(col_attr.type, String):
            filters.append(col_attr.like(search_term))
   
    results = db.query(Article).filter(or_(*filters)).all()
    return results

def filter_data(db: Session, filter_params: ArticleFilterVM):
    query = db.query(Article)
    
    if filter_params.id is not None:
        query = query.filter(Article.id == filter_params.id)
    if filter_params.image_url:
        query = query.filter(Article.image_url == filter_params.image_url)
    if filter_params.title:
        query = query.filter(Article.title == filter_params.title)
    if filter_params.article_url:
        query = query.filter(Article.article_url == filter_params.article_url)
    if filter_params.highlight:
        query = query.filter(Article.highlight == filter_params.highlight)
    if filter_params.time_publish:
        query = query.filter(Article.time_publish == filter_params.time_publish)
    if filter_params.category:
        query = query.filter(Article.category == filter_params.category)
    if filter_params.date_published:
        query = query.filter(Article.date_published == filter_params.date_published)
    if filter_params.publisher_name:
        query = query.filter(Article.publisher_name == filter_params.publisher_name)
    if filter_params.detail_content:
        query = query.filter(Article.detail_content == filter_params.detail_content)

    return query.all()