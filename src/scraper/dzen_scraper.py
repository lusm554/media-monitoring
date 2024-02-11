from bs4 import BeautifulSoup, SoupStrainer
if __name__ == '__main__':
  from article import Article
else:
  from .article import Article
import requests
import datetime
import logging

logger = logging.getLogger(__name__)

class DzenScraper:
  def parse_page(self, html):
    logger.info(f'Parsing html page with size {len(html)} bytes')
    only_tags_with_role_main = SoupStrainer(role='main')
    soup = BeautifulSoup(html, 'lxml', parse_only=only_tags_with_role_main)
    search_articles = soup.find_all('article')
    result = []
    if len(search_articles) == 0:
      logger.info(f'Found {len(result)} articles')
      return result
    for element_article in search_articles:
      element_article_a = element_article.find('a')

      link = element_article_a.get('href')
      title = element_article_a.find('span').get_text()
      source_name = element_article.find(attrs={'class': 'mg-snippet-source-info__agency-name'}).get_text()
      publish_time = element_article.find(attrs={'class': 'mg-snippet-source-info__time'}).get_text()
      publish_time = datetime.datetime.now()

      article = Article(
        title=title,
        url=link,
        publish_time=publish_time,
        publisher_name=source_name,
        scraper='dzen',
      )
      result.append(article)
    logger.info(f'Found {len(result)} articles')
    return result

  def fetch_page(self):
    cookies = {
      'KIykI': '1',
      'HgGedof': '1',
      'zen_sso_checked': '1',
      'yandex_login': '',
      'sso_status': 'sso.passport.yandex.ru:synchronized',
    }
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive',
      'Referer': 'https://sso.dzen.ru/',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'same-site',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
    }
    _now = datetime.datetime.now()
    posix_to = int(_now.timestamp()) * 1000 # to ms
    posix_from = int( (_now - datetime.timedelta(hours=24)).timestamp() ) * 1000 # to ms
    params = {
      'issue_tld': 'ru', # region
      'text': 'ЦФА', # text request
      'filter_date': f'{posix_from},{posix_to}', # time period in unix seconds since 1970
      'flat': '1', # flag for no aggregation by article theme
    }
    response = requests.get('https://dzen.ru/news/search', params=params, headers=headers, cookies=cookies)
    logger.info(f'Fetched dzen {response.url}')
    logger.info(f'Fetched status {response.status_code}')
    assert response.status_code == 200
    html = response.text
    return html

  def fetch_page_articles(self): 
    html = self.fetch_page()
    _arts = self.parse_page(html)
    return _arts

  def fetch_articles(self):
    articles = []
    try:
      _arts = self.fetch_page_articles()
      if len(_arts) == 0:
        return articles
      articles.extend(_arts)
    except Exception as error:
      logger.error(f'Error while fetching dzen article {error!r}')  
    return articles

if __name__ == '__main__':
  scrp = DzenScraper()
  arts = scrp.fetch_articles()
  for art in arts:
    print(art)
    print()
    
