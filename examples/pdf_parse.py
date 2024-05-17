import fitz
import re
from pprint import pprint

filepath = 'pdfs/a-token_ab.pdf'

def pdf_to_text(filepath):
  with fitz.open(filepath) as document:
    print(f'{document.page_count=}')
    pprint(document.metadata)
    document_text = ''
    for page in document:
      text = page.get_text()
      document_text += text
    return document_text

def parse_text(text):
  pass

def parse_pdf(filepath):
  file_text = pdf_to_text(filepath)
  res = parse_text(file_text)

parse_pdf(filepath)
