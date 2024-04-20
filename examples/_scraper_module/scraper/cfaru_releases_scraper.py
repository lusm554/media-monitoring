from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class CfaReleasesScraper(BaseScraper):
  def page_fetcher(self):
    pass
  
  def page_parser(self):
    pass
  
  def fetch_and_parse(self, period):
    pass