from natasha import Doc, MorphVocab, Segmenter

cfa_keys_words = [
  'цфа',
  'цифровые финансовые активы',
  'цифровые активы',
]

morph_vocab = MorphVocab()
segmenter = Segmenter()

def normalize(text):
  text = text.lower()
  doc = Doc(text)
  doc.segment(segmenter=segmenter)
  for token in doc.tokens:
    if token.pos and token.feats:
      token.lemmatize(morph_vocab)
    else:
      token.lemma = token.text
  return ' '.join(token.lemma for token in doc.tokens)

def filter_cfa_kw(texts):
  normalized_kw = [normalize(kw) for kw in cfa_keys_words]
  print(normalized_kw)
  for t in texts:
    print(normalize(t))
    print([normalize(t).find(kw) for kw in normalized_kw])
    print()

  texts = [t for t in texts if any(normalize(t).find(kw) != -1 for kw in normalized_kw)]
  return texts

test = [
  'Анализ ЦФА смещается от спекулятивного к фундаментальному ',
  ' В "Хезболлах" сообщили о пуске 80 ракет по городу Цфат ',
  ' "Хезболле" заявили о запуске 80 реактивных снарядов по городу Цфат в Израиле ',
]

#print(test)
test = filter_cfa_kw(test)
print(test)
