from urllib.parse import urlparse
from .base_scraper import NewsBaseScraper
from .dzen_news_scraper import CfaDzenNewsScraper
from .rss_news_scraper import CfaRssNewsScraper
from .google_news_scraper import CfaGoogleNewsScraper

class CfaAllNewsScraper(NewsBaseScraper):
  def __init__(self):
    super().__init__()
    self.NEWS_SCRAPERS = [
      CfaDzenNewsScraper,
      CfaRssNewsScraper,
      CfaGoogleNewsScraper,
    ]

  def filter_by_blacklist(self, articles):
    return [
      article for article in articles
      if not urlparse(article.url).netloc in self.cfa_news_url_blacklist
    ]
