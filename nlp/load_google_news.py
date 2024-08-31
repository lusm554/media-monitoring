import sys; sys.path.insert(0,'.')
import scraper_lib as scraper
from scraper_lib import Periods, Article
import pickle
from bs4 import BeautifulSoup, SoupStrainer
import logging
import requests
import concurrent.futures
import time
import goose3

logger = logging.getLogger(__name__)

import dateparser
import datetime

def unformatted_time2datetime(time_str):
  settings = {'TIMEZONE': 'Europe/Moscow'}
  if isinstance(time_str, datetime.datetime):
    return time_str
  try:
    parsed_dttm = dateparser.parse(time_str, settings=settings)
  except:
    parsed_dttm = datetime.datetime.now()
  return parsed_dttm

class CfaGoogleNewsScraper:
  def __init__(self, *args, **kwargs):
    self.error = 'ignore'
    self.HEADERS = {
      'authority': 'www.google.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cache-control': 'max-age=0',
      'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
      'sec-ch-ua-arch': '"arm"',
      'sec-ch-ua-bitness': '"64"',
      'sec-ch-ua-full-version': '"116.0.5843.0"',
      'sec-ch-ua-full-version-list': '"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5843.0"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-model': '""',
      'sec-ch-ua-platform': '"macOS"',
      'sec-ch-ua-platform-version': '"13.4.0"',
      'sec-ch-ua-wow64': '?0',
      'ec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

  def page_fetcher(self, for_period, page_num):
    '''
    Запрашивает HTML страницу новостей ЦФА гугла за определенный период и номер страницы.
    Проверяет статус ответа.
    '''
    _ggle_fmt_period = 'd'
    if for_period == Periods.LAST_WEEK:
      _ggle_fmt_period = 'w'
    if for_period == Periods.ALL_AVAILABLE_TIME:
      _ggle_fmt_period = 'y'
    params = dict(
      q='ЦФА', # query
      tbm='nws', # page section
      source='lnt', # idk
      tbs=f'lr:lang_1ru,qdr:{_ggle_fmt_period},sbd:1', # region and period # d - day , w - week
      lr='lang_ru', # language
      start=page_num, # page number, because of pagination
    )
    response = requests.get(
      f'https://www.google.ru/search',
      params=params,
      headers=self.HEADERS,
      timeout=5, # seconds
    )
    logger.info(f'Fetched in {response.elapsed.total_seconds():.2f}, {response.request.method} {response.status_code} {response.url!r}')
    assert response.status_code == 200
    html = response.text
    return html

  def page_parser(self, page_html):
    '''
    Парсит страницу новостей. Ищет все ссылки в div'e search.
    Определяет характеристики новости, формирует экземпляр Article.
    Собирает список статей.
    '''
    only_tags_with_id_search = SoupStrainer(id='search')
    soup = BeautifulSoup(page_html, 'lxml', parse_only=only_tags_with_id_search)
    search_links = soup.find_all('a')
    articles_parsed = list()
    for article_link in search_links:
      article_href = article_link.get('href')
      article_title = article_link.find(attrs={'role': 'heading'}).string
      article_source_name = article_link.find('span').string
      article_publish_time = unformatted_time2datetime(
        article_link.find_all('span')[-1].string
      )
      article = Article(
        title=article_title,
        url=article_href,
        publish_time=article_publish_time,
        publisher_name=article_source_name,
        scraper='google',
        body_text=self.add_news_body(article_href)
      )
      articles_parsed.append(article)
    return articles_parsed

  def add_news_body(self, url):
    g = goose3.Goose()
    try:
      text = g.extract(url=url).cleaned_text
      if len(text) == 0:
        text = None
    except Exception as error:
      print(error)
      text = None
    return text

  def fetch_and_parse(self, period):
    '''
    Собирает в себе методы в таски, которые выполняются асинхронно.
    Асинхронно запрашивается и парсится несколько страниц для эффективности.
    '''
    final_articles = set()
    try:
      pages = 31
      n = 3
      for i in range(0, pages, n):
        _range = range(i, i+n)
        print(_range)
        with concurrent.futures.ThreadPoolExecutor() as executor:
          logger.debug(f'{executor._max_workers=}')
          fetch_and_parse_jobs = {
            executor.submit(
              lambda page_num: self.page_parser(
                page_html=self.page_fetcher(
                  for_period=period,
                  page_num=page_num,
                ),
              ),
              page_num
            ): page_num
            for page_num in _range
          }
          for done_job in concurrent.futures.as_completed(fetch_and_parse_jobs):
            cfa_articles = done_job.result()
            final_articles.update(cfa_articles)
        time.sleep(5)
      logger.info(f'Found {len(final_articles)} articles for {period}')
      # extract news text
      #final_articles = self.add_news_body_to_article(final_articles)
      return final_articles
    except Exception as error:
      if self.error == 'raise':
        raise error
      logger.error(error)
      return final_articles

pickle_filepath = 'news_sample_google.pickle'
'''
result = CfaGoogleNewsScraper().fetch_and_parse(scraper.Periods.ALL_AVAILABLE_TIME)
print(len(result))

with open(pickle_filepath, 'wb') as f:
  pickle.dump(result, f)
'''

import pandas as pd
with open(pickle_filepath, 'rb') as f:
  result = pickle.load(f)
  result = [a.to_dict() for a in result]
  result = pd.DataFrame(result)
  result.to_csv('google_news.csv', index=False)
  print(pd.read_csv('google_news.csv').info())


