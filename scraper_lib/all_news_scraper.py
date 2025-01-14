from urllib.parse import urlparse
from .base_scraper import NewsBaseScraper
from .dzen_news_scraper import CfaDzenNewsScraper
from .rss_news_scraper import CfaRssNewsScraper
from .google_news_scraper import CfaGoogleNewsScraper
import datetime
import logging

logger = logging.getLogger(__name__)

class CfaAllNewsScraper(NewsBaseScraper):
  '''
  Объединяет в себе все парсеры новостей для удобства парсинга всех новостей за раз.
  '''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if self.error == 'ignore':
      logger.warning(f'Error handler set to {self.error!r}')
    logger.warning(f'Scraper timezone {self.timezone!r}')
    self.NEWS_SCRAPERS = [
      CfaDzenNewsScraper,
      CfaRssNewsScraper,
      CfaGoogleNewsScraper,
    ]

  def filter_by_blacklist(self, articles):
    '''
    Исключает новости, домены которых находятся в черном списке self.cfa_news_url_blacklist.
    '''
    return [
      article for article in articles
      if not urlparse(article.url).netloc in self.cfa_news_url_blacklist
    ]

  def filter_no_cfa_news(self, articles):
    cfa_keys_sentences = [
      'цифровые финансовые активы',
      'цифровых финансовых активов',
      'цифровым финансовым активам',
      'цифровыми финансовыми активами',
      'цифровых финансовых активах',
      'цифровые активы',
    ]
    cfa_keys_words = [
      'цфа',
    ]
    return [
      art for art in articles
      if any(kw==token for token in map(str.strip, str(art.title).lower().split(' ')) for kw in cfa_keys_words)
      or any(ks in str(art.title).lower() for ks in cfa_keys_sentences)
    ]

  def convert_datetimes_timezone(self, articles):
    result = list()
    for a in articles:
      if isinstance(a.publish_time, datetime.datetime):
        a.publish_time = a.publish_time.astimezone(self.timezone)
      result.append(a)
    return result

  def fetch_and_parse(self, period):
    '''
    Забирает новости по каждому парсеру, вызывая метод fetch_and_parse у каждого парсера.
    Формирует конченый список уникальных новостей.
    '''
    all_scrapers_articles = list()
    try:
      for scraper in self.NEWS_SCRAPERS:
        scraper_articles = scraper(error=self.error).fetch_and_parse(period=period)
        all_scrapers_articles.extend(scraper_articles)
      all_scrapers_articles = self.filter_by_blacklist(all_scrapers_articles)
      logger.info(f'Found without cfa key words filter {len(all_scrapers_articles)} articles for {period}')
      all_scrapers_articles = self.filter_no_cfa_news(all_scrapers_articles)
      all_scrapers_articles = self.convert_datetimes_timezone(all_scrapers_articles)
      all_scrapers_articles = list(set(all_scrapers_articles))
      for a in all_scrapers_articles: a.set_hash_attr('title')
      all_scrapers_articles = list(set(all_scrapers_articles))
      for a in all_scrapers_articles: a.set_hash_attr('_filter_url') # default key
      logger.info(f'Found {len(all_scrapers_articles)} articles for {period}')
      logger.info(f'Run {len(self.NEWS_SCRAPERS)} scrapers')
      return all_scrapers_articles
    except Exception as error:
      if self.error == 'raise':
        raise error
      logger.error(error)
      return all_scrapers_articles
