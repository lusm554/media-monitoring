from rss_scraper import rss_scraper
from google_scraper import GoogleScraper
from pprint import pprint

class Scraper:
  def __init__(self, from_rss, from_google):  
    self.from_rss = from_rss
    self.from_google = from_google 

  def get_articles_from_rss(self):
    rss_articles = self.from_rss().fetch_last_news()
    return rss_articles
    
  def get_articles_from_google(self):
    go_articles = self.from_google().fetch_articles()
    return go_articles

if __name__ == '__main__':
  scrp = Scraper(from_rss=rss_scraper, from_google=GoogleScraper)
  _1 = scrp.get_articles_from_rss()
  _2 = scrp.get_articles_from_google()
  pprint(_1)
  print('\n'*3)
  pprint(_2)

