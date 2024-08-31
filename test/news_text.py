import sys; sys.path.insert(0,'.')
import scraper_lib as scraper
from scraper_lib import Article
import datetime
from pprint import pprint

#news = scraper.CfaGoogleNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
news = scraper.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
pprint(news)

exit()

#news = scraper.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
CfaGoogleNewsScraper
#pprint(news)
articles =[Article(
title='«Газпром» показал рост финансовых показателей в первом полугодии',
url='https://www.vedomosti.ru/business/articles/2024/08/30/1058910-gazprom-pokazal-rost-finansovih-pokazatelei-v-pervom-polugodii',
publish_time=datetime.datetime(2024, 8, 30, 0, 57, 35, 736090),
publisher_name='Ведомости',
scraper='google',
db_id=None
),
 Article(
title='Депутат Рады призвал жителей украинского Покровска эвакуироваться',
url='https://www.vedomosti.ru/politics/news/2024/08/29/1058860-deputat-radi-prizval',
publish_time=datetime.datetime(2024, 8, 29, 17, 57, 35, 711814),
publisher_name='Ведомости',
scraper='google',
db_id=None
),
 Article(
title='ПВО сбила ночью 18 украинских беспилотников',
url='https://www.vedomosti.ru/politics/news/2024/08/30/1058925-pvo-sbila-nochyu',
publish_time=datetime.datetime(2024, 8, 30, 7, 57, 35, 748592),
publisher_name='Ведомости',
scraper='google',
db_id=None
),
 Article(
title='Новый этап тестирования цифрового рубля стартует 1 сентября 2024',
url='https://bosfera.ru/press-release/novyy-etap-testirovaniya-cifrovogo-rublya-startuet-1-sentyabrya-2024?utm_source=yxnews&utm_medium=desktop&utm_referrer=https%3A%2F%2Fdzen.ru%2Fnews%2Fsearch%3Ftext%3D',
publish_time=datetime.datetime(2024, 8, 30, 11, 30),
publisher_name='Банковское обозрение',
scraper='dzen',
db_id=None
),
 Article(
title='Революция микрозаймов: ЦБ собирается кардинально реформировать рынок МФО',
url='https://www.dp.ru/a/2024/08/30/revoljucija-mikrozajmov-cb?utm_source=yxnews&utm_medium=desktop&utm_referrer=https%3A%2F%2Fdzen.ru%2Fnews%2Fsearch%3Ftext%3D',
publish_time=datetime.datetime(2024, 8, 30, 7, 0),
publisher_name='DP.RU',
scraper='dzen',
db_id=None
),
 Article(
title='Песков: арест граждан Колумбии в Москве не относится к темам АП',
url='https://www.vedomosti.ru/politics/news/2024/08/30/1059012-peskov-arest-grazhdan',
publish_time=datetime.datetime(2024, 8, 30, 12, 57, 35, 727994),
publisher_name='Ведомости',
scraper='google',
db_id=None
),
 Article(
title='Финансовый менеджер: какие задачи выполняет и какие навыки ему нужны',
url='https://www.fd.ru/articles/163157-finansovyy-menedjer-kakie-zadachi-vypolnyaet-i-kakie-navyki-emu-nujny?utm_source=yxnews&utm_medium=desktop&utm_referrer=https%3A%2F%2Fdzen.ru%2Fnews%2Fsearch%3Ftext%3D',
publish_time=datetime.datetime(2024, 8, 30, 2, 6),
publisher_name='Финансовый директор',
scraper='dzen',
db_id=None
),
 Article(
title='Генштаб ВСУ признал крушение истребителя F-16',
url='https://www.vedomosti.ru/politics/news/2024/08/29/1058887-genshtab-vsu-priznal',
publish_time=datetime.datetime(2024, 8, 29, 20, 57, 35, 726477),
publisher_name='Ведомости',
scraper='google',
db_id=None
),
 Article(
title='Рынок решений для безопасной разработки софта может вырасти в 6 раз за 4 \nгода',
url='https://www.vedomosti.ru/technology/articles/2024/08/30/1058904-rinok-reshenii-dlya-bezopasnoi-razrabotki-softa-mozhet-virasti',
publish_time=datetime.datetime(2024, 8, 30, 0, 57, 35, 733780),
publisher_name='Ведомости',
scraper='google',
db_id=None
),
 Article(
title='Названы самые инновационные банки в России',
url='https://www.sravni.ru/novost/2024/8/30/nazvany-samye-innovaczionnye-banki-v-rossii/?utm_source=yxnews&utm_medium=desktop&utm_referrer=https%3A%2F%2Fdzen.ru%2Fnews%2Fsearch%3Ftext%3D',
publish_time=datetime.datetime(2024, 8, 30, 9, 0),
publisher_name='Сравни.ру',
scraper='dzen',
db_id=None
),
 Article(
title='Венеция-2024: с Леди Гагой, но без Netflix',
url='https://vedomosti.ru/lifestyle/articles/2024/08/30/1058875-venetsiya-2024-s-ledi-gagoi-no-bez-netflix',
publish_time=datetime.datetime(2024, 8, 29, 23, 57, 35, 732775),
publisher_name='Ведомости',
scraper='google',
db_id=None
),
 Article(
title='Эволюция управления активами',
url='https://elitetrader.ru/index.php?newsid=712089&utm_source=yxnews&utm_medium=desktop&utm_referrer=https%3A%2F%2Fdzen.ru%2Fnews%2Fsearch%3Ftext%3D',
publish_time=datetime.datetime(2024, 8, 30, 10, 49),
publisher_name='Элитный трейдер',
scraper='dzen',
db_id=None
),
 Article(
title='Песков: у Дурова не было договоренностей с Кремлем',
url='https://www.vedomosti.ru/politics/articles/2024/08/30/1059007-durova-ne-bilo-dogovorennostei-kremlem',
publish_time=datetime.datetime(2024, 8, 30, 12, 57, 35, 726925),
publisher_name='Ведомости',
scraper='google',
db_id=None
),
 Article(
title='WSJ: истребители F-16 уязвимы перед российскими средствами ПВО',
url='https://www.vedomosti.ru/politics/news/2024/08/29/1058914-istrebiteli-f-16-uyazvimi',
publish_time=datetime.datetime(2024, 8, 29, 23, 57, 35, 751941),
publisher_name='Ведомости',
scraper='google',
db_id=None
),
 Article(
title='Путин 3 сентября посетит Монголию с официальным визитом',
url='https://www.vedomosti.ru/politics/articles/2024/08/29/1058841-putin-posetit-mongoliyu',
publish_time=datetime.datetime(2024, 8, 29, 16, 57, 35, 724852),
publisher_name='Ведомости',
scraper='google',
db_id=None
)] 

'''
import newspaper
import time

urls = [a.url for a in articles]
for url in urls:
  print(url)
  try:
    _text_extractor = newspaper.Article(url)
    _text_extractor.download()
    _text_extractor.parse()
    text = _text_extractor.text
    print(text) 
  except Exception as error:
    print(error)
  print()
  print()
  print()
  print()
  print()
  time.sleep(.2)
'''

import goose3
import time

urls = [a.url for a in articles]
g = goose3.Goose()

def get_article_text(url):
  try:
    text = g.extract(url=url).cleaned_text
  except:
    text = ''
  return text

'''
for url in urls:
  print(url)
  try:
    text = g.extract(url=url).cleaned_text
    print(text) 
  except Exception as error:
    print(error)
  print()
  print()
  print()
  print()
  print()
  time.sleep(.2)
'''

'''
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
  print(f'{executor._max_workers=}')
  fetch_and_parse_jobs = {
    executor.submit(
      get_article_text,
      article_url
    ): article_url
    for article_url in urls
  }
  for done_job in concurrent.futures.as_completed(fetch_and_parse_jobs):
    result = done_job.result()
    print(len(result))
'''


