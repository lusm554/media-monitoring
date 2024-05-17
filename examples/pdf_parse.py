import fitz
import re
import os
from pprint import pprint

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

def parse_a_token_text(text):
  cfa_nominal_pattern = re.compile(r'Цена приобретения ЦФА при их выпуске.*?составляет\s+(\d{1,3}(?: \d{3})*(?:,\d{2})?)', re.DOTALL)
  cfa_start_placement_dt_pattern = re.compile(r'Дата начала размещения ЦФА: (.*)')
  cfa_end_placement_dt_pattern = re.compile(r'Дата завершения \(окончания\) размещения ЦФА: (.*)')
  cfa_nominal_value = find_with_pattern(cfa_nominal_pattern, text)
  cfa_start_placement_dt = find_with_pattern(cfa_start_placement_dt_pattern, text)
  cfa_end_placement_dt = find_with_pattern(cfa_end_placement_dt_pattern, text)
  return cfa_end_placement_dt, cfa_start_placement_dt, cfa_nominal_value

def parse_pdf(filepath, parse_text):
  file_text = pdf_to_text(filepath)
  cfa_end_placement_dt, cfa_start_placement_dt, cfa_nominal_value = parse_text(file_text)
  print(cfa_nominal_value)
  print(cfa_start_placement_dt)
  print(cfa_end_placement_dt)

def main():
  '''
  filepath = 'pdfs/a-token_ab.pdf'
  parse_pdf(filepath)
  '''
  for root, dirs, files in os.walk('pdfs/'):
    for file in files:
      if not file.startswith('a-token'): continue
      #if not file.startswith('sberbank'): continue
      filepath = os.path.join(root, file)
      print(filepath)
      parse_pdf(filepath, parse_a_token_text)
      print()

if __name__ == '__main__':
  main()
