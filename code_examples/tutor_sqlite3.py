import sqlite3
import datetime
from collections import namedtuple
from pprint import pprint 


def adapt_datetime_epoch(val):
  """Adapt datetime.datetime to Unix timestamp."""
  _ = val.timestamp()
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


def fill_rss_sources():
  with con:
    con.execute('''
      CREATE TABLE rss_sources (
        id INTEGER PRIMARY KEY,
        title VARCHAR NOT NULL,
        start_dt TIMESTAMP NOT NULL,
        end_dt TIMESTAMP NOT NULL,
        rss_url VARCHAR NOT NULL,
        feed_name VARCHAR DEFAULT NULL
      )
    ''')
    
    start_dt = datetime.datetime.now()
    end_dt = datetime.datetime.max.replace(year=datetime.datetime.max.year-1)
    val = ('Comnews', start_dt, end_dt, 'https://www.comnews.ru/rss', None, )
    con.execute(
      '''
        INSERT INTO rss_sources(title, start_dt, end_dt, rss_url, feed_name)
        VALUES (?, ?, ?, ?, ?)
      ''',
      val
    )
    res = con.execute('select * from rss_sources')
    res = res.fetchone()
    pprint(res)

fill_rss_sources()
