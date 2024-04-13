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
  CfaNewsScraper
  CfaGoogleNewsScraper
  CfaDzenNewsScraper
  CfaRssNewsScraper
  CfaReleasesScraper

