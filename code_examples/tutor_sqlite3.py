import sqlite3
import datetime
from collections import namedtuple
from pprint import pprint 


def adapt_datetime_epoch(val):
  """Adapt datetime.datetime to Unix timestamp."""
  return int(val.timestamp())
sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)

def convert_timestamp(val):
  """Convert Unix epoch timestamp to datetime.datetime object."""
  return datetime.datetime.fromtimestamp(int(val))
sqlite3.register_converter("timestamp", convert_timestamp)

def namedtuple_factory(cursor, row):
  fields = [column[0] for column in cursor.description]
  cls = namedtuple('Row', fields)
  return cls._make(row)

con = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
con.row_factory = namedtuple_factory

with con:
  con.execute('''
    CREATE TABLE rss_sources (
      id INTEGER PRIMARY KEY,
      title VARCHAR NOT NULL,
      rss_url VARCHAR NOT NULL,
      feed_name VARCHAR DEFAULT NULL,
      dt TIMESTAMP NOT NULL
    )
  ''')
  
  curr_dt = datetime.datetime.now()
  val = ('Comnews', 'https://www.comnews.ru/rss', None, curr_dt)
  con.execute('''
    INSERT INTO rss_sources(title, rss_url, feed_name, dt)
    VALUES (?, ?, ?, ?)
  ''',
  val
  )
  res = con.execute('select * from rss_sources')
  res = res.fetchone()
  print('result', res.dt, type(res.dt))
  pprint(res)


exit()
res = con.execute('select * from sqlite_master')
pprint(res.fetchone())

