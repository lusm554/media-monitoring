from pprint import pprint
import fitz
import re, os

def pdf_to_text(filepath):
  with fitz.open(filepath) as document:
    document_text = ''
    for page in document:
      text = page.get_text()
      document_text += text
  return document_text

def preprocess_text(text):
  text = text.lower()
  text = re.sub(r'\s+', ' ', text)
  text = re.sub(r'[^\w\s]', '', text)
  return text

'''
def tokenize_text(text):
  tokens = nltk.word_tokenize(text, language='russian')
  return tokens

def lemmatize_tokens(tokens):
  from pymystem3 import Mystem
  mystem = Mystem()
  lemmatized_tokens = mystem.lemmatize(' '.join(tokens))
  lemmatized_tokens = [token for token in lemmatized_tokens if token.strip()]
  return lemmatized_tokens

def extract_values(tokens, keywords):
  values = list()
  for i, token in enumerate(tokens):
    if token in keywords:
      context_window = tokens[max(0, i-5):i+5]
      values.append((token, context_window))
  return values

def parse_context(context_window, keyword):
  for word in context_window:
    if keyword == 'приобретение' and word.isdigit():
      return f"Номинал: {word}"
  return None
'''

def test_ner(text):
  #text = 'Европейский союз добавил в санкционный список девять политических деятелей из самопровозглашенных республик Донбасса — Донецкой народной республики (ДНР) и Луганской народной республики (ЛНР) — в связи с прошедшими там выборами. Об этом говорится в документе, опубликованном в официальном журнале Евросоюза. В новом списке фигурирует Леонид Пасечник, который по итогам выборов стал главой ЛНР. Помимо него там присутствуют Владимир Бидевка и Денис Мирошниченко, председатели законодательных органов ДНР и ЛНР, а также Ольга Позднякова и Елена Кравченко, председатели ЦИК обеих республик. Выборы прошли в непризнанных республиках Донбасса 11 ноября. На них удержали лидерство действующие руководители и партии — Денис Пушилин и «Донецкая республика» в ДНР и Леонид Пасечник с движением «Мир Луганщине» в ЛНР. Президент Франции Эмманюэль Макрон и канцлер ФРГ Ангела Меркель после встречи с украинским лидером Петром Порошенко осудили проведение выборов, заявив, что они нелегитимны и «подрывают территориальную целостность и суверенитет Украины». Позже к осуждению присоединились США с обещаниями новых санкций для России.'
  # NO PREPROCESSING NEEDED HERE 1!!!!!!!!!!!!!!!!! 
  from slovnet import NER
  from navec import Navec
  from ipymarkup import show_span_ascii_markup as show_markup
  navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
  #navec = Navec.load('navec_hudlit_v1_12B_500K_300d_100q.tar')
  ner = NER.load('slovnet_ner_news_v1.tar')
  ner.navec(navec)
  markup = ner(text)
  show_markup(markup.text, markup.spans)

def test_extractors(text):
  from natasha import (
    Doc,
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    MorphVocab,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,
  )
  segmenter = Segmenter()
  morph_vocab = MorphVocab()

  emb = NewsEmbedding()
  morph_tagger = NewsMorphTagger(emb)
  syntax_parser = NewsSyntaxParser(emb)
  ner_tagger = NewsNERTagger(emb)

  names_extractor = NamesExtractor(morph_vocab)
  dates_extractor = DatesExtractor(morph_vocab)
  money_extractor = MoneyExtractor(morph_vocab)
  addr_extractor = AddrExtractor(morph_vocab)

  doc = Doc(text)
  doc.segment(segmenter)
  doc.tag_morph(morph_tagger)
  doc.parse_syntax(syntax_parser)
  doc.tag_ner(ner_tagger)
  pprint(doc.tokens[:10])

def main():
  filepath = 'pdfs/a-token_alrosa.pdf'
  filetext = pdf_to_text(filepath)
  #filetext = preprocess_text(filetext)
  #test_ner(filetext)
  test_extractors(filetext)
  '''
  tokens = tokenize_text(filetext)
  lemmatized_tokens = lemmatize_tokens(tokens)
  keywords = ['приобретение']
  extracted_values = extract_values(lemmatized_tokens, keywords)
  for kw, context in extracted_values:
    result = parse_context(context, kw)
    if result:
      print(result)
  '''

if __name__ == '__main__':
  main()
