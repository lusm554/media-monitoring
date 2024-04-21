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
  
  def page_platform_parser(self, platform_html, platform_name):
    site_url = 'https://цфа.рф/'
    date_pattern = re.compile(r'^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$')
    last_date = None
    last_span_header = None
    platform_releases = set()
    for nxt in platform_html.find_all(['span', 'li']):
      span_text = nxt.get_text()
      span_text = span_text.strip()
      if span_text == '':
        continue
      if date_pattern.match(span_text):
        last_date = span_text
        last_span_header = None
      else:
        is_span_header = not any(parent.name == 'li' for n, parent in zip(range(3), nxt.parents))
        if is_span_header and nxt.name =='span':
          last_span_header = span_text
        else:
          tag_a = nxt.find('a')
          if tag_a is None:
            continue
          emit_name = tag_a.get_text()
          emit_href = urllib.parse.urljoin(site_url, tag_a.get('href'))
          emit_date = last_date
          if last_span_header:
            emit_name = f'{last_span_header} {emit_name}'
          release = Release(
            platform_name=platform_name,
            url=emit_href,
            release_time=emit_date,
            title=emit_name,
          )
          platform_releases.add(release)
    return platform_releases

  def fetch_and_parse(self, period):
    pass