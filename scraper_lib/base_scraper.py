from abc import abstractmethod
import datetime
import concurrent.futures
import goose3

class Periods:
  '''
  Класс периодов для фильтрации новостей и выпусков.
  '''
  LAST_24_HOURS = datetime.timedelta(hours=24)
  LAST_WEEK = datetime.timedelta(weeks=1)
  ALL_AVAILABLE_TIME = datetime.timedelta(weeks=104)

class BaseScraper:
  '''
  Базовый класс для всех скреперов.
  Содержит общие методы для всех скреперов. 
  '''
  def __init__(self, error='raise'):
    if not error in ('raise', 'ignore'):
      raise ValueError(f"error argument should be 'raise' or 'ignore'")
    self.error = error

  def filter_by_period(self):
    raise NotImplemented()

  @abstractmethod
  def fetch_and_parse(self, period):
    raise NotImplemented()

  def __repr__(self):
    cls_name = self.__class__.__name__
    return f'{cls_name}()'

class NewsBaseScraper(BaseScraper):
  '''
  Базовый класс для скреперов новостей.
  Содержит общие методы для скреперов новостей. 
  '''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.cfa_news_url_blacklist = (
      'echomsk.spb.ru',
      'forpost-sevastopol.ru',
      'adi19.ru',
    )

  def add_news_body_to_article(self, articles):
    g = goose3.Goose()
    def get_article_text(url):
      try:
        text = g.extract(url=url).cleaned_text
        if len(text) == 0:
          text = None
      except Exception as error:
        print(error)
        text = None
      return text
    result = set()
    with concurrent.futures.ThreadPoolExecutor() as executor:
      fetch_and_parse_jobs = {
        executor.submit(
          get_article_text,
          article.url
        ): article
        for article in articles
      }
      for done_job in concurrent.futures.as_completed(fetch_and_parse_jobs):
        article = fetch_and_parse_jobs[done_job]
        article_body_text = done_job.result()
        article.body_text = article_body_text
        result.add(article)
    return result

  @abstractmethod
  def filter_news_by_blacklist(self):
    '''
    Фильтрует новости по черному списку.
    '''
    raise NotImplemented()
