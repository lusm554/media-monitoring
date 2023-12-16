from rss_scraper import rss_scraper
from pprint import pprint

class Scraper:
  def __init__(self, from_rss, from_google):  
    self.from_rss = from_rss
    self.from_google = from_google 

  def get_articles_from_rss(self):
    rss_articles = rss_scraper().fetch_last_news()
    return rss_articles
    


if __name__ == '__main__':
  scrp = Scraper(from_rss=rss_scraper, from_google=None)
  scrp.get_articles_from_rss()
