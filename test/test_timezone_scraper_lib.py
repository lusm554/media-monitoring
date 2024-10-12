import sys; sys.path.insert(0, '.')
import scraper_lib as scraper

import datetime
import logging
logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S %Z',
  handlers=[
    logging.StreamHandler(),
  ],
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

'''
releases = scraper.CfaReleasesScraper().fetch_and_parse(scraper.Periods.LAST_WEEK, add_pdf_text=False)
for r in releases:
  print(r.release_time, r.title)
'''

#news = scraper.CfaAllNewsScraper().fetch_and_parse(scraper.Periods.LAST_24_HOURS)
news = scraper.CfaAllNewsScraper().fetch_and_parse(scraper.Periods.LAST_WEEK)
news = sorted(news, key=lambda n: n.publish_time, reverse=True)
for n in news:
	print(n.title)
