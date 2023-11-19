import pickle
import feedparser

class FeedConf:
  def __init__(self, title, rss_url, feed_name=None):
    self.title = title
    self.rss_url = rss_url
    self.feed_name = feed_name

  def __repr__(self):
    return f'{self.__class__.__name__}(title={self.title!r}, feed_name={self.feed_name!r}, rss_url={self.rss_url!r}'

RSS_FEEDS = (
  FeedConf(title='РИА Новости', rss_url='https://ria.ru/export/rss2/archive/index.xml'),
  FeedConf(title='Рамблер', rss_url='https://news.rambler.ru/rss/'),
  FeedConf(title='РБК', rss_url='https://rssexport.rbc.ru/rbcnews/news/30/full.rss'),
  FeedConf(title='Новости Mail.ru', rss_url='https://news.mail.ru/rss/90/'),
  FeedConf(title='Регнум', rss_url='https://regnum.ru/rss'),
  FeedConf(title='ТАСС', rss_url='https://tass.ru/rss/v2.xml'),
  FeedConf(title='Интерфакс', rss_url='https://www.interfax.ru/rss.asp'),
  FeedConf(title='RT на русском', rss_url='https://russian.rt.com/rss'),
  FeedConf(title='Известия', rss_url='https://iz.ru/xml/rss/all.xml'),
  FeedConf(title='Российская газета', rss_url='https://rg.ru/xml/index.xml'),
  FeedConf(title='Коммерсантъ', rss_url='https://www.kommersant.ru/RSS/news.xml'),
  FeedConf(title='Ведомости', feed_name='Все новости', rss_url='https://www.vedomosti.ru/rss/news.xml'),
  FeedConf(title='Ведомости', feed_name='Все материалы', rss_url='https://www.vedomosti.ru/rss/articles.xml'),
)

class Feed:
  pass 

class RSSDAO:
  def __init__(self, feeds):
    self.feeds = feeds
    self._cache_filepath = 'data/rss_cache.pickle'

  def fetch(self):
    for feed in self.feeds:
      rss_response = feedparser.parse(feed.rss_url)
      yield feed, rss_response 

  def save_rss(self, data):
    with open(self._cache_filepath, 'wb') as file:
      pickle.dump(data, file)

  def read_rss(self):
    with open(self._cache_filepath, 'rb') as file:
      data = pickle.load(file)
    return data
