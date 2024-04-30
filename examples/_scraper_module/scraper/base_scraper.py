from abc import abstractmethod
import datetime

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

  @abstractmethod
  def filter_news_by_blacklist(self):
    '''
    Фильтрует новости по черному списку.
    '''
    raise NotImplemented()
