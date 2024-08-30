from sqlalchemy import create_engine, text, select as _select
from sqlalchemy.orm import Session
import datetime
from storage.postgres_datamap import Base, News, RegularNewsSubscribers, Users, NewsPosts
from scraper_lib import Article

HOST, PORT = 'localhost', '5432' # db
USER, PWD = 'postgres', ''
DATABASE = 'test'
URL = f'postgresql+psycopg2://{USER}:{PWD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(URL)

def connect():
  return engine.connect()

def create_tables_if_not_exists():
  Base.metadata.create_all(engine)

def recreate_tables():
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)

def news_to_article_converter(func):
  def rename_db_row_keys_to_article(dbrow):
    dbrow['db_id'] = dbrow.pop('id')
    return dbrow
  def wrapper(*args, **kwargs):
    news = func(*args, **kwargs)
    news = [Article.from_dict(rename_db_row_keys_to_article(n.__dict__)) for n in news]
    return news
  return wrapper

def db_row_to_dict_converter(func):
  from collections.abc import Iterable
  def filter_alchemy_attrs(dct):
    if '_sa_instance_state' in dct:
      del dct['_sa_instance_state']
    return dct
  def wrapper(*args, **kwargs):
    db_result = func(*args, **kwargs)
    if isinstance(db_result, Iterable):
      db_result = [filter_alchemy_attrs(n.__dict__) for n in db_result]
    else:
      db_result = filter_alchemy_attrs(db_result.__dict__)
    return db_result
  return wrapper

####################### NEWS POST #######################
def add_news_post(post_articles):
 with Session(engine) as session:
  try:
    for post_article in post_articles:
      session.add(NewsPosts(**post_article))
    session.commit()
  except Exception as error:
    session.rollback()
    print(error)

@db_row_to_dict_converter
def get_news_post(post_id):
  with Session(engine) as session:
    try:
        post = session.query(NewsPosts).filter_by(bot_post_id=post_id).all()
        return post
    except Exception as error:
      print(error)
      return list()

@news_to_article_converter
def get_articles_by_news_post(post_id):
  with Session(engine) as session:
    try:
        articles = (
          session
            .query(News)
            .filter(NewsPosts.bot_post_id == post_id)
            .filter(NewsPosts.news_id == News.id)
            .all()
        )
        return articles
    except Exception as error:
      print(error)
      return list()

@db_row_to_dict_converter
def get_n_news_posts(n=100):
  with Session(engine) as session:
    try:
      return session.query(NewsPosts).limit(n).all()
    except Exception as error:
      print(error)
      return list()

####################### USER #######################
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

####################### NEWS SUBSCRIBER #######################
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

####################### NEWS #######################
def add_news(news_list):
  with Session(engine) as session:
    try:
      for news in news_list:
        existing_news = session.query(News).filter_by(url=news["url"]).first()
        if not existing_news:
          news = news.to_dict()
          del news['db_id']
          session.add(News(**news))
      session.commit()
    except Exception as error:
      session.rollback()
      raise error

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
