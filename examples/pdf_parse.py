import fitz
import re
import os
from pprint import pprint

def pdf_to_text(filepath):
  with fitz.open(filepath) as document:
    print(f'{document.page_count=}')
    pprint(document.metadata)
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

def parse_text(text):
  #print(text)
  cfa_nominal_pattern = re.compile(r'Цена приобретения ЦФА в течение Периода размещения ЦФА.*?составляет\s+(\d{1,3}(?: \d{3})*(?:,\d{2})?)', re.DOTALL)
  cfa_nominal_value = find_with_pattern(cfa_nominal_pattern, text)
  print(cfa_nominal_value)

def parse_pdf(filepath):
  file_text = pdf_to_text(filepath)
  res = parse_text(file_text)

def main():
  filepath = 'pdfs/a-token_ab.pdf'
  parse_pdf(filepath)

if __name__ == '__main__':
  main()
