import requests
import time

COOKIES = {
  'KIykI': '1',
  'HgGedof': '1',
  'zen_sso_checked': '1',
  'yandex_login': '',
  'sso_status': 'sso.passport.yandex.ru:synchronized',
}
HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive',
  'Referer': 'https://sso.dzen.ru/',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-site',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
}

import json
for i in range(12):
  url = f'https://dzen.ru/news/search?filter_date=1712523600000%2C1713042000000&flat=1&p={i}&text=цфа+date%3A20240408..20240414&ajax=1'
  res = requests.get(
    url=url,
    headers=HEADERS,
    cookies=COOKIES,
  )
  print(res.status_code)
  print(res.url)
  #data = res.text # get json
  data = res.json()
  print(data.keys())
  print(len(data.get('data').get('stories', [])))
  print()
  time.sleep(1)
