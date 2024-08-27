import sys; sys.path.insert(0,'.')
import scraper_lib as scraper
from pprint import pprint
import dateparser

#news = scraper.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
news = scraper.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.ALL_AVAILABLE_TIME)
print(news)

settings = {'TIMEZONE': 'Europe/Moscow'}
res = dict()
for n in news:
  try:
    t = n.publish_time
    res[t] = str(dateparser.parse(t, settings=settings))
  except Exception as error:
    print(t)
    print(error)
    print()
    print()

pprint(res)
