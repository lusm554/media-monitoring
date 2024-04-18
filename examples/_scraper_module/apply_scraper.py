import logging
from pprint import pprint
logging.basicConfig(
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  level=logging.INFO,
)

#from scraper import CfaDzenNewsScraper, Periods
#dzen_news = CfaDzenNewsScraper().fetch_and_parse(period=Periods.LAST_24_HOURS)
#dzen_news = CfaDzenNewsScraper().fetch_and_parse(period=Periods.LAST_WEEK)
#pprint(dzen_news)

from scraper import CfaRssNewsScraper, Periods
rss_news = CfaRssNewsScraper().fetch_and_parse(period=Periods.LAST_24_HOURS)
pprint(rss_news)

'''
Scraper:
  News:
    - rss
    - google
    - dzen
  Emits:
    - cfa_ru

Module public classes:
  CfaAllNewsScraper
    - join_articles
    - fetch_and_parse
      1. fetch_and_parse from CfaGoogleNewsScraper, CfaDzenNewsScraper, CfaRssNewsScraper, CfaReleasesScraper
      2. join_articles
  CfaGoogleNewsScraper
    - fetch_and_parse
      1. filter_by_period
      2. filter_by_blacklist
  CfaDzenNewsScraper
    - fetch_and_parse
      1. filter_by_period
      2. filter_by_blacklist
  CfaRssNewsScraper
    - fetch_and_parse
      1. filter_by_period
      2. filter_by_blacklist
  CfaReleasesScraper
    - fetch_and_parse
      1. filter_by_period
      2. filter_by_blacklist

Common things among classes:
  BaseScraper:
    - news url blacklist
    - filter_by_blacklist
    - __repr__ method
    - filter_by_period method

Periods:
  Periods.LAST_24_HOURS
  Periods.LAST_WEEK
  Periods.ALL_AVAILABLE_TIME

CfaAllNewsScraper.fetch_and_parse(period=Periods.LAST_24_HOURS)
CfaReleasesScraper.fetch_and_parse(period=Periods.LAST_WEEK)
'''