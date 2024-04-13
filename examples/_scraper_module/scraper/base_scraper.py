class Periods:
  '''
  Класс периодов для фильтрации новостей и выпусков.
  '''
  LAST_24_HOURS = 1
  LAST_WEEK = 2
  ALL_AVAILABLE_TIME = 3

class BaseScraper:
  '''
  Базовый класс для всех скреперов.
  Содержит общие методы для всех скреперов. 
  '''
  def filter_by_period(self):
    # check for instance of Periods or datetime
    pass
  
  def fetch_and_parse(self):
    pass

class NewsBaseScraper(BaseScraper):
  '''
  Базовый класс для скреперов новостей.
  Содержит общие методы для скреперов новостей. 
  '''
  def __init__(self):
    self.cfa_news_url_blacklist = (
      'echomsk.spb.ru',
      'forpost-sevastopol.ru',
      'adi19.ru',
    )
  
  def filter_news_by_blacklist(self):
    pass
