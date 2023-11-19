from fetch_rss import RSSDAO, RSS_FEEDS

def fetch_data():
  rss = RSSDAO(feeds=RSS_FEEDS)
  feeds = rss.fetch()
  yield from feeds

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
        yield fobj, entry

def io(op, *args):
  import pickle
  def write(data, filepath):
    with open(filepath, 'wb') as f:
      pickle.dump(data, f)
  def read(filepath):
    with open(filepath, 'rb') as f:
      return pickle.load(f)
  if op == 'write':
    return write(*args)
  elif op == 'read':
    return read(*args)

def last_news_rss():
  input_data = fetch_data()
  kwfeeds = process(input_data)
  result = list(kwfeeds)
  #io('write', result, 'cache.pickle')
  #result = io('read', 'cache.pickle')
  return result

if __name__ == '__main__':
  last_news_rss()
