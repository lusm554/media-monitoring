class Periods:
  LAST_24_HOURS = 1
  LAST_WEEK = 2
  ALL_AVAILABLE_TIME = 3

class BaseScraper:
  def filter_by_period(self):
    # check for instance of Periods or datetime
    pass
  
  def fetch_and_parse(self):
    pass

class NewsBaseScraper(BaseScraper):
  def __init__(self):
    self.cfa_news_url_blacklist = (
      'echomsk.spb.ru',
      'forpost-sevastopol.ru',
      'adi19.ru',
    )
  
  def filter_news_by_blacklist(self):
    pass


if __name__ == '__main__':
  # print(Periods.LAST_24_HOURS)
  # print(Periods.LAST_WEEK)
  # print(Periods.ALL_AVAILABLE_TIME)
