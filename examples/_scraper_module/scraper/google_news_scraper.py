from .base_scraper import NewsBaseScraper, Periods
import requests
import time
import logging

logger = logging.getLogger(__name__)

class CfaGoogleNewsScraper(NewsBaseScraper):
  def __init__(self):
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

  def page_fetcher(self, for_period):
    for page_num in range(10):
      _ggle_fmt_period = 'd'
      if for_period == Periods.LAST_WEEK:
        _ggle_fmt_period = 'w'
      params = dict(
        q='ЦФА', # query
        tbm='nws', # page section
        source='lnt', # idk
        tbs=f'lr:lang_1ru,qdr:{_ggle_fmt_period}', # region and period # d - day , w - week
        lr='lang_ru', # language
        start=page_num, # page number, because of pagination
      )
      response = requests.get(
        f'https://www.google.ru/search',
        params=params,
        headers=self.HEADERS,
        timeout=2, # seconds
      )
      logger.info(f'Google fetched url {response.url}')
      logger.debug(f'Fetched status {response.status_code}')
      logger.info(f'Google fetched in {response.elapsed.total_seconds()} seconds')
      assert response.status_code == 200
      html = response.text
      yield html
      time.sleep(.05)


