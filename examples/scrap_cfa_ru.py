import requests
import datetime
from bs4 import BeautifulSoup, SoupStrainer
from collections import defaultdict
import re
from pprint import pprint
import urllib

def get_html():
  url = 'https://цфа.рф/cfa-vypusk.html'
  res = requests.get(url)
  res.encoding = 'utf-8'
  html = res.text
  print('Status code', res.status_code)
  print('Url', res.url)
  print(f'Fetched in {res.elapsed.total_seconds()} seconds')
  print()
  return html

def parse_cfaru(html):
  only_tags_with_id_imcontent = SoupStrainer('main', {'id': 'imContent'})
  soup = BeautifulSoup(
    markup=html,
    features='lxml',
    parse_only=only_tags_with_id_imcontent,
  )
  
  platform_headings = soup.find_all('h3', {'class': 'imHeading3'})
  emits_by_platform = { heading.get_text(): heading.parent for heading in platform_headings }

  def parse_platform(div):
    site_url = 'https://цфа.рф/'
    date_pattern = re.compile(r'^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$')
    last_date = None 
    last_span_header = None
    date_emits = defaultdict(lambda: defaultdict(set))
    for span in div.find_all('span'):
      text = span.get_text()
      text = text.strip()
      if text == '':
        continue
      is_date = date_pattern.match(text)
      if is_date:
        last_date = text
        last_span_header = None
      else:
        if last_date == '12.10.2023':
          print(text)
        is_span_header = not any(parent.name == 'li' for n, parent in zip(range(3), span.parents))
        if is_span_header:
          #print(is_span_header, text)
          last_span_header = text
        else: 
          if span.find('a') is None:
            continue
          href = span.find('a').get('href')
          href = urllib.parse.urljoin(site_url, href)
          #print(text, href)
          if last_span_header:
            date_emits[last_date][(last_span_header, text)].add(href)
          else:
            date_emits[last_date][text].add(href)
    return date_emits 

  
  for platform_name, platform_emits_div in emits_by_platform.items():
    if platform_name != 'На платформе А-Токен':
      continue
    print(platform_name)
    platform_emits = parse_platform(platform_emits_div)
    break
    #pprint(platform_emits)
    for k,v in sorted(platform_emits.items(), key=lambda x: datetime.datetime.strptime(x[0], '%d.%m.%Y'), reverse=True):
      print(k)
      for kk, vv in v.items():
        print('\t', kk, vv)
      print()
    print()
    print()
    print()

html = get_html()
parsed = parse_cfaru(html)
