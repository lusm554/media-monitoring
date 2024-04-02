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
  platform_headings = soup.find_all('h3', {'class': 'imHeading3'})
  
  from pprint import pprint
  pprint(platform_headings)
  print()
  print()

  emits_by_platform = { heading.get_text(): heading.parent for heading in platform_headings }

  def parse_platform(_):
    import re
    date_patter = re.compile(r'^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$')
    from collections import defaultdict
    last_day = None 
    day_emits = defaultdict(set)
    for ch in _.find_all('span'):
      ch = ch.get_text()
      ch = ch.strip()
      #is_date = datetime.strptime(ch, '%d.%m.%Y')
      is_date = date_patter.match(ch)
      if is_date:
        last_day = ch
      else:
        if ch != '':
          day_emits[last_day].add(ch)
    pprint(day_emits)

  for name, _ in emits_by_platform.items():
    print(name)
    parse_platform(_)
    print()
    print()
    print()


html = get_html()
#print(html)
parsed = parse_cfaru(html)
#print(parsed)
