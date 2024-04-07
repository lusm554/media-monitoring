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

  # Идея 3 способа:
  # 1. Выбор всех тегов a - название выпуска и ссылка на pdf
  # 2. От тега проходит вверх по дереву, парсить span'ы пока не появится дата - дата выпуска
  
  def parse_platform_method2(platform_div):
    '''
    
    '''
    site_url = 'https://цфа.рф/'
    date_pattern = re.compile(r'^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$')
    last_date = None
    last_span_header = None
    for nxt in platform_div.descendants:
      if nxt.name not in ('span', 'li'): continue
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
          print(is_span_header, span_text) 
        else:
          tag_a = nxt.find('a')
          if tag_a is None:
            continue
          emit_name = tag_a.get_text()
          emit_href = tag_a.get('href')
          #print('\t', emit_name, emit_href)

  def parse_platform_method1(div):
    '''
    Вариант с перебором всех span тегов в div'е платформы.
    По тексту span'а определяется дата.
    Имя выпуска и ссылка на pdf определяется через поиск тега a.
    Проблема: часть выпусков не улавливает, тк название выпуска разбито на несколько span (нахуя - непонятно)
    '''
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
        is_span_header = not any(parent.name == 'li' for n, parent in zip(range(3), span.parents))
        if is_span_header:
          last_span_header = text
        else: 
          if span.find('a') is None:
            continue
          tag_a = span.find('a')
          text = tag_a.string
          href = tag_a.get('href')
          href = urllib.parse.urljoin(site_url, href)
          print(text, href)
          if last_span_header:
            date_emits[last_date][(last_span_header, text)].add(href)
          else:
            date_emits[last_date][text].add(href)
    return date_emits 

  
  for platform_name, platform_emits_div in emits_by_platform.items():
    '''
    if platform_name = 'На платформе А-Токен':
      print(platform_name)
      platform_emits = parse_platform_method2(platform_emits_div)
    else:
      break
    '''
    if True:
      print(platform_name)
      platform_emits = parse_platform_method2(platform_emits_div)     
    if False:
      platform_emits = parse_platform_method1(platform_emits_div)
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
