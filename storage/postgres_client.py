from sqlalchemy import create_engine, text, select as _select
from sqlalchemy.orm import Session
import datetime
from storage.postgres_datamap import Base, News, RegularNewsSubscribers, Users
from scraper_lib import Article

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

def db_row_to_dict_converter(func):
  def wrapper(*args, **kwargs):
    users = func(*args, **kwargs)
    users = [n.__dict__ for n in users]
    return users
  return wrapper

def add_user(user):
  with Session(engine) as session:
    try:
      session.add(Users(**user))
      session.commit()
    except Exception as error:
      session.rollback()
      print(error)

@db_row_to_dict_converter
def get_n_users(n=100):
  with Session(engine) as session:
    try:
      return session.query(Users).limit(n).all()
    except Exception as error:
      print(error)
      return list()

def add_news_subscriber(news_subscriber):
  with Session(engine) as session:
    try:
      existing_subscriber = (
        session
          .query(RegularNewsSubscribers)
          .filter_by(telegram_user_id=news_subscriber["telegram_user_id"])
          .first()
      )
      if not existing_subscriber:
        session.add(RegularNewsSubscribers(**news_subscriber))
      session.commit()
    except Exception as error:
      session.rollback()
      print(error)

def delete_news_subscriber(subsciber_telegram_id):
  with Session(engine) as session:
    try:
      (session
        .query(RegularNewsSubscribers)
        .filter_by(telegram_user_id=subsciber_telegram_id)
        .delete()
      )
      session.commit()
    except Exception as error:
      session.rollback()
      print(error)

@db_row_to_dict_converter
def get_n_news_subscribers(n=100):
  with Session(engine) as session:
    try:
      return session.query(RegularNewsSubscribers).limit(n).all()
    except Exception as error:
      print(error)
      return list()

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

def news_to_article_converter(func):
  def wrapper(*args, **kwargs):
    news = func(*args, **kwargs)
    news = [Article.from_dict(n.__dict__) for n in news]
    return news
  return wrapper

@news_to_article_converter
def get_n_news(n=100):
  with Session(engine) as session:
    try:
      return session.query(News).limit(n).all()
    except Exception as error:
      print(error)
      return list()

@news_to_article_converter
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

def get_last_24h_news():
  start_dt = datetime.datetime.now() - datetime.timedelta(hours=24)
  end_dt = datetime.datetime.now()
  news = get_news_by_date_range(start_dt, end_dt)
  return news
