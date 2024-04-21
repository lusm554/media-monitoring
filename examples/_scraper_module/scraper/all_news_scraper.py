from urllib.parse import urlparse
from .base_scraper import NewsBaseScraper
from .dzen_news_scraper import CfaDzenNewsScraper
from .rss_news_scraper import CfaRssNewsScraper
from .google_news_scraper import CfaGoogleNewsScraper
import logging

logger = logging.getLogger(__name__)

class CfaAllNewsScraper(NewsBaseScraper):
  '''
  Объединяет в себе все парсеры новостей для удобства парсинга всех новостей за раз.
  '''
  def __init__(self):
    super().__init__()
    self.NEWS_SCRAPERS = [
      CfaDzenNewsScraper,
      CfaRssNewsScraper,
      CfaGoogleNewsScraper,
    ]

  def filter_by_blacklist(self, articles):
    '''
    Исключает новости, домены которых находятся в черном списке self.cfa_news_url_blacklist.
    '''
    return [
      article for article in articles
      if not urlparse(article.url).netloc in self.cfa_news_url_blacklist
    ]

  def fetch_and_parse(self, period):
    '''
    Забирает новости по каждому парсеру, вызывая метод fetch_and_parse у каждого парсера.
    Формирует конченый список уникальных новостей.
    '''
    all_scrapers_articles = list()
    for scraper in self.NEWS_SCRAPERS:
      scraper_articles = scraper().fetch_and_parse(period=period)
      all_scrapers_articles.extend(scraper_articles)
    all_scrapers_articles = self.filter_by_blacklist(all_scrapers_articles)
    all_scrapers_articles = list(set(all_scrapers_articles))
    return all_scrapers_articles