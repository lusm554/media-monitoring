from .base_scraper import BaseScraper
from .release import Release
from collections import defaultdict
from bs4 import BeautifulSoup, SoupStrainer
import datetime
import requests
import re
import urllib
import logging

logger = logging.getLogger(__name__)

class CfaReleasesScraper(BaseScraper):
  '''
  Парсер выпусков ЦФА с сайта цфа.рф.
  Запрашивает HTML страницу, находит платформы и выпуски, парсит в эклземпляры класса Release.
  '''
  def page_fetcher(self):
    '''
    Запрашивает HTML страницы выпусков ЦФА.
    Проверяет статус ответа.
    '''
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
    '''
    Парсит div платформы и преобразует в экземпляр класса Release.
    Так как выпуски платформы разбиты на много элементов,
    но находятся последовательно, их можно парсить проходя по дереву div'а выпуска.
    Каждый выпуск соонтосится со своей датой.
    Итеративно проходит по элементам span и li, проверяет элемент на дату и признак нескольких решений в рамках однгого выпуска.
    Далее находит элемент 'a', формирует эклземпляр Release.
    Из-за уебанской структуры страницы ссылки дублируются и соответственно результаты. Чтобы это избежать выпуски платформы фильтруются через set().
    '''
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
          emit_date = datetime.datetime.strptime(last_date, "%d.%m.%Y")
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

  def page_parser(self, page_html):
    '''
    Находит div'ы выпусков по платформам через заголовки h3 платформ.
    Затем через парсит каждый div платформы через self.page_platform_parser.
    '''
    only_tags_with_id_imcontent = SoupStrainer('main', {'id': 'imContent'})
    soup = BeautifulSoup(
      markup=page_html,
      features='lxml',
      parse_only=only_tags_with_id_imcontent,
    )
    platform_headings = soup.find_all('h3', {'class': 'imHeading3'})
    emits_by_platform = { heading.get_text(): heading.parent for heading in platform_headings }
    releases = set()
    for platform_name, platform_html in emits_by_platform.items():
      platform_releases = self.page_platform_parser(platform_html, platform_name)
      releases.update(platform_releases)
    return releases

  def fetch_and_parse(self, period):
    '''
    Собирает методы вместе, запрашивает код страницы затем парсит ее в экземпляры Release.
    '''
    page_html = self.page_fetcher()
    cfa_releases = self.page_parser(page_html)
    releases_start_time = datetime.datetime.now() - period
    cfa_releases = [
      release
      for release in cfa_releases
      if release.release_time >= releases_start_time
    ]
    return cfa_releases