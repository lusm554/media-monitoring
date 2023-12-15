import requests
from pprint import pprint

def parse_page(html):
  from bs4 import BeautifulSoup, SoupStrainer
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
    result.append( (title, article_link, source_name) )
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

for i in range(0, 500, 10):
  response = requests.get(
      f'https://www.google.com/search?q=%D0%A6%D0%A4%D0%90&tbm=nws&source=lnt&tbs=qdr:d&start={i}',
      headers=headers,
  )
  print(response.url)
  html = response.text
  links = parse_page(html)
  if links == []:
    break
  pprint(links) 
  print();print()

