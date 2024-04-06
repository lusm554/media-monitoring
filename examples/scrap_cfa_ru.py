import requests
import datetime
from bs4 import BeautifulSoup, SoupStrainer
from collections import defaultdict
import re
from pprint import pprint

def get_html():
  url = 'https://цфа.рф/cfa-vypusk.html'
  res = requests.get(url)
  res.encoding = 'utf-8'
  html = res.text
  print('Status code', res.status_code)
  print('Url', res.url)
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
  def parse_platform(_):
    date_patter = re.compile(r'^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$')
    last_day = None 
    day_emits = defaultdict(set)
    for ch in _.find_all('span'):
      ch = ch.get_text()
      ch = ch.strip()
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

html = get_html()
parsed = parse_cfaru(html)
