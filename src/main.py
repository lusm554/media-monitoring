import feedparser
from rss import RSSFeed

rss_feeds = (
  RSSFeed(title='РИА Новости', rss_url='https://ria.ru/export/rss2/archive/index.xml'),
  RSSFeed(title='Рамблер', rss_url='https://news.rambler.ru/rss/'),
  RSSFeed(title='РБК', rss_url='https://rssexport.rbc.ru/rbcnews/news/30/full.rss'),
  RSSFeed(title='Новости Mail.ru', rss_url='https://news.mail.ru/rss/90/'),
  RSSFeed(title='Регнум', rss_url='https://regnum.ru/rss'),
  RSSFeed(title='ТАСС', rss_url='https://tass.ru/rss/v2.xml'),
  RSSFeed(title='Интерфакс', rss_url='https://www.interfax.ru/rss.asp'),
  RSSFeed(title='RT на русском', rss_url='https://russian.rt.com/rss'),
  RSSFeed(title='Известия', rss_url='https://iz.ru/xml/rss/all.xml'),
  RSSFeed(title='Российская газета', rss_url='https://rg.ru/xml/index.xml'),
  RSSFeed(title='Коммерсантъ', rss_url='https://www.kommersant.ru/RSS/news.xml'),
  RSSFeed(title='Ведомости', feed_name='Все новости', rss_url='https://www.vedomosti.ru/rss/news.xml'),
  RSSFeed(title='Ведомости', feed_name='Все материалы', rss_url='https://www.vedomosti.ru/rss/articles.xml'),
)

import pickle
from pprint import pprint

def read_rss():
  for feed in rss_feeds:
    d = feedparser.parse(feed.rss_url)
    yield feed, d 
  
def cache_rss(data, filename):
  with open(filename, 'wb') as f:
    pickle.dump(data, f)

def from_cache(filename):
  with open(filename, 'rb') as f:
    return pickle.load(f)

def fetch_and_cache(): 
  rss_stream = read_rss()
  for n, obj in enumerate(rss_stream):
    cache_rss(obj, f'cache/data{n}.pickle')
    
fetch_and_cache()
