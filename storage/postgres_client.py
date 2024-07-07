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

def engine():
  host = 'localhost'
  #host = 'db'
  port = '5432'

  user = 'postgres'
  pwd = ''

  database = 'test'
  url = f'postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{database}'
  engine = create_engine(url)
  return engine

def connect():
  _engine = engine()
  return _engine.connect()

class Base(DeclarativeBase):
  pass

class News(Base):
  __tablename__ = "cfa_news"
  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str]
  url: Mapped[Optional[str]]

  def __repr__(self) -> str:
    return ''
    return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

def create_tables():
  _engine = engine()
  Base.metadata.create_all(_engine)

def insert():
  _engine = engine()
  with Session(_engine) as session:
    row = News(
      title='test',
      url='https://google.com',
    )
    session.add(row)
    session.commit()

def select():
  _engine = engine()
  sql = text('select * from cfa_news')
  print(sql)
  with connect() as conn:
    res = conn.execute(sql)
    res = list(res)
    print(res)


