from pprint import pprint
import fitz
import re, os
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
morph_vocab = MorphVocab()

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)

'''
Parse plan:
  Parse pdf to text:
    1. Through fitz parse pdf pages to text string
  Parse text:
    1. Segment text - split on tokens and sentences
    2. Tag morph and parse syntax
    3. Tag ner
    4. Lemmatization
    5. Normalization
    6. Get period text fragment
    7. Get nominal text fragment
    Parse start, end dt:
      1. Parse all dates in text fragment
      2. By keywords detect start and end placement date
    Parse nominal:
      1. Parse all money in text frament
      2. By keywords detect cfa nominal
'''

def pdf_to_text(filepath):
  with fitz.open(filepath) as document:
    document_text = ''
    for page in document:
      text = page.get_text()
      document_text += text
  return document_text

def preproc_text(text):
  segmenter = Segmenter()
  emb = NewsEmbedding()
  morph_tagger = NewsMorphTagger(emb)
  syntax_parser = NewsSyntaxParser(emb)
  ner_tagger = NewsNERTagger(emb)
  doc = Doc(text)
  doc.segment(segmenter)
  doc.tag_morph(morph_tagger)
  doc.parse_syntax(syntax_parser)
  doc.tag_ner(ner_tagger)
  return doc

def split_on_sections(text):
  section_pattern = re.compile(r'^\d+\.\d+\.\s.+', re.MULTILINE)
  sections = list(section_pattern.finditer(text))
  extracted_sections = list()
  for i, section in enumerate(sections):
    start = section.end()
    end = sections[i + 1].start() if (i + 1) < len(sections) else len(text)
    section_text = text[section.start():end]
    #print(start, end)
    #print(section)
    extracted_sections.append(section_text)
  return extracted_sections

def parse_pdf(pdf_filepath):
  pdf_text = pdf_to_text(pdf_filepath)
  sections = split_on_sections(pdf_text)
  #preproced_text = preproc_text(pdf_text)
  #print(preproced_text)
  return sections

def main():
  pdf_filepath = 'pdfs/a-token_alrosa.pdf'
  pdf_filepath = 'pdfs/mosbirzha_rostelec.pdf'
  parse_pdf(pdf_filepath)

#main()

def test_on_all_files():
  found_cnt = 0
  not_found_cnt = 0
  for root, dirs, files in os.walk('pdfs/'):
    for file in files:
      filepath = os.path.join(root, file)
      s = parse_pdf(filepath)
      if len(s) > 10:
        found_cnt += 1
      else:
        print(filepath)
        print(len(s))
        print()
        not_found_cnt += 1
  print(found_cnt)
  print(not_found_cnt)

test_on_all_files()

'''
def test_date_extarctor():
  text = '
  2.7. Период приема Заявок на участие в Выпуске ЦФА (Период размещения ЦФА).
  Дата начала размещения ЦФА: 29.03.2024 с 12.00 часов московского времени.
  Дата завершения (окончания) размещения ЦФА: 12.04.2024 до 16.00 часов московского времени включительно.
  Дата Выпуска ЦФА: 12.04.2024.
  '
  dts = dates_extractor(text)
  dts = list(dts)
  pprint(dts)
test_date_extarctor()
'''

