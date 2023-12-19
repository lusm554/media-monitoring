from pprint import pprint
import datetime
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class Scraper:
  def __init__(self, from_rss, from_google, article_wrp):  
    self.from_rss = from_rss()
    self.from_google = from_google()
    self.article_wrp = article_wrp
  
  def get_rss_media_index(self):
    return self.from_rss.feed_list

  def get_articles_from_rss(self):
    rss_articles = self.from_rss.scraper.fetch_last_news()
    return rss_articles

  def get_articles_from_google(self):
    go_articles = self.from_google.fetch_articles()
    return go_articles

  def get_distinct_arts(self, arts):
    wrapped_arts_set = set(self.article_wrp(art) for art in arts) # custom class for comprasion by article link
    arts = [wrp.article for wrp in wrapped_arts_set]
    return arts

  def filter_by_urls_blacklist(self, arts):
    publishers_blacklist = (
      'echomsk.spb.ru',
      'forpost-sevastopol.ru',
    )
    arts = [art for art in arts if urlparse(art.url).netloc not in publishers_blacklist]
    return arts

  def filter_by_period(self, arts, time_period):
    assert time_period in ('24h', 'all_available'), f'Parameter time_period {time_period!r} not found, try 24h'
    if time_period == '24h':
      arts = [ art for art in arts if (datetime.datetime.now() - art.publish_time).days == 0 ]
    return arts

  def get_articles(self, time_period='24h'):
    assert time_period in ('24h', 'all_available'), f'Parameter time_period {time_period!r} not found, try 24h'
    union_articles = [*self.get_articles_from_rss(), *self.get_articles_from_google()]
    set_articles = self.get_distinct_arts(union_articles)
    allowed_publishers_articles = self.filter_by_urls_blacklist(set_articles)
    period_articles = self.filter_by_period(allowed_publishers_articles, time_period) 
    logger.info(f'Found {len(period_articles)} articles by period {time_period!r} in rss and google')
    return period_articles

def get_scraper_instance(rss_scrp, go_scrp, article_wrp):
  scraper = Scraper(from_rss=rss_scrp, from_google=go_scrp, article_wrp=article_wrp)
  return scraper

if __name__ == '__main__':
  logging.basicConfig(
    format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
  )
  scrp = Scraper(from_rss=RSS, from_google=GoogleScraper)
  arts = scrp.get_articles()
  for i in arts:
    print(i.publish_time, (datetime.datetime.now() - i.publish_time), i.title)

  print(scrp.get_rss_media_index())
