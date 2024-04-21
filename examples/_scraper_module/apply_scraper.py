import logging
from pprint import pprint
logging.basicConfig(
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  level=logging.INFO,
)

'''
TODO:
  1. Doc strings
  2. logging
'''

def how_to_apply_cfaru_releases_scraper():
  from scraper import CfaReleasesScraper, Periods
  # cfa_releases = CfaReleasesScraper().fetch_and_parse(period=Periods.LAST_24_HOURS)
  cfa_releases = CfaReleasesScraper().fetch_and_parse(period=Periods.LAST_WEEK)
  plt = None
  for release in sorted(cfa_releases, key=lambda x:x.platform_name):
    if plt != release.platform_name:
      plt = release.platform_name
      print(plt)
      print('\t', release.release_time, release.title)
    else:
      print('\t', release.release_time, release.title)
how_to_apply_cfaru_releases_scraper()

def how_to_apply_dzen_news_scraper():
  from scraper import CfaDzenNewsScraper, Periods
  dzen_news = CfaDzenNewsScraper().fetch_and_parse(period=Periods.LAST_24_HOURS)
  # dzen_news = CfaDzenNewsScraper().fetch_and_parse(period=Periods.LAST_WEEK)
  pprint(dzen_news)
# how_to_apply_dzen_news_scraper()

def how_to_apply_rss_news_scraper():
  from scraper import CfaRssNewsScraper, Periods
  rss_news = CfaRssNewsScraper().fetch_and_parse(period=Periods.LAST_24_HOURS)
  # rss_news = CfaRssNewsScraper().fetch_and_parse(period=Periods.LAST_WEEK)
  pprint(rss_news)
# how_to_apply_rss_news_scraper()

def how_to_apply_google_news_scraper():
  from scraper import CfaGoogleNewsScraper, Periods
  google_news = CfaGoogleNewsScraper().fetch_and_parse(period=Periods.LAST_24_HOURS)
  # google_news = CfaGoogleNewsScraper().fetch_and_parse(period=Periods.LAST_WEEK)
  print(f'{len(google_news)=}')
  pprint(google_news)
# how_to_apply_google_news_scraper()

def how_to_apply_all_news_scraper():
  from scraper import CfaAllNewsScraper, Periods
  all_news = CfaAllNewsScraper().fetch_and_parse(period=Periods.LAST_24_HOURS)
  # all_news = CfaAllNewsScraper().fetch_and_parse(period=Periods.LAST_WEEK)
  print(f'{len(all_news)=}')
  print(f'{len(set(all_news))=}')
  pprint(all_news[:5])
# how_to_apply_all_news_scraper()

'''
Scraper:
  News:
    - rss
    - google
    - dzen
  Emits:
    - cfa_ru
  Other info:
    - conds cfa

Module public classes:
  CfaAllNewsScraper
    - join_articles
    - fetch_and_parse
      1. fetch_and_parse from CfaGoogleNewsScraper, CfaDzenNewsScraper, CfaRssNewsScraper
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