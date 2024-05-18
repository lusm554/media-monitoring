import fitz
import re
import os
from pprint import pprint

atoken_patterns = {
  'cfa_nominal_pattern': re.compile(r'Цена приобретения ЦФА при их выпуске.*?составляет\s+(\d{1,3}(?: \d{3})*(?:,\d{2})?)', re.DOTALL),
  'cfa_start_placement_dt_pattern': re.compile(r'Дата начала размещения ЦФА: (.*)'),
  'cfa_end_placement_dt_pattern': re.compile(r'Дата завершения \(окончания\) размещения ЦФА: (.*)'),
}

sberbank_patterns = {
  'cfa_nominal': re.compile(r'Цена приобретения.*?составляет\s+(\d+)\s+\(.*?\)\s+рублей', re.DOTALL),
  'cfa_start_placement_dt': re.compile(r'Дата и время начала размещения ЦФА[\s\S]*?(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2} МСК)'),
  'cfa_end_placement_dt': re.compile(r'Дата и время окончания размещения ЦФА[\s\S]*?(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2} МСК)'),
}

def pdf_to_text(filepath):
  with fitz.open(filepath) as document:
    #print(f'{document.page_count=}')
    #pprint(document.metadata)
    document_text = ''
    for page in document:
      text = page.get_text()
      document_text += text
  return document_text

def find_with_pattern(pattern, text):
  match = pattern.search(text)
  if match:
    return match.group(1)
  return None

def parse_text(text, patterns):
  values_by_patterns = {
    pattern_key: find_with_pattern(pattern, text)
    for pattern_key, pattern in patterns.items()
  }
  return values_by_patterns

def parse_pdf(filepath, patterns):
  file_text = pdf_to_text(filepath)
  #print(file_text)
  res = parse_text(file_text, patterns)
  pprint(res)


def main():
  #filepath = 'pdfs/a-token_ab.pdf'
  filepath = 'pdfs/sberbank_rs.pdf'
  parse_pdf(filepath, sberbank_patterns)
  '''
  for root, dirs, files in os.walk('pdfs/'):
    for file in files:
      filepath = os.path.join(root, file)
      if file.startswith('a-token'): 
        continue
        #parse_pdf(filepath, atoken_patterns)
      if file.startswith('sberbank'):
        print(filepath)
        parse_pdf(filepath, sberbank_patterns)
        pass
  '''

if __name__ == '__main__':
  main()
  pass
