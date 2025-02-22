from sqlalchemy import create_engine, text, select as _select
from sqlalchemy.orm import Session
import datetime
from scraper_lib import Article, Release
from collections.abc import Iterable
from storage.postgres_datamap import (
  Base,
  News,
  RegularNewsSubscribers,
  Users,
  NewsPosts,
  ReleasesPosts,
  Releases,
)

import logging
logger = logging.getLogger(__name__)

HOST, PORT = 'db', '5432' # db
#HOST, PORT = 'localhost', '5432'
USER, PWD = 'postgres', 'postgres'
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

def recreate_only_news_releases_related_tables():
  tables = [
    News.__table__,
    Releases.__table__, 
    NewsPosts.__table__,
    ReleasesPosts.__table__,
  ]
  Base.metadata.drop_all(engine, tables=tables)
  Base.metadata.create_all(engine, tables=tables)

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

def news_to_article_converter(func):
  def rename_db_row_keys_to_article(dbrow):
    dbrow['db_id'] = dbrow.pop('id')
    return dbrow
  def wrapper(*args, **kwargs):
    news = func(*args, **kwargs)
    news = [Article.from_dict(rename_db_row_keys_to_article(n.__dict__)) for n in news]
    return news
  return wrapper

def rows_to_releases_converter(func):
  def rename_db_row_keys_to_article(dbrow):
    dbrow['db_id'] = dbrow.pop('id')
    del dbrow['_sa_instance_state']
    return dbrow
  def wrapper(*args, **kwargs):
    releases = func(*args, **kwargs)
    releases = [Release.from_dict(rename_db_row_keys_to_article(n.__dict__)) for n in releases]
    return releases
  return wrapper

def get_n_rows_factory(table, result_convertor=None):
  def selector(n=100):
    with Session(engine) as session:
      try:
        return session.query(table).limit(n).all()
      except Exception as error:
        logger.error(error)
        return list()
  if result_convertor:
    selector = result_convertor(selector)
  return selector

get_n_releases_posts = get_n_rows_factory(ReleasesPosts, db_row_to_dict_converter)
#get_n_releases = get_n_rows_factory(Releases, db_row_to_dict_converter)
get_n_releases = get_n_rows_factory(Releases, rows_to_releases_converter)
get_n_news_posts = get_n_rows_factory(NewsPosts, db_row_to_dict_converter)
get_n_users = get_n_rows_factory(Users, db_row_to_dict_converter)
get_n_news_subscribers = get_n_rows_factory(RegularNewsSubscribers, db_row_to_dict_converter)
get_n_news = get_n_rows_factory(News, news_to_article_converter)

##############################################
#1. use add all
#2. filter for existing
#3. filter for keys
#4. add only from dict

def add_rows_factory(table, filter_existing_rows_key=None, filter_row_keys=None):
  def add_rows(rows):
    with Session(engine) as session:
      try:
        if not isinstance(rows, Iterable) or isinstance(rows, dict):
          rows = [rows]
        rows = [r.to_dict() if isinstance(r, Article) or isinstance(r, Release) else r for r in rows]
        if filter_row_keys:
          rows = [{k:v for k,v in row.items() if not k in filter_row_keys} for row in rows]
        if filter_existing_rows_key:
          rows = [
            row for row in rows 
            if not (
              session
                .query(table)
                .filter(getattr(table, filter_existing_rows_key) == row[filter_existing_rows_key])
                .first()
            )
          ]
        rows = [table(**row) for row in rows]
        session.add_all(rows)
        session.commit()
      except Exception as error:
        session.rollback()
        logger.error(error)
  return add_rows

add_user = add_rows_factory(Users, filter_existing_rows_key='telegram_user_id')
add_news = add_rows_factory(News, filter_existing_rows_key='url', filter_row_keys=['db_id', '_filter_url', 'hash_attr'])
add_news_posts = add_rows_factory(NewsPosts, filter_existing_rows_key='bot_post_id')
add_news_subscriber = add_rows_factory(RegularNewsSubscribers, filter_existing_rows_key='telegram_user_id')
add_releases = add_rows_factory(Releases, filter_existing_rows_key='url', filter_row_keys=['db_id'])
add_releases_posts = add_rows_factory(ReleasesPosts, filter_existing_rows_key='bot_post_id')

##############################################
def get_rows_by_col(table, key, result_convertor=None):
  def selector(col_val):
    with Session(engine) as session:
      try:
        if not isinstance(col_val, Iterable) or isinstance(col_val, str):
          col_val = [col_val] 
        #return session.query(table).filter(getattr(table, key) == col_val).all()
        return session.query(table).filter(getattr(table, key).in_(col_val)).all()
      except Exception as error:
        logger.error(error)
        return list()
  if result_convertor:
    selector = result_convertor(selector)
  return selector

get_news_post = get_rows_by_col(table=NewsPosts, key='bot_post_id', result_convertor=db_row_to_dict_converter)
get_releases = get_rows_by_col(table=Releases, key='url', result_convertor=db_row_to_dict_converter)
get_news = get_rows_by_col(table=News, key='url', result_convertor=db_row_to_dict_converter)

####################### NEWS POST #######################

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
      logger.error(error)
      return list()

@news_to_article_converter
def get_releases_by_release_post(post_id):
  with Session(engine) as session:
    try:
        articles = (
          session
            .query(Releases)
            .filter(ReleasesPosts.bot_post_id == post_id)
            .filter(ReleasesPosts.release_id == Releases.id)
            .all()
        )
        return articles
    except Exception as error:
      logger.error(error)
      return list()

####################### NEWS SUBSCRIBER #######################
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
      logger.error(error)

####################### NEWS #######################
def get_rows_by_date_range_factory(table, table_dt_col, delta_in_hours, result_convertor=None):
  def selector():
    with Session(engine) as session:
      try:
        # hard fix
        import zoneinfo # add since Python 3.9
        time_zone_moscow = zoneinfo.ZoneInfo("Europe/Moscow")
        start_dt = datetime.datetime.now(tz=time_zone_moscow) - datetime.timedelta(hours=delta_in_hours)
        end_dt = datetime.datetime.now(tz=time_zone_moscow)
        return session.query(table).filter(
          getattr(table, table_dt_col) >= start_dt,
          getattr(table, table_dt_col) <= end_dt,
        ).all()
      except Exception as error:
        logger.error(error)
        return list()
  if result_convertor:
    selector = result_convertor(selector)
  return selector

get_last_24h_news = get_rows_by_date_range_factory(
  table=News, table_dt_col='publish_time', delta_in_hours=24, result_convertor=news_to_article_converter
)

get_last_24h_releases = get_rows_by_date_range_factory(
  table=Releases, table_dt_col='release_time', delta_in_hours=24, result_convertor=rows_to_releases_converter
)
