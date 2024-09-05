import sys; sys.path.insert(0,'.')
import scraper_lib as scraper
from nlp import lsa_summarizer

news = scraper.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
for n in news:
  print(n.body_text)
  print('*'*50)
  print(lsa_summarizer(n.body_text))
  print('*'*50)
  print('*'*50)
