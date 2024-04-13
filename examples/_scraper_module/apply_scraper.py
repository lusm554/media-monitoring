import logging
from scraper import Scraper

logging.basicConfig(
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  level=logging.INFO,
)

Scraper:
  News:
    - rss
    - google
    - dzen
  Emits:
    - cfa_ru

Module public classes:
  CfaAllNewsScraper
  CfaGoogleNewsScraper
  CfaDzenNewsScraper
  CfaRssNewsScraper
  CfaReleasesScraper

  Periods.LAST_24_HOURS
  Periods.LAST_WEEK
  Periods.ALL_AVAILABLE_TIME

CfaAllNewsScraper.fetch_and_parse(period=Periods.LAST_24_HOURS)
CfaReleasesScraper.fetch_and_parse(period=Periods.LAST_WEEK)
