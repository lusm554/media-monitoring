import sys; sys.path.insert(0,'.')
import scraper_lib as scraper
from pprint import pprint
import pickle

'''
news = scraper.CfaAllNewsScraper(error='ignore').fetch_and_parse(period=scraper.Periods.ALL_AVAILABLE_TIME)
#news = scraper.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
result = dict()

for n in news:
  result[n.title] = n.to_dict()

with open('news_sample.pickle', 'wb') as f:
  pickle.dump(result, f)

'''
with open('news_sample.pickle', 'rb') as f:
  result = pickle.load(f)
  print(len(result))

import pandas as pd
df = pd.DataFrame(result.values(), dtype=str)
print(df.info())
df.to_csv('raw_news.csv')
