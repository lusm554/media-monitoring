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

from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid
import os

class CfaReleasePDF2TextScraper:
  def __init__(self):
    options = ChromeOptions()
    options.add_argument("--headless")
    options.page_load_strategy = 'eager' # normal
    options.add_experimental_option("prefs", {
      "download.default_directory": '/Users/lusm/fromgit/media_monitoring_bot/pdfs',
      "download.directory_upgrade": True,
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "plugins.always_open_pdf_externally": True,
      "safebrowsing.disable_download_protection": True,
    })
    driver = webdriver.Chrome(options=options)
    self.driver = driver

  def __check_element_disappear__(self, driver):
    try:
      driver.find_element(By.XPATH, '//div[@id="preloader"]')
      return False
    except NoSuchElementException:
      return True

  def __check_file_downloaded__(self, filepath):
    filepath = '/Users/lusm/fromgit/media_monitoring_bot/pdfs/' + filepath
    return lambda _: os.path.isfile(filepath)

  def parse_pdf_to_text(self, pdf_filepath):
    from pdfminer.high_level import extract_text
    import re
    pdf_filepath = '/Users/lusm/fromgit/media_monitoring_bot/pdfs/' + pdf_filepath
    text = extract_text(pdf_filepath)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    print(len(text))
    return text

  def fetch_and_parse(self, cfa_url):
    try:
      driver = self.driver
      driver.get(cfa_url)
      WebDriverWait(driver, timeout=15).until(self.__check_element_disappear__)
      btn = WebDriverWait(driver, timeout=30).until(
        EC.element_to_be_clickable(
          (By.XPATH, '//button[(@aria-label="Download") and (@class="svg-button icon group2")]')
        )
      )
      driver.execute_script("arguments[0].click();", btn);
      btn = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@class="download-full-button"]'))
      )
      filepath = '_'.join([str(uuid.uuid4()), *cfa_url.split('/')[-2:]]).lower() + '.pdf'
      driver.execute_script("arguments[0].setAttribute('download',arguments[1])", btn, filepath)
      driver.execute_script("arguments[0].click();", btn);
      WebDriverWait(driver, timeout=15, ).until(self.__check_file_downloaded__(filepath))
      pdf_text = self.parse_pdf_to_text(filepath)
      return pdf_text
    except:
      raise ValueError('Cannot get pdfs from url.')

  def driver_quite(self):
    self.driver.quit()

class CfaReleasesScraper(BaseScraper):
  '''
  Парсер выпусков ЦФА с сайта цфа.рф.
  Запрашивает HTML страницу, находит платформы и выпуски, парсит в эклземпляры класса Release.
  '''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if self.error == 'ignore':
      logger.warning(f'Error handler set to {self.error!r}')
    self.pdf2text_scraper = CfaReleasePDF2TextScraper()

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
    logger.info(f'Fetched in {response.elapsed.total_seconds():.2f}, {response.request.method} {response.status_code} {response.url!r}')
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
    for nxt in platform_html.find_all(['b', 'span', 'li']):
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
          emit_date = datetime.datetime(year=2000, month=1, day=1) if last_date is None else datetime.datetime.strptime(last_date, "%d.%m.%Y")
          if last_span_header:
            emit_name = f'{last_span_header} {emit_name}'
          release = Release(
            platform_name=platform_name,
            url=emit_href,
            release_time=emit_date,
            title=emit_name,
          )
          platform_releases.add(release)
    logger.debug(f'For {platform_name!r} parsed {len(platform_releases)} releases')
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
    logger.info(f'Found {len(emits_by_platform)} platforms')
    releases = set()
    for platform_name, platform_html in emits_by_platform.items():
      platform_releases = self.page_platform_parser(platform_html, platform_name)
      releases.update(platform_releases)
    return releases

  def add_pdf_text(self, release):
    if release.url.endswith('.pdf'):
      return release
    release_dict = release.to_dict()
    release_dict['pdf_text'] = self.pdf2text_scraper.fetch_and_parse(release.url)
    release = Release.from_dict(release_dict)
    return release

  def fetch_and_parse(self, period, add_pdf_text=False):
    '''
    Собирает методы вместе, запрашивает код страницы затем парсит ее в экземпляры Release.
    '''
    cfa_releases = []
    try:
      page_html = self.page_fetcher()
      cfa_releases = self.page_parser(page_html)
      releases_start_time = datetime.datetime.now() - period
      cfa_releases = [
        release
        for release in cfa_releases
        if release.release_time >= releases_start_time
      ]
      if add_pdf_text:
        cfa_releases = [self.add_pdf_text(release) for release in cfa_releases]
      logger.info(f'Found {len(cfa_releases)} releases for {period}')
      return cfa_releases
    except Exception as error:
      if self.error == 'raise':
        raise error
      logger.error(error)
      return cfa_releases



