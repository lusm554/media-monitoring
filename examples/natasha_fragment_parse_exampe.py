from pprint import pprint
from natasha import (
  MorphVocab,
  NamesExtractor,
  DatesExtractor,
  MoneyExtractor,
  AddrExtractor,
)
morph_vocab = MorphVocab()

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)


def test_date_extarctor():
  text = '''
  2.7. Период приема Заявок на участие в Выпуске ЦФА (Период размещения ЦФА).
  Дата начала размещения ЦФА: 29.03.2024 с 12.00 часов московского времени.
  Дата завершения (окончания) размещения ЦФА: 12.04.2024 до 16.00 часов московского времени включительно.
  Дата Выпуска ЦФА: 12.04.2024.
  '''
  dts = dates_extractor(text)
  dts = list(dts)
  pprint(dts)

test_date_extarctor()

