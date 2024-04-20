from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup, SoupStrainer
import logging

logger = logging.getLogger(__name__)

class CfaReleasesScraper(BaseScraper):
  def page_fetcher(self):
    response = requests.get(
      f'https://цфа.рф/cfa-vypusk.html',
      timeout=2, # seconds
    )
    response.encoding = 'utf-8'
    logger.info(f'Cfaru fetched url {response.url}')
    logger.debug(f'Fetched status {response.status_code}')
    logger.info(f'Cfaru fetched in {response.elapsed.total_seconds()} seconds')
    assert response.status_code == 200
    html = response.text
    return html
  
  def page_parser(self):
    pass
  
  def fetch_and_parse(self, period):
    pass