from transformers import pipeline
from pprint import pprint

clf = pipeline('zero-shot-classification')
result = clf(
  'Sell stocks, buy crypto',
  ['Crypto', 'politics', 'cooking'],
)
pprint(result)


news = [
  'ПСБ разместил рекордный среди банков третий выпуск ЦФА',
  'В Госдуме подготовили проект о повышении предельного размера платежей за коммунальные услуги',
  'Окно к деньгам?',
  'В ЖК «hideOUT» инвесторам будет доступен цифровой квадратный метр',
  ' Рынок ЦФА показал рекордный рост ',
  '  Генпрокурор России сообщил о создании ПО для контроля криптовалютных операций ',
]

result = clf(
  news,
  ['Цифровые Финансовые Активы', 'ЦФА', 'Политика'],
)
pprint(result)
