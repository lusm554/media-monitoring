import re
import os
import requests
from pprint import pprint

def search_in_txt(filepath):
  print(filepath)
  url_pattern = "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
  with open(filepath, 'r') as file:
    for line in file:
      res = re.findall(url_pattern, line) 
      yield from res

def walk_dir(path='./', fext='.txt'):
  for root, dirs, files in os.walk(path):
    for name in files:
      if fext in name:
        yield os.path.join(root, name)
    for d in dirs:
      yield from walk_dir(os.path.join(root, name))

def filter_rss(source_url):
  try:
    _url = f'https://{source_url}/rss'
    r = requests.get(_url)
    cntnt = r.headers.get('Content-Type')
    if r.status_code == 200 and ('xml' in cntnt or 'rss' in cntnt):
      return True
  except Exception as e:
    return False
  return False

def main():
  txt_news_sources = ( search_in_txt(filepath) for filepath in walk_dir() )
  txt_news_sources = ( src for batch in txt_news_sources for src in batch )
  txt_news_sources = { src for src in txt_news_sources }
  valid_news_sources = ( src for src in txt_news_sources if filter_rss(src) )
  result = list(valid_news_sources)
  print(result)

if __name__ == '__main__':
  main()
