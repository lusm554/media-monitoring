from rss_scraper import rss_scraper
from google_scraper import GoogleScraper
from pprint import pprint
from article import WrappedArticle
import logging

logger = logging.getLogger(__name__)

class Scraper:
  def __init__(self, from_rss, from_google):  
    self.from_rss = from_rss
    self.from_google = from_google 

  def get_articles_from_rss(self):
    rss_articles = self.from_rss().fetch_last_news()
    return rss_articles

  def get_articles_from_google(self):
    go_articles = self.from_google().fetch_articles()
    return go_articles

  def get_distinct_arts(self, arts):
    wrapped_arts_set = set(WrappedArticle(art) for art in arts) # custom class for comprasion by article link
    arts = [wrp.article for wrp in wrapped_arts_set]
    return arts

  def get_articles(self):
    from_rss = self.get_articles_from_rss()
    from_google = self.get_articles_from_google()
    articles = [*from_rss, *from_google]
    articles = self.get_distinct_arts(articles)
    logger.info(f'Found {len(articles)} articles in rss and google')
    return articles

if __name__ == '__main__':
  logging.basicConfig(
    format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
  )
  scrp = Scraper(from_rss=rss_scraper, from_google=GoogleScraper)
  arts = scrp.get_articles()
  for i in arts:
    print(i)

