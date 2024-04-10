import requests
from bs4 import BeautifulSoup, SoupStrainer
from collections import defaultdict
import re
from pprint import pprint
import urllib
import datetime

def fetch_cfa_ru_html():
  url = 'https://цфа.рф/cfa-vypusk.html'
  res = requests.get(url)
  res.encoding = 'utf-8'
  html = res.text
  print('Status code', res.status_code)
  print('Url', res.url)
  print(f'Fetched in {res.elapsed.total_seconds()} seconds')
  print()
  return html
 
def parse_emits_page(html):
  only_tags_with_id_imcontent = SoupStrainer('main', {'id': 'imContent'})
  soup = BeautifulSoup(
    markup=html,
    features='lxml',
    parse_only=only_tags_with_id_imcontent,
  )
  platform_headings = soup.find_all('h3', {'class': 'imHeading3'})
  emits_by_platform = { heading.get_text(): heading.parent for heading in platform_headings }

  def parse_platform(platform_div):
    site_url = 'https://цфа.рф/'
    date_pattern = re.compile(r'^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$')
    last_date = None
    last_span_header = None
    date_emits = defaultdict(lambda: defaultdict(set))
    for nxt in platform_div.find_all(['span', 'li']):
      span_text = nxt.get_text()
      span_text = span_text.strip()
      if span_text == '':
        continue
      is_date = date_pattern.match(span_text)       
      if is_date:
        last_date = span_text
        last_span_header = None
      else:
        is_span_header = not any(parent.name == 'li' for n, parent in zip(range(3), nxt.parents))
        if is_span_header and nxt.name =='span':
          last_span_header = span_text
        else:
          tag_a = nxt.find('a')
          if tag_a is None:
            continue
          emit_name = tag_a.get_text()
          emit_href = tag_a.get('href')
          emit_href = urllib.parse.urljoin(site_url, emit_href)
          if last_span_header:
            date_emits[last_date][(last_span_header, emit_name)].add(emit_href)
          else:
            date_emits[last_date][emit_name].add(emit_href)
    return date_emits

  result_emits_by_platform = dict()
  show_log = False
  for platform_name, platform_emits_div in emits_by_platform.items():
    if show_log:
      print(platform_name)
    platform_emits = parse_platform(platform_emits_div)     
    result_emits_by_platform[platform_name] = platform_emits
    _platform_emits = sorted(platform_emits.items(), key=lambda x: datetime.datetime.strptime(x[0], '%d.%m.%Y'), reverse=True)
    if show_log:
      for k,v in _platform_emits:
        print(k)
        for kk, vv in v.items():
          print('\t', kk, vv)
        print()
      print()
      print()
  return result_emits_by_platform

def emits_to_telegram_format(emits):
  msg = ''
  for platform_name, emits in emits.items():
    if platform_name != 'На платформе А-Токен':
      continue
    msg += f'{platform_name}\n'
    for emit_date, date_emits in emits.items():
      msg += f'\t{emit_date}\n' 
      for emit_name, emit_href in date_emits.items():
        if isinstance(emit_name, tuple):
          emit_name = ', '.join(emit_name)
        emit_href = list(emit_href)[0]
        msg += f'\t\t{emit_name} - {emit_href}\n' 
  print(msg)
  print(len(msg))
    

def main():
  cfa_emits_page_html = fetch_cfa_ru_html()
  emits = parse_emits_page(cfa_emits_page_html)
  print(f'{len(emits)=}')
  print(emits.keys())
  print()
  print()
  print()
  emits_to_telegram_format(emits)

if __name__ == '__main__':
  main()
