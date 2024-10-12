cfa_keys_words = [
  'цфа',
  'цифровые финансовые активы',
  'цифровые активы',
]


def filter_cfa_kw(texts):
  kw = [kw.lower().strip() for kw in cfa_keys_words]
  texts = [[token.lower().strip() for token in t.split(' ')] for t in texts]
  texts = [' '.join(t) for t in texts if any(kww==token for kww in kw for token in t)]
  return texts

test = [
  'Анализ ЦФА смещается от спекулятивного к фундаментальному ',
  ' В "Хезболлах" сообщили о пуске 80 ракет по городу Цфат ',
  ' "Хезболле" заявили о запуске 80 реактивных снарядов по городу Цфат в Израиле ',
]

test = filter_cfa_kw(test)
print(test)
