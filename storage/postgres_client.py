from sqlalchemy import create_engine, text, select as _select
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from datetime import datetime
from typing import get_type_hints

HOST, PORT = 'localhost', '5432' # db
USER, PWD = 'postgres', ''
DATABASE = 'test'
URL = f'postgresql+psycopg2://{USER}:{PWD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(URL)

class Base(DeclarativeBase):
  pass

class News(Base):
  __tablename__ = "cfa_news"
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  title: Mapped[str]
  url: Mapped[str] = mapped_column(unique=True)
  publish_time: Mapped[datetime] = mapped_column(index=True)
  publisher_name: Mapped[str]
  scraper: Mapped[str]

  def __repr__(self) -> str:
    cls_level_attrs = get_type_hints(self).keys()
    repr_str = ', '.join(f"{attr}={getattr(self, attr)!r}" for attr in cls_level_attrs)
    return f"{self.__class__.__name__}({repr_str})"

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





