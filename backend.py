import bot
import storage
import os

import locale
locale.setlocale(
  category=locale.LC_ALL,
  locale='ru_RU',
)

import datetime
import logging
logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S %Z',
  handlers=[
    #logging.FileHandler(datetime.datetime.now().strftime('shared/logs/log_%Y-%m-%d_%H-%M-%S.log')),
    logging.StreamHandler(),
  ],
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

storage.create_tables_if_not_exists()
#storage.recreate_tables()

'''
import scraper_lib
import nlp
releases_scraper = scraper_lib.CfaReleasesScraper(error='ignore')

def get_releases_not_in_db(scraper_releases):
  scraper_releases_in_db = storage.get_releases([c.url for c in scraper_releases])
  scraper_releases_in_db_urls = {t['url'] for t in scraper_releases_in_db}
  scraper_releases_not_in_db = [r for r in scraper_releases if r.url not in scraper_releases_in_db_urls]
  return scraper_releases_not_in_db

scraper_releases = releases_scraper.fetch_and_parse(scraper_lib.Periods.LAST_WEEK)
releases_not_in_db = get_releases_not_in_db(scraper_releases) # 1. Get releases not in db
print(len(scraper_releases))
print(len(releases_not_in_db))

releases = [releases_scraper.add_pdf_text(r) for r in releases_not_in_db] # 2. Get pdf, convert to text
for r in releases:
  desc = nlp.release_text_to_desc(r.pdf_text) # 3. Pdf text ner
  for k,v in desc.items():
    setattr(r, k, v)

storage.add_releases(releases) # 4. Save releases to db

print(len(storage.get_n_releases()))
print((storage.get_n_releases()))
exit()
'''

'''
from pprint import pprint
import scraper_lib
releases = scraper_lib.CfaReleasesScraper(error='ignore').fetch_and_parse(scraper_lib.Periods.LAST_WEEK)
print(releases)
storage.add_releases(releases)
print(storage.get_n_releases())

articles = scraper_lib.CfaAllNewsScraper(error='ignore').fetch_and_parse(period=scraper_lib.Periods.LAST_24_HOURS)
storage.add_news(articles)
articles = storage.get_n_news()
pprint(articles)
exit()
'''

BOT_TOKEN = os.getenv('BOT_TOKEN')
assert BOT_TOKEN
bot.start(BOT_TOKEN)
