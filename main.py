import feedparser
from rssfeed import RSSFeed

rss_feeds = (
  RSSFeed(title='РИА Новости', rss_url='https://ria.ru/export/rss2/archive/index.xml'),
  RSSFeed(title='Рамблер', rss_url='https://news.rambler.ru/rss/'),
  RSSFeed(title='РБК', rss_url='https://rssexport.rbc.ru/rbcnews/news/30/full.rss'),
  RSSFeed(title='Новости Mail.ru', rss_url='https://news.mail.ru/rss/90/'),
  RSSFeed(title='Регнум', rss_url='https://regnum.ru/rss'),
  RSSFeed(title='ТАСС', rss_url='https://tass.ru/rss/v2.xml'),
  RSSFeed(title='Интерфакс', rss_url='https://www.interfax.ru/rss.asp'),
  RSSFeed(title='RT на русском', rss_url='https://russian.rt.com/rss'),
)

import pickle
from pprint import pprint
pprint(rss_feeds)
print()

def read_rss():
  for feed in rss_feeds:
    d = feedparser.parse(feed.rss_url)
    yield feed, d 
  
def cache_rss(rss):
  with open('cache.pickle', 'wb') as f:
    pickle.dump(rss, f)

def from_cache():
  with open('cache.pickle', 'rb') as f:
    return pickle.load(f)


for feed, data in read_rss():
  pprint(feed)
  pprint(data.keys())
  print('\n'*2)

exit()
rss = from_cache()
for k in rss:
  pprint(k)
  pprint(type(rss[k]))
  print('\n'*2)
