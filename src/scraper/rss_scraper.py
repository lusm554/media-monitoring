import feedparser
import datetime
import concurrent.futures
import time
import logging
from time import mktime
from .article import Article
import os

logger = logging.getLogger(__name__)

def _structdt2datetime(struct_time):
  dt = datetime.datetime.fromtimestamp(mktime(struct_time))
  return dt

class FeedItem:
  def __init__(self, title, rss_url, feed_name=None):
    self.title = title
    self.rss_url = rss_url
    self.feed_name = feed_name

  def __repr__(self):
    return f'{self.__class__.__name__}(title={self.title!r}, feed_name={self.feed_name!r}, rss_url={self.rss_url!r})'

class FeedsList:
  def __init__(self):
    self.RSS_FEEDS = (
      FeedItem(title='РИА Новости', rss_url='https://ria.ru/export/rss2/archive/index.xml'),
      FeedItem(title='Рамблер', rss_url='https://news.rambler.ru/rss/'),
      FeedItem(title='РБК', rss_url='https://rssexport.rbc.ru/rbcnews/news/30/full.rss'),
      FeedItem(title='Новости Mail.ru', rss_url='https://news.mail.ru/rss/90/'),
      FeedItem(title='Регнум', rss_url='https://regnum.ru/rss'),
      FeedItem(title='ТАСС', rss_url='https://tass.ru/rss/v2.xml'),
      FeedItem(title='Интерфакс', rss_url='https://www.interfax.ru/rss.asp'),
      FeedItem(title='RT на русском', rss_url='https://russian.rt.com/rss'),
      FeedItem(title='Известия', rss_url='https://iz.ru/xml/rss/all.xml'),
      FeedItem(title='Российская газета', rss_url='https://rg.ru/xml/index.xml'),
      FeedItem(title='Коммерсантъ', rss_url='https://www.kommersant.ru/RSS/news.xml'),
      FeedItem(title='Ведомости', feed_name='Все новости', rss_url='https://www.vedomosti.ru/rss/news.xml'),
      FeedItem(title='Ведомости', feed_name='Все материалы', rss_url='https://www.vedomosti.ru/rss/articles.xml'),
      FeedItem(title='lenta.ru', rss_url='https://lenta.ru/rss'),
      FeedItem(title='Московский Комсомолец', feed_name='Все материалы', rss_url='https://www.mk.ru/rss/news/index.xml'),
      FeedItem(title='Московский Комсомолец', feed_name='Новостная лента', rss_url='https://www.mk.ru/rss/news/index.xml'),
      FeedItem(title='Газета.ru', rss_url='https://www.gazeta.ru/export/rss/social_more.xml'),
      FeedItem(title='RT', rss_url='https://russian.rt.com/rss'),
      FeedItem(title='Финмаркет', rss_url='http://www.finmarket.ru/rss/mainnews.asp'),
      FeedItem(title='Росбалт', rss_url='https://www.rosbalt.ru/feed/'),
      FeedItem(title='Прайм', feed_name='Основной поток', rss_url='https://1prime.ru/export/rss2/index.xml'),
      FeedItem(title='Прайм', feed_name='Финансы', rss_url='https://1prime.ru/export/rss2/finance/index.xml'),
      FeedItem(title='Прайм', feed_name='Экономика', rss_url='https://1prime.ru/export/rss2/state_regulation/index.xml'),
      FeedItem(title='Bits.media', rss_url='https://bits.media/rss2/'),
      FeedItem(title='Indicator', rss_url='https://indicator.ru/exports/rss'),
      FeedItem(title='Финам', feed_name='Новости компаний', rss_url='https://www.finam.ru/analysis/conews/rsspoint/'),
      FeedItem(title='Финам', feed_name='Новости мировых рынков', rss_url='https://www.finam.ru/international/advanced/rsspoint/'),
      FeedItem(title='Comnews', rss_url='https://www.comnews.ru/rss'),
      FeedItem(title='tadviser.ru', rss_url='https://www.tadviser.ru/xml/tadviser.xml'),
    )

  def __iter__(self):
    return iter(self.RSS_FEEDS)

class RssScraper:
  def __init__(self, feeds):
    self.feeds = feeds

  def __fetch_feed__(self, feed):
    rss_response = feedparser.parse(feed.rss_url)
    return feed, rss_response

  def __check_kw__(self, article):
    def check_kw(text):
      if not isinstance(text, str): return False
      text = text.lower()
      flag = False
      if 'цфа' in text:
        flag = True
      if 'цифровые финансовые активы' in text:
        flag = True
      return flag

    def check_for_rss_content(article):
      title = article.get('title')
      return check_kw(title)
    return check_for_rss_content(article)

  def proc_feed(self, feed):
    feeditem, rss_res = self.__fetch_feed__(feed)
    cfa_arts = []
    for article in rss_res.entries:
      if not self.__check_kw__(article):
        continue
      _article = Article(
        title=article.title,
        url=article.link,
        publish_time=_structdt2datetime(article.published_parsed),
        publisher_name=feeditem.title,
        scraper='rss',
      )
      cfa_arts.append(_article)
    return cfa_arts

  def fetch_last_news(self):
    result = []
    workers_cnt = min(32, (os.cpu_count() or 1) + 6)
    logger.info(f'Fetching rss articles with {workers_cnt} workers')
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers_cnt) as executor:
      future_to_proc_feed = { executor.submit(self.proc_feed, feed): feed for feed in self.feeds }
      for future in concurrent.futures.as_completed(future_to_proc_feed):
        feed = future_to_proc_feed[future]
        try:
          arts = future.result()
          result.extend(arts)
        except Exception as exc:
          logger.error(f'Exception while fetching rss: {exc!r}') 
    logger.info(f'Found {len(result)} articles in {len(self.feeds)} sources')
    return result

class RSS:
  def __init__(self, scraper=RssScraper, feed_list=FeedsList):
    self.feed_list = list(feed_list())
    self.scraper = scraper(feeds=self.feed_list)

if __name__ == '__main__':
  logging.basicConfig(
    format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
  )
  s = rss_scraper()
  r = s.fetch_last_news()
  print(r)
