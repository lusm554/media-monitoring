from sqlalchemy import create_engine, text, select as _select
from sqlalchemy.orm import Session
from datetime import datetime
from storage.postgres_datamap import Base

HOST, PORT = 'localhost', '5432' # db
USER, PWD = 'postgres', ''
DATABASE = 'test'
URL = f'postgresql+psycopg2://{USER}:{PWD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(URL)

def connect():
  return engine.connect()

def create_tables():
  Base.metadata.create_all(engine)

def recreate_tables():
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)

def add_news(news_list):
  with Session(engine) as session:
    try:
      for news in news_list:
        existing_news = session.query(News).filter_by(url=news["url"]).first()
        if not existing_news:
          session.add(News(**news))
      session.commit()
    except Exception as error:
      session.rollback()
      print(error)

def get_news_by_date_range(start_dt, end_dt):
  with Session(engine) as session:
    try:
      return session.query(News).filter(
        News.publish_time >= start_dt,
        News.publish_time <= end_dt,
      ).all()
    except Exception as error:
      print(error)
      return list()

#- get news like Article class
#- save newss from Article class

import datetime 

def save_news(articles):
  news = [
    {
      'title': art.title,
      'url': art.url,
      'publish_time': art.publish_time,
      'publisher_name': art.publisher_name,
      'scraper': art.scraper,
    }
    for art in articles
  ]
  add_news(news)

def get_news():
  start_dt = datetime.datetime.now() - datetime.timedelta(hours=24)
  end_dt = datetime.datetime.now()
  rows = get_news_by_date_range(start_dt, end_dt)





