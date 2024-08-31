import sys; sys.path.insert(0,'.')
import scraper_lib as scraper
from pprint import pprint
import pickle

def load_all_scrapers():
  news = scraper.CfaAllNewsScraper(error='ignore').fetch_and_parse(period=scraper.Periods.ALL_AVAILABLE_TIME)
  #news = scraper.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
  result = dict()

  for n in news:
    result[n.title] = n.to_dict()

  with open('news_sample.pickle', 'wb') as f:
    pickle.dump(result, f)

  with open('news_sample.pickle', 'rb') as f:
    result = pickle.load(f)
    print(len(result))

def load_google():
  #news = scraper.CfaGoogleNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.ALL_AVAILABLE_TIME)
  news = scraper.CfaGoogleNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_WEEK)
  #news = scraper.CfaGoogleNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
  result = dict()

  for n in news:
    result[n.title] = n.to_dict()

  pickle_filepath = 'news_sample_google.pickle'
  with open(pickle_filepath, 'wb') as f:
    pickle.dump(result, f)

  with open(pickle_filepath, 'rb') as f:
    result = pickle.load(f)
    print(len(result))

#load_google()

pickle_filepath = 'news_sample_google.pickle'
with open(pickle_filepath, 'rb') as f:
  result = pickle.load(f)
  pprint(result.keys()) 

def save_to_csv():
  with open('news_sample.pickle', 'rb') as f:
    result = pickle.load(f)
    print(len(result))

  import pandas as pd
  df = pd.DataFrame(result.values(), dtype=str)
  print(df.info())
  df.to_csv('raw_news.csv')
