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
  FeedConf(title='lenta.ru', rss_url='https://lenta.ru/rss'),
  FeedConf(title='Московский Комсомолец', feed_name='Все материалы', rss_url='https://www.mk.ru/rss/news/index.xml'),
  FeedConf(title='Московский Комсомолец', feed_name='Новостная лента', rss_url='https://www.mk.ru/rss/news/index.xml'),
  FeedConf(title='Газета.ru', rss_url='https://www.gazeta.ru/export/rss/social_more.xml'),
  FeedConf(title='RT', rss_url='https://russian.rt.com/rss'),
  FeedConf(title='Финмаркет', rss_url='http://www.finmarket.ru/rss/mainnews.asp'),
  FeedConf(title='Росбалт', rss_url='https://www.rosbalt.ru/feed/'),
  FeedConf(title='Прайм', feed_name='Основной поток', rss_url='https://1prime.ru/export/rss2/index.xml'),
  FeedConf(title='Прайм', feed_name='Финансы', rss_url='https://1prime.ru/export/rss2/finance/index.xml'),
  FeedConf(title='Прайм', feed_name='Экономика', rss_url='https://1prime.ru/export/rss2/state_regulation/index.xml'),
  FeedConf(title='Bits.media', rss_url='https://bits.media/rss2/'),
  FeedConf(title='Indicator', rss_url='https://indicator.ru/exports/rss'),
  FeedConf(title='Финам', feed_name='Новости компаний', rss_url='https://www.finam.ru/analysis/conews/rsspoint/'),
  FeedConf(title='Финам', feed_name='Новости мировых рынков', rss_url='https://www.finam.ru/international/advanced/rsspoint/'),
  FeedConf(title='Comnews', rss_url='https://www.comnews.ru/rss'),
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
