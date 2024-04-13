from bs4 import BeautifulSoup, SoupStrainer
import concurrent.futures
import os
from .article import Article
from pprint import pprint
import requests
import datetime
import time
import logging

logger = logging.getLogger(__name__)

class GoogleScraper:
  def __init__(self):
    pass

  def convert_publish_to_datetime(self, publish_dt):
    time_unit, unit_type, _ = publish_dt.split(maxsplit=2) 
    if 'час' in unit_type:
      publish_time = datetime.datetime.now() - datetime.timedelta(hours=int(time_unit))
    elif 'мин' in unit_type:
      publish_time = datetime.datetime.now() - datetime.timedelta(minutes=int(time_unit))
    else:
      publish_time = datetime.datetime.now()
    return publish_time
   
  def parse_page(self, html):
    logger.info(f'Parsing html page with size {len(html)} bytes')
    only_tags_with_id_search = SoupStrainer(id='search')
    soup = BeautifulSoup(html, 'lxml', parse_only=only_tags_with_id_search)
    search_links = soup.find_all('a')
    result = []
    if len(search_links) == 0:
      logger.info(f'Found {len(result)} articles')
      return result
    for element_a in search_links:
      link = element_a.get('href')
      title = element_a.find(attrs={'role': 'heading'}).string
      source_name = element_a.find('span').string
      publish_time = element_a.find_all('span')[-1].string
      article = Article(
        title=title,
        url=link,
        publish_time=self.convert_publish_to_datetime(publish_time),
        publisher_name=source_name,
        scraper='google',
      )
      result.append(article)
    logger.info(f'Found {len(result)} articles')
    return result

  def fetch_page(self, page_num):
    headers = {
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
    params = {
      'q': 'ЦФА', # query
      'tbm': 'nws', # page section
      'source': 'lnt', # idk
      'tbs': 'lr:lang_1ru,qdr:d', # region and period
      'lr': 'lang_ru', # language
      'start': page_num # page number, because of pagination
    }
    if self.time_period == 'all_available':
      del params['tbs']
    response = requests.get(
        f'https://www.google.com/search',
        params=params,
        headers=headers,
        timeout=5, # seconds
    )
    logger.info(f'Fetched google {response.url}')
    logger.info(f'Fetched status {response.status_code}')
    assert response.status_code == 200
    html = response.text
    return html

  def fetch_page_articles(self, page_num): 
    html = self.fetch_page(page_num)
    _arts = self.parse_page(html)
    return _arts

  def async_fetch_articles(self, time_period):
    self.time_period = time_period
    def async_fetch_batch(page_num_range):
      result = []
      empty_page_flag = False
      with concurrent.futures.ThreadPoolExecutor(max_workers=workers_cnt) as executor:
        future_to_proc_page = { executor.submit(self.fetch_page_articles, page_num): page_num for page_num in page_num_range }
        for future in concurrent.futures.as_completed(future_to_proc_page):
          page_num = future_to_proc_page[future]
          try:
            arts = future.result()
            if len(arts) == 0:
              empty_page_flag = True
            logger.info(f'Page {page_num} arts len {len(arts)}')
            result.extend(arts)
          except Exception as exc:
            logger.error(f'Exception while fetching google page num {page_num} {exc!r}') 
      return result, empty_page_flag
    result = []
    workers_cnt = min(32, (os.cpu_count() or 1) + 4)
    logger.info(f'Fetching google articles with {workers_cnt} workers')
    batch_size = 14
    prev_offset = 0
    page_step = 10
    batch_cnt = 5
    for offset in range(batch_size*page_step, batch_size*page_step*batch_cnt, batch_size*page_step):
      _pages_range = range(prev_offset, offset, page_step)
      logger.info(f'Fetching batch {_pages_range}')
      batch_result, empty_page_flag = async_fetch_batch(_pages_range)
      result.extend(batch_result)
      prev_offset = offset
      logger.info(f'Done fetching batch {_pages_range}')
      if empty_page_flag:
        break
    logger.info(f'Found {len(result)} articles in google')
    return result

  def fetch_articles(self):
    articles = []
    _err_cnt = 0
    for page_num in range(0, 500, 10):
      try:
        _arts = self.fetch_page_articles(page_num)
        if len(_arts) == 0:
          return articles
        articles.extend(_arts)
        time.sleep(.5)
      except Exception as error:
        logger.error(f'Error while fetching google article, try num {_err_cnt}: {error!r}')  
        if _err_cnt == 1:
          break
        _err_cnt += 1
        time.sleep(3)
    return articles

if __name__ == '__main__':
  logging.basicConfig(
    format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
  )
  scrp = GoogleScraper()
  #arts = scrp.fetch_articles()
  arts = scrp.async_fetch_articles()
  print('len arts', len(arts))
  '''
  for i in arts:
    print(i) 
  '''
