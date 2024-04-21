from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup, SoupStrainer
import logging

logger = logging.getLogger(__name__)

class Release:
  __slots__ = ('platform_name', 'url', 'release_time', 'title')
  def __init__(self, platform_name, url, release_time, title):
    self.platform_name = platform_name
    self.url = url
    self.release_time = release_time
    self.title = title

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class')
    return self.url == other.url

  def __ne__(self, other):
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class')
    return self.url != other.url

  def __hash__(self):
    return hash(self.url)

  def __repr__(self):
    items = [ (attr, getattr(self, attr)) for attr in self.__slots__ ]
    return f'{self.__class__.__name__}(\n{",\n".join(f"{k}={v!r}"  for k,v in items)}\n)'

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