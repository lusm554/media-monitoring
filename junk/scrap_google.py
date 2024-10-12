import requests
from fake_headers import Headers
from pprint import pprint

class IO:
  @staticmethod
  def write(obj):
    import pickle
    with open('temp_cache.pickle', 'wb') as f:
      pickle.dump(obj, f)

  @staticmethod
  def read():
    import pickle
    with open('temp_cache.pickle', 'rb') as f:
      obj = pickle.load(f)
    return obj

def get_page_html(url):
  headers = Headers(headers=False).generate()
  pprint(headers)
  r = requests.get(url, headers=headers)
  print(r.status_code)
  assert r.status_code == 200
  html = r.text
  return html

from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint

def parse_page(html):
  only_tags_with_id_search = SoupStrainer(id='search')
  soup = BeautifulSoup(html, 'lxml', parse_only=only_tags_with_id_search)
  links = soup.find_all('a')
  if links == []:
    print(soup.prettify()) 
    return []

  result = []
  for link in links:
    article_link = link.get('href')
    title = link.find(attrs={'role': 'heading'}).string
    source_name = link.find('span').string
    publish_time = link.find_all('span')[-1].string
    print(article_link)
    print(title)
    print(source_name)
    print(publish_time)
    print('\n' * 2)
    print(link.prettify())
    result.append( (title, article_link) )
    break
  return result

'''
html = get_page_html()
#print(html)
IO.write(html)
exit()
'''

first_page_html = IO.read()
parse_page(first_page_html)

