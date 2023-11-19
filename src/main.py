from fetch_rss import RSSDAO, RSS_FEEDS

from pprint import pprint

def fetch_data():
  rss = RSSDAO(feeds=RSS_FEEDS)
  feeds = rss.fetch()
  yield from feeds
  #rss.save_rss(next(feeds))
  #return [rss.read_rss()]

def process(feeds):
  def check_kw(text):
    if not isinstance(text, str): return False
    text = text.lower()
    flag = False
    if 'цфа' in text:
      flag = True
    if 'цифровые финансовые активы' in text:
      flag = True
    return flag

  for fobj, f in feeds:
    for entry in f.entries:
      title = entry.get('title')
      if check_kw(title):
        pprint(entry)
        yield entry

def main():
  input_data = fetch_data()
  kwfeeds = process(input_data)
  for _ in kwfeeds:
    pass


if __name__ == '__main__':
  main()
