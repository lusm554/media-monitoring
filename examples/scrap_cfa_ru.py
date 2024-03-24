import requests
import datetime

def get_html():
  headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-us,en;q=0.9',
    'connection': 'keep-alive',
    'referer': 'https://sso.dzen.ru/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'upgrade-insecure-requests': '1',
    'user-agent': 'mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/537.36 (khtml, like gecko) chrome/116.0.0.0 safari/537.36',
    'sec-ch-ua': '"not)a;brand";v="24", "chromium";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macos"',
  }

  # https://цфа.рф/cfa-vypusk.html
  url = 'https://цфа.рф/cfa-vypusk.html'
  #res = requests.get(url, headers=headers)
  res = requests.get(url)
  res.encoding = 'utf-8'

  print('status code', res.status_code)
  print('req url', res.url)
  print()
  html = res.text
  return html

def parse_cfaru(html):
  from bs4 import BeautifulSoup, SoupStrainer
  only_tags_with_id_imcontent = SoupStrainer('main', {'id': 'imContent'})
  soup = BeautifulSoup(
    html,
    'lxml',
    parse_only=only_tags_with_id_imcontent,
  )
  return soup.prettify()
  return
  links = soup.find_all('article')
  for l in links:
    title_a = l.find('a')
    #print(title_a.prettify())
    href = title_a.get('href')
    title = title_a.find('span').get_text()
    source_name = l.find(attrs={'class': 'mg-snippet-source-info__agency-name'}).get_text()
    title_publish_time = l.find(attrs={'class': 'mg-snippet-source-info__time'}).get_text()
    print(href)
    print(source_name)
    print(title)
    print(title_publish_time)
    print()

html = get_html()
print(html)
parsed = parse_cfaru(html)
print(parsed)
