from bs4 import BeautifulSoup, SoupStrainer
from article import Article
from pprint import pprint
import requests
import datetime

def convert_publish_to_datetime(publish_dt):
  time_unit, unit_type, _ = publish_dt.split(maxsplit=2) 
  if 'час' in unit_type:
    publish_time = datetime.datetime.now() - datetime.timedelta(hours=int(time_unit))
  elif 'мин' in unit_type:
    publish_time = datetime.datetime.now() - datetime.timedelta(minutes=int(time_unit))
  else:
    publish_time = datetime.datetime.now()
  return publish_time
 
def parse_page(html):
  only_tags_with_id_search = SoupStrainer(id='search')
  soup = BeautifulSoup(html, 'lxml', parse_only=only_tags_with_id_search)
  search_links = soup.find_all('a')
  result = []
  if len(search_links) == 0:
    return result
  for element_a in search_links:
    link = element_a.get('href')
    title = element_a.find(attrs={'role': 'heading'}).string
    source_name = element_a.find('span').string
    publish_time = element_a.find_all('span')[-1].string
    article = Article(
      title=title,
      url=link,
      publish_time=convert_publish_to_datetime(publish_time),
      publisher_name=source_name,
    )
    result.append(article)
  return result

headers = {
    'authority': 'www.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"116.0.5843.0"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5843.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"13.4.0"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

if __name__ == '__main__':
  for i in range(0, 500, 10):
    params = {
      'q': 'ЦФА',
      'tbm': 'nws',
      'source': 'lnt',
      'tbs': 'lr:lang_1ru,qdr:d',
      'lr': 'lang_ru',
      'start': i
    }
    response = requests.get(
        f'https://www.google.com/search',
        params=params,
        headers=headers,
    )
    print(response.url)
    html = response.text
    links = parse_page(html)
    if links == []:
      break

    for l in links:
      print(l.title, l.publish_time)
    print();print()
    break